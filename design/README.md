# Two-story rear addition — design variants

5916 Panama Ave, Richmond, CA 94804 · APN 510-132-010-8 · Zoning RL2

## Variants

| Folder | Stair | Program | Yard door | Cost range |
| --- | --- | --- | --- | ---: |
| [`V0/`](V0/) | Straight (~9.8′ into yard) | Full: king BR + full bath + office + shower bath | 6′ slider | ≈ $298k–$482k |
| [`L stair/`](L%20stair/) | L around SW (~4′) | Same full program | 6′ slider | ≈ $299k–$484k |
| [`spiral_stairs/`](spiral_stairs/) | Ø5′ spiral (~5′) | Same full program + 6′×5′ furniture window | 6′ slider | ≈ $292k–$476k |
| [`lean/`](lean/) | Ø5′ spiral (~5′) | **Smaller 14′×18′; shower bath; upstairs toilet only** | **5′ double doors** | **≈ $210k–$355k** |

## Cost comparison

See **[`cost-estimates.md`](cost-estimates.md)** for line items.

## Generator

```bash
python3 generate_plans.py --params lean/params.json --out lean
python3 generate_plans.py --params "L stair/params.json" --out "L stair"
python3 generate_plans.py --params V0/params.json --out V0
python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs
```

Existing-house reference: [`../existing-house/`](../existing-house/).  
Owner sketches: [`../sketches/`](../sketches/).
