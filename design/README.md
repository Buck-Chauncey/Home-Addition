# Two-story rear addition — design variants

5916 Panama Ave, Richmond, CA 94804 · APN 510-132-010-8 · Zoning RL2

Three stair options for the same floor-plan concept (king bedroom + full bath
on the first floor; office + shower bath on the second; dining-room corridor
bump-out with 6′ double slider).

## Variants

| Folder | Stair | Yard intrusion | Notes |
| --- | --- | --- | --- |
| [`V0/`](V0/) | Straight exterior run | ~9.8′ past SW corner | Simplest stair; eats backyard |
| [`L stair/`](L%20stair/) | L around SW corner | ~4′ (landings) | Best daily-use / yard compromise |
| [`spiral_stairs/`](spiral_stairs/) | Ø5′ CRC spiral at SE entry | ~5′ (spiral) | People via spiral; **6′×5′ west furniture window** for desks etc. |

Each folder has its own `params.json`, dimensioned PNGs, and README.

## Cost comparison

See **[`cost-estimates.md`](cost-estimates.md)** for side-by-side line items.

| Variant | Low | High |
| --- | ---: | ---: |
| V0 (straight) | ≈ $298k | ≈ $482k |
| L stair | ≈ $299k | ≈ $484k |
| spiral_stairs | ≈ $292k | ≈ $476k |

## Shared program (all variants)

- First floor: bedroom 12′-11″ × 11′-2″ (king), E–W closet 9′ × 2′-6″, Bath 1
  9′ × 6′, corridor bump-out of dining with 6′ double slider
- Second floor: office 11′-5″ × 14′-6½″, Bath 2 11′-5″ × 5′-6″
- East face at 5′ GF / 9′ upper setbacks (conforming); 9′ / 8′ ceilings
- ~595 sq ft new gross; FAR 1,437 of 2,500; ridge ≈ 22′-6″ of 30′

## Generator

```bash
python3 generate_plans.py --params "L stair/params.json" --out "L stair"
python3 generate_plans.py --params V0/params.json --out V0
python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs
```

Existing-house reference drawings: [`../existing-house/`](../existing-house/).
Owner sketches: [`../sketches/`](../sketches/).
