#!/usr/bin/env python3
"""Parametric plan generator for the 5916 Panama Ave two-story rear addition.

Reads dimensions from params.json and produces dimensioned PNG drawings:
  first-floor-plan.png, second-floor-plan.png, site-plan.png, south-elevation.png

Plan orientation (matches the owner's floorplanner sketches):
  bottom = north (existing house / Panama Ave side), left = east (property line),
  top = south (backyard), right = west.

Coordinates: x in inches, 0 at the addition's ground-floor EAST exterior face,
increasing WEST. y in inches, 0 at the addition's NORTH exterior face (house
side), increasing SOUTH. Drawings are rendered with x to the right and y up,
which yields the sketch orientation described above.
"""

import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "params.json")))

EXT = P["walls"]["exterior_thickness"]
INT = P["walls"]["interior_thickness"]

WALL_COLOR = "#222222"
ROOM_COLOR = "#f5e3c3"
DIM_COLOR = "#555555"
FIXTURE_COLOR = "#9fb7c9"


def ft_in(inches):
    """Format inches as feet-inches, e.g. 138.5 -> 11'-6 1/2\"."""
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
        return f'{sign}{ft}\''
    return f'{sign}{ft}\'-{whole}{frac_txt}"'


def dim_h(ax, x0, x1, y, label=None, offset=0):
    """Horizontal dimension line."""
    y = y + offset
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM_COLOR, lw=0.9))
    for x in (x0, x1):
        ax.plot([x, x], [y - 3, y + 3], color=DIM_COLOR, lw=0.7)
    ax.text((x0 + x1) / 2, y + 3, label or ft_in(abs(x1 - x0)),
            ha="center", va="bottom", fontsize=8, color=DIM_COLOR)


def dim_v(ax, y0, y1, x, label=None, offset=0):
    """Vertical dimension line."""
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
    """White gap in a wall to indicate a door/opening."""
    if horizontal:
        ax.add_patch(Rectangle((x, y - 1), w, EXT + 2, facecolor="white",
                               edgecolor="none", zorder=4))
    else:
        ax.add_patch(Rectangle((x - 1, y), EXT + 2, w, facecolor="white",
                               edgecolor="none", zorder=4))


def window(ax, x, y, w, horizontal=True, wall=EXT):
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


# ----------------------------------------------------------------------------
# First floor
# ----------------------------------------------------------------------------

def first_floor():
    f = P["first_floor"]
    h = P["existing_house"]
    W, D = f["main_block_ext_width"], f["main_block_ext_depth"]
    nz = f["north_zone_interior_depth"]
    bathw = f["bath_interior_width"]
    closw = f["closet_interior_width"]
    cor_ns = f["corridor_interior_ns"]

    # existing-house geometry (local coordinates)
    hx_east = h["east_face_local_x"]            # house east face (east of addition face)
    x_bd = h["bedroom_dining_wall_local_x"]     # bedroom/dining wall centerline
    x_dk = h["dining_kitchen_wall_local_x"]     # dining/kitchen wall centerline
    din_e, din_w = x_bd + 4, x_dk - 4.5         # dining interior faces (approx)

    fig, ax = base_axes(
        "First floor — bedroom + full bath + walk-in closet; corridor bumps out of the DINING ROOM\n"
        "East face at 5'-0\" side setback (conforming); 9'-0\" ceilings")

    iw, idp = W - 2 * EXT, D - 2 * EXT          # interior width / depth
    entryw = iw - bathw - INT                   # open entry width (former hall)
    bedd = idp - nz - INT                       # bedroom zone depth
    bedw = iw - closw - INT                     # bedroom width

    y_zone = EXT + nz                           # wall between north zone and bedroom zone
    x_bath = EXT + bathw                        # bath / entry wall
    x_clos = EXT + closw                        # closet / bedroom wall

    # corridor bump-out west of the main block, in front of the dining room
    cor_w_int = din_w                           # corridor west interior face aligns w/ dining west wall
    cor_x1 = cor_w_int + EXT                    # bump-out west exterior face

    # ---- existing house context (ghost, north of y=0) -----------------------
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

    # ---- room fills ---------------------------------------------------------
    room(ax, EXT, EXT, bathw, nz, "BATH 1", f"{ft_in(bathw)} × {ft_in(nz)}")
    # open entry: former hall + corridor bump, one continuous space
    ax.add_patch(Rectangle((x_bath + INT, 0), entryw, EXT + nz, facecolor=ROOM_COLOR,
                           edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((din_e, 0), cor_w_int - din_e, cor_ns, facecolor=ROOM_COLOR,
                           edgecolor="none", zorder=1))
    ax.text((x_bath + W) / 2, nz - 6, "ENTRY", ha="center", fontsize=9, color="#333333",
            zorder=5)
    ax.text((W + cor_w_int) / 2, cor_ns / 2, "CORRIDOR\n(open to dining)", ha="center",
            va="center", fontsize=7.5, color="#333333", zorder=5)
    room(ax, EXT, y_zone + INT, closw, bedd, "WALK-IN\nCLOSET", ft_in(closw) + " deep", fs=8)
    room(ax, x_clos + INT, y_zone + INT, bedw, bedd, "BEDROOM",
         f"{ft_in(bedw)} × {ft_in(bedd)}")

    # ---- walls --------------------------------------------------------------
    wall_rect(ax, 0, 0, EXT, D)                          # east wall
    wall_rect(ax, 0, D - EXT, W, EXT)                    # south wall
    wall_rect(ax, 0, 0, x_bd, EXT)                       # north wall vs existing bedroom
    wall_rect(ax, W - EXT, 0, EXT, EXT)                  # NW corner post
    wall_rect(ax, W - EXT, cor_ns + EXT, EXT, D - cor_ns - EXT)  # west wall (south of corridor)
    wall_rect(ax, W - EXT, cor_ns, cor_x1 - W + EXT, EXT)        # corridor south wall
    wall_rect(ax, cor_w_int, 0, EXT, cor_ns + EXT)               # corridor west wall
    wall_rect(ax, EXT, y_zone, iw, INT)                  # zone wall
    wall_rect(ax, x_bath, EXT, INT, nz)                  # bath / entry wall
    wall_rect(ax, x_clos, y_zone + INT, INT, bedd)       # closet / bedroom wall

    # opening in the existing dining rear wall (drawn as orange span at y=0)
    ax.plot([din_e, cor_w_int], [0, 0], color="#e07000", lw=3, zorder=6)
    ax.text((din_e + cor_w_int) / 2, -16,
            f"existing dining rear wall opened {ft_in(cor_w_int - din_e)} (new header)",
            ha="center", fontsize=8, color="#8a4b00", zorder=6,
            bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.8))

    # circulation arrow: dining -> corridor -> entry -> bedroom
    ax.annotate("", xy=(x_bath + INT + entryw / 2, y_zone - 8),
                xytext=((din_e + cor_w_int) / 2, -40),
                arrowprops=dict(arrowstyle="-|>", color="#2f7d2f", lw=1.6,
                                connectionstyle="arc3,rad=0.25"), zorder=6)

    # doors
    door(ax, x_bath, EXT + nz - 34, 30, horizontal=False)     # bath door from entry
    door(ax, x_bath + INT + 12, y_zone, 32, horizontal=True)  # bedroom door from entry
    door(ax, x_clos, y_zone + INT + bedd - 40, 32, horizontal=False)  # closet door

    # windows: south egress window in bedroom, west window, corridor south window
    window(ax, x_clos + INT + bedw / 2 - 24, D - EXT, 48, horizontal=True)
    ax.text(x_clos + INT + bedw / 2, D + 4, "egress window (CRC R310)",
            ha="center", fontsize=7, color="#4a6172")
    window(ax, W - EXT, y_zone + INT + bedd / 2 - 18, 36, horizontal=False)
    window(ax, W + 12, cor_ns, cor_w_int - W - 24, horizontal=True)
    ax.text((W + cor_x1) / 2, cor_ns + EXT + 5, "window\n(daylight for dining)",
            ha="center", va="bottom", fontsize=6.5, color="#4a6172")

    # fixtures — bath 1: tub along east wall, WC north wall, double vanity on zone wall
    fixture(ax, EXT, EXT + 6, 30, 60, "TUB\n30×60")
    fixture(ax, EXT + 36, EXT, 30, 28, "WC")
    fixture(ax, EXT + bathw - 62, EXT + nz - 22, 60, 22, "DOUBLE VANITY 60\"")
    ax.text(EXT + bathw / 2, -10, "bath wet wall backs existing bedroom",
            ha="center", fontsize=7, color="#4a6172",
            bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.8))
    # king bed in bedroom
    fixture(ax, x_clos + INT + (bedw - 76) / 2, y_zone + INT + bedd - 80 - 8, 76, 80,
            "KING BED\n76×80")

    # dimensions
    dim_h(ax, 0, W, D + EXT, offset=26)
    dim_h(ax, 0, x_clos + INT / 2, D + EXT, offset=12, label=ft_in(x_clos + INT / 2))
    dim_v(ax, 0, D, -14, offset=-26)
    dim_v(ax, 0, EXT + nz + INT / 2, -14, offset=-12, label=ft_in(EXT + nz + INT / 2))
    dim_h(ax, W, cor_x1, cor_ns + EXT + 26, label=ft_in(cor_x1 - W))
    dim_v(ax, 0, cor_ns + EXT, cor_x1 + 10, label=ft_in(cor_ns + EXT))

    # setback annotation (above the building, clear of dimension lines)
    ax.annotate("", xy=(-60, D + 44), xytext=(0, D + 44),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.2))
    ax.text(-30, D + 50, "5'-0\" side setback\n(east property line)",
            ha="center", fontsize=8, color="#b00000")
    ax.plot([-60, -60], [-140, D + 90], color="#b00000", lw=1.4, linestyle="--")

    compass(ax, -95, D + 95)
    ax.set_xlim(-100, x_dk + 140)
    ax.set_ylim(-150, D + 100)
    fig.savefig(os.path.join(HERE, "first-floor-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    areas = {
        "footprint_sqft": (W * D + (cor_x1 - W) * (cor_ns + EXT)) / 144.0,
        "interior_sqft": (iw * idp + (cor_w_int - (W - EXT)) * cor_ns) / 144.0,
        "dining_opening_in": cor_w_int - din_e,
    }
    return areas


# ----------------------------------------------------------------------------
# Second floor
# ----------------------------------------------------------------------------

def second_floor():
    s = P["second_floor"]
    f = P["first_floor"]
    st = P["stair"]
    off = s["east_face_offset_from_ground_east_face"]
    W, D = s["ext_width"], s["ext_depth"]
    bathd = s["bath_interior_depth"]

    fig, ax = base_axes(
        "Second floor — office + shower bath, exterior-stair access\n"
        "East face at 9'-0\" side setback (conforming); 8'-0\" ceilings")

    iw, idp = W - 2 * EXT, D - 2 * EXT
    offd = idp - bathd - INT                     # office depth

    x0 = off                                     # second-floor east face (plan coords)
    wall_rect(ax, x0, 0, W, EXT)
    wall_rect(ax, x0, D - EXT, W, EXT)
    wall_rect(ax, x0, 0, EXT, D)
    wall_rect(ax, x0 + W - EXT, 0, EXT, D)
    y_zone = EXT + bathd
    wall_rect(ax, x0 + EXT, y_zone, iw, INT)

    room(ax, x0 + EXT, EXT, iw, bathd, "BATH 2",
         f"{ft_in(iw)} × {ft_in(bathd)}", dy=14)
    room(ax, x0 + EXT, y_zone + INT, iw, offd, "OFFICE",
         f"{ft_in(iw)} × {ft_in(offd)}")

    # fixtures: shower NE corner (stacks over Bath 1 plumbing), WC, vanity
    fixture(ax, x0 + EXT, EXT, 36, 36, "SHOWER\n36×36")
    fixture(ax, x0 + EXT + 42, EXT, 30, 28, "WC")
    fixture(ax, x0 + EXT + 78, EXT, 48, 22, "VANITY 48\"")
    fixture(ax, x0 + EXT + iw - 66, y_zone + INT + 16, 60, 30, "DESK")

    # doors
    door(ax, x0 + EXT + 16, y_zone, 30, horizontal=True)         # bath door
    entry_x = x0 + EXT + 8                                        # entry door on south wall, east end
    door(ax, entry_x, D - EXT, 36, horizontal=True)
    ax.text(entry_x + 18, D + 6, "ENTRY", ha="center", fontsize=8, color="#8a4b00")

    # windows: office south + west, bath north
    window(ax, x0 + EXT + iw / 2 - 30, D - EXT, 60, horizontal=True)
    window(ax, x0 + W - EXT, y_zone + INT + offd / 2 - 24, 48, horizontal=False)
    window(ax, x0 + EXT + iw - 40, 0, 30, horizontal=True)

    # ghost of first floor below
    ax.add_patch(Rectangle((0, 0), f["main_block_ext_width"], f["main_block_ext_depth"],
                           fill=False, edgecolor="#999999", lw=1.0, linestyle=":", zorder=0))
    ax.text(off / 2, f["main_block_ext_depth"] / 2, "first floor\nbelow\n(4'-0\" offset)",
            ha="center", va="center", fontsize=7, color="#888888", rotation=90)
    # existing house line (1-story roof below, north of the addition)
    ax.plot([-20, x0 + W + 30], [0, 0], color="#aaaaaa", lw=1.2, linestyle="--", zorder=0)
    ax.text(x0 + W + 34, -2, "existing 1-story house / roof below ↓",
            ha="left", va="top", fontsize=7, color="#888888")

    # exterior stair + landing along south wall
    land = st["top_landing"]
    treads = math.ceil(st["total_rise"] / st["riser_max"]) - 1
    run = treads * st["tread_run"]
    ly = D
    ax.add_patch(Rectangle((x0, ly), land, land, facecolor="#d9d9d9",
                           edgecolor="#666666", lw=1.0, zorder=2))
    ax.text(x0 + land / 2, ly + land / 2, "LANDING\n4'×4'", ha="center",
            va="center", fontsize=7)
    sx = x0 + land
    ax.add_patch(Rectangle((sx, ly), run, st["width"], facecolor="#e8e8e8",
                           edgecolor="#666666", lw=1.0, zorder=2))
    for i in range(1, treads):
        tx = sx + i * st["tread_run"]
        ax.plot([tx, tx], [ly, ly + st["width"]], color="#999999", lw=0.5)
    ax.add_patch(FancyArrow(sx + run - 20, ly + st["width"] / 2, -(run - 45), 0,
                            width=0.6, head_width=6, head_length=10, color="#444444"))
    ax.text(sx + run / 2, ly + st["width"] + 6,
            f"exterior stair: {treads + 1} risers @ {st['total_rise'] / (treads + 1):.2f}\", "
            f"{treads} treads @ {st['tread_run']}\" — rises to the EAST (left)",
            ha="center", fontsize=7.5)

    # dimensions
    dim_h(ax, x0, x0 + W, D + land + 14, offset=22)
    dim_v(ax, 0, D, x0 - 14, offset=-24, label=ft_in(D))
    dim_v(ax, 0, EXT + bathd + INT / 2, x0 - 14, offset=-10,
          label=ft_in(EXT + bathd + INT / 2))
    dim_h(ax, 0, x0, -16, label="4'-0\" offset")

    # setback annotation (above the building, clear of dimension lines)
    sy = D + land + 34
    ax.annotate("", xy=(-108 + off, sy), xytext=(x0, sy),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.2))
    ax.text(x0 - 54, sy + 6, "9'-0\" upper-story side setback",
            ha="center", fontsize=8, color="#b00000")
    ax.plot([off - 108, off - 108], [-50, sy + 30], color="#b00000", lw=1.4,
            linestyle="--")

    compass(ax, off - 108, -70)
    ax.set_xlim(off - 150, x0 + land + run + 40)
    ax.set_ylim(-120, sy + 50)
    fig.savefig(os.path.join(HERE, "second-floor-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {
        "plate_sqft": W * D / 144.0,
        "interior_sqft": iw * idp / 144.0,
        "stair_run_in": run,
        "treads": treads,
        "riser_in": st["total_rise"] / (treads + 1),
    }


# ----------------------------------------------------------------------------
# Site plan (feet)
# ----------------------------------------------------------------------------

def site_plan():
    s = P["site_ft"]
    f = P["first_floor"]
    h = P["existing_house"]
    sec = P["second_floor"]
    st = P["stair"]
    lw_, ld = s["lot_width"], s["lot_depth"]
    e_house = P["setbacks"]["existing_house_east_face_from_pl_ft"]
    e_gf = P["setbacks"]["east_pl_to_addition_ground_face_ft"]
    e_uf = P["setbacks"]["east_pl_to_addition_upper_face_ft"]

    fig, ax = plt.subplots(figsize=(9, 13))
    ax.set_title("Site plan (schematic) — 5916 Panama Ave, lot 50' × 100'\n"
                 "bottom = Panama Ave (north); left = east", fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    # lot
    ax.add_patch(Rectangle((0, 0), lw_, ld, fill=False, edgecolor="black", lw=1.5))
    ax.text(lw_ / 2, -4, "PANAMA AVE (north)", ha="center", fontsize=10, weight="bold")

    # setback lines
    for x, lbl, c in [(5, "5' side", "#b00000"), (9, "9' upper side", "#e07000"),
                      (lw_ - 5, "5' side", "#b00000")]:
        ax.plot([x, x], [0, ld], color=c, lw=1.0, linestyle="--")
        ax.text(x + 0.4, ld - 2, lbl, fontsize=7, color=c, rotation=90, va="top")
    for y, lbl in [(20, "20' front"), (ld - 20, "20' rear"), (ld - 10, "10' reduced rear (optional)")]:
        ax.plot([0, lw_], [y, y], color="#b00000", lw=1.0, linestyle="--")
        ax.text(1, y + 0.4, lbl, fontsize=7, color="#b00000")

    # existing house per the Compass marketing plan (40.25' x 30.5')
    hx, hy = e_house, s["house_front_setback"]
    hw, hd = h["width_ft"], h["depth_ft"]
    ax.add_patch(Rectangle((hx, hy), hw, hd, facecolor="#c9b8a3", edgecolor="#7a6a55", lw=1.2))
    ax.text(hx + hw / 2, hy + hd / 2,
            "EXISTING HOUSE\n40.25' × 30.5' (919 sq ft)\nfront setback assumed — verify",
            ha="center", va="center", fontsize=8.5)

    # front porch (front-center) and attached garage (front-west)
    p = s["porch"]
    ax.add_patch(Rectangle((p["x0"], hy - p["depth"]), p["width"], p["depth"],
                           facecolor="#d3c7b5", edgecolor="#7a6a55", lw=1.0))
    ax.text(p["x0"] + p["width"] / 2, hy - p["depth"] / 2, "PORCH", ha="center",
            va="center", fontsize=7)
    g = s["garage"]
    gx = hx + hw - g["width"]
    gy = hy - g["front_proud"]
    ax.add_patch(Rectangle((gx, gy), g["width"], g["length"], facecolor="#d3c7b5",
                           edgecolor="#7a6a55", lw=1.0))
    ax.text(gx + g["width"] / 2, gy + g["length"] / 2, "GARAGE\n(attached)",
            ha="center", va="center", fontsize=8)
    ax.text(gx + g["width"] / 2, 8, "DRIVEWAY", ha="center", fontsize=7, color="#777777")

    # mud-room ramp at rear west (approximate)
    ax.add_patch(Rectangle((hx + hw - 5, hy + hd), 4, 7, facecolor="#e0e0e0",
                           edgecolor="#888888", lw=0.8))
    ax.text(hx + hw - 3, hy + hd + 3.5, "ramp", ha="center", va="center", fontsize=6.5)

    # shed in the rear-east yard (approximate from marketing site plan)
    sh = s["shed"]
    shy = ld - sh["from_rear_pl"] - sh["depth"]
    ax.add_patch(Rectangle((sh["x0"], shy), sh["width"], sh["depth"],
                           facecolor="#d3c7b5", edgecolor="#7a6a55", lw=1.0))
    ax.text(sh["x0"] + sh["width"] / 2, shy + sh["depth"] / 2,
            "SHED 135 sq ft\n(verify position)", ha="center", va="center", fontsize=7.5)

    # addition ground floor
    ay = hy + hd
    aw = f["main_block_ext_width"] / 12.0
    ad = f["main_block_ext_depth"] / 12.0
    cor_x1 = h["dining_kitchen_wall_local_x"] - 4.5 + EXT   # bump-out west face (local in)
    cw = (cor_x1 - f["main_block_ext_width"]) / 12.0
    cd = (f["corridor_interior_ns"] + EXT) / 12.0
    ax.add_patch(Rectangle((e_gf, ay), aw, ad, facecolor="#9ec99e",
                           edgecolor="#3c6e3c", lw=1.4))
    ax.add_patch(Rectangle((e_gf + aw, ay), cw, cd, facecolor="#9ec99e",
                           edgecolor="#3c6e3c", lw=1.4))
    ax.text(e_gf + aw / 2, ay + ad / 2 - 2, "ADDITION\nground floor",
            ha="center", va="center", fontsize=8)

    # second floor outline
    sx = e_uf
    sw2 = sec["ext_width"] / 12.0
    ax.add_patch(Rectangle((sx, ay), sw2, ad, fill=False, edgecolor="#1d4ed8",
                           lw=1.4, linestyle="-."))
    ax.text(sx + sw2 / 2, ay + ad / 2 + 3.5, "2nd floor", ha="center",
            fontsize=8, color="#1d4ed8")

    # exterior stair along south wall of addition
    land = st["top_landing"] / 12.0
    treads = math.ceil(st["total_rise"] / st["riser_max"]) - 1
    run = treads * st["tread_run"] / 12.0
    stw = st["width"] / 12.0
    ax.add_patch(Rectangle((e_uf, ay + ad), land, land, facecolor="#bfbfbf",
                           edgecolor="#555555"))
    ax.add_patch(Rectangle((e_uf + land, ay + ad), run, stw, facecolor="#dddddd",
                           edgecolor="#555555"))
    ax.text(e_uf + land + run / 2, ay + ad + stw + 0.6,
            "exterior stair (bottom W → top E)", fontsize=7, ha="center")

    ax.annotate("", xy=(0, ay + ad / 2), xytext=(e_gf, ay + ad / 2),
                arrowprops=dict(arrowstyle="<->", color="#b00000", lw=1.0))
    ax.text(e_gf / 2, ay + ad / 2 + 0.6, "5'", fontsize=8, color="#b00000", ha="center")

    ax.text(1, 1.5, "E ◄  lot line | W ►  (left = east)", fontsize=8, color="#444444")
    ax.set_xlim(-4, lw_ + 4)
    ax.set_ylim(-8, ld + 4)
    fig.savefig(os.path.join(HERE, "site-plan.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {"addition_rear_extent_ft": ay + ad,
            "rear_yard_remaining_ft": ld - (ay + ad)}


# ----------------------------------------------------------------------------
# South elevation (viewed from backyard looking north; east on the right)
# ----------------------------------------------------------------------------

def south_elevation():
    f = P["first_floor"]
    sec = P["second_floor"]
    st = P["stair"]
    lv = P["levels"]

    ff = lv["first_finish_floor_above_grade"]
    c1 = f["ceiling_height_ft"] * 12
    fl = lv["floor_assembly_depth"]
    c2 = sec["ceiling_height_ft"] * 12
    sf = ff + c1 + fl                       # second finish floor
    plate2 = sf + c2
    W1 = f["main_block_ext_width"]
    W2 = sec["ext_width"]
    pitch = lv["roof_pitch_in_12"]
    ridge = plate2 + 10 + (W2 / 2) * pitch / 12.0

    treads = math.ceil(st["total_rise"] / st["riser_max"]) - 1
    risers = treads + 1
    riser_h = st["total_rise"] / risers

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("South elevation (from backyard, looking north) — east on RIGHT\n"
                 "exterior stair rises west → east to second-floor entry", fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    # In this view, x=0 at east face, increasing WEST, but drawn mirrored so east
    # is on the right: use xd = -x.
    def xd(x):
        return -x

    # ground line
    ax.plot([xd(W1 + 140), xd(-90)], [0, 0], color="#553311", lw=2)
    ax.text(xd(-88), -14, "grade", fontsize=8, color="#553311")

    # first floor mass
    ax.add_patch(Rectangle((xd(W1), 0), W1, ff + c1 + fl, facecolor="#e8dcc8",
                           edgecolor="#555555", lw=1.2))
    # second floor mass (east face inset 4')
    off = sec["east_face_offset_from_ground_east_face"]
    ax.add_patch(Rectangle((xd(off + W2), sf - fl), W2, fl + c2 + 8,
                           facecolor="#dfd2ba", edgecolor="#555555", lw=1.2))
    # simple gable roof over second floor
    rx0, rx1 = xd(off + W2) - 12, xd(off) + 12
    ax.plot([rx0, (rx0 + rx1) / 2, rx1], [plate2 + 8, ridge, plate2 + 8],
            color="#555555", lw=1.4)
    # shed roof over exposed first-floor strip (east 4')
    ax.plot([xd(off), xd(0) + 8], [sf + 6, sf - 10], color="#555555", lw=1.2)

    # floor lines + labels
    for y, lbl in [(ff, f'1st FF  +{ft_in(ff)}'), (sf, f'2nd FF  +{ft_in(sf)}'),
                   (plate2, f'2nd plate  +{ft_in(plate2)}')]:
        ax.plot([xd(W1) - 6, xd(0) + 6], [y, y], color="#888888", lw=0.7, linestyle=":")
        ax.text(xd(W1) - 10, y, lbl, ha="right", va="center", fontsize=8, color="#555555")
    ax.text(xd(W2 / 2 + off), ridge + 8, f"ridge ≈ +{ft_in(ridge)}  (max 30')",
            ha="center", fontsize=8, color="#555555")

    # entry door on second floor (east end)
    ax.add_patch(Rectangle((xd(off + 14 + 36), sf), 36, 80, facecolor="#b98b4e",
                           edgecolor="#6b4c26", lw=1))
    # windows
    ax.add_patch(Rectangle((xd(off + W2 / 2 + 55), sf + 36), 60, 48,
                           facecolor="#dfeefb", edgecolor="#4a6172", lw=1))
    ax.add_patch(Rectangle((xd(W1 / 2 + 24 - off / 2), ff + 30), 48, 48,
                           facecolor="#dfeefb", edgecolor="#4a6172", lw=1))
    ax.text(xd(W1 / 2 - off / 2), ff + 20, "bedroom egress", ha="center",
            fontsize=7, color="#4a6172")

    # stair profile: bottom at west (left), rising to east (right)
    run = st["tread_run"]
    x_top = off + st["top_landing"]         # plan-x where stair leaves the landing
    pts_x, pts_y = [], []
    for i in range(treads + 1):
        x_plan = x_top + (treads - i) * run
        pts_x.append(xd(x_plan))
        pts_y.append((i) * riser_h)
    # draw steps
    for i in range(treads):
        x0, y0 = pts_x[i], pts_y[i]
        ax.plot([x0, x0], [y0, y0 + riser_h], color="#333333", lw=1.2)
        ax.plot([x0, x0 + run], [y0 + riser_h, y0 + riser_h], color="#333333", lw=1.2)
    # top landing
    ax.plot([xd(x_top), xd(off)], [st["total_rise"], st["total_rise"]],
            color="#333333", lw=2.0)
    # guard
    ax.plot([pts_x[0], pts_x[-1]], [42, st["total_rise"] + 42], color="#777777", lw=1)
    ax.plot([xd(x_top), xd(off)], [st["total_rise"] + 42, st["total_rise"] + 42],
            color="#777777", lw=1)
    ax.text(pts_x[len(pts_x) // 2], st["total_rise"] / 2 - 30,
            f"{risers} risers @ {riser_h:.2f}\" | {treads} treads @ {run}\"\n"
            f"guard 42\", handrail 34–38\"", fontsize=8, ha="center")

    ax.text(xd(0) + 30, 10, "E →", fontsize=10, weight="bold")
    ax.text(pts_x[0] - 55, 10, "← W", fontsize=10, weight="bold")

    ax.set_xlim(pts_x[0] - 90, xd(0) + 80)
    ax.set_ylim(-30, ridge + 40)
    fig.savefig(os.path.join(HERE, "south-elevation.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    return {"second_ff_in": sf, "ridge_ft": ridge / 12.0}


if __name__ == "__main__":
    a1 = first_floor()
    a2 = second_floor()
    a3 = site_plan()
    a4 = south_elevation()

    gross = a1["footprint_sqft"] + a2["plate_sqft"]
    print(f"First-floor footprint: {a1['footprint_sqft']:.0f} sq ft "
          f"(interior {a1['interior_sqft']:.0f})")
    print(f"Second-floor plate:    {a2['plate_sqft']:.0f} sq ft "
          f"(interior {a2['interior_sqft']:.0f})")
    print(f"New gross floor area:  {gross:.0f} sq ft")
    print(f"Stair: {a2['treads'] + 1} risers @ {a2['riser_in']:.2f}\", "
          f"run {a2['stair_run_in'] / 12:.1f} ft")
    print(f"Addition rear extent:  {a3['addition_rear_extent_ft']:.1f} ft from front PL; "
          f"rear yard remaining {a3['rear_yard_remaining_ft']:.1f} ft (schematic)")
    print(f"Second finish floor:   {a4['second_ff_in'] / 12:.2f} ft; "
          f"ridge ≈ {a4['ridge_ft']:.1f} ft (limit 30 ft)")
    print(f"FAR check: 842 existing + {gross:.0f} new = {842 + gross:.0f} "
          f"of 2,500 sq ft allowed")
    print(f"Coverage check: 1,360 house + 277 garage + {a1['footprint_sqft']:.0f} addition "
          f"= {1360 + 277 + a1['footprint_sqft']:.0f} of 2,500 sq ft allowed")
