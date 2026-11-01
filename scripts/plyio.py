"""Minimal reader/writer for binary little-endian 3D Gaussian Splatting PLY files."""
import numpy as np

SH_C0 = 0.28209479177387814


def read_ply(path):
    with open(path, "rb") as f:
        header = b""
        while not header.endswith(b"end_header\n"):
            line = f.readline()
            if not line:
                raise ValueError("Not a PLY file: missing end_header")
            header += line
        text = header.decode("ascii")
        if "binary_little_endian" not in text:
            raise ValueError("Only binary_little_endian PLY files are supported")
        count, props, in_vertex = 0, [], False
        for line in text.splitlines():
            parts = line.split()
            if parts[:2] == ["element", "vertex"]:
                count, in_vertex = int(parts[2]), True
            elif parts and parts[0] == "element":
                in_vertex = False
            elif parts and parts[0] == "property" and in_vertex:
                if parts[1] != "float":
                    raise ValueError(f"Unsupported property type: {line}")
                props.append(parts[2])
        data = np.fromfile(f, dtype="<f4", count=count * len(props)).reshape(count, len(props))
    return props, data


def write_ply(path, props, data):
    header = ("ply\nformat binary_little_endian 1.0\n"
              f"element vertex {len(data)}\n"
              + "".join(f"property float {p}\n" for p in props)
              + "end_header\n")
    with open(path, "wb") as f:
        f.write(header.encode("ascii"))
        f.write(np.ascontiguousarray(data, dtype="<f4").tobytes())


def gaussian_attributes(props, data):
    ix = {p: i for i, p in enumerate(props)}
    xyz = data[:, [ix["x"], ix["y"], ix["z"]]]
    opacity = 1.0 / (1.0 + np.exp(-data[:, ix["opacity"]]))
    scales = np.exp(data[:, [ix["scale_0"], ix["scale_1"], ix["scale_2"]]])
    rgb = np.clip(0.5 + SH_C0 * data[:, [ix["f_dc_0"], ix["f_dc_1"], ix["f_dc_2"]]], 0, 1)
    return xyz, opacity, scales, rgb


def core_box(xyz, low=5, high=95, margin=0.2):
    """Axis-aligned box around the main scene, ignoring far-away floaters."""
    lo, hi = np.percentile(xyz, low, axis=0), np.percentile(xyz, high, axis=0)
    pad = (hi - lo) * margin
    return lo - pad, hi + pad
