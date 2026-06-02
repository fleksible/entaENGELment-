# Monorepo Topology

Dependency and domain topology of the EntaENGELment workspace. Arrows point
from consumer to dependency (flow is leaf-ward; the graph is acyclic — see
`SYNTHBIOSIS.md` §4, Axiom S6).

```mermaid
graph TD
  subgraph GOLD["GOLD core (read-only)"]
    VOIDMAP["VOIDMAP.yml"]
    POLICIES["policies / index / spec / seeds"]
  end

  subgraph JS["JS/TS membrane (pnpm + Turborepo)"]
    UIAPP["entaengelment-ui<br/>(ui-app · Next.js app)"]
    TYPES["@enta/types<br/>(domain types · type-only)"]
    TSCONFIG["@enta/tsconfig<br/>(compiler covenant)"]
  end

  subgraph PY["Python core (sovereign)"]
    SRC["src / tools / tests"]
    BIO["bio_spiral_viewer"]
  end

  UIAPP -->|workspace:*| TYPES
  UIAPP -->|extends| TSCONFIG
  TYPES -->|extends| TSCONFIG

  TYPES -. mirrors schema .-> VOIDMAP

  POLICIES -. governs all .-> JS
  POLICIES -. governs all .-> PY

  classDef gold fill:#fdf2c4,stroke:#b8860b,color:#5b4a00;
  classDef js fill:#e6f0ff,stroke:#3b6fb5,color:#143a66;
  classDef py fill:#e8f7ec,stroke:#3a9d5d,color:#11502b;
  class VOIDMAP,POLICIES gold;
  class UIAPP,TYPES,TSCONFIG js;
  class SRC,BIO py;
```

## Reading the graph

- **`ui-app`** is a leaf consumer: it depends on `@enta/types` (`workspace:*`)
  and extends `@enta/tsconfig`. It does not depend on the Python core.
- **`@enta/types`** is the single source of truth for domain types and *mirrors*
  the GOLD `VOIDMAP.yml` schema as a read-only consumer (dotted arrow — no write
  relationship).
- **`@enta/tsconfig`** is the shared compiler covenant every TS package extends.
- The **Python core** is a separate sovereign domain with its own toolchain; the
  JS membrane neither imports from nor gates it.
- **GOLD policies** govern every domain but are edited by none of them.

Turbo task graph: `typecheck`/`build` flow `@enta/tsconfig → @enta/types →
ui-app` via `dependsOn: ["^typecheck"|"^build"]`.
