#!/usr/bin/env python3
"""Parametric plan generator for the 5916 Panama Ave two-story rear addition.

Usage:
  python3 generate_plans.py --params "L stair/params.json" --out "L stair"
  python3 generate_plans.py --params V0/params.json --out V0
  python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs

Plan orientation (matches the owner's floorplanner sketches):
  bottom = north (existing house / Panama Ave side), left = east (property line),
  top = south (backyard), right = west.
"""

import argparse
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow, Circle, Arc, Wedge

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = HERE
P = {}
EXT = 6.5
INT = 4.5

WALL_COLOR = "#222222"
ROOM_COLOR = "#f5e3c3"
DIM_COLOR = "#555555"
FIXTURE_COLOR = "#9fb7c9"


def load_params(path):
    global P, EXT, INT
    with open(path) as f:
        P = json.load(f)
    EXT = P["walls"]["exterior_thickness"]
    INT = P["walls"]["interior_thickness"]


def out_path(name):
    return os.path.join(OUTDIR, name)


def ft_in(inches):
    sign = "-" if inches < 0 else ""
    inches = abs(inches)
    ft = int(inches // 12)
    rem = inches - ft * 12
    whole = int(rem)
    frac = rem - whole
    frac_txt = ""
    if abs(frac - 0.5) < 0.01:
        frac_txt = " 1/2"
    elif abs(frac - 0.25) < 0.01:
        frac_txt = " 1/4"
    elif abs(frac - 0.75) < 0.01:
        frac_txt = " 3/4"
    elif frac > 0.01:
        frac_txt = f" {frac:.2f}".rstrip("0")
    if whole == 0 and not frac_txt:
        return f"{sign}{ft}'"
    return f'{sign}{ft}\'-{whole}{frac_txt}"'


def dim_h(ax, x0, x1, y, label=None, offset=0):
    y = y + offset
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM_COLOR, lw=0.9))
    for x in (x0, x1):
        ax.plot([x, x], [y - 3, y + 3], color=DIM_COLOR, lw=0.7)
    ax.text((x0 + x1) / 2, y + 3, label or ft_in(abs(x1 - x0)),
            ha="center", va="bottom", fontsize=8, color=DIM_COLOR)


def dim_v(ax, y0, y1, x, label=None, offset=0):
    x = x + offset
    ax.annotate("", xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM_COLOR, lw=0.9))
    for y in (y0, y1):
        ax.plot([x - 3, x + 3], [y, y], color=DIM_COLOR, lw=0.7)
    ax.text(x + 3, (y0 + y1) / 2, label or ft_in(abs(y1 - y0)),
            ha="left", va="center", fontsize=8, color=DIM_COLOR, rotation=90)


def wall_rect(ax, x, y, w, h, color=WALL_COLOR):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="none", zorder=3))


def room(ax, x, y, w, h, name, sub=None, fs=10, dy=0):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=ROOM_COLOR, edgecolor="none", zorder=1))
    label = name if not sub else f"{name}\n{sub}"
    ax.text(x + w / 2, y + h / 2 + dy, label, ha="center", va="center",
            fontsize=fs, zorder=5, color="#333333")


def fixture(ax, x, y, w, h, name, fs=7):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FIXTURE_COLOR,
                           edgecolor="#4a6172", lw=0.8, zorder=4))
    ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=fs, zorder=5)


def door(ax, x, y, w, horizontal=True):
    if horizontal:
        ax.add_patch(Rectangle((x, y - 1), w, EXT + 2, facecolor="white",
                               edgecolor="none", zorder=4))
    else:
        ax.add_patch(Rectangle((x - 1, y), EXT + 2, w, facecolor="white",
                               edgecolor="none", zorder=4))


def window(ax, x, y, w, horizontal=True, wall=None):
    wall = EXT if wall is None else wall
    if horizontal:
        ax.add_patch(Rectangle((x, y), w, wall, facecolor="#dfeefb",
                               edgecolor="#4a6172", lw=0.8, zorder=4))
    else:
        ax.add_patch(Rectangle((x, y), wall, w, facecolor="#dfeefb",
                               edgecolor="#4a6172", lw=0.8, zorder=4))


def compass(ax, x, y):
    ax.text(x, y, "N ▼ (to existing house / Panama Ave)\nS ▲ (backyard)   "
                  "E ◄ (property line)   W ►",
            fontsize=8, color="#444444", ha="left", va="top",
            bbox=dict(boxstyle="round", fc="#f0f0f0", ec="#999999"))


def base_axes(title):
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_title(title, fontsize=13)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def stair_shape():
    return P["stair"].get("shape", "L")


def stair_geom():
    """Return geometry dict for the configured stair shape."""
    st = P["stair"]
    shape = st.get("shape", "L")
    D = P["first_floor"]["main_block_ext_depth"]
    off = P["second_floor"]["east_face_offset_from_ground_east_face"]
    risers = math.ceil(st["total_rise"] / st["riser_max"])
    riser = st["total_rise"] / risers

    if shape == "straight":
        land = st["top_landing"]
        treads = risers - 1
        run = treads * st["tread_run"]
        west_over = max(0, (off + land + run) - P["first_floor"]["main_block_ext_width"])
        return {
            "shape": "straight", "risers": risers, "riser": riser,
            "treads": treads, "tread": st["tread_run"], "width": st["width"],
            "top_landing": (off, D, land, land),
            "run": (off + land, D, run, st["width"]),
            "yard_projection_in": max(land, west_over),
            "west_overhang_in": west_over,
            "summary": f"straight: {risers} risers @ {riser:.2f}\", run {run/12:.1f} ft "
                       f"(+{west_over/12:.1f}' past SW corner)",
        }

    if shape == "spiral":
        dia = st["diameter"]
        land = st["top_landing"]
        # Spiral centered just south of the SE entry, against the south wall
        cx = off + land / 2
        cy = D + dia / 2
        return {
            "shape": "spiral", "risers": risers, "riser": riser,
            "diameter": dia, "center": (cx, cy),
            "top_landing": (off, D, land, land),
            "yard_projection_in": dia,
            "west_overhang_in": 0,
            "summary": (
                f"spiral Ø{ft_in(dia)}: {risers} risers @ {riser:.2f}\" "
                f"(CRC R311.7.10.1 — rise≤9.5\", walkline≥6.75\", clear≥26\")"
            ),
        }

    # L-stair (default)
    up_r = st["upper_flight_risers"]
    lo_r = risers - up_r
    w, land, cland, tread = st["width"], st["top_landing"], st["corner_landing"], st["tread_run"]
    up_x0 = off + land
    up_len = (up_r - 1) * tread
    lo_len = (lo_r - 1) * tread
    cx = up_x0 + up_len
    return {
        "shape": "L", "risers": risers, "riser": riser,
        "up_r": up_r, "lo_r": lo_r, "tread": tread, "width": w,
        "top_landing": (off, D, land, land),
        "upper": (up_x0, D, up_len, w),
        "corner": (cx, D, cland, cland),
        "lower": (cx, D - lo_len, w, lo_len),
        "pad": (cx, D - lo_len - 36, w, 36),
        "corner_height": st["total_rise"] - up_r * riser,
        "yard_projection_in": max(land, cland),
        "west_overhang_in": max(0, (cx + cland) - P["first_floor"]["main_block_ext_width"]),
        "summary": f"L-stair: {risers} risers — upper {up_r} south + lower {lo_r} west",
    }


def draw_stair_rect(ax, rect, color="#e8e8e8", scale=1.0, dx=0.0, dy=0.0):
    x0, y0, w, h = [v * scale for v in rect]
    ax.add_patch(Rectangle((x0 + dx, y0 + dy), w, h, facecolor=color,
                           edgecolor="#666666", lw=0.9, zorder=2))
    return x0 + dx, y0 + dy, w, h


def draw_stair_plan(ax, g):
    """Draw stair on a floor plan (inch coords). Returns (xmax, ymax) for limits."""
    if g["shape"] == "straight":
        tl = draw_stair_rect(ax, g["top_landing"], color="#d9d9d9")
        ax.text(tl[0] + tl[2] / 2, tl[1] + tl[3] / 2, "LANDING\n4'×4'", ha="center",
                va="center", fontsize=7, zorder=5)
        rx, ry, rw, rh = draw_stair_rect(ax, g["run"])
        for i in range(1, g["treads"]):
            ax.plot([rx + i * g["tread"], rx + i * g["tread"]], [ry, ry + rh],
                    color="#999999", lw=0.5, zorder=3)
        ax.add_patch(FancyArrow(rx + rw - 20, ry + rh / 2, -(rw - 45), 0,
                                width=0.6, head_width=6, head_length=10,
                                color="#444444", zorder=4))
        ax.text(rx + rw / 2, ry + rh + 6, g["summary"] + " — rises to EAST (left)",
                ha="center", fontsize=7.5)
        return rx + rw, ry + rh

    if g["shape"] == "spiral":
        tl = draw_stair_rect(ax, g["top_landing"], color="#d9d9d9")
        ax.text(tl[0] + tl[2] / 2, tl[1] + tl[3] / 2, "LANDING\n4'×4'", ha="center",
                va="center", fontsize=7, zorder=5)
        cx, cy = g["center"]
        r = g["diameter"] / 2
        ax.add_patch(Circle((cx, cy), r, facecolor="#e8e8e8", edgecolor="#666666",
                            lw=1.2, zorder=2))
        ax.add_patch(Circle((cx, cy), 4, facecolor="#666666", edgecolor="none", zorder=4))
        # tread rays
        for i in range(g["risers"]):
            ang = math.radians(i * (360 / g["risers"]) - 90)
            ax.plot([cx, cx + r * math.cos(ang)], [cy, cy + r * math.sin(ang)],
                    color="#999999", lw=0.6, zorder=3)
        # UP arrow arc
        ax.add_patch(Arc((cx, cy), r * 1.3, r * 1.3, angle=0, theta1=-20, theta2=200,
                         color="#444444", lw=1.2, zorder=4))
        ax.text(cx, cy + r + 10, g["summary"], ha="center", fontsize=7.5)
        ax.text(cx, cy - r - 8, "UP ↻  (people only — furniture via west window)",
                ha="center", fontsize=7, color="#1d4ed8")
        return cx + r, cy + r

    # L
    tl = draw_stair_rect(ax, g["top_landing"], color="#d9d9d9")
    ax.text(tl[0] + tl[2] / 2, tl[1] + tl[3] / 2, "LANDING\n4'×4'", ha="center",
            va="center", fontsize=7, zorder=5)
    ux, uy, uw, uh = draw_stair_rect(ax, g["upper"])
    for i in range(1, g["up_r"] - 1):
        ax.plot([ux + i * g["tread"], ux + i * g["tread"]], [uy, uy + uh],
                color="#999999", lw=0.5, zorder=3)
    ax.add_patch(FancyArrow(ux + uw - 14, uy + uh / 2, -(uw - 28), 0,
                            width=0.5, head_width=5, head_length=8, color="#444444",
                            zorder=4))
    cx, cy, cw, ch = draw_stair_rect(ax, g["corner"], color="#d0d0d0")
    ax.text(cx + cw / 2, cy + ch / 2, "CORNER\n42\"×42\"", ha="center",
            va="center", fontsize=6.5, zorder=5)
    lx, ly, lw, lh = draw_stair_rect(ax, g["lower"])
    for i in range(1, g["lo_r"] - 1):
        ax.plot([lx, lx + lw], [ly + lh - i * g["tread"], ly + lh - i * g["tread"]],
                color="#999999", lw=0.5, zorder=3)
    ax.add_patch(FancyArrow(lx + lw / 2, ly + 14, 0, lh - 28,
                            width=0.5, head_width=5, head_length=8, color="#444444",
                            zorder=4))
    px, py, pw, ph = draw_stair_rect(ax, g["pad"], color="#c8c8c8")
    ax.text(px + pw / 2 + 18, py + ph / 2, "BOTTOM ↑ UP", ha="left", va="center",
            fontsize=6.5, color="#555555")
    ax.text((ux + cx + cw) / 2, cy + ch + 8,
            g["summary"] + "\n(lower flight partly under 2'-6\" cantilever; yard stays clear)",
            ha="center", fontsize=7.5)
    return max(cx + cw, ux + uw), cy + ch


def draw_stair_site(ax, g, e_gf, ay):
    if g["shape"] == "straight":
        for key, color in [("top_landing", "#bfbfbf"), ("run", "#dddddd")]:
            draw_stair_rect(ax, g[key], color=color, scale=1 / 12.0, dx=e_gf, dy=ay)
        r = g["run"]
        ax.text(e_gf + (r[0] + r[2] / 2) / 12.0, ay + (r[1] + r[3]) / 12.0 + 0.6,
                "straight stair (projects into yard)", fontsize=7, ha="center")
    elif g["shape"] == "spiral":
        draw_stair_rect(ax, g["top_landing"], color="#bfbfbf", scale=1 / 12.0,
                        dx=e_gf, dy=ay)
        cx, cy = g["center"]
        ax.add_patch(Circle((e_gf + cx / 12.0, ay + cy / 12.0), g["diameter"] / 24.0,
                            facecolor="#dddddd", edgecolor="#555555", lw=1.0, zorder=2))
        ax.text(e_gf + cx / 12.0, ay + cy / 12.0 + g["diameter"] / 24.0 + 0.6,
                f"spiral Ø{g['diameter']/12:.0f}'", fontsize=7, ha="center")
    else:
        for key, color in [("top_landing", "#bfbfbf"), ("upper", "#dddddd"),
                           ("corner", "#bfbfbf"), ("lower", "#dddddd"), ("pad", "#c8c8c8")]:
            draw_stair_rect(ax, g[key], color=color, scale=1 / 12.0, dx=e_gf, dy=ay)
        ax.text(e_gf + g["corner"][0] / 12.0 + 1.5,
                ay + g["top_landing"][1] / 12.0 + g["corner"][3] / 12.0 + 0.8,
                "L-stair (hugs SW corner)", fontsize=7, ha="center")


# ============================================================================
# First floor (identical across variants)
# ============================================================================

def first_floor():
    f = P["first_floor"]
    h = P["existing_house"]
    W, D = f["main_block_ext_width"], f["main_block_ext_depth"]
    nz = f["north_zone_interior_depth"]
    bathw = f["bath_interior_width"]
    closd = f.get("closet_interior_depth", 30)
    cor_ns = f["corridor_interior_ns"]
    yard_door = f.get("yard_door", "slider")
    door_w = f.get("yard_door_width", f.get("slider_width", 72))
    bath_fix = f.get("bath_fixtures", "tub")
    closet_style = f.get("closet_style", "east_west")
    lean = closet_style == "reach_in_west" or closd == 0

    hx_east = h["east_face_local_x"]
    x_bd = h["bedroom_dining_wall_local_x"]
    x_dk = h["dining_kitchen_wall_local_x"]
    din_e, din_w = x_bd + 4, x_dk - 4.5

    door_lbl = (f'{ft_in(door_w)} DOUBLE DOORS → backyard' if yard_door == "double"
                else f'{ft_in(door_w)} DOUBLE SLIDER → backyard')
    title = (
        f"First floor — LEAN: bedroom + shower bath; dining corridor with {door_lbl.split('→')[0].strip()}\n"
        f"east face at 5'-0\" setback; {f['ceiling_height_ft']:.0f}'-0\" ceilings; "
        f"main block {ft_in(W)} × {ft_in(D)}"
        if lean else
        "First floor — bedroom + full bath + E-W closet; wide corridor off the DINING ROOM\n"
        f"with {door_lbl}; east face at 5'-0\" setback; 9'-0\" ceilings"
    )
    fig, ax = base_axes(title)

    iw, idp = W - 2 * EXT, D - 2 * EXT
    entryw = iw - bathw - INT
    y_zone = EXT + nz
    if lean:
        y_bed = y_zone + INT
        bedd = D - EXT - y_bed
        entry_south = y_zone
    else:
        y_clos = y_zone + INT + closd
        y_bed = y_clos + INT
        bedd = D - EXT - y_bed
        entry_south = y_clos
    x_bath = EXT + bathw
    cor_w_int = din_w
    cor_x1 = cor_w_int + EXT

    ghost_d = 110
    for x0, x1, name in [(hx_east, x_bd, "EXISTING BEDROOM\n(rear windows covered —\nverify egress at side window)"),
                         (x_bd, x_dk, "DINING ROOM"),
                         (x_dk, x_dk + 130, "KITCHEN\n(sink wall untouched)")]:
        ax.add_patch(Rectangle((x0, -ghost_d), x1 - x0, ghost_d, fill=False,
                               edgecolor="#aaaaaa", lw=1.0, linestyle="--", zorder=0))
        ax.text((x0 + x1) / 2, -ghost_d / 2, name, ha="center", va="center",
                fontsize=7.5, color="#888888", zorder=0)
    ax.text((hx_east + x_dk + 100) / 2, -ghost_d - 10, "EXISTING HOUSE (1 story)",
            ha="center", fontsize=9, color="#777777")

    room(ax, EXT, EXT, bathw, nz, "BATH 1", f"{ft_in(bathw)} × {ft_in(nz)}")
    if not lean:
        room(ax, EXT, y_zone + INT, bathw, closd, "CLOSET (sliders)",
             f"{ft_in(bathw)} × {ft_in(closd)}", fs=8)
    ax.add_patch(Rectangle((x_bath + INT, 0), entryw, entry_south, facecolor=ROOM_COLOR,
                           edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((W - EXT, 0), cor_w_int - W + EXT, cor_ns,
                           facecolor=ROOM_COLOR, edgecolor="none", zorder=1))
    ax.text(x_bath + INT + entryw / 2, entry_south / 2, "ENTRY", ha="center",
            va="center", fontsize=8, color="#333333", zorder=5, rotation=90)
    ax.text((W + cor_w_int) / 2, cor_ns / 2, "CORRIDOR\n(open to dining)", ha="center",
            va="center", fontsize=7.5, color="#333333", zorder=5)
    room(ax, EXT, y_bed, iw, bedd, "BEDROOM", f"{ft_in(iw)} × {ft_in(bedd)}",
         dy=-bedd / 2 + 22)

    wall_rect(ax, 0, 0, EXT, D)
    wall_rect(ax, 0, D - EXT, W, EXT)
    wall_rect(ax, 0, 0, x_bd, EXT)
    wall_rect(ax, W - EXT, 0, EXT, EXT)
    wall_rect(ax, W - EXT, cor_ns + EXT, EXT, D - cor_ns - EXT)
    wall_rect(ax, W - EXT, cor_ns, cor_x1 - W + EXT, EXT)
    wall_rect(ax, cor_w_int, 0, EXT, cor_ns + EXT)
    wall_rect(ax, x_bath, EXT, INT, entry_south - EXT)  # bath / entry
    if lean:
        wall_rect(ax, EXT, y_zone, iw, INT)              # bath+entry / bedroom
    else:
        wall_rect(ax, EXT, y_zone, bathw, INT)           # bath / closet
        wall_rect(ax, EXT, entry_south, iw, INT)         # closet+entry / bedroom

    ax.plot([din_e, cor_w_int], [0, 0], color="#e07000", lw=3, zorder=6)
    ax.text((din_e + cor_w_int) / 2, -16,
            f"existing dining rear wall opened {ft_in(cor_w_int - din_e)} (new header)",
            ha="center", fontsize=8, color="#8a4b00", zorder=6,
            bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.8))
    ax.annotate("", xy=(x_bath + INT + entryw / 2 - 10, entry_south - 16),
                xytext=((din_e + cor_w_int) / 2, -40),
                arrowprops=dict(arrowstyle="-|>", color="#2f7d2f", lw=1.6,
                                connectionstyle="arc3,rad=0.3"), zorder=6)

    door(ax, x_bath, EXT + nz - 34, 30, horizontal=False)
    door(ax, x_bath + INT + 5, y_zone if lean else entry_south, 32, horizontal=True)
    if not lean:
        door(ax, EXT + bathw / 2 - 30, entry_south, 60, horizontal=True)
        ax.text(EXT + bathw / 2, entry_south + INT + 4, "closet sliders", ha="center",
                fontsize=6.5, color="#666666", zorder=6)
    else:
        # reach-in closet on west wall of bedroom
        rw = f.get("reach_in_width", 60)
        rd = f.get("reach_in_depth", 24)
        fixture(ax, W - EXT - rd, y_bed + 12, rd, rw, "REACH-IN\nCLOSET")

    window(ax, EXT + iw / 2 - 24, D - EXT, 48, horizontal=True)
    ax.text(EXT + iw / 2, D + 4, "egress window (CRC R310)",
            ha="center", fontsize=7, color="#4a6172")
    window(ax, W - EXT, y_bed + bedd / 2 - 18, 36, horizontal=False)

    # yard door in corridor south wall
    yd_x = (W - EXT + cor_w_int) / 2 - door_w / 2
    window(ax, yd_x, cor_ns, door_w, horizontal=True)
    if yard_door == "double":
        ax.plot([yd_x + door_w / 2, yd_x + door_w / 2], [cor_ns, cor_ns + EXT],
                color="#4a6172", lw=1.0, zorder=5)
    ax.annotate("", xy=(yd_x + door_w / 2 + 26, cor_ns + EXT + 16),
                xytext=(yd_x + door_w / 2 - 26, cor_ns + EXT + 16),
                arrowprops=dict(arrowstyle="<->", color="#1d4ed8", lw=1.0))
    ax.text(yd_x + door_w / 2, cor_ns + EXT + 22, door_lbl,
            ha="center", fontsize=7.5, color="#1d4ed8")

    if bath_fix == "shower":
        fixture(ax, EXT, EXT + 4, 36, 36, "SHOWER\n36×36")
        fixture(ax, EXT + 42, EXT, 30, 28, "WC")
        fixture(ax, x_bath - 40, y_zone - 22, 36, 22, "VANITY 36\"")
    else:
        fixture(ax, EXT, EXT + 4, 30, 60, "TUB\n30×60")
        fixture(ax, EXT + 34, EXT, 30, 28, "WC")
        fixture(ax, x_bath - 62, y_zone - 22, 60, 22, "DOUBLE VANITY 60\"")
    ax.text(EXT + bathw / 2, -10, "bath wet wall backs existing bedroom",
            ha="center", fontsize=7, color="#4a6172",
            bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.8))
    fixture(ax, EXT + 8, y_bed + (bedd - 76) / 2, 80, 76, "KING BED\n76×80")

    dim_h(ax, 0, W, D + EXT, offset=26)
    dim_v(ax, 0, D, -14, offset=-26)
    dim_v(ax, 0, y_zone + INT / 2, -14, offset=-12, label=ft_in(y_zone + INT / 2))
    dim_v(ax, y_bed, D - EXT, -14, offset=-12, label=ft_in(bedd))
    dim_h(ax, W, cor_x1, cor_ns + EXT + 44, label=ft_in(cor_x1 - W))
    dim_v(ax, 0, cor_ns + EXT, cor_x1 + 10, label=ft_in(cor_ns + EXT))

    ax.annotate("", xy=(-60, D + 44), xytext=(0, D + 44),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.2))
    ax.text(-30, D + 50, "5'-0\" side setback\n(east property line)",
            ha="center", fontsize=8, color="#b00000")
    ax.plot([-60, -60], [-140, D + 90], color="#b00000", lw=1.4, linestyle="--")

    compass(ax, -95, D + 95)
    ax.set_xlim(-100, x_dk + 140)
    ax.set_ylim(-150, D + 100)
    fig.savefig(out_path("first-floor-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {
        "footprint_sqft": (W * D + (cor_x1 - W) * (cor_ns + EXT)) / 144.0,
        "interior_sqft": (iw * idp + (cor_w_int - (W - EXT)) * cor_ns) / 144.0,
        "dining_opening_in": cor_w_int - din_e,
        "bedroom": (iw, bedd),
        "lean": lean,
    }


# ============================================================================
# Second floor
# ============================================================================

def second_floor():
    s = P["second_floor"]
    f = P["first_floor"]
    st = P["stair"]
    off = s["east_face_offset_from_ground_east_face"]
    W, D = s["ext_width"], s["ext_depth"]
    bathd = s["bath_interior_depth"]
    bath_type = s.get("bath_type", "shower")  # shower | toilet_only
    has_kit = s.get("kitchenette", False)
    flush = off < 1
    shape = stair_shape()
    title_stair = {"L": "L-stair access", "straight": "straight exterior-stair access",
                   "spiral": "spiral-stair access + furniture window"}[shape]
    if has_kit:
        room_title = "ADU studio (kitchenette + full bath)"
    elif bath_type == "toilet_only":
        room_title = "room + toilet only"
    else:
        room_title = "office + shower bath"
    setback_note = ("East face at 5'-0\" setback, flush with 1st floor (ADU)"
                    if flush else
                    "East face at 9'-0\" side setback (conforming)")

    fig, ax = base_axes(
        f"Second floor — {room_title}, {title_stair}\n"
        f"{setback_note}; 8'-0\" ceilings")

    iw, idp = W - 2 * EXT, D - 2 * EXT
    x0 = off
    wall_rect(ax, x0, 0, W, EXT)
    wall_rect(ax, x0, D - EXT, W, EXT)
    wall_rect(ax, x0, 0, EXT, D)
    wall_rect(ax, x0 + W - EXT, 0, EXT, D)

    if bath_type == "toilet_only":
        bathw = s.get("bath_interior_width", 54)
        y_zone = EXT + bathd
        wall_rect(ax, x0 + EXT, y_zone, bathw, INT)
        wall_rect(ax, x0 + EXT + bathw, EXT, INT, bathd)
        room(ax, x0 + EXT, EXT, bathw, bathd, "WC",
             f"{ft_in(bathw)} × {ft_in(bathd)}\n(toilet + lav)", fs=8, dy=4)
        ax.add_patch(Rectangle((x0 + EXT, y_zone + INT), iw, idp - bathd - INT,
                               facecolor=ROOM_COLOR, edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((x0 + EXT + bathw + INT, EXT),
                               iw - bathw - INT, bathd + INT,
                               facecolor=ROOM_COLOR, edgecolor="none", zorder=1))
        ax.text(x0 + EXT + iw / 2, y_zone + INT + (idp - bathd - INT) / 2,
                f"ROOM\n{ft_in(iw)} × {ft_in(idp)} clear\n(open plan)",
                ha="center", va="center", fontsize=10, zorder=5, color="#333333")
        fixture(ax, x0 + EXT, EXT, 30, 28, "WC")
        fixture(ax, x0 + EXT + bathw - 22, EXT + 4, 20, 18, "LAV")
        door(ax, x0 + EXT + bathw / 2 - 12, y_zone, 28, horizontal=True)
        fixture(ax, x0 + EXT + iw - 66, y_zone + INT + 20, 60, 30, "DESK")
        west_win_y0 = y_zone + INT + 20
        west_win_span = idp - bathd - INT - 40
    elif has_kit:
        # ADU: bath NE + kitchenette NW strip + open studio south
        bathw = s.get("bath_interior_width", 90)
        kit_d = s.get("kitchenette_depth", 30)
        y_bath = EXT + bathd
        y_kit = EXT + kit_d
        kit_w = iw - bathw - INT
        wall_rect(ax, x0 + EXT, y_bath, bathw, INT)
        wall_rect(ax, x0 + EXT + bathw, EXT, INT, bathd)
        wall_rect(ax, x0 + EXT + bathw + INT, y_kit, kit_w, INT)
        room(ax, x0 + EXT, EXT, bathw, bathd, "BATH",
             f"{ft_in(bathw)} × {ft_in(bathd)}", fs=8, dy=8)
        room(ax, x0 + EXT + bathw + INT, EXT, kit_w, kit_d, "KITCHENETTE",
             f"{ft_in(kit_w)} × {ft_in(kit_d)}", fs=7, dy=0)
        # studio fill
        ax.add_patch(Rectangle((x0 + EXT, y_bath + INT), iw, idp - bathd - INT,
                               facecolor=ROOM_COLOR, edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((x0 + EXT + bathw + INT, y_kit + INT), kit_w,
                               bathd - kit_d, facecolor=ROOM_COLOR,
                               edgecolor="none", zorder=1))
        ax.text(x0 + EXT + iw / 2, y_bath + INT + (idp - bathd - INT) / 2,
                f"ADU STUDIO\nliving / sleeping\n{ft_in(iw)} wide",
                ha="center", va="center", fontsize=10, zorder=5, color="#333333")
        fixture(ax, x0 + EXT, EXT + 4, 36, 36, "SHOWER\n36×36")
        fixture(ax, x0 + EXT + 42, EXT, 30, 28, "WC")
        fixture(ax, x0 + EXT + bathw - 40, y_bath - 22, 36, 22, "VANITY")
        door(ax, x0 + EXT + bathw / 2 - 14, y_bath, 28, horizontal=True)
        # kitchenette fixtures along north wall
        kx = x0 + EXT + bathw + INT
        fixture(ax, kx + 4, EXT, 30, 24, "SINK")
        fixture(ax, kx + 38, EXT, 30, 24, "COOK\nTOP")
        fixture(ax, kx + kit_w - 28, EXT, 24, 28, "MINI\nFRIDGE")
        fixture(ax, x0 + EXT + iw - 70, y_bath + INT + 24, 60, 30, "BED / SOFA")
        west_win_y0 = y_bath + INT + 24
        west_win_span = idp - bathd - INT - 48
        ax.text(x0 + EXT + 4, -12, "ADU — confirm CA/Richmond ADU standards with Planning",
                fontsize=7.5, color="#8a4b00",
                bbox=dict(boxstyle="round", fc="#fff8e8", ec="#e07000"))
    else:
        y_zone = EXT + bathd
        wall_rect(ax, x0 + EXT, y_zone, iw, INT)
        offd = idp - bathd - INT
        room(ax, x0 + EXT, EXT, iw, bathd, "BATH 2",
             f"{ft_in(iw)} × {ft_in(bathd)}", dy=14)
        room(ax, x0 + EXT, y_zone + INT, iw, offd, "OFFICE",
             f"{ft_in(iw)} × {ft_in(offd)}")
        fixture(ax, x0 + EXT, EXT, 36, 36, "SHOWER\n36×36")
        fixture(ax, x0 + EXT + 42, EXT, 30, 28, "WC")
        fixture(ax, x0 + EXT + 78, EXT, 48, 22, "VANITY 48\"")
        fixture(ax, x0 + EXT + iw - 66, y_zone + INT + 16, 60, 30, "DESK")
        door(ax, x0 + EXT + 16, y_zone, 30, horizontal=True)
        west_win_y0 = y_zone + INT + (offd - 48) / 2
        west_win_span = 48
        bathw = iw
        y_bath = y_zone

    entry_x = x0 + EXT + 8
    door(ax, entry_x, D - EXT, 36, horizontal=True)
    ax.text(entry_x + 18, D + 6, "ENTRY", ha="center", fontsize=8, color="#8a4b00")

    window(ax, x0 + EXT + iw / 2 - 30, D - EXT, 60, horizontal=True)
    if has_kit:
        window(ax, x0 + EXT + bathw + INT + 8, 0, 28, horizontal=True)
    elif bath_type != "toilet_only":
        window(ax, x0 + EXT + iw - 40, 0, 30, horizontal=True)
    else:
        window(ax, x0 + EXT + bathw + INT + 10, 0, 30, horizontal=True)

    if s.get("furniture_window"):
        fw = s.get("furniture_window_width", 72)
        wy = west_win_y0 if bath_type == "toilet_only" or has_kit else west_win_y0
        if has_kit:
            wy = (EXT + bathd + INT) + 16
        window(ax, x0 + W - EXT, wy, min(fw, west_win_span if west_win_span > 40 else fw),
               horizontal=False)
        ax.text(x0 + W + 8, wy + fw / 2,
                f"FURNITURE ACCESS\n{ft_in(fw)} × {ft_in(s.get('furniture_window_height', 60))}\n"
                f"operable window/door",
                ha="left", va="center", fontsize=7.5, color="#1d4ed8",
                bbox=dict(boxstyle="round", fc="#eef5ff", ec="#1d4ed8"))
    else:
        window(ax, x0 + W - EXT, west_win_y0, min(48, max(24, west_win_span)),
               horizontal=False)

    ax.add_patch(Rectangle((0, 0), f["main_block_ext_width"], f["main_block_ext_depth"],
                           fill=False, edgecolor="#999999", lw=1.0, linestyle=":", zorder=0))
    if flush:
        ax.text(x0 + W + 8, D / 2, "walls flush\nwith 1st floor\n(5' setback)",
                ha="left", va="center", fontsize=7.5, color="#2f7d2f")
    else:
        ax.text(off - 6, f["main_block_ext_depth"] / 2, "first floor\nbelow\n(4'-0\" offset)",
                ha="center", va="center", fontsize=7, color="#888888", rotation=90)
    ax.plot([-20, x0 + W + 30], [0, 0], color="#aaaaaa", lw=1.2, linestyle="--", zorder=0)
    ax.text(x0 + W + 34, -2, "existing 1-story house / roof below ↓",
            ha="left", va="top", fontsize=7, color="#888888")
    fW = f["main_block_ext_width"]
    if abs((x0 + W) - fW) > 2:
        dim_h(ax, fW, x0 + W, -16, label=f"{ft_in(x0 + W - fW)} cantilever")
    else:
        dim_h(ax, 0, W, -16, label="flush with 1st floor")

    g = stair_geom()
    xmax, ymax = draw_stair_plan(ax, g)

    land = st.get("top_landing", 48)
    dim_h(ax, x0, x0 + W, D + land + 14, offset=22)
    dim_v(ax, 0, D, x0 - 14, offset=-24, label=ft_in(D))
    dim_v(ax, 0, EXT + bathd + INT / 2, x0 - 14, offset=-10,
          label=ft_in(EXT + bathd + INT / 2))
    if not flush:
        dim_h(ax, 0, x0, -16, label="4'-0\" offset")

    sy = max(D + land, ymax) + 34
    setback_ft = P["setbacks"]["east_pl_to_addition_upper_face_ft"]
    ax.annotate("", xy=(-12 * setback_ft, sy), xytext=(x0, sy),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.2))
    ax.text(x0 - 6 * setback_ft, sy + 6,
            f"{setback_ft:.0f}'-0\" side setback"
            + (" (flush ADU)" if flush else ""),
            ha="center", fontsize=8, color="#b00000")
    ax.plot([-12 * setback_ft, -12 * setback_ft], [-50, sy + 30], color="#b00000",
            lw=1.4, linestyle="--")

    compass(ax, -12 * setback_ft - 40, -70)
    ax.set_xlim(-12 * setback_ft - 80, max(x0 + W, xmax) + 90)
    ax.set_ylim(-120, sy + 50)
    fig.savefig(out_path("second-floor-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {
        "plate_sqft": W * D / 144.0,
        "interior_sqft": iw * idp / 144.0,
        "riser_in": g["riser"],
        "risers": g["risers"],
        "yard_projection_in": g["yard_projection_in"],
        "summary": g["summary"],
        "shape": g["shape"],
        "up_r": g.get("up_r"),
        "lo_r": g.get("lo_r"),
    }


# ============================================================================
# Site plan
# ============================================================================

def site_plan():
    s = P["site_ft"]
    f = P["first_floor"]
    h = P["existing_house"]
    sec = P["second_floor"]
    lw_, ld = s["lot_width"], s["lot_depth"]
    e_house = P["setbacks"]["existing_house_east_face_from_pl_ft"]
    e_gf = P["setbacks"]["east_pl_to_addition_ground_face_ft"]
    e_uf = P["setbacks"]["east_pl_to_addition_upper_face_ft"]

    fig, ax = plt.subplots(figsize=(9, 13))
    ax.set_title("Site plan (schematic) — 5916 Panama Ave, lot 50' × 100'\n"
                 "bottom = Panama Ave (north); left = east", fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), lw_, ld, fill=False, edgecolor="black", lw=1.5))
    ax.text(lw_ / 2, -4, "PANAMA AVE (north)", ha="center", fontsize=10, weight="bold")

    for x, lbl, c in [(5, "5' side", "#b00000"), (9, "9' upper side", "#e07000"),
                      (lw_ - 5, "5' side", "#b00000")]:
        ax.plot([x, x], [0, ld], color=c, lw=1.0, linestyle="--")
        ax.text(x + 0.4, ld - 2, lbl, fontsize=7, color=c, rotation=90, va="top")
    for y, lbl in [(20, "20' front"), (ld - 20, "20' rear"), (ld - 10, "10' reduced rear (optional)")]:
        ax.plot([0, lw_], [y, y], color="#b00000", lw=1.0, linestyle="--")
        ax.text(1, y + 0.4, lbl, fontsize=7, color="#b00000")

    hx, hy = e_house, s["house_front_setback"]
    hw, hd = h["width_ft"], h["depth_ft"]
    ax.add_patch(Rectangle((hx, hy), hw, hd, facecolor="#c9b8a3", edgecolor="#7a6a55", lw=1.2))
    ax.text(hx + hw / 2, hy + hd / 2,
            "EXISTING HOUSE\n40.25' × 30.5' (919 sq ft)\nfront setback assumed — verify",
            ha="center", va="center", fontsize=8.5)

    p = s["porch"]
    ax.add_patch(Rectangle((p["x0"], hy - p["depth"]), p["width"], p["depth"],
                           facecolor="#d3c7b5", edgecolor="#7a6a55", lw=1.0))
    ax.text(p["x0"] + p["width"] / 2, hy - p["depth"] / 2, "PORCH", ha="center",
            va="center", fontsize=7)
    gar = s["garage"]
    gx = hx + hw - gar["width"]
    gy = hy - gar["front_proud"]
    ax.add_patch(Rectangle((gx, gy), gar["width"], gar["length"], facecolor="#d3c7b5",
                           edgecolor="#7a6a55", lw=1.0))
    ax.text(gx + gar["width"] / 2, gy + gar["length"] / 2, "GARAGE\n(attached)",
            ha="center", va="center", fontsize=8)
    ax.text(gx + gar["width"] / 2, 8, "DRIVEWAY", ha="center", fontsize=7, color="#777777")
    ax.add_patch(Rectangle((hx + hw - 5, hy + hd), 4, 7, facecolor="#e0e0e0",
                           edgecolor="#888888", lw=0.8))
    ax.text(hx + hw - 3, hy + hd + 3.5, "ramp", ha="center", va="center", fontsize=6.5)
    sh = s["shed"]
    shy = ld - sh["from_rear_pl"] - sh["depth"]
    ax.add_patch(Rectangle((sh["x0"], shy), sh["width"], sh["depth"],
                           facecolor="#d3c7b5", edgecolor="#7a6a55", lw=1.0))
    ax.text(sh["x0"] + sh["width"] / 2, shy + sh["depth"] / 2,
            "SHED 135 sq ft\n(verify position)", ha="center", va="center", fontsize=7.5)

    ay = hy + hd
    aw = f["main_block_ext_width"] / 12.0
    ad = f["main_block_ext_depth"] / 12.0
    cor_x1 = h["dining_kitchen_wall_local_x"] - 4.5 + EXT
    cw = (cor_x1 - f["main_block_ext_width"]) / 12.0
    cd = (f["corridor_interior_ns"] + EXT) / 12.0
    ax.add_patch(Rectangle((e_gf, ay), aw, ad, facecolor="#9ec99e",
                           edgecolor="#3c6e3c", lw=1.4))
    ax.add_patch(Rectangle((e_gf + aw, ay), cw, cd, facecolor="#9ec99e",
                           edgecolor="#3c6e3c", lw=1.4))
    ax.text(e_gf + aw / 2, ay + ad / 2 - 2, "ADDITION\nground floor",
            ha="center", va="center", fontsize=8)

    sx = e_uf
    sw2 = sec["ext_width"] / 12.0
    flush = abs(e_uf - e_gf) < 0.1 and abs(sw2 - aw) < 0.1
    ax.add_patch(Rectangle((sx, ay), sw2, ad, fill=False, edgecolor="#1d4ed8",
                           lw=1.4, linestyle="-."))
    label = "2nd fl ADU\n(flush walls)" if sec.get("kitchenette") else "2nd floor"
    if flush and sec.get("kitchenette"):
        label = "2nd fl ADU (flush @ 5')"
    ax.text(sx + sw2 / 2, ay + ad / 2 + 3.5, label, ha="center",
            fontsize=8, color="#1d4ed8")

    g = stair_geom()
    draw_stair_site(ax, g, e_gf, ay)

    ax.annotate("", xy=(0, ay + ad / 2), xytext=(e_gf, ay + ad / 2),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.0))
    ax.text(e_gf / 2, ay + ad / 2 + 0.6, "5'", fontsize=8, color="#b00000", ha="center")
    ax.text(1, 1.5, "E ◄  lot line | W ►  (left = east)", fontsize=8, color="#444444")
    ax.set_xlim(-4, lw_ + 4)
    ax.set_ylim(-8, ld + 4)
    fig.savefig(out_path("site-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {"addition_rear_extent_ft": ay + ad,
            "rear_yard_remaining_ft": ld - (ay + ad),
            "stair_yard_projection_ft": g["yard_projection_in"] / 12.0}


# ============================================================================
# South elevation
# ============================================================================

def south_elevation():
    f = P["first_floor"]
    sec = P["second_floor"]
    st = P["stair"]
    lv = P["levels"]

    ff = lv["first_finish_floor_above_grade"]
    c1 = f["ceiling_height_ft"] * 12
    fl = lv["floor_assembly_depth"]
    c2 = sec["ceiling_height_ft"] * 12
    sf = ff + c1 + fl
    plate2 = sf + c2
    W1 = f["main_block_ext_width"]
    W2 = sec["ext_width"]
    pitch = lv["roof_pitch_in_12"]
    ridge = plate2 + 10 + (W2 / 2) * pitch / 12.0
    g = stair_geom()
    riser_h = g["riser"]

    shape = g["shape"]
    subtitle = {
        "L": "L-stair: upper flight along south wall; lower flight turns north at SW corner",
        "straight": "straight exterior stair rises west → east to second-floor entry",
        "spiral": "spiral stair at SE entry (people); furniture via west-wall window",
    }[shape]

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title(f"South elevation (from backyard, looking north) — east on RIGHT\n{subtitle}",
                 fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    def xd(x):
        return -x

    ax.plot([xd(W1 + 160), xd(-90)], [0, 0], color="#553311", lw=2)
    ax.text(xd(-88), -14, "grade", fontsize=8, color="#553311")

    ax.add_patch(Rectangle((xd(W1), 0), W1, ff + c1 + fl, facecolor="#e8dcc8",
                           edgecolor="#555555", lw=1.2))
    off = sec["east_face_offset_from_ground_east_face"]
    ax.add_patch(Rectangle((xd(off + W2), sf - fl), W2, fl + c2 + 8,
                           facecolor="#dfd2ba", edgecolor="#555555", lw=1.2))
    rx0, rx1 = xd(off + W2) - 12, xd(off) + 12
    ax.plot([rx0, (rx0 + rx1) / 2, rx1], [plate2 + 8, ridge, plate2 + 8],
            color="#555555", lw=1.4)
    ax.plot([xd(off), xd(0) + 8], [sf + 6, sf - 10], color="#555555", lw=1.2)

    for y, lbl in [(ff, f'1st FF  +{ft_in(ff)}'), (sf, f'2nd FF  +{ft_in(sf)}'),
                   (plate2, f'2nd plate  +{ft_in(plate2)}')]:
        ax.plot([xd(W1) - 6, xd(0) + 6], [y, y], color="#888888", lw=0.7, linestyle=":")
        ax.text(xd(W1) - 10, y, lbl, ha="right", va="center", fontsize=8, color="#555555")
    ax.text(xd(W2 / 2 + off), ridge + 8, f"ridge ≈ +{ft_in(ridge)}  (max 30')",
            ha="center", fontsize=8, color="#555555")

    ax.add_patch(Rectangle((xd(off + 14 + 36), sf), 36, 80, facecolor="#b98b4e",
                           edgecolor="#6b4c26", lw=1))
    ax.add_patch(Rectangle((xd(off + W2 / 2 + 55), sf + 36), 60, 48,
                           facecolor="#dfeefb", edgecolor="#4a6172", lw=1))
    ax.add_patch(Rectangle((xd(W1 / 2 + 24 - off / 2), ff + 30), 48, 48,
                           facecolor="#dfeefb", edgecolor="#4a6172", lw=1))
    ax.text(xd(W1 / 2 - off / 2), ff + 20, "bedroom egress", ha="center",
            fontsize=7, color="#4a6172")

    if shape == "straight":
        run = g["tread"]
        x_top = off + st["top_landing"]
        treads = g["treads"]
        for i in range(treads):
            x_plan = x_top + (treads - 1 - i) * run
            y0 = i * riser_h
            ax.plot([xd(x_plan + run), xd(x_plan + run)], [y0, y0 + riser_h],
                    color="#333333", lw=1.2)
            ax.plot([xd(x_plan + run), xd(x_plan)], [y0 + riser_h, y0 + riser_h],
                    color="#333333", lw=1.2)
        ax.plot([xd(x_top), xd(off)], [st["total_rise"], st["total_rise"]],
                color="#333333", lw=2.0)
        ax.plot([xd(x_top + treads * run), xd(x_top)],
                [42, st["total_rise"] + 42], color="#777777", lw=1)
        ax.plot([xd(x_top), xd(off)], [st["total_rise"] + 42, st["total_rise"] + 42],
                color="#777777", lw=1)
        ax.text(xd(x_top + treads * run / 2), st["total_rise"] / 2 - 20,
                f"{g['risers']} risers @ {riser_h:.2f}\" | {treads} treads @ {run}\"\n"
                f"guard 42\", handrail 34–38\"", fontsize=8, ha="center")
        xmin = xd(x_top + treads * run) - 90
    elif shape == "spiral":
        cx, _ = g["center"]
        r = g["diameter"] / 2
        # spiral as stacked ellipse/cylinder from grade to 2nd FF
        ax.add_patch(Rectangle((xd(cx + r), 0), g["diameter"], st["total_rise"],
                               facecolor="#d0d0d0", edgecolor="#333333", lw=1.2, alpha=0.7))
        for i in range(0, g["risers"], 2):
            y = i * riser_h
            ax.plot([xd(cx + r), xd(cx - r)], [y, y], color="#888888", lw=0.5)
        ax.text(xd(cx), st["total_rise"] / 2,
                f"SPIRAL\nØ{ft_in(g['diameter'])}\n{g['risers']} risers\n@ {riser_h:.2f}\"",
                ha="center", va="center", fontsize=8)
        ax.plot([xd(off + st["top_landing"]), xd(off)],
                [st["total_rise"], st["total_rise"]], color="#333333", lw=2.0)
        xmin = xd(W1 + 40) - 40
    else:
        run = g["tread"]
        x_top = off + st["top_landing"]
        up_treads = g["up_r"] - 1
        for i in range(up_treads):
            x_plan = x_top + (up_treads - 1 - i) * run
            y0 = g["corner_height"] + i * riser_h
            ax.plot([xd(x_plan + run), xd(x_plan + run)], [y0, y0 + riser_h],
                    color="#333333", lw=1.2)
            ax.plot([xd(x_plan + run), xd(x_plan)], [y0 + riser_h, y0 + riser_h],
                    color="#333333", lw=1.2)
        ax.plot([xd(x_top), xd(off)], [st["total_rise"], st["total_rise"]],
                color="#333333", lw=2.0)
        ax.plot([xd(x_top), xd(off)], [st["total_rise"] + 42, st["total_rise"] + 42],
                color="#777777", lw=1)
        ax.plot([xd(x_top + up_treads * run), xd(x_top)],
                [g["corner_height"] + 42, st["total_rise"] + 42], color="#777777", lw=1)
        cx = g["corner"][0]
        ax.add_patch(Rectangle((xd(cx + g["corner"][2]), g["corner_height"] - 4),
                               g["corner"][2], 8, facecolor="#bbbbbb",
                               edgecolor="#333333", lw=1.0, zorder=3))
        ax.add_patch(Rectangle((xd(cx + g["width"] + 8), 0), g["width"] + 8,
                               g["corner_height"], fill=False, edgecolor="#666666",
                               lw=1.0, linestyle="--", zorder=2))
        ax.text(xd(cx + g["width"] / 2), g["corner_height"] / 2,
                f"lower flight\n{g['lo_r']} risers\n(turns north)",
                ha="center", va="center", fontsize=7, color="#555555")
        xmin = xd(W1 + 90)

    ax.text(xd(off + W2 / 2), -22, g["summary"] + " | guard 42\", handrail 34–38\"",
            fontsize=8, ha="center")
    ax.text(xd(0) + 30, 10, "E →", fontsize=10, weight="bold")
    ax.text(xd(W1) - 30, 10, "← W", fontsize=10, weight="bold")
    ax.set_xlim(xmin, xd(0) + 80)
    ax.set_ylim(-40, ridge + 40)
    fig.savefig(out_path("south-elevation.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)
    return {"second_ff_in": sf, "ridge_ft": ridge / 12.0}


# ============================================================================
# West elevation
# ============================================================================

def west_elevation():
    f = P["first_floor"]
    h = P["existing_house"]
    sec = P["second_floor"]
    st = P["stair"]
    lv = P["levels"]

    ff = lv["first_finish_floor_above_grade"]
    c1 = f["ceiling_height_ft"] * 12
    fl = lv["floor_assembly_depth"]
    c2 = sec["ceiling_height_ft"] * 12
    sf = ff + c1 + fl
    plate2 = sf + c2
    W1 = f["main_block_ext_width"]
    W2 = sec["ext_width"]
    D = f["main_block_ext_depth"]
    off = sec["east_face_offset_from_ground_east_face"]
    pitch = lv["roof_pitch_in_12"]
    ridge = plate2 + 10 + (W2 / 2) * pitch / 12.0
    eaves = plate2 + 8
    cor_d = f["corridor_interior_ns"] + EXT
    door_w = f.get("yard_door_width", f.get("slider_width", 72))
    yard_door = f.get("yard_door", "slider")
    door_short = ("double doors" if yard_door == "double" else "slider")
    g = stair_geom()
    riser_h = g["riser"]
    shape = g["shape"]
    cant_in = off + W2 - W1
    flush = abs(cant_in) < 2

    subtitle = {
        "L": "L-stair lower flight in profile; corridor bump-out",
        "straight": "straight stair wraps past SW corner (end view)",
        "spiral": "spiral at SE (dashed, far side); west furniture window",
    }[shape]
    if flush:
        subtitle = subtitle + "; flush walls @ 5' setback (ADU)"
    elif abs(cant_in) >= 2:
        subtitle = subtitle + "; 2'-6\" cantilever"

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_title(f"West elevation (from side yard, looking east) — south on RIGHT\n{subtitle}",
                 fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    house_d = 110
    south_extent = D + g["yard_projection_in"] + 40
    ax.plot([-house_d - 20, south_extent], [0, 0], color="#553311", lw=2)
    ax.text(-house_d - 18, -14, "grade", fontsize=8, color="#553311")

    ax.add_patch(Rectangle((-house_d, 0), house_d, ff + 96, facecolor="#ddd5c8",
                           edgecolor="#999999", lw=1.0, linestyle="--", zorder=0))
    ax.text(-house_d / 2, (ff + 96) / 2, "EXISTING\nHOUSE", ha="center", va="center",
            fontsize=8, color="#888888")

    ax.add_patch(Rectangle((0, 0), cor_d, ff + c1 + 6, facecolor="#e8dcc8",
                           edgecolor="#555555", lw=1.2, zorder=2))
    ax.add_patch(Rectangle((cor_d - 4, ff + 6), 4, 80, facecolor="#dfeefb",
                           edgecolor="#1d4ed8", lw=1.2, zorder=3))
    ax.text(cor_d / 2, ff + c1 / 2,
            f"CORRIDOR\nbump-out\n({ft_in(door_w)} {door_short}\non south face)",
            ha="center", va="center", fontsize=7, color="#333333", zorder=4)

    # first-floor main-block west wall
    if flush:
        ax.add_patch(Rectangle((cor_d, 0), D - cor_d, ff + c1 + fl, facecolor="#e8dcc8",
                               edgecolor="#555555", lw=1.2, zorder=1))
    else:
        ax.add_patch(Rectangle((cor_d, 0), D - cor_d, ff + c1 + fl, facecolor="#d9ceb8",
                               edgecolor="#555555", lw=1.0, linestyle="--", zorder=1))
        ax.text((cor_d + D) / 2, ff + 20, "1st fl. west wall\n(2'-6\" under cantilever)",
                ha="center", va="bottom", fontsize=7, color="#666666")
    ax.add_patch(Rectangle((D / 2 + 20, ff + 30), 36, 48, facecolor="#dfeefb",
                           edgecolor="#4a6172", lw=1, zorder=2))

    # second-floor west face
    ax.add_patch(Rectangle((0, sf - fl), D, fl + c2 + 8, facecolor="#dfd2ba",
                           edgecolor="#555555", lw=1.2, zorder=3))

    if sec.get("furniture_window"):
        fw = sec.get("furniture_window_width", 72)
        fh = sec.get("furniture_window_height", 60)
        sill = sf + sec.get("furniture_window_sill", 24)
        ax.add_patch(Rectangle((D / 2 - fw / 2, sill), fw, fh, facecolor="#b8d4f0",
                               edgecolor="#1d4ed8", lw=1.5, zorder=4))
        ax.text(D / 2, sill + fh / 2,
                f"FURNITURE ACCESS\n{ft_in(fw)} × {ft_in(fh)}\noperable",
                ha="center", va="center", fontsize=8, color="#0b3d91", zorder=5)
    else:
        ax.add_patch(Rectangle((D / 2 + 10, sf + 36), 48, 48, facecolor="#dfeefb",
                               edgecolor="#4a6172", lw=1, zorder=4))

    mid = D / 2
    ax.plot([0 - 8, mid, D + 8], [eaves, ridge, eaves], color="#555555", lw=1.4, zorder=4)
    ax.plot([0 - 8, D + 8], [eaves, eaves], color="#555555", lw=1.0, zorder=4)

    for y, lbl in [(ff, f'1st FF  +{ft_in(ff)}'), (sf, f'2nd FF  +{ft_in(sf)}'),
                   (plate2, f'2nd plate  +{ft_in(plate2)}')]:
        ax.plot([-20, D + 20], [y, y], color="#888888", lw=0.7, linestyle=":")
        ax.text(-24, y, lbl, ha="right", va="center", fontsize=8, color="#555555")
    ax.text(mid, ridge + 8, f"ridge ≈ +{ft_in(ridge)}  (max 30')",
            ha="center", fontsize=8, color="#555555")
    if abs(cant_in) >= 2:
        ax.text(D + 10, sf - fl / 2, "2'-6\" cantilever\n(2nd fl. west face\ntoward viewer)",
                fontsize=7, color="#1d4ed8", va="center")
    else:
        ax.text(D + 10, sf - fl / 2, "walls flush\n(5' setback both floors)",
                fontsize=7, color="#2f7d2f", va="center")

    if shape == "L":
        lo_treads = g["lo_r"] - 1
        run = g["tread"]
        y_bot = g["lower"][1]
        for i in range(lo_treads):
            y_plan = y_bot + i * run
            z0 = i * riser_h
            ax.plot([y_plan, y_plan], [z0, z0 + riser_h], color="#333333", lw=1.2, zorder=5)
            ax.plot([y_plan, y_plan + run], [z0 + riser_h, z0 + riser_h],
                    color="#333333", lw=1.2, zorder=5)
        pad = g["pad"]
        ax.add_patch(Rectangle((pad[1], 0), pad[3], 4, facecolor="#bbbbbb",
                               edgecolor="#333333", lw=1.0, zorder=5))
        ax.add_patch(Rectangle((D, g["corner_height"] - 4), g["corner"][3], 8,
                               facecolor="#bbbbbb", edgecolor="#333333", lw=1.0, zorder=5))
        ax.plot([y_bot, D], [42, g["corner_height"] + 42], color="#777777", lw=1, zorder=5)
        ax.add_patch(Rectangle((D + 4, g["corner_height"]), g["corner"][3] - 8,
                               st["total_rise"] - g["corner_height"], fill=False,
                               edgecolor="#666666", lw=1.0, linestyle="--", zorder=4))
        ax.text(D + g["corner"][3] / 2, (g["corner_height"] + st["total_rise"]) / 2,
                f"upper flight\n{g['up_r']} risers\n(turns east)",
                ha="center", va="center", fontsize=7, color="#555555", zorder=5)
    elif shape == "straight":
        # End view of stair projecting west past SW corner
        overhang = g["west_overhang_in"]
        ax.add_patch(Rectangle((D, 0), 36, st["total_rise"], fill=False,
                               edgecolor="#666666", lw=1.2, linestyle="--", zorder=4))
        ax.text(D + 18, st["total_rise"] / 2,
                f"straight stair\nend view\n(+{ft_in(overhang)} into yard)",
                ha="center", va="center", fontsize=7.5, color="#555555")
    else:
        # Spiral is on the far (east) side of the south wall — dashed ghost
        ax.add_patch(Circle((D + 20, st["total_rise"] / 2), 28, fill=False,
                            edgecolor="#666666", lw=1.2, linestyle="--", zorder=4))
        ax.text(D + 20, st["total_rise"] / 2,
                f"spiral\n(SE corner,\nfar side)",
                ha="center", va="center", fontsize=7.5, color="#555555")

    ax.text(D / 2, -28, g["summary"], fontsize=8, ha="center")
    ax.text(-house_d / 2, -28, "← N (existing house)", fontsize=10, weight="bold")
    ax.text(D + 20, -28, "S (backyard) →", fontsize=10, weight="bold")
    ax.set_xlim(-house_d - 80, south_extent + 20)
    ax.set_ylim(-50, ridge + 40)
    fig.savefig(out_path("west-elevation.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)
    return {"cantilever_in": off + W2 - W1, "corridor_depth_in": cor_d}


def run_all():
    a1 = first_floor()
    a2 = second_floor()
    a3 = site_plan()
    a4 = south_elevation()
    a5 = west_elevation()

    gross = a1["footprint_sqft"] + a2["plate_sqft"]
    print(f"OUT: {OUTDIR}")
    print(f"Stair: {a2['summary']}")
    print(f"Yard projection: {a2['yard_projection_in']/12:.1f} ft")
    print(f"First-floor footprint: {a1['footprint_sqft']:.0f} sq ft")
    print(f"Second-floor plate:    {a2['plate_sqft']:.0f} sq ft")
    print(f"New gross floor area:  {gross:.0f} sq ft")
    print(f"FAR: 842 + {gross:.0f} = {842+gross:.0f} / 2500")
    print(f"Ridge ≈ {a4['ridge_ft']:.1f} ft")
    return {"a1": a1, "a2": a2, "a3": a3, "a4": a4, "a5": a5, "gross": gross}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default=os.path.join(HERE, "params.json"))
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()
    OUTDIR = args.out if os.path.isabs(args.out) else os.path.join(HERE, args.out)
    os.makedirs(OUTDIR, exist_ok=True)
    params = args.params if os.path.isabs(args.params) else os.path.join(HERE, args.params)
    load_params(params)
    run_all()
