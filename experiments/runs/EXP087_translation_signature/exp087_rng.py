#!/usr/bin/env python3
"""EXP087 deterministic RNG. All stochastic bundle components (mock data
generation, any randomized harness step) derive from the pinned MASTER_SEED
via independent per-stream seeds. Re-running with the same seed reproduces
bit-identical outputs."""

import random

import exp087_guards as G


def make_py_rng(stream_seed):
    """Independent Python RNG for one named stream."""
    return random.Random(G.MASTER_SEED * 100003 + stream_seed)


def gaussian(rng, mu, sigma):
    return rng.gauss(mu, sigma)
