# Two-story rear addition — formalized mockup (v3)

5916 Panama Ave, Richmond, CA 94804 · APN 510-132-010-8 · Zoning RL2

Code-conforming development of the owner's floorplanner sketches
(`../sketches/`), now positioned against the **actual house plan** from the
2021 Compass marketing drawings (`../existing-house/`): house 40.25′ × 30.5′
(919 sq ft living), rear (south) wall from east: **bedroom ≈ 13′ → dining
room ≈ 8.6′ → kitchen → mud room** (ramp at the far west).

Owner decisions incorporated:

1. Ground floor at the **5′-0″ east side setback** (7.5″ west of the existing
   east wall plane) — no variance needed.
2. Second floor **narrowed** to the **9′-0″ upper-story side setback**
   (4′-0″ offset from the addition's ground-floor east face).
3. Exterior stair along the **south (backyard) wall**, bottom at the west,
   rising to the east; entry door at the second floor's southeast corner.
4. **The corridor is a bump-out of the dining room** — the dining room's rear
   wall is opened ≈ 7′-10″ (new header) and the corridor flows around into the
   addition's entry. **No separate hall**: the entry is one continuous open
   space from the dining room to the bedroom and bath doors.
5. **Wide corridor with a 6′-0″ double sliding door to the backyard** (v3):
   the main block narrowed from 16′-6″ to **14′-0″** so the corridor's south
   face is ≈ 7′ wide — room for the slider. The **closet flipped to run
   east–west against the bathroom wall**, and the main block deepened from
   19′-0″ to **21′-6″** so the bedroom stays king-size comfortable.
6. The addition's bathroom backs against the existing rear **bedroom** wall.
7. **9′-0″ first-floor ceilings**, 8′-0″ second floor.

## How the addition meets the existing house

- The main block (14′-0″ wide) sits behind the existing rear bedroom and just
  laps the east edge of the dining room. The corridor bump-out spans the rest
  of the dining room's rear wall. Walking path: dining room → corridor
  (double slider to the yard on its south face) → entry passage → bedroom/bath.
- The bump-out's west wall aligns with the dining/kitchen wall, so the
  **kitchen sink wall and its window are untouched**.
- The existing rear bedroom keeps its side window but loses its two rear
  (south) windows — **verify the remaining window satisfies egress/light/vent**,
  or plan a replacement window as part of the work.
- A window in the corridor's south wall returns daylight to the dining room.
- The shed (135 sq ft) and mud-room ramp are in the rear yard but clear of the
  addition and stair (verify shed position — it sits near the rear fence).

## Drawings (regenerate with `python3 generate_plans.py`, dimensions in `params.json`)

| File | Contents |
| --- | --- |
| `first-floor-plan.png` | Bedroom, full bath, walk-in closet, entry + dining bump-out, existing rooms shown for context |
| `second-floor-plan.png` | Office, shower bath, entry landing + stair |
| `site-plan.png` | Lot plan with real house footprint, garage, porch, shed, setback lines |
| `south-elevation.png` | Massing, floor levels, stair profile |

Plan orientation matches the owner's sketches and the marketing plans:
bottom = north (Panama side), left = east (property line), top = south (backyard).

## Room schedule

### First floor — footprint 327 sq ft (interior 286 sq ft)

| Room | Clear dimensions | Notes |
| --- | --- | --- |
| Bedroom | 12′-11″ × 11′-2″ | King bed (76″×80″) headboard on the east wall with 6′+ of clear floor beside it; egress window on south wall, window on west wall |
| Closet | 9′-0″ × 2′-6″ | Runs east–west against the bathroom wall; sliding doors facing the bedroom |
| Bath 1 (full) | 9′-0″ × 6′-0″ | 30×60 tub, WC, 60″ double vanity; wet wall backs the existing bedroom |
| Entry passage | 3′-6½″ wide | From the corridor past bath and closet to the bedroom door — no hall |
| Corridor (dining bump-out) | ≈ 7′-10″ opening × 3′-2″ deep | Fully open to the dining room; **6′-0″ double sliding door to the backyard** in its south face |

Main block 14′-0″ × 21′-6″ exterior; bump-out beyond the main block 6′-11″ × 3′-8½″.

### Second floor — plate 269 sq ft (interior 233 sq ft)

| Room | Clear dimensions | Notes |
| --- | --- | --- |
| Office | 11′-5″ × 14′-6½″ | Windows south + west; entry door at SE corner |
| Bath 2 | 11′-5″ × 5′-6″ | 36×36 shower stacked over Bath 1 wet wall, WC, 48″ vanity |

Plate 12′-6″ × 21′-6″, east face 4′-0″ west of the ground-floor east face; the
west wall cantilevers 2′-6″ beyond the narrowed first-floor west wall.

### Exterior stair

- 19 risers @ 7.37″ (max 7¾″ ✓), 18 treads @ 10.5″ (min 10″ ✓), 36″ wide
- Straight run 15′-9″ along the south wall + 4′×4′ top landing = 19′-9″ total;
  the bottom ~9′ extends past the addition's southwest corner into the yard
  (an L-return at the bottom is the fallback if that projection is unwanted)
- Total rise 11′-8″ (grade → second finish floor, assuming first floor framed
  ~18″ above grade to match the existing floor level — **field-verify**)
- Guards 42″, handrail 34″–38″, lighting at the top landing

## Zoning compliance (RL2, RMC 15.04.201.030)

| Check | Required | Proposed | Status |
| --- | --- | --- | --- |
| East side setback, ground | 5′ | 5′-0″ | ✓ conforming |
| East side setback, upper | 9′ | 9′-0″ | ✓ conforming |
| Rear setback | 20′ (10′ optional) | ≈ 28′ remaining (house rear at ~50.5′ w/ assumed 20′ front setback) | ✓ verify front setback on site |
| Height | 30′ max | ridge ≈ 22′-6″ | ✓ |
| Lot coverage | ≤ 2,500 sq ft | ≈ 1,964 + stair/landing | ✓ |
| Residential floor area | ≤ 2,500 sq ft | 842 existing + 595 new = 1,437 | ✓ |

With the real 30.5′ house depth the rear yard has generous margin: the
addition reaches ≈ 72′ from the front line and the stair ≈ 75.5′, vs the 20′
rear setback line at 80′. Open items: (a) confirm the front setback (drives
everything above); (b) design review / compatibility standards
(RMC 15.04.201.040).

## Building-code checklist (2022/2025 CRC as adopted by Richmond)

| Item | Provision | How this design complies |
| --- | --- | --- |
| New bedroom egress | R310 | South-wall egress window (≥5.7 sq ft net clear, sill ≤44″) |
| Existing bedroom egress | R310 | Rear windows are covered by the addition — verify the remaining side window qualifies, or upgrade it |
| Light + ventilation | R303 | Glazing ≥8% of floor area, openable ≥4% (or mech vent) per room; corridor south window daylights the dining room |
| Ceiling heights | R305 | 9′ / 8′ ≥ 7′ min |
| Bath clearances | R307 | WC 15″ min center-to-side, 21″ front (Bath 1 has 22″ to vanity); shower 36×36 ≥ 30″ min |
| Stairs | R311.7 | Risers 7.37″ ≤ 7¾″, treads 10.5″ ≥ 10″, width 36″, landings ≥36″, handrail + 42″ guards |
| Exterior wall fire rating | R302.1 | East wall at exactly 5′ → no rating required, unlimited openings |
| Smoke/CO alarms | R314/R315 | Bedrooms, entry, each story (incl. existing house per alteration trigger) |
| Energy | Title 24 | New windows low-e, QII insulation, mini-split HVAC, possible PV trigger — energy consultant to model |
| Second floor access | R311 | Habitable office served by exterior stair + door; not a sleeping room, so no EERO required (add one if it may ever be a bedroom) |

## Structural notes (for the engineer)

- With the closet flipped east–west there is no first-floor bearing wall under
  the second-floor east wall (4′-0″ line): flush beams (LVL) carry it — the
  longest segment spans the ~11′ bedroom depth.
- Second-floor west wall cantilevers 2′-6″ past the first-floor west wall
  (floor joists span east–west, ~10′ back-span — within the 1:3 cantilever rule).
- New header (~8′) in the existing dining rear wall for the corridor opening;
  6′-0″ slider header in the corridor's south wall.
- Corridor bump-out is a one-story flat/shed-roof element.
- The addition's north wall furs against the existing bedroom/dining rear wall;
  second-floor north wall rises above the existing 1-story roof (flashing/tie-in).
- Foundation: new crawlspace stem walls matching existing floor level
  (assumed +18″ — verify), tied to the existing foundation at the connection.

## Preliminary cost estimate (Bay Area, 2026, contractor-built, mid/standard finishes)

595 sq ft new gross floor area, two baths (stacked plumbing), exterior stair,
6′ double slider. (The cantilever and flush beams add modest framing cost —
covered within the framing range below.)

| Line item | Low | High |
| --- | ---: | ---: |
| Architecture/drafting, structural, Title 24 | $18,000 | $30,000 |
| Survey (property corners — needed for the 5′ setback) | $3,000 | $6,000 |
| Permits, plan check, city + school fees | $10,000 | $18,000 |
| Site prep, excavation, demo at rear wall | $8,000 | $14,000 |
| Foundation (crawlspace stem walls, ~327 sq ft) | $28,000 | $45,000 |
| Framing labor + lumber (two-story + stair structure) | $55,000 | $80,000 |
| Roofing + gutters + tie-in | $10,000 | $16,000 |
| Windows + exterior doors (incl. 6′ double slider) | $13,000 | $22,000 |
| Siding, exterior trim, paint | $16,000 | $26,000 |
| Exterior stair, landing, guardrails | $10,000 | $16,000 |
| Plumbing rough + fixtures (2 baths, stacked) | $28,000 | $45,000 |
| Electrical (panel work, rough, fixtures) | $14,000 | $22,000 |
| HVAC (2-zone mini-split) | $9,000 | $14,000 |
| Insulation + drywall | $14,000 | $22,000 |
| Interior finishes (floors, doors, trim, paint) | $16,000 | $26,000 |
| Bath tile + finish (2 baths) | $14,000 | $26,000 |
| Dining-room wall opening + structural header | $6,000 | $12,000 |
| **Construction subtotal** | **$272,000** | **$440,000** |
| Contingency (10%) | $27,000 | $44,000 |
| **Total project** | **≈ $299,000** | **≈ $484,000** |

That is roughly **$500–$815 per new gross sq ft** — normal for a small
two-story Bay Area addition with two bathrooms (small projects carry a high
fixed-cost share; the two baths and the stair are the big drivers).

Per the owner: formalize first, then value-engineer. Obvious levers for the
next pass, in rough order of impact: owner-builder/owner-GC on select trades,
simplifying Bath 1 (single vanity, shower instead of tub), slab-on-grade if a
floor-level step is acceptable, stock windows, and phasing interior finishes.

## Assumptions to field-verify

1. Front setback of the existing house (marketing site plan is not to scale) —
   drives the rear-yard math, though margin is large.
2. Exact positions of the bedroom/dining and dining/kitchen walls (taken from
   the marketing floor plan, ±6″).
3. Existing finish-floor height above grade (drives stair rise + foundation).
4. Exact east property line location (survey) — design assumes the owner's
   52.5″ measurement to the existing wall is accurate.
5. Existing rear bedroom's side window size (egress after rear windows are covered).
6. Shed position vs. the stair bottom; location of sewer lateral, water, gas,
   and electrical panel capacity.
