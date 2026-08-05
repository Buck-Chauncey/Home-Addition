# Cost estimates by stair variant

5916 Panama Ave addition — preliminary Bay Area contractor-built estimates
(mid/standard finishes, 2026). All three variants share the same ~595 sq ft
gross floor area, two baths, foundation, and corridor/slider. **Only the
exterior stair (and the spiral’s furniture window) differ.**

Ranges include ~10% contingency. Soft costs (architect, survey, permits) are
the same across variants.

## Summary comparison

| | **V0** straight stair | **L stair** | **spiral_stairs** |
| --- | ---: | ---: | ---: |
| Yard intrusion | ~9.8′ past SW corner | ~4′ (landings only) | ~5′ (spiral Ø) |
| Stair comfort / furniture | Best for daily use; awkward for desks | Good daily use; furniture still hard | People only; desks via 6′×5′ west window |
| Stair construction | Simplest | Corner landing +$1–3k | Prefab spiral often cheaper than site-built L |
| **Low total** | **≈ $298k** | **≈ $299k** | **≈ $292k** |
| **High total** | **≈ $482k** | **≈ $484k** | **≈ $476k** |
| Δ vs L stair (midpoint) | ≈ −$1.5k | baseline | ≈ −$7.5k |

The spiral is usually the cheapest stair option if a stock/prefab unit is used;
the straight run is simplest to build but costs yard space; the L-stair is the
best everyday compromise for yard + comfort.

## Shared soft costs (all variants)

| Line item | Low | High |
| --- | ---: | ---: |
| Architecture / drafting / structural / Title 24 | $18,000 | $30,000 |
| Survey (property corners for 5′ setback) | $3,000 | $6,000 |
| Permits, plan check, city + school fees | $10,000 | $18,000 |
| **Soft-cost subtotal** | **$31,000** | **$54,000** |

## Shared construction (all variants)

| Line item | Low | High |
| --- | ---: | ---: |
| Site prep, excavation, demo at rear wall | $8,000 | $14,000 |
| Foundation (crawlspace, ~327 sq ft) | $28,000 | $45,000 |
| Framing labor + lumber (two-story shell) | $50,000 | $72,000 |
| Roofing + gutters + tie-in | $10,000 | $16,000 |
| Windows + exterior doors (base, excl. furniture window) | $12,000 | $20,000 |
| Siding, exterior trim, paint | $16,000 | $26,000 |
| Plumbing rough + fixtures (2 baths, stacked) | $28,000 | $45,000 |
| Electrical | $14,000 | $22,000 |
| HVAC (2-zone mini-split) | $9,000 | $14,000 |
| Insulation + drywall | $14,000 | $22,000 |
| Interior finishes | $16,000 | $26,000 |
| Bath tile + finish (2 baths) | $14,000 | $26,000 |
| Dining-room wall opening + header | $6,000 | $12,000 |
| **Shared construction subtotal** | **$225,000** | **$360,000** |

## Variant-specific lines

### V0 — straight stair

| Line item | Low | High |
| --- | ---: | ---: |
| Straight exterior stair, landing, guards | $9,000 | $14,000 |
| Construction + stair | $234,000 | $374,000 |
| Contingency 10% | $23,000 | $37,000 |
| Soft costs | $31,000 | $54,000 |
| **V0 total** | **≈ $298,000** | **≈ $482,000** |

### L stair — L around SW corner (baseline design)

| Line item | Low | High |
| --- | ---: | ---: |
| L-stair, corner landing, guards (+$1–3k vs straight) | $11,000 | $18,000 |
| Construction + stair | $236,000 | $378,000 |
| Contingency 10% | $24,000 | $38,000 |
| Soft costs | $31,000 | $54,000 |
| **L stair total** | **≈ $299,000** | **≈ $484,000** |

### spiral_stairs — spiral + furniture window

| Line item | Low | High |
| --- | ---: | ---: |
| Prefab/code spiral, top landing, guards | $6,000 | $12,000 |
| 6′×5′ operable furniture window/door (west) | $3,000 | $6,000 |
| Construction + stair + window | $234,000 | $378,000 |
| Contingency 10% | $23,000 | $38,000 |
| Soft costs | $31,000 | $54,000 |
| **spiral_stairs total** | **≈ $292,000** | **≈ $476,000** |

> Prefab spiral pricing varies widely ($4k–$15k installed). A custom ornamental
> spiral can exceed the L-stair cost; the low end assumes a stock aluminum/steel
> unit meeting CRC R311.7.10.1.

## What actually moves the needle (all variants)

In rough order of impact if you want to go cheaper later:

1. Owner-GC / self-perform select trades
2. Bath 1: shower instead of tub; single vanity
3. Slab-on-grade instead of crawlspace (if a floor-level step is OK)
4. Stock windows; phase interior finishes
5. Stair choice (spiral saves a little; straight saves almost nothing vs L)

## Folder map

| Folder | Stair | Plans |
| --- | --- | --- |
| [`V0/`](V0/) | Straight run (~9.8′ into yard) | first/second floor, site, S+W elev |
| [`L stair/`](L%20stair/) | L around SW corner (~4′ projection) | same set |
| [`spiral_stairs/`](spiral_stairs/) | Ø5′ spiral + 6′×5′ west furniture window | same set |

Regenerate any variant:
```bash
python3 generate_plans.py --params "L stair/params.json" --out "L stair"
python3 generate_plans.py --params V0/params.json --out V0
python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs
```
