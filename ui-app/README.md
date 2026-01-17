# EntaENGELment UI

Web-App für die Visualisierung der EntaENGELment-Konzepte (Guard System, VOIDMAP, Metatron-Regel).

## Features

- **Metatron HUD** - Fokus & Aufmerksamkeit Monitor (G4)
- **VOIDMAP Explorer** - Durchsuchen aller VOIDs mit Filter
- **Guard Dashboard** - G0-G6 Status-Überwachung
- **Nichtraum View** - Visualisierung des geschützten Bereichs (G2)

## Tech Stack

- Next.js 14 (App Router)
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
```

## Datenquellen

Im MVP werden die Daten statisch eingebunden:

- **VOIDMAP**: Aus `VOIDMAP.yml` geparsed (statisch in `lib/voidmap-parser.ts`)
- **Guards**: Aus `CLAUDE.md` extrahiert (statisch in `lib/guard-definitions.ts`)
- **Metatron**: Mock-Daten für Simulation (in `lib/mock-data.ts`)

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
