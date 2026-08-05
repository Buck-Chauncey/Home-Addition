# Spiral stairs — code-compliant exterior spiral + furniture window

Same floor plans as V0 / L stair, but second-floor access is a **CRC-compliant
exterior spiral** at the SE entry, with a **large west-wall window** so desks
and other bulky items never go up the stairs.

## Spiral stair (CRC R311.7.10.1)

| Spec | Value | Code limit |
| --- | --- | --- |
| Diameter | 5′-0″ (60″) | — |
| Risers | 15 @ 9.33″ | ≤ 9½″ |
| Walkline tread | ≥ 6¾″ (identical treads) | ≥ 6¾″ |
| Clear width at/below handrail | ≥ 26″ | ≥ 26″ |
| Headroom | ≥ 6′-6″ | ≥ 6′-6″ |
| Top landing | 4′×4′ at entry door | ≥ spiral diameter for landing surface |
| Yard projection | ≈ 5′ (the spiral itself) | — |

People-only access. Confirm with Richmond Building that a spiral may serve as
the sole means of egress for this second-floor office (~233 sq ft interior).

## Furniture access window (west wall of office)

- **6′-0″ wide × 5′-0″ high**, operable (sliding or French casement / patio door)
- Sill ~24″ above second finish floor
- Sized so a desk, mattress, or sectional can be lifted through from the yard
  (under the 2′-6″ cantilever — plan a temporary lift path)

## Rooms (same as other variants)

| Room | Clear dimensions |
| --- | --- |
| Bedroom | 12′-11″ × 11′-2″ |
| Closet | 9′-0″ × 2′-6″ |
| Bath 1 | 9′-0″ × 6′-0″ |
| Corridor | ~7′-10″ opening × 3′-2″ deep + 6′ double slider |
| Office | 11′-5″ × 14′-6½″ |
| Bath 2 | 11′-5″ × 5′-6″ |

Regenerate:
`python3 ../generate_plans.py --params spiral_stairs/params.json --out spiral_stairs`
