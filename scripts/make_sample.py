"""Create a small, GitHub-friendly sample of a Gaussian splat PLY.

Keeps the most opaque Gaussians inside the main scene volume.
"""
import argparse

import numpy as np

from plyio import core_box, gaussian_attributes, read_ply, write_ply


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ply", help="full-resolution 3DGS .ply")
    ap.add_argument("out_ply", help="output sample .ply")
    ap.add_argument("--count", type=int, default=80000, help="number of Gaussians to keep (default 80000)")
    a = ap.parse_args()
    props, data = read_ply(a.ply)
    xyz, opacity, _, _ = gaussian_attributes(props, data)
    lo, hi = core_box(xyz)
    idx = np.flatnonzero(np.all((xyz >= lo) & (xyz <= hi), axis=1))
    idx = np.sort(idx[np.argsort(-opacity[idx])][: a.count])
    write_ply(a.out_ply, props, data[idx])
    print(f"wrote {len(idx):,} of {len(data):,} gaussians to {a.out_ply}")


if __name__ == "__main__":
    main()
