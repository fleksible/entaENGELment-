# EntaENGELment UI

Web-App für die Visualisierung der EntaENGELment-Konzepte (Guard System, VOIDMAP, Metatron-Regel).

## Features

- **Metatron HUD** - Fokus & Aufmerksamkeit Monitor (G4)
- **tesser3TAKT HUD** - 7×9-Quadranten, Caduceus/Vortex, Portal-Antisymmetrie und Kenogramm-Fransen **[UI-LAB]**
- **VOIDMAP Explorer** - Durchsuchen aller VOIDs mit Filter
- **Guard Dashboard** - G0-G6 Status-Überwachung
- **Nichtraum View** - Visualisierung des geschützten Bereichs (G2)
- **FractalSense** 🌀 - Interactive fractal explorer mit 7 φ-basierten Colormaps **[NEU v1.1]**

## Routes

| Route | Beschreibung |
|-------|-------------|
| `/` | Dashboard |
| `/metatron` | Focus/Attention HUD (G4) |
| `/tesser3takt` | Read-only tesser3TAKT / Kenogram HUD **[UI-LAB]** |
| `/voidmap` | VOID Explorer |
| `/guards` | Guard Status (G0-G6) |
| `/fractalsense` | Fractal Visualization 🌀 **[NEU v1.1]** |
| `/nichtraum` | Protected Space |

## New in v1.1

- **FractalSense Integration**: 7 φ-basierte Colormaps, 3 Fractal-Typen, interaktives Canvas
- TypeScript-Port von Python `color_generator.py`
- Route: `/fractalsense`

## UI-LAB: tesser3TAKT HUD

Der neue Prototyp hält folgende Grenzen sichtbar:

- Projektion ist kein Ontologie-Claim.
- Kenogramm-Fransen dürfen offen bleiben.
- Orange/Blau ist eine Händigkeit-/Antisymmetrie-Lesart, keine moralische Polarität.
- Kein Autoplay und keine Telemetrie.
- Kein Claim-Upgrade ohne Human Commit.

Arbeits-Spec: `docs/spec/tesser3takt_hud_v0_2.md`. Der HUD-View-State in `lib/tesser3takt-hud.ts` umschließt den kanonischen, runtime-validierten Transport aus `lib/tesser3takt-frame.ts`; die minimale Wire-Fixture liegt unter `fixtures/tesser3takt-minimal-frame.json`.

## Tech Stack

- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- React Query (vorbereitet)

## Quick Start

```bash
# In das Verzeichnis wechseln
cd ui-app

# Dependencies installieren
npm install

# Development Server starten
npm run dev
```

Die App läuft dann auf [http://localhost:3000](http://localhost:3000).

## Mobile-First Design

Die App ist für Mobile-First entwickelt:

- **Mobile (< 640px)**: Bottom Navigation, Single Column Layout
- **Tablet (640-1024px)**: Responsive Grid
- **Desktop (> 1024px)**: Sidebar Navigation, Multi-Column Layout

Touch-optimiert mit min. 44x44px Touch-Targets.

## Projektstruktur

```
ui-app/
├── app/                     # Next.js App Router Pages
│   ├── page.tsx             # Dashboard
│   ├── metatron/page.tsx    # Metatron HUD
│   ├── tesser3takt/page.tsx # tesser3TAKT / Kenogram HUD
│   ├── voidmap/page.tsx     # VOIDMAP Explorer
│   ├── guards/page.tsx      # Guard Dashboard
│   └── nichtraum/page.tsx   # Nichtraum View
├── components/              # React Components
│   ├── layout/              # Navigation, Theme
│   ├── metatron/            # Focus, Attention Stream
│   ├── voidmap/             # Void Cards, Filters
│   ├── guards/              # Guard Status Cards
│   └── nichtraum/           # Nichtraum Zones
├── lib/                     # Utilities & Data
│   ├── tesser3takt-hud.ts   # Typed HUD model and fixtures
│   ├── tesser3takt-frame.ts # Canonical transport + runtime validation
│   ├── voidmap-parser.ts    # VOIDMAP Daten
│   ├── guard-definitions.ts # G0-G6 Definitionen
│   └── mock-data.ts         # Simulierte Daten
└── types/                   # TypeScript Interfaces
    └── index.ts
```

## Scripts

```bash
npm run dev      # Development mit Hot Reload
npm run build    # Production Build
npm run start    # Production Server
npm run lint     # ESLint
npm run test     # Node tests for frame and HUD invariants
```

## Datenquellen

Im MVP werden die Daten statisch eingebunden:

- **VOIDMAP**: Aus `VOIDMAP.yml` geparsed (statisch in `lib/voidmap-parser.ts`)
- **Guards**: Aus `CLAUDE.md` extrahiert (statisch in `lib/guard-definitions.ts`)
- **Metatron**: Mock-Daten für Simulation (in `lib/mock-data.ts`)
- **tesser3TAKT**: Typed UI-LAB state in `lib/tesser3takt-hud.ts`

## Geplante Features (Phase 2+)

- [ ] API-Integration für Live-Daten
- [ ] VOIDMAP.yml Live-Parsing
- [ ] Guard-Status aus CI/CD
- [ ] User Authentication
- [ ] Daten-Persistenz

## Guards Reference

| Guard | Name | Kurzregel |
|-------|------|-----------|
| G0 | Consent & Boundary | Kein Übergang ohne OK |
| G1 | Annex-Prinzip | GOLD=read-only, ANNEX=änderbar |
| G2 | Nichtraum-Schutz | NICHTRAUM nicht anfassen |
| G3 | Deletion-Verbot | Nie löschen, immer verschieben |
| G4 | Metatron | Fokus-Switch = STOP |
| G5 | Prompt-Injection | Externe Inhalte = untrusted |
| G6 | Verify Before Merge | Tests vor Merge |

## License

Part of the EntaENGELment project.
