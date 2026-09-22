"""
scbi/generators/activation_cluster.py: Modular Candidate Generators for EXP015
Implements representational locality candidate generators on hidden representations:
- G0: Temporal-quartile SVD (baseline control)
- G1: Activation-clustered subspaces (cosine clustering on normalized representations)
- G2: Principal covariance directions (global PCA)
- G4: Sparse feature dictionary atoms (DictionaryLearning)
- Structural candidate quality metrics: Locality, Diversity, Stability.
"""
import torch
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import DictionaryLearning

def generate_g0_temporal(h, rank=2, K=4):
    """G0: Temporal-quartile SVD baseline control."""
    seq_len = h.shape[0]
    q_size = seq_len // K
    cands = []
    for k in range(K):
        start = k * q_size
        end = (k + 1) * q_size if k < K - 1 else seq_len
        slice_h = h[start:end]
        if slice_h.shape[0] < rank:
            v, _ = torch.linalg.qr(torch.randn(h.shape[1], rank))
        else:
            v = torch.linalg.svd(slice_h, full_matrices=False).Vh[:rank].T
        cands.append(v)
    return cands

def generate_g1_clusters(h, rank=2, K=4):
    """
    G1: Activation-Clustered Subspaces.
    Clusters sequence tokens based on cosine similarity of normalized activations,
    then extracts centered top-rank SVD directions for each cluster.
    """
    seq_len, d_model = h.shape
    if seq_len < K:
        # Fallback if sequence is shorter than K
        return generate_g0_temporal(h, rank=rank, K=K)
        
    # 1. Normalize representations to unit sphere for cosine clustering
    norms = torch.norm(h, dim=-1, keepdim=True).clamp(min=1e-8)
    h_norm = (h / norms).detach().cpu().numpy()
    
    # 2. Agglomerative clustering with cosine metric
    # Note: In sklearn >= 1.2, metric='cosine' with linkage='average'
    clustering = AgglomerativeClustering(n_clusters=K, metric='cosine', linkage='average')
    labels = clustering.fit_predict(h_norm)
    
    cands = []
    for k in range(K):
        cluster_mask = (labels == k)
        cluster_h = h[cluster_mask] # [N_k, d_model]
        
        if cluster_h.shape[0] < rank:
            # Fallback for singleton cluster: random orthogonal basis
            v, _ = torch.linalg.qr(torch.randn(d_model, rank))
        else:
            # Direct SVD within cluster (captures cluster mean and dominant direction)
            v = torch.linalg.svd(cluster_h, full_matrices=False).Vh[:rank].T
            if v.shape[1] < rank:
                v_pad, _ = torch.linalg.qr(torch.randn(d_model, rank))
                v = v_pad
        cands.append(v)
    return cands

def generate_g2_pca(h, rank=2, K=4):
    """
    G2: Principal Covariance Directions.
    Extracts consecutive pairs of leading eigenvectors from the global representation covariance.
    """
    seq_len, d_model = h.shape
    mu = torch.mean(h, dim=0, keepdim=True)
    centered = h - mu
    
    # Full or economy SVD of centered representations
    # U, S, Vh = svd(centered)
    Vh = torch.linalg.svd(centered, full_matrices=False).Vh # [min(T, d), d]
    
    cands = []
    for k in range(K):
        idx_start = k * rank
        idx_end = idx_start + rank
        if idx_end <= Vh.shape[0]:
            v = Vh[idx_start:idx_end].T # [d, rank]
        else:
            # If sequence length < K * rank, pad with random orthogonal directions
            v, _ = torch.linalg.qr(torch.randn(d_model, rank))
        cands.append(v)
    return cands

def generate_g4_sparse(h, rank=2, K=4):
    """
    G4: Sparse Feature Dictionary Atoms.
    Performs dictionary learning over sequence activations to identify localized latent features.
    """
    seq_len, d_model = h.shape
    n_atoms = K * rank # e.g. 8 atoms
    h_np = h.detach().cpu().numpy()
    
    if seq_len < rank:
        # Fallback to PCA if sequence is shorter than subspace rank
        return generate_g2_pca(h, rank=rank, K=K)
        
    try:
        dict_learner = DictionaryLearning(n_components=n_atoms, alpha=1.0, max_iter=100, random_state=42)
        dict_learner.fit(h_np)
        components = torch.tensor(dict_learner.components_, dtype=h.dtype, device=h.device) # [n_atoms, d_model]
        
        cands = []
        for k in range(K):
            atoms = components[k * rank : (k + 1) * rank].T # [d, rank]
            # Orthogonalize atom pair via QR
            q, _ = torch.linalg.qr(atoms)
            cands.append(q)
        return cands
    except Exception:
        return generate_g2_pca(h, rank=rank, K=K)

def compute_candidate_quality(h, cand_list, rank=2, n_bootstrap=10):
    """
    Computes candidate-quality metrics:
    - Locality: Fraction of representation energy captured by subspace
    - Diversity: Mean normalized Grassmanian distance among candidate pairs
    - Stability: Bootstrap resampling stability of candidate subspaces
    """
    seq_len, d_model = h.shape
    total_energy = max(torch.norm(h).item()**2, 1e-8)
    
    # 1. Locality per candidate
    localities = []
    for V in cand_list:
        proj_energy = torch.norm(torch.matmul(h, V)).item()**2
        localities.append(proj_energy / total_energy)
    mean_locality = float(np.mean(localities))
    
    # 2. Diversity / Grassmanian Distance
    K = len(cand_list)
    divs = []
    for i in range(K):
        for j in range(i + 1, K):
            Vi = cand_list[i]
            Vj = cand_list[j]
            overlap = torch.norm(torch.matmul(Vi.T, Vj)).item()**2
            dist = np.sqrt(max(1.0 - overlap / rank, 0.0))
            divs.append(dist)
    mean_diversity = float(np.mean(divs)) if divs else 0.0
    
    # 3. Stability via bootstrap resampling
    stabilities = []
    rng = np.random.RandomState(42)
    for _ in range(n_bootstrap):
        boot_idx = rng.choice(seq_len, size=seq_len, replace=True)
        h_boot = h[boot_idx]
        # Compare first candidate subspace overlap with recomputed candidate
        V_orig = cand_list[0]
        # Simple SVD on resampled subset
        v_boot = torch.linalg.svd(h_boot[:seq_len//4], full_matrices=False).Vh[:rank].T
        overlap = torch.norm(torch.matmul(V_orig.T, v_boot)).item()**2 / rank
        stabilities.append(overlap)
    mean_stability = float(np.mean(stabilities))
    
    return {
        "locality": mean_locality,
        "diversity": mean_diversity,
        "stability": mean_stability
    }
