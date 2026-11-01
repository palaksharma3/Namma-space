"""Print summary statistics of a 3D Gaussian Splatting PLY file."""
import argparse
import os

import numpy as np

from plyio import core_box, gaussian_attributes, read_ply


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ply", help="path to a 3DGS .ply file")
    a = ap.parse_args()
    props, data = read_ply(a.ply)
    xyz, opacity, scales, _ = gaussian_attributes(props, data)
    n_rest = sum(p.startswith("f_rest_") for p in props)
    sh_degree = int(round(np.sqrt(n_rest / 3 + 1))) - 1 if n_rest else 0
    lo, hi = core_box(xyz)
    inside = np.all((xyz >= lo) & (xyz <= hi), axis=1)
    print(f"file              : {a.ply} ({os.path.getsize(a.ply) / 1e6:.1f} MB)")
    print(f"gaussians         : {len(data):,}")
    print(f"attributes        : {len(props)} float32 ({len(props) * 4} bytes per gaussian)")
    print(f"SH degree         : {sh_degree}")
    print(f"main volume size  : {np.round(hi - lo, 3).tolist()} scene units (x, y, z)")
    print(f"inside main volume: {inside.mean():.2%} (rest = likely floaters/background)")
    print(f"opacity           : mean {opacity.mean():.3f}, below 0.05: {np.mean(opacity < 0.05):.2%}")
    print(f"max-axis scale    : median {np.median(scales.max(1)):.4f} scene units")


if __name__ == "__main__":
    main()
