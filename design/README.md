# Two-story rear addition — formalized mockup (v2)

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
5. The addition's bathroom backs against the existing rear **bedroom** wall.
6. **9′-0″ first-floor ceilings**, 8′-0″ second floor.

## How the addition meets the existing house

- The main block (16′-6″ wide) sits behind the existing rear bedroom and laps
  ≈ 4′ of the dining room's rear wall — that lap plus the bump-out is the
  connection. Walking path: dining room → corridor → entry → bedroom/bath.
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

### First floor — footprint 330 sq ft (interior 290 sq ft)

| Room | Clear dimensions | Notes |
| --- | --- | --- |
| Bedroom | 11′-6½″ × 11′-6½″ | Fits king bed (76″×80″) with ≥30″ on both sides; egress window on south wall |
| Walk-in closet | 3′-6″ × 11′-6½″ | East wall (property-line side); its west wall carries the second-floor east wall |
| Bath 1 (full) | 9′-6″ × 6′-0″ | 30×60 tub, WC, 60″ double vanity; wet wall backs the existing bedroom |
| Entry | 5′-6½″ wide | Open to the corridor — no door, no hall |
| Corridor (dining bump-out) | ≈ 8′ of opening × 3′-2″ deep | Fully open to the dining room; south window |

Main block 16′-6″ × 19′-0″ exterior; bump-out beyond the main block ≈ 4′-5″ × 3′-8½″.

### Second floor — plate 238 sq ft (interior 205 sq ft)

| Room | Clear dimensions | Notes |
| --- | --- | --- |
| Office | 11′-5″ × 12′-0½″ | Windows south + west; entry door at SE corner |
| Bath 2 | 11′-5″ × 5′-6″ | 36×36 shower stacked over Bath 1 wet wall, WC, 48″ vanity |

Plate 12′-6″ × 19′-0″, east face 4′-0″ west of the ground-floor east face.

### Exterior stair

- 19 risers @ 7.37″ (max 7¾″ ✓), 18 treads @ 10.5″ (min 10″ ✓), 36″ wide
- Straight run 15′-9″ along the south wall + 4′×4′ top landing = 19′-9″ total;
  the bottom ~7′ extends past the addition's southwest corner into the yard
  (an L-return at the bottom is the fallback if that projection is unwanted)
- Total rise 11′-8″ (grade → second finish floor, assuming first floor framed
  ~18″ above grade to match the existing floor level — **field-verify**)
- Guards 42″, handrail 34″–38″, lighting at the top landing

## Zoning compliance (RL2, RMC 15.04.201.030)

| Check | Required | Proposed | Status |
| --- | --- | --- | --- |
| East side setback, ground | 5′ | 5′-0″ | ✓ conforming |
| East side setback, upper | 9′ | 9′-0″ | ✓ conforming |
| Rear setback | 20′ (10′ optional) | ≈ 30′ remaining (house rear at ~50.5′ w/ assumed 20′ front setback) | ✓ verify front setback on site |
| Height | 30′ max | ridge ≈ 22′-6″ | ✓ |
| Lot coverage | ≤ 2,500 sq ft | ≈ 1,967 + stair/landing | ✓ |
| Residential floor area | ≤ 2,500 sq ft | 842 existing + 567 new = 1,409 | ✓ |

With the real 30.5′ house depth the rear yard has generous margin: the
addition reaches ≈ 69.5′ from the front line and the stair ≈ 73′, vs the 20′
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

- Second-floor east wall bears on the closet's west wall line (stacked bearing);
  a flush beam picks up the load across the 6′ Bath 1 span.
- New header (~8′) in the existing dining rear wall for the corridor opening.
- Corridor bump-out is a one-story flat/shed-roof element; the two-story mass
  stacks north/south walls directly.
- The addition's north wall furs against the existing bedroom/dining rear wall;
  second-floor north wall rises above the existing 1-story roof (flashing/tie-in).
- Foundation: new crawlspace stem walls matching existing floor level
  (assumed +18″ — verify), tied to the existing foundation at the connection.

## Preliminary cost estimate (Bay Area, 2026, contractor-built, mid/standard finishes)

567 sq ft new gross floor area, two baths (stacked plumbing), exterior stair.

| Line item | Low | High |
| --- | ---: | ---: |
| Architecture/drafting, structural, Title 24 | $18,000 | $30,000 |
| Survey (property corners — needed for the 5′ setback) | $3,000 | $6,000 |
| Permits, plan check, city + school fees | $10,000 | $18,000 |
| Site prep, excavation, demo at rear wall | $8,000 | $14,000 |
| Foundation (crawlspace stem walls, ~330 sq ft) | $28,000 | $45,000 |
| Framing labor + lumber (two-story + stair structure) | $55,000 | $80,000 |
| Roofing + gutters + tie-in | $10,000 | $16,000 |
| Windows + exterior doors | $12,000 | $20,000 |
| Siding, exterior trim, paint | $16,000 | $26,000 |
| Exterior stair, landing, guardrails | $10,000 | $16,000 |
| Plumbing rough + fixtures (2 baths, stacked) | $28,000 | $45,000 |
| Electrical (panel work, rough, fixtures) | $14,000 | $22,000 |
| HVAC (2-zone mini-split) | $9,000 | $14,000 |
| Insulation + drywall | $14,000 | $22,000 |
| Interior finishes (floors, doors, trim, paint) | $16,000 | $26,000 |
| Bath tile + finish (2 baths) | $14,000 | $26,000 |
| Dining-room wall opening + structural header | $6,000 | $12,000 |
| **Construction subtotal** | **$271,000** | **$438,000** |
| Contingency (10%) | $27,000 | $44,000 |
| **Total project** | **≈ $298,000** | **≈ $482,000** |

That is roughly **$525–$850 per new gross sq ft** — normal for a small
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
