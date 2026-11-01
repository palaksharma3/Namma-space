# Namma Space - Smartphone-to-Web Indoor Digital Twin (Techfest 2026-27, Round 1)

**Live web viewer (free roaming, zero install):** https://superspl.at/scene/0681979d
Full-screen viewer: https://superspl.at/s?id=0681979d

Turns an ordinary smartphone scan of an indoor space into a photorealistic, walkable 3D digital twin in the
browser using **3D Gaussian Splatting (3DGS)**. No GPU workstation is needed at any step.

| Stage | Tool | Output |
|---|---|---|
| 1. Capture | iPhone + Scaniverse, following [SOP.md](SOP.md) | live scan |
| 2. Reconstruction | Scaniverse on-device 3DGS | `Indirapuram.ply` - 463,573 Gaussians, 115 MB |
| 3. Clean & align | SuperSplat Editor (runs in the browser) | `scene.ssproj`, `supersplat_cleaned.ply` |
| 4. Publish & optimise | superspl.at (SOG compression + collision voxels) | 7.85 MB SOG, 5 cm voxel octree |
| 5. Web walkthrough | SuperSplat / PlayCanvas web viewer | public URL above |

## Repository layout

```
docs/      technical abstract (PDF) and figures
scripts/   Python tools to inspect, sample and map 3DGS .ply files
test/      sample data: down-sampled scene + published collision voxels
SOP.md     capture Standard Operating Procedure
```

## Reconstruct the model step by step

1. **Capture** - install Scaniverse (iOS/Android) and scan the space following [SOP.md](SOP.md); let it process on the phone.
2. **Export** - export the splat as **PLY** and copy it to the laptop.
3. **Clean & align** - open https://superspl.at/editor in Chrome/Edge, then **File > Import** (not *Open*) and pick the PLY.
   Use **Orient** (click 3 floor points, *Align to Grid*), **Measure** (type a known real length such as a door width to set metric scale)
   and the selection tools + *Delete* to remove floaters. Save with **File > Save** (`.ssproj`) and **File > Export > PLY**.
4. **Publish** - log in at https://superspl.at, **File > Publish**, open the scene in **Studio**, set the start camera
   (pencil icon, *Apply*), **Collision > Generate** (scene type *Indoor*, seed inside the room) and **Save**.
5. **Explore** - open the scene URL: `1` orbit, `2` fly, `3` walk; `W A S D` + mouse to move and look, `Q/E` down/up, `H` help.

## Run the scripts on the sample data (Python 3.9+)

```bash
pip install -r requirements.txt
python scripts/ply_stats.py test/sample_scene.ply
python scripts/topdown_map.py test/sample_scene.ply test/topdown_preview.png
python scripts/make_sample.py path/to/full_scene.ply test/sample_scene.ply --count 80000
```

To see the sample in 3D, drag `test/sample_scene.ply` into https://superspl.at/editor.

## Data

- `test/sample_scene.ply` - 80,000 most-opaque Gaussians of the cleaned scene (small enough for GitHub).
- `test/scene.voxel.json` + `test/scene.voxel.bin` - published collision octree (5 cm voxels) used by walk mode.
- Full-resolution files (`Indirapuram.ply`, `supersplat_cleaned.ply`, `scene.ssproj`; > 100 MB each, above GitHub's file limit):
  **[add Google Drive link]**

## Credits and licences

Scaniverse (Niantic Spatial) for capture and on-device reconstruction; SuperSplat Editor/Viewer, PlayCanvas Engine and
splat-transform (PlayCanvas, MIT licence) for editing, compression, collision and viewing; NumPy and Pillow for the scripts.
Method: B. Kerbl et al., *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM TOG 42(4), SIGGRAPH 2023.
