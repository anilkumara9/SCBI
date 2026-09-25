/* gen_spearman_null.c
 *
 * Exact null distribution of D = sum_{i=1..n} (i - pi_i)^2 over all
 * permutations pi in S_n (Spearman's rho null distribution, since
 * rho = 1 - 6D / (n(n^2-1)) for untied ranks).
 *
 * Method: TRUE EXACT subset DP over bitmasks (2^n states), layer by layer
 * (popcount). dp[mask][d] = number of injective assignments of positions
 * 1..popcount(mask) to the values in `mask` with partial sum-of-squared-
 * displacements == d. Transition assigns the next position m+1 to each
 * unused value v, shifting d by (m+1-v)^2.
 *
 * This is a deterministic, complete enumeration of the permutation null --
 * NOT Monte Carlo. Counts are exact (unsigned __int128; n! <= 24! < 2^79).
 *
 * The D_max_partial(m) cap keeps early layers small: for layer m we only
 * track d <= min(d_hi, max achievable partial D at layer m).
 *
 * Memory: O(C(n,n/2) * d_hi)  -- use d_hi chunking (multiple runs) for n=24.
 * Time:   O(2^n * n * d_hi).
 *
 * Compile: gcc -O3 -fopenmp -o gen_spearman_null gen_spearman_null.c
 * Usage:   ./gen_spearman_null n d_hi   > counts_n_dhi.txt
 *   (prints count[d] for d = 0..d_hi, one decimal integer per line)
 *
 * Part of the EXP084 bundle (LOG-265). The shipped JSON tables in
 * ../exp084_spearman_tables/ were generated with this program; see
 * ../BUILD_NOTES.md for the exact generation commands and verification.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#ifdef _OPENMP
#include <omp.h>
#endif

static void print_u128(unsigned __int128 x) {
    if (x == 0) { putchar('0'); putchar('\n'); return; }
    char buf[40];
    int i = 0;
    while (x > 0) { buf[i++] = (char)('0' + (int)(x % 10)); x /= 10; }
    while (i > 0) putchar(buf[--i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s n d_hi\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    int d_hi = atoi(argv[2]);
    if (n < 1 || n > 24 || d_hi < 0) {
        fprintf(stderr, "bounds: 1 <= n <= 24, d_hi >= 0\n");
        return 1;
    }
    int dmax = n * (n * n - 1) / 3;
    if (d_hi > dmax) d_hi = dmax;

    int N = 1 << n;

    uint8_t *popcnt = malloc((size_t)N);
    if (!popcnt) { fprintf(stderr, "OOM popcnt\n"); return 1; }
    for (int mask = 0; mask < N; mask++)
        popcnt[mask] = (uint8_t)__builtin_popcount((unsigned)mask);

    int *cnt = calloc((size_t)(n + 1), sizeof(int));
    for (int mask = 0; mask < N; mask++) cnt[popcnt[mask]]++;

    int *lstart = malloc((size_t)(n + 2) * sizeof(int));
    lstart[0] = 0;
    for (int m = 0; m <= n; m++) lstart[m + 1] = lstart[m] + cnt[m];

    uint32_t *lmasks = malloc((size_t)N * sizeof(uint32_t));
    int *fill = calloc((size_t)(n + 1), sizeof(int));
    for (int mask = 0; mask < N; mask++) {
        int m = popcnt[mask];
        lmasks[lstart[m] + fill[m]++] = (uint32_t)mask;
    }

    int32_t *rank = malloc((size_t)N * sizeof(int32_t));
    if (!rank) { fprintf(stderr, "OOM rank\n"); return 1; }
    for (int m = 0; m <= n; m++)
        for (int i = 0; i < cnt[m]; i++)
            rank[lmasks[lstart[m] + i]] = i;
    free(popcnt);

    /* max partial D achievable at layer m */
    int *dmp = malloc((size_t)(n + 1) * sizeof(int));
    dmp[0] = 0;
    for (int m = 1; m <= n; m++) {
        int mx = 0;
        for (int i = 1; i <= m; i++) {
            int a = (i - 1) * (i - 1), b = (n - i) * (n - i);
            mx += (a > b ? a : b);
        }
        dmp[m] = mx;
    }

    int dcap_cur = d_hi < dmp[0] ? d_hi : dmp[0];
    unsigned __int128 *dp_cur =
        calloc((size_t)cnt[0] * (dcap_cur + 1), sizeof(unsigned __int128));
    if (!dp_cur) { fprintf(stderr, "OOM dp_cur layer 0\n"); return 1; }
    dp_cur[0] = 1;

    for (int m = 0; m < n; m++) {
        int dcap_nxt = d_hi < dmp[m + 1] ? d_hi : dmp[m + 1];
        size_t stride_cur = (size_t)dcap_cur + 1;
        size_t stride_nxt = (size_t)dcap_nxt + 1;
        unsigned __int128 *dp_next =
            calloc((size_t)cnt[m + 1] * stride_nxt, sizeof(unsigned __int128));
        if (!dp_next) {
            fprintf(stderr, "OOM dp_next layer %d (need %.1f GB)\n",
                    m + 1, (double)cnt[m + 1] * stride_nxt * 16 / 1e9);
            return 1;
        }
        uint32_t *lm_next = lmasks + lstart[m + 1];
        int n_next = cnt[m + 1];
#pragma omp parallel for schedule(static)
        for (int jj = 0; jj < n_next; jj++) {
            /* Each dest mask is written by exactly one thread: race-free.
             * Predecessors of dest are dest-with-one-bit-cleared (layer m). */
            uint32_t dest = lm_next[jj];
            unsigned __int128 *dst_base = dp_next + (size_t)jj * stride_nxt;
            for (int v = 1; v <= n; v++) {
                uint32_t bit = 1u << (v - 1);
                if (!(dest & bit)) continue;
                int i = rank[dest ^ bit];
                unsigned __int128 *src = dp_cur + (size_t)i * stride_cur;
                int sh = (m + 1 - v) * (m + 1 - v);
                if (sh > dcap_nxt) continue;
                unsigned __int128 *dst = dst_base + sh;
                int dlim = dcap_cur;
                int maxd = dcap_nxt - sh;
                if (dlim > maxd) dlim = maxd;
                for (int d = 0; d <= dlim; d++) dst[d] += src[d];
            }
        }
        free(dp_cur);
        dp_cur = dp_next;
        dcap_cur = dcap_nxt;
    }

    for (int d = 0; d <= dcap_cur; d++) print_u128(dp_cur[d]);
    free(dp_cur);
    free(lmasks);
    free(lstart);
    free(cnt);
    free(fill);
    free(rank);
    free(dmp);
    return 0;
}
