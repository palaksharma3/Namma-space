"""Render a top-down (floor-plan style) map of a Gaussian splat scene.

Floor-level colour is blended with the density of taller structures (walls,
furniture), giving a quick 2-D occupancy preview - the prototype of the
navigation grid planned for Round 2.
"""
import argparse

import numpy as np
from PIL import Image

from plyio import core_box, gaussian_attributes, read_ply


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ply", help="path to a 3DGS .ply file")
    ap.add_argument("out_png", help="output image path")
    ap.add_argument("--res", type=float, default=0.02, help="cell size in scene units (default 0.02)")
    ap.add_argument("--y-up", action="store_true", help="input already uses +Y up (default assumes the 3DGS/COLMAP +Y-down convention)")
    a = ap.parse_args()

    props, data = read_ply(a.ply)
    xyz, opacity, scales, rgb = gaussian_attributes(props, data)
    if not a.y_up:
        xyz = xyz * np.array([-1.0, -1.0, 1.0])  # 180 degrees about Z, as the PlayCanvas viewer does
    smax = scales.max(1)
    keep = (opacity > 0.3) & (smax < np.percentile(smax, 90))
    lo, hi = core_box(xyz)
    keep &= np.all((xyz >= lo) & (xyz <= hi), axis=1)
    xyz, rgb = xyz[keep], rgb[keep]
    x, y, z = xyz.T

    floor_y = np.percentile(y, 5)
    height = np.percentile(y, 95) - floor_y
    near_floor = y < floor_y + 0.08 * height
    tall = (y > floor_y + 0.12 * height) & (y < floor_y + 0.9 * height)

    xb = np.arange(x.min(), x.max() + a.res, a.res)
    zb = np.arange(z.min(), z.max() + a.res, a.res)
    cnt = np.histogram2d(x[near_floor], z[near_floor], bins=[xb, zb])[0]
    col = np.stack([np.histogram2d(x[near_floor], z[near_floor], bins=[xb, zb], weights=rgb[near_floor, c])[0]
                    for c in range(3)], -1)
    floor = np.where(cnt[..., None] > 0, col / np.maximum(cnt[..., None], 1), 0.0)
    dens = np.log1p(np.histogram2d(x[tall], z[tall], bins=[xb, zb])[0])
    if np.any(dens > 0):
        dens = np.clip(dens / max(np.percentile(dens[dens > 0], 99), 1e-6), 0, 1)

    img = np.where(cnt[..., None] > 0, 0.25 + 0.65 * floor, 0.07)
    alpha = (dens ** 0.8)[..., None] * 0.9
    img = img * (1 - alpha) + np.array([0.25, 0.92, 1.0]) * alpha
    img = (np.clip(img, 0, 1).transpose(1, 0, 2)[::-1] * 255).astype(np.uint8)
    Image.fromarray(img).save(a.out_png)
    print(f"saved {a.out_png} ({img.shape[1]}x{img.shape[0]} px; floor y={floor_y:.3f}, room height={height:.3f} scene units)")


if __name__ == "__main__":
    main()
