# Surface Map / The Aperture Atlas

The Crimson Hexagonal Archive Knowledge Graph. Lives at [surfacemap.org](https://surfacemap.org).

## What this is

An interactive knowledge graph mapping every surface, entity, identity, document, and platform in the Crimson Hexagonal Archive. Built from the v3.0 Digital Topology Work Plan.

**The graph maps itself.** `surfacemap.org` appears as a node within its own topology.

## Architecture

- **6 node types:** INFRASTRUCTURE, SURFACE, ENTITY, IDENTITY, DOCUMENT, PLATFORM (the architecture IS six)
- **Edge types use Wikidata property IDs** (P31, P50, P127, P356, P496, P527, P856, P921, P1889, P2860, etc.) — every edge is either already on Wikidata (`live`) or is a pending edit (`pending`)
- **`spxi:` extensions** for archive-internal relations that can't be represented on Wikidata
- The graph is both visualization AND Wikidata edit queue

## Files

- `index.html` — the visualization (React 18 + D3 v7 from CDN, no build step)
- `topology-source.json` — all nodes, edges, measurements
- `robots.txt`, `sitemap.xml` — standard SPXI compliance

## Modes

1. **Default** — color by node type
2. **Basin Overlay** — color entities by basin state (ghost/contested/captured/immanent)
3. **Ghost Mode** — make absence visible (banned, lapsed, revoked nodes prominent)
4. **Aperture View** — color by aperture type (input/output/relay)
5. **Wikidata Sync** — color edges by sync status (green=live, yellow=pending, gray=blocked)

## References

- [EA-RBT-01: The Writable Retrieval Basin](https://doi.org/10.5281/zenodo.19763346) — basin dynamics
- [EA-HK-01: The Holographic Kernel](https://doi.org/10.5281/zenodo.19763365) — reconstructive compression
- [SPXI Protocol](https://doi.org/10.5281/zenodo.19614870) — entity inscription standard

## Author

Lee Sharks · [ORCID 0009-0000-1599-0703](https://orcid.org/0009-0000-1599-0703) · Semantic Economy Institute · Crimson Hexagonal Archive

CC BY 4.0

∮ = 1
