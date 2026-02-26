"""Superquadric mesh element."""

import numpy as np


class Superquadric:
    """A superquadric surface represented as a triangle mesh."""

    def __init__(
        self,
        scalings,
        exponents,
        translation,
        rotation,
        color,
        resolution,
        visible,
        alpha=1.0,
        rotation_matrix=None,
        tapering=None,
        bending=None,
        wireframe=False,
    ):
        """Initialize a superquadric.

        Args:
            scalings: Scale factors (3,).
            exponents: Superquadric exponents (3,).
            translation: Translation vector (3,).
            rotation: Quaternion rotation [x, y, z, w] (4,).
            color: RGB color array-like in 0-255.
            resolution: Sampling resolution.
            visible: Whether the mesh is visible.
            alpha: Transparency in [0, 1].
            rotation_matrix: Optional 3x3 rotation matrix to apply to vertices.
            tapering: Optional tapering parameters [kx, ky] (2,).
            bending: Optional bending parameters [kb_z, alpha_z, kb_x, alpha_x, kb_y, alpha_y] (6,).
            wireframe: Whether to show wireframe overlay.
        """
        self.scalings = scalings
        self.exponents = exponents
        self.translation = translation
        self.rotation = rotation
        self.color = color
        self.resolution = resolution
        self.visible = visible
        self.alpha = alpha
        self.rotation_matrix = rotation_matrix
        self.tapering = tapering if tapering is not None else np.array([0.0, 0.0])
        self.bending = bending if bending is not None else np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.wireframe = wireframe

    def get_properties(self, binary_filename):
        """Return JSON-serializable properties for this element.

        Args:
            binary_filename: Name of the binary data file (unused for superquadrics).

        Returns:
            A dict of properties for the web viewer.
        """
        json_dict = {
            'type': 'superquadric',
            'visible': self.visible,
            'alpha': float(self.alpha),
            'scalings': self.scalings.tolist(),
            'exponents': self.exponents.tolist(),
            'resolution': int(self.resolution),
            'translation': self.translation.tolist(),
            'rotation': self.rotation.tolist(),
            'color': self.color.tolist(),
            'tapering': self.tapering.tolist(),
            'bending': self.bending.tolist(),
            'wireframe': bool(self.wireframe),
        }
        if self.rotation_matrix is not None:
            json_dict['rotation_matrix'] = self.rotation_matrix.tolist()
        return json_dict

    def write_binary(self, path):
        """Write binary payload for this element (no-op for superquadrics)."""
        return

    def write_blender(self, path):
        """Write a Blender-friendly mesh for this element."""
        import open3d as o3d

        def f(o, m):
            sin_o = np.sin(o)
            return np.sign(sin_o) * np.abs(sin_o) ** m

        def g(o, m):
            cos_o = np.cos(o)
            return np.sign(cos_o) * np.abs(cos_o) ** m

        def quat_to_rot_matrix(quat):
            x, y, z, w = quat
            xx = x * x
            yy = y * y
            zz = z * z
            xy = x * y
            xz = x * z
            yz = y * z
            wx = w * x
            wy = w * y
            wz = w * z
            return np.array([
                [1.0 - 2.0 * (yy + zz), 2.0 * (xy - wz), 2.0 * (xz + wy)],
                [2.0 * (xy + wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - wx)],
                [2.0 * (xz - wy), 2.0 * (yz + wx), 1.0 - 2.0 * (xx + yy)],
            ], dtype=np.float32)

        def apply_bending_axis(x, y, z, val_kb, val_alpha, axis):
            if np.abs(val_kb) < 1e-3:
                return x, y, z

            if axis == 'z':
                u, v_coord, w = x, y, z
            elif axis == 'x':
                u, v_coord, w = y, z, x
            else:
                u, v_coord, w = z, x, y

            sin_alpha = np.sin(val_alpha)
            cos_alpha = np.cos(val_alpha)
            r = u * cos_alpha + v_coord * sin_alpha
            inv_kb = 1.0 / val_kb
            gamma = w * val_kb
            rho = inv_kb - r
            R = inv_kb - rho * np.cos(gamma)
            expr = R - r
            u = u + expr * cos_alpha
            v_coord = v_coord + expr * sin_alpha
            w = rho * np.sin(gamma)

            if axis == 'z':
                return u, v_coord, w
            if axis == 'x':
                return w, u, v_coord
            return v_coord, w, u

        A = float(self.scalings[0])
        B = float(self.scalings[1])
        C = float(self.scalings[2])
        r = float(self.exponents[0])
        s = float(self.exponents[1])
        t = float(self.exponents[2])
        N = max(10, min(round(int(self.resolution) * 0.8), 50))

        def deform_vertex(x, y, z):
            """Apply tapering and bending to a single vertex."""
            if self.tapering is not None and (abs(self.tapering[0]) > 1e-6 or abs(self.tapering[1]) > 1e-6):
                z_norm = z / C
                fx = self.tapering[0] * z_norm + 1.0
                fy = self.tapering[1] * z_norm + 1.0
                x = x * fx
                y = y * fy
            if self.bending is not None:
                x, y, z = apply_bending_axis(x, y, z, self.bending[4], self.bending[5], 'y')
                x, y, z = apply_bending_axis(x, y, z, self.bending[2], self.bending[3], 'x')
                x, y, z = apply_bending_axis(x, y, z, self.bending[0], self.bending[1], 'z')
            return x, y, z

        def eval_pt(u_val, v_val):
            """Evaluate deformed surface point at parameter (u, v)."""
            x = A * g(v_val, r) * g(u_val, s)
            y = B * g(v_val, r) * f(u_val, s)
            z = C * f(v_val, t)
            return deform_vertex(x, y, z)

        # --- Arc-length parameterization ---
        def arc_length_sample(param_start, param_end, n_out, eval_fn):
            """Find parameter values producing equally-spaced points on a 3D curve."""
            n_dense = 500
            dense_params = [param_start + (param_end - param_start) * i / (n_dense - 1)
                            for i in range(n_dense)]
            dense_pts = [eval_fn(p) for p in dense_params]

            cum_len = [0.0] * n_dense
            for i in range(1, n_dense):
                dx = dense_pts[i][0] - dense_pts[i - 1][0]
                dy = dense_pts[i][1] - dense_pts[i - 1][1]
                dz = dense_pts[i][2] - dense_pts[i - 1][2]
                cum_len[i] = cum_len[i - 1] + np.sqrt(dx * dx + dy * dy + dz * dz)

            total_len = cum_len[-1]
            if total_len < 1e-12:
                return [param_start + (param_end - param_start) * i / (n_out - 1)
                        for i in range(n_out)]

            result = [0.0] * n_out
            result[0] = param_start
            result[-1] = param_end
            j = 0
            for i in range(1, n_out - 1):
                target_len = total_len * i / (n_out - 1)
                while j < n_dense - 2 and cum_len[j + 1] < target_len:
                    j += 1
                seg_len = cum_len[j + 1] - cum_len[j]
                frac = (target_len - cum_len[j]) / seg_len if seg_len > 1e-15 else 0.0
                result[i] = dense_params[j] + frac * (dense_params[j + 1] - dense_params[j])
            return result

        # Sample u at the equator (v=0), v at prime meridian (u=0)
        u_samples = arc_length_sample(-np.pi, np.pi, N, lambda u_val: (
            A * g(0.0, r) * g(u_val, s),
            B * g(0.0, r) * f(u_val, s),
            C * f(0.0, t),
        ))
        v_samples = arc_length_sample(-np.pi / 2, np.pi / 2, N, lambda v_val: (
            A * g(v_val, r) * g(0.0, s),
            B * g(v_val, r) * f(0.0, s),
            C * f(v_val, t),
        ))

        # --- Iterative grid resampling for equal edge lengths ---
        def resample_grid(u_samp, v_samp):
            """Resample grid so all edges are equal length on the 3D surface."""
            nu = len(u_samp)
            nv = len(v_samp)

            def dist3(a, b):
                dx, dy, dz = a[0] - b[0], a[1] - b[1], a[2] - b[2]
                return np.sqrt(dx * dx + dy * dy + dz * dz)

            # Step 1: Average arc-length distributions along u across all v-rows
            u_cum = [0.0] * nu
            for j_idx in range(nv):
                v_val = v_samp[j_idx]
                prev = eval_pt(u_samp[0], v_val)
                row_cum = 0.0
                for i_idx in range(1, nu):
                    cur = eval_pt(u_samp[i_idx], v_val)
                    row_cum += dist3(prev, cur)
                    u_cum[i_idx] += row_cum
                    prev = cur
            for i_idx in range(nu):
                u_cum[i_idx] /= nv

            u_total = u_cum[-1]
            new_u = list(u_samp)
            if u_total > 1e-12:
                new_u[0] = u_samp[0]
                new_u[-1] = u_samp[-1]
                k = 0
                for i_idx in range(1, nu - 1):
                    target = u_total * i_idx / (nu - 1)
                    while k < nu - 2 and u_cum[k + 1] < target:
                        k += 1
                    seg = u_cum[k + 1] - u_cum[k]
                    frac = (target - u_cum[k]) / seg if seg > 1e-15 else 0.0
                    new_u[i_idx] = u_samp[k] + frac * (u_samp[k + 1] - u_samp[k])

            # Step 2: Average arc-length distributions along v across all u-columns
            v_cum = [0.0] * nv
            for i_idx in range(nu):
                u_val = new_u[i_idx]
                prev = eval_pt(u_val, v_samp[0])
                col_cum = 0.0
                for j_idx in range(1, nv):
                    cur = eval_pt(u_val, v_samp[j_idx])
                    col_cum += dist3(prev, cur)
                    v_cum[j_idx] += col_cum
                    prev = cur
            for j_idx in range(nv):
                v_cum[j_idx] /= nu

            v_total = v_cum[-1]
            new_v = list(v_samp)
            if v_total > 1e-12:
                new_v[0] = v_samp[0]
                new_v[-1] = v_samp[-1]
                k = 0
                for j_idx in range(1, nv - 1):
                    target = v_total * j_idx / (nv - 1)
                    while k < nv - 2 and v_cum[k + 1] < target:
                        k += 1
                    seg = v_cum[k + 1] - v_cum[k]
                    frac = (target - v_cum[k]) / seg if seg > 1e-15 else 0.0
                    new_v[j_idx] = v_samp[k] + frac * (v_samp[k + 1] - v_samp[k])

            return new_u, new_v

        # --- Curvature-based subdivision ---
        def subdivide_high_curvature(u_samp, v_samp):
            """Insert midpoints where surface normals change rapidly."""
            nu = len(u_samp)
            nv = len(v_samp)
            eps = 1e-4

            # Compute normals at each grid point via central differences
            normals = [[None] * nu for _ in range(nv)]
            for j_idx in range(nv):
                for i_idx in range(nu):
                    u_val, v_val = u_samp[i_idx], v_samp[j_idx]
                    du_p = eval_pt(u_val + eps, v_val)
                    du_m = eval_pt(u_val - eps, v_val)
                    dv_p = eval_pt(u_val, v_val + eps)
                    dv_m = eval_pt(u_val, v_val - eps)
                    tu = (du_p[0] - du_m[0], du_p[1] - du_m[1], du_p[2] - du_m[2])
                    tv = (dv_p[0] - dv_m[0], dv_p[1] - dv_m[1], dv_p[2] - dv_m[2])
                    # Cross product tu x tv
                    nx = tu[1] * tv[2] - tu[2] * tv[1]
                    ny = tu[2] * tv[0] - tu[0] * tv[2]
                    nz = tu[0] * tv[1] - tu[1] * tv[0]
                    length = np.sqrt(nx * nx + ny * ny + nz * nz)
                    if length > 1e-12:
                        nx /= length
                        ny /= length
                        nz /= length
                    normals[j_idx][i_idx] = (nx, ny, nz)

            u_set = set(u_samp)
            v_set = set(v_samp)

            # Check u-edges (along rows)
            for j_idx in range(nv):
                for i_idx in range(nu - 1):
                    n1 = normals[j_idx][i_idx]
                    n2 = normals[j_idx][i_idx + 1]
                    dot = n1[0] * n2[0] + n1[1] * n2[1] + n1[2] * n2[2]
                    if dot < 0.95:  # normal changes by > ~18 degrees
                        u_set.add((u_samp[i_idx] + u_samp[i_idx + 1]) * 0.5)

            # Check v-edges (along columns)
            for i_idx in range(nu):
                for j_idx in range(nv - 1):
                    n1 = normals[j_idx][i_idx]
                    n2 = normals[j_idx + 1][i_idx]
                    dot = n1[0] * n2[0] + n1[1] * n2[1] + n1[2] * n2[2]
                    if dot < 0.95:
                        v_set.add((v_samp[j_idx] + v_samp[j_idx + 1]) * 0.5)

            return sorted(u_set), sorted(v_set)

        # --- Build mesh from parameter grid ---
        def build_mesh(u_samp, v_samp):
            """Build vertex positions and triangle faces from parameter grid."""
            nu = len(u_samp)
            nv = len(v_samp)
            positions = []
            for j_idx in range(nv):
                for i_idx in range(nu):
                    px, py, pz = eval_pt(u_samp[i_idx], v_samp[j_idx])
                    positions.append([px, py, pz])

            faces = []
            for j_idx in range(nv - 1):
                for i_idx in range(nu - 1):
                    i00 = j_idx * nu + i_idx
                    i10 = j_idx * nu + (i_idx + 1)
                    i11 = (j_idx + 1) * nu + (i_idx + 1)
                    i01 = (j_idx + 1) * nu + i_idx
                    faces.append([i00, i10, i11])
                    faces.append([i00, i11, i01])
                # Seam: connect last u column to first u column
                i00 = j_idx * nu + (nu - 1)
                i10 = j_idx * nu + 0
                i11 = (j_idx + 1) * nu + 0
                i01 = (j_idx + 1) * nu + (nu - 1)
                faces.append([i00, i10, i11])
                faces.append([i00, i11, i01])

            return np.array(positions, dtype=np.float32), np.array(faces, dtype=np.int32)

        # --- Pipeline: arc-length → 5x resample → subdivide → 3x resample → build ---
        cur_u = u_samples
        cur_v = v_samples
        for _ in range(5):
            cur_u, cur_v = resample_grid(cur_u, cur_v)

        cur_u, cur_v = subdivide_high_curvature(cur_u, cur_v)
        for _ in range(3):
            cur_u, cur_v = resample_grid(cur_u, cur_v)

        vertices, faces = build_mesh(cur_u, cur_v)

        # Apply rotation
        if self.rotation_matrix is not None:
            rot = np.array(self.rotation_matrix, dtype=np.float32)
        else:
            rot = quat_to_rot_matrix(self.rotation)
        vertices = vertices @ rot.T

        # Apply translation
        vertices = vertices + np.array(self.translation, dtype=np.float32)

        mesh_sq = o3d.geometry.TriangleMesh()
        mesh_sq.vertices = o3d.utility.Vector3dVector(vertices)
        mesh_sq.triangles = o3d.utility.Vector3iVector(faces)
        mesh_sq.compute_vertex_normals()
        o3d.io.write_triangle_mesh(path, mesh_sq)
        return