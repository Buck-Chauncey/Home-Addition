# Cost estimates by design variant

5916 Panama Ave addition — preliminary Bay Area contractor-built estimates
(mid/standard finishes, 2026). Ranges include ~10% contingency.

## Summary comparison

| | **V0** | **L stair** | **spiral_stairs** | **lean** |
| --- | ---: | ---: | ---: | ---: |
| New gross floor area | ~595 sf | ~595 sf | ~595 sf | **~501 sf** |
| Footprint | ~327 sf | ~327 sf | ~327 sf | **~276 sf** |
| Upstairs wet room | Full bath | Full bath | Full bath | **Toilet + lav only** |
| Yard door | 6′ slider | 6′ slider | 6′ slider | **5′ double doors** |
| Stair | Straight (~9.8′ into yard) | L (~4′) | Spiral Ø5′ (~5′) | **Spiral Ø5′ (~5′)** |
| **Low total** | **≈ $298k** | **≈ $299k** | **≈ $292k** | **≈ $210k** |
| **High total** | **≈ $482k** | **≈ $484k** | **≈ $476k** | **≈ $355k** |

**Lean is the clear cost winner** — roughly **$80k–$130k less** than the full two-bath variants, mainly from a smaller shell, no upstairs shower bath, simpler Bath 1, and cheaper yard doors.

---

## Soft costs (all variants)

| Line item | Low | High |
| --- | ---: | ---: |
| Architecture / drafting / structural / Title 24 | $18,000 | $30,000 |
| Survey (property corners for 5′ setback) | $3,000 | $6,000 |
| Permits, plan check, city + school fees | $10,000 | $18,000 |
| **Soft-cost subtotal** | **$31,000** | **$54,000** |

---

## Full variants (V0 / L stair / spiral_stairs) — shared shell

~595 sq ft gross, two full baths, 14′×21′-6″ main block, 6′ slider.

| Line item | Low | High |
| --- | ---: | ---: |
| Site prep, excavation, demo at rear wall | $8,000 | $14,000 |
| Foundation (crawlspace, ~327 sq ft) | $28,000 | $45,000 |
| Framing labor + lumber (two-story shell) | $50,000 | $72,000 |
| Roofing + gutters + tie-in | $10,000 | $16,000 |
| Windows + exterior doors (base, excl. furniture window) | $12,000 | $20,000 |
| Siding, exterior trim, paint | $16,000 | $26,000 |
| Plumbing rough + fixtures (2 full baths, stacked) | $28,000 | $45,000 |
| Electrical | $14,000 | $22,000 |
| HVAC (2-zone mini-split) | $9,000 | $14,000 |
| Insulation + drywall | $14,000 | $22,000 |
| Interior finishes | $16,000 | $26,000 |
| Bath tile + finish (2 baths) | $14,000 | $26,000 |
| Dining-room wall opening + header | $6,000 | $12,000 |
| **Shared construction subtotal** | **$225,000** | **$360,000** |

### Stair adders (full variants)

| Variant | Stair line | Low total | High total |
| --- | --- | ---: | ---: |
| V0 straight | $9k–$14k | ≈ $298k | ≈ $482k |
| L stair | $11k–$18k | ≈ $299k | ≈ $484k |
| spiral_stairs (+ 6′×5′ furniture window $3–6k) | $6k–$12k spiral | ≈ $292k | ≈ $476k |

---

## Lean variant — smaller shell, toilet upstairs, spiral, double doors

~501 sq ft gross, 14′×18′ main block, shower bath downstairs, WC-only upstairs.

| Line item | Low | High |
| --- | ---: | ---: |
| Soft costs (same as above) | $31,000 | $54,000 |
| Site prep, excavation, demo | $7,000 | $12,000 |
| Foundation (crawlspace, ~276 sq ft) | $22,000 | $36,000 |
| Framing labor + lumber (smaller two-story) | $40,000 | $58,000 |
| Roofing + gutters + tie-in | $8,000 | $13,000 |
| Windows + 5′ double doors + furniture window | $10,000 | $18,000 |
| Siding, exterior trim, paint | $12,000 | $20,000 |
| Plumbing (1 shower bath + upstairs WC/lav, stacked) | $16,000 | $28,000 |
| Electrical | $11,000 | $18,000 |
| HVAC (2-zone mini-split) | $8,000 | $13,000 |
| Insulation + drywall | $11,000 | $18,000 |
| Interior finishes | $12,000 | $20,000 |
| Bath tile + finish (1 shower bath only) | $6,000 | $12,000 |
| Dining-room wall opening + header | $6,000 | $12,000 |
| Prefab spiral stair + landing + guards | $6,000 | $12,000 |
| **Lean construction subtotal** | **$164,000** | **$278,000** |
| Contingency 10% | $16,000 | $28,000 |
| Soft costs | $31,000 | $54,000 |
| **Lean total** | **≈ $210,000** | **≈ $355,000** |

### Where lean saves vs L stair (approx. midpoint)

| Cut | Savings |
| --- | ---: |
| Smaller footprint / less shell | ~$35k–$55k |
| No upstairs shower bath (WC only) | ~$25k–$40k |
| Shower + single vanity vs tub + double | ~$8k–$15k |
| 5′ double doors vs 6′ slider | ~$2k–$5k |
| Prefab spiral vs site-built L | ~$2k–$6k |
| **Total vs full L stair** | **~$80k–$130k** |

---

## Further cuts (any variant)

1. Owner-GC / self-perform paint, floors, some finish  
2. Slab-on-grade instead of crawlspace (if a floor step is OK)  
3. Stock windows; phase closet built-ins  
4. One-story only (drops the upstairs room entirely) — largest possible cut  

## Folder map

| Folder | Notes |
| --- | --- |
| [`V0/`](V0/) | Straight stair, full program |
| [`L stair/`](L%20stair/) | L-stair, full program |
| [`spiral_stairs/`](spiral_stairs/) | Spiral + 6′×5′ furniture window, full program |
| [`lean/`](lean/) | **Smaller shell, shower bath, upstairs toilet only, spiral, 5′ double doors** |

```bash
python3 generate_plans.py --params lean/params.json --out lean
python3 generate_plans.py --params "L stair/params.json" --out "L stair"
python3 generate_plans.py --params V0/params.json --out V0
python3 generate_plans.py --params spiral_stairs/params.json --out spiral_stairs
```
