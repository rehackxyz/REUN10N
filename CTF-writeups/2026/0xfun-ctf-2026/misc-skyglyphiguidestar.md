# misc - Skyglyph I: Guide Star

then inspect skyglyph_p75.png

Flag: `0xfun{5t4R5_t3LL_5t0r135}`

Solved by 171k
import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "tracker_dump.csv"


def load_data():
    xs = []
    ys = []
    fluxes = []
    named = []

    with CSV_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row["x_px"])
            y = float(row["y_px"])
            flux = float(row["flux"])
            xs.append(x)
            ys.append(y)
            fluxes.append(flux)
            if row["name"]:
                ra_h = float(row["ra_h"])
                dec_deg = float(row["dec_deg"])
                named.append((row["name"], x, y, ra_h, dec_deg))

    return np.array(xs), np.array(ys), np.array(fluxes), named


def choose_tangent_point(guide_stars):
    ras_deg = [ra_h * 15.0 for (_, _, _, ra_h, _) in guide_stars]
    decs_deg = [dec_deg for (_, _, _, _, dec_deg) in guide_stars]
    ra0 = math.radians(sum(ras_deg) / len(ras_deg))
    dec0 = math.radians(sum(decs_deg) / len(decs_deg))
    return ra0, dec0


def radec_to_gnomonic(ra, dec, ra0, dec0):
    """Standard gnomonic projection. All angles in radians."""
    dra = ra - ra0
    if dra > math.pi:
        dra -= 2 * math.pi
    if dra < -math.pi:
        dra += 2 * math.pi

    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)
    sin_dec0 = math.sin(dec0)
    cos_dec0 = math.cos(dec0)

    denom = sin_dec * sin_dec0 + cos_dec * cos_dec0 * math.cos(dra)
    xi = cos_dec * math.sin(dra) / denom
    eta = (sin_dec * cos_dec0 - cos_dec * sin_dec0 * math.cos(dra)) / denom
    return xi, eta


def build_camera_model(guide_stars, ra0, dec0):
    """Fit affine + radial distortion model: pixel -> tangent plane."""
    xs = [x for (_, x, _, _, _) in guide_stars]
    ys = [y for (_, _, y, _, _) in guide_stars]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)

    A_rows = []
    u_targets = []
    v_targets = []
    sky_uv = {}

    for name, x, y, ra_h, dec_deg in guide_stars:
        p = x - cx
        q = y - cy
        r2 = p * p + q * q

        ra = math.radians(ra_h * 15.0)
        dec = math.radians(dec_deg)
        u, v = radec_to_gnomonic(ra, dec, ra0, dec0)

        A_rows.append([1.0, p, q, r2 * p, r2 * q])
        u_targets.append(u)
        v_targets.append(v)
        sky_uv[name] = (u, v)

    A = np.array(A_rows)
    u_targets = np.array(u_targets)
    v_targets = np.array(v_targets)

    a_coeffs, *_ = np.linalg.lstsq(A, u_targets, rcond=None)
    b_coeffs, *_ = np.linalg.lstsq(A, v_targets, rcond=None)

    return (cx, cy, a_coeffs, b_coeffs, sky_uv)


def apply_camera_model(xs, ys, model):
    cx, cy, a, b, _ = model
    p = xs - cx
    q = ys - cy
    r2 = p * p + q * q
    A = np.stack([np.ones_like(p), p, q, r2 * p, r2 * q], axis=1)
    u = A @ a
    v = A @ b
    return u, v


def orient_with_deneb_altair(u, v, sky_uv):
    """Use Vega as origin, Deneb for +X, Altair for +Y sign."""
    vega = sky_uv["Vega"]
    deneb = sky_uv["Deneb"]
    altair = sky_uv["Altair"]

    u0 = u - vega[0]
    v0 = v - vega[1]

    dx = deneb[0] - vega[0]
    dy = deneb[1] - vega[1]

    theta = -math.atan2(dy, dx)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    u_rot = cos_t * u0 - sin_t * v0
    v_rot = sin_t * u0 + cos_t * v0

    alt_u0 = altair[0] - vega[0]
    alt_v0 = altair[1] - vega[1]
    alt_u_rot = cos_t * alt_u0 - sin_t * alt_v0
    alt_v_rot = sin_t * alt_u0 + cos_t * alt_v0

    if alt_v_rot < 0:
        v_rot = -v_rot

    return u_rot, v_rot


def make_plot(u, v, fluxes, out_path, percentile=None):
    """Create a single plot with optional flux filtering."""
    fluxes_arr = np.asarray(fluxes)
    
    if percentile is not None:
        thresh = np.percentile(fluxes_arr, percentile)
        mask = fluxes_arr >= thresh
        u_plot = u[mask]
        v_plot = v[mask]
        flux_plot = fluxes_arr[mask]
    else:
        u_plot = u
        v_plot = v
        flux_plot = fluxes_arr

    u_min, u_max = np.min(u_plot), np.max(u_plot)
    v_min, v_max = np.min(v_plot), np.max(v_plot)
    pad_u = 0.1 * (u_max - u_min)
    pad_v = 0.1 * (v_max - v_min)

    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # Use size based on flux
    if percentile is None:
        sizes = np.clip(flux_plot / np.max(flux_plot) * 15, 0.3, 8)
    else:
        sizes = 3
    
    ax.scatter(u_plot, v_plot, s=sizes, c='white', marker='.', 
               linewidths=0, alpha=0.8)
    
    ax.set_xlim(u_min - pad_u, u_max + pad_u)
    ax.set_ylim(v_min - pad_v, v_max + pad_v)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=500, facecolor='black', bbox_inches='tight')
    plt.close()


def main():
    xs, ys, fluxes, named = load_data()
    print(f"Total detections: {len(xs)}")
    print(f"Guide stars: {len(named)}")

    ra0, dec0 = choose_tangent_point(named)
    print(f"Tangent point: RA={math.degrees(ra0):.3f}°, Dec={math.degrees(dec0):.3f}°")

    model = build_camera_model(named, ra0, dec0)
    u, v = apply_camera_model(xs, ys, model)
    
    sky_uv = model[4]
    print("\nCalibration residuals (guide stars):")
    for name, x, y, ra_h, dec_deg in named:
        ra = math.radians(ra_h * 15.0)
        dec = math.radians(dec_deg)
        u_true, v_true = radec_to_gnomonic(ra, dec, ra0, dec0)
        u_pred, v_pred = apply_camera_model(np.array([x]), np.array([y]), model)
        err = math.sqrt((u_true - u_pred[0])**2 + (v_true - v_pred[0])**2)
        print(f"  {name:10s}: error = {err:.6f}")

    u_o, v_o = orient_with_deneb_altair(u, v, sky_uv)

    # Try a wide range of flux thresholds
    print("\nGenerating plots with different flux thresholds...")
    for p in [50, 60, 70, 75, 80, 85, 88, 90, 92, 94, 95, 96, 97, 98, 99]:
        out = HERE / f"skyglyph_p{p:02d}.png"
        make_plot(u_o, v_o, fluxes, out, percentile=p)
        print(f"  Wrote {out.name}")
     
    out_all = HERE / "skyglyph_all.png"
    make_plot(u_o, v_o, fluxes, out_all, percentile=None)
    print(f"  Wrote {out_all.name}")
    
    print("\nTrying inverted flux filtering (dimmest stars)...")
    fluxes_inv = np.max(fluxes) - fluxes
    for p in [50, 60, 70, 80, 90]:
        out = HERE / f"skyglyph_inv_p{p:02d}.png"
        make_plot(u_o, v_o, fluxes_inv, out, percentile=p)
        print(f"  Wrote {out.name}")


if __name__ == "__main__":
    main()

Solved by: ha1qal