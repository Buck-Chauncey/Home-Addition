# Two-story rear addition — design variants

5916 Panama Ave, Richmond, CA 94804 · APN 510-132-010-8 · Zoning RL2

## Variants

| Folder | Stair | Program | 2nd fl setback | Cost range |
| --- | --- | --- | --- | ---: |
| [`V0/`](V0/) | Straight | Full two-bath | 9′ inset | ≈ $298k–$482k |
| [`L stair/`](L%20stair/) | L | Full two-bath | 9′ inset | ≈ $299k–$484k |
| [`spiral_stairs/`](spiral_stairs/) | Spiral | Full + furniture window | 9′ inset | ≈ $292k–$476k |
| [`lean/`](lean/) | Spiral | Smaller; upstairs toilet only | 9′ inset | ≈ $210k–$355k |
| [`ADU/`](ADU/) | Spiral | **Studio ADU upstairs (kitchenette + full bath)** | **5′ flush** | **≈ $240k–$400k** |

## Cost comparison

See **[`cost-estimates.md`](cost-estimates.md)**.

## Generator

```bash
python3 generate_plans.py --params ADU/params.json --out ADU
python3 generate_plans.py --params lean/params.json --out lean
python3 generate_plans.py --params "L stair/params.json" --out "L stair"
python3 generate_plans.py --params V0/params.json --out V0
python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs
```

Existing-house reference: [`../existing-house/`](../existing-house/).  
Owner sketches: [`../sketches/`](../sketches/).
