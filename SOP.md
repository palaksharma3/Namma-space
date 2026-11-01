# Capture SOP v1.0 (Standard Operating Procedure)

3DGS can only reconstruct what the camera saw from enough viewpoints, with sharp images and accurate camera poses.
Every rule protects one of these: **coverage, sharpness, pose accuracy**.

**Equipment:** any iPhone (A12+) or Android phone with the free **Scaniverse** app (LiDAR optional). No tripod, PC or GPU. ~5 min per room.

1. **Prepare the space (~2 min)** - all lights on and fixed, curtains/doors in final state, ceiling fans off, no people/pets in view, walkways clear.
   *Why: 3DGS assumes a static scene; moving things become blur/floaters.*
2. **Plan zones** - each zone scannable in <= 180 s (one room or ~5 m of corridor); neighbouring zones overlap >= 1 m at doorways.
   *Why: long splat scans risk processing failure; overlap allows merging.*
3. **Loop 1 - perimeter, looking inward** - phone at chest height (~1.3 m), walk slowly along the walls keeping the room centre in frame.
   *Why: camera movement (parallax) lets the tracker recover depth and poses.*
4. **Loop 2 - centre, looking outward** - turn slowly through 360 degrees, then sweep every wall, corner and doorway.
   *Why: walls seen only at grazing angles reconstruct poorly.*
5. **Height passes** - one low pass (~0.5 m, tilted up) along furniture/floor edges, one high pass (tilted down) for table tops and ceiling.
   *Why: floor boundaries and furniture legs define the walkable area for navigation.*
6. **Movement rules** - slow and smooth, no fast spins, never fill the frame with a blank wall or bright lamp from < 0.5 m, look back once after each doorway.
   *Why: motion blur and textureless frames are the most common failures.*
7. **Process and check on site** - run on-device splat processing, orbit the preview; rescan any zone with holes, blur or floating blobs.
8. **Export and record scale** - export the splat as **.PLY** (master copy); tape-measure one real distance (e.g. door width) for metric calibration.

**Large venues:** parallel operators per zone, merge zones in SuperSplat, or pose a walkthrough video with COLMAP/GLOMAP and train with Brush/gsplat on a cloud GPU.
