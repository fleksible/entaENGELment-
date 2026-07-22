'use client';

import { useMemo, useState } from 'react';
import {
  buildTesserHudFrame,
  KENO_FRINGES,
  KNIGHT_TRAJECTORY,
  landauPotential,
  LYRA_CHANNELS,
  PORTAL_DISTINCT_RIGHT_STATE_ID,
  PORTAL_LEFT_STATE_ID,
  type KenoStatus,
  type ObserverMode,
} from '@/lib/tesser3takt-hud';

const QUADRANT_ORIGINS = [
  { x: 40, y: 78 },
  { x: 326, y: 78 },
  { x: 40, y: 308 },
  { x: 326, y: 308 },
] as const;

const CELL_W = 24;
const CELL_H = 22;
const COLS = 9;
const ROWS = 7;

const FIBER_COLORS = [
  '#ef4444',
  '#f97316',
  '#eab308',
  '#22c55e',
  '#06b6d4',
  '#3b82f6',
  '#a855f7',
] as const;

const STATUS_STYLES: Record<KenoStatus, string> = {
  UNOBSERVED: 'border-zinc-600 text-zinc-300 bg-zinc-800/60',
  UNBOUND: 'border-amber-500/50 text-amber-300 bg-amber-500/10',
  CONFLICT: 'border-fuchsia-500/50 text-fuchsia-300 bg-fuchsia-500/10',
  WITHHELD: 'border-sky-500/50 text-sky-300 bg-sky-500/10',
  FORBIDDEN: 'border-red-500/50 text-red-300 bg-red-500/10',
};

const GUARD_STYLES = {
  PASS: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300',
  HOLD: 'border-amber-500/40 bg-amber-500/10 text-amber-300',
  LOOP: 'border-sky-500/40 bg-sky-500/10 text-sky-300',
  STOP: 'border-red-500/40 bg-red-500/10 text-red-300',
} as const;

const REGIME_STYLES = {
  SYMMETRIC: 'border-zinc-600 bg-zinc-800/60 text-zinc-300',
  CRITICAL: 'border-amber-500/40 bg-amber-500/10 text-amber-300',
  BROKEN: 'border-violet-500/40 bg-violet-500/10 text-violet-300',
  LOOSENED: 'border-sky-500/40 bg-sky-500/10 text-sky-300',
  OVERWOUND: 'border-rose-500/40 bg-rose-500/10 text-rose-300',
} as const;

function cellCenter(quadrant: number, column: number, row: number) {
  const origin = QUADRANT_ORIGINS[quadrant];
  return {
    x: origin.x + (column + 0.5) * CELL_W,
    y: origin.y + (row + 0.5) * CELL_H,
  };
}

function fiberPath(index: number, torsion: number) {
  const points: string[] = [];
  const amplitude = 42 * (1 - torsion) + 6;
  const turns = 1.1 + 4.6 * torsion;
  const spread = (index - 3) * (11 * (1 - torsion) + 2);

  for (let i = 0; i <= 90; i += 1) {
    const t = i / 90;
    const x = 118 + 404 * t;
    const envelope = Math.sin(Math.PI * t);
    const y =
      270 +
      spread +
      amplitude * envelope * Math.sin(2 * Math.PI * turns * t + index * 0.62);
    points.push(`${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`);
  }

  return points.join(' ');
}

function landauPath(control: number) {
  const points: string[] = [];
  for (let i = 0; i <= 100; i += 1) {
    const phi = -1.8 + (3.6 * i) / 100;
    const potential = landauPotential(phi, control);
    const x = 20 + (220 * i) / 100;
    const y = 116 - Math.min(96, potential * 28 + 20);
    points.push(`${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`);
  }
  return points.join(' ');
}

export function Tesser3TaktHudV2() {
  const [control, setControl] = useState(-0.34);
  const [torsion, setTorsion] = useState(0.48);
  const [zLayer, setZLayer] = useState(4);
  const [observerMode, setObserverMode] = useState<ObserverMode>('OUTER');
  const [selectedFringe, setSelectedFringe] = useState('Kη-01');
  const [rightStateId, setRightStateId] = useState(PORTAL_DISTINCT_RIGHT_STATE_ID);
  const [claimPromotionRequested, setClaimPromotionRequested] = useState(false);
  const [consentFailed, setConsentFailed] = useState(false);

  const frame = buildTesserHudFrame({
    observerMode,
    control,
    torsion,
    zLayer,
    leftStateId: PORTAL_LEFT_STATE_ID,
    rightStateId,
    guardInputs: {
      claimPromotionRequested,
      consentFailed,
    },
  });
  const portalCollision = frame.transport.collisionProxy;

  const selected =
    KENO_FRINGES.find((fringe) => fringe.id === selectedFringe) ?? KENO_FRINGES[0];

  const trajectory = useMemo(
    () => {
      const boundaryByStep = new Map(
        frame.transport.boundaryTransitions.map((transition) => [
          transition.stepIndex,
          transition,
        ]),
      );

      return KNIGHT_TRAJECTORY.map((step, stepIndex) => ({
        ...step,
        ...cellCenter(step.quadrant, step.column, step.row),
        boundaryTransition: boundaryByStep.get(stepIndex),
      }));
    },
    [frame.transport.boundaryTransitions],
  );

  return (
    <div className="space-y-6 md:space-y-8">
      <header className="pt-2 md:pt-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-3xl">⌬</span>
          <div>
            <h1 className="text-2xl font-bold text-zinc-100 md:text-3xl">
              tesser3TAKT · Kenogram HUD v0.2
            </h1>
            <p className="mt-1 text-sm text-zinc-500 md:text-base">
              SPEC-WIP · projection-only · regime ≠ guard · no oracle
            </p>
          </div>
          <div className="ml-auto flex flex-wrap gap-2">
            <span
              className={`rounded-full border px-3 py-1 text-xs font-bold ${REGIME_STYLES[frame.regime.state]}`}
            >
              {frame.regime.state}
            </span>
            <span
              className={`rounded-full border px-3 py-1 text-xs font-bold ${GUARD_STYLES[frame.guardState]}`}
            >
              {frame.guardState}
            </span>
          </div>
        </div>
      </header>

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/35 p-3">
          <div className="text-xs text-zinc-500">Knight graph</div>
          <div className="mt-1 text-xl font-semibold text-zinc-100">63 / 164</div>
          <div className="text-xs text-zinc-500">vertices / edges · d=6</div>
        </div>
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/35 p-3">
          <div className="text-xs text-zinc-500">S₄ adjacent swaps</div>
          <div className="mt-1 text-xl font-semibold text-zinc-100">24 / 36</div>
          <div className="text-xs text-zinc-500">3-regular · d=6</div>
        </div>
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/35 p-3">
          <div className="text-xs text-zinc-500">Lyra</div>
          <div className="mt-1 text-xl font-semibold text-zinc-100">7</div>
          <div className="text-xs text-zinc-500">independent channels</div>
        </div>
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/35 p-3">
          <div className="text-xs text-zinc-500">Address space</div>
          <div className="mt-1 text-xl font-semibold text-zinc-100">63 + X</div>
          <div className="text-xs text-zinc-500">residual channel unoccupied</div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.65fr_.85fr]">
        <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950/70 p-3 md:p-5">
          <svg
            viewBox="0 0 760 560"
            className="h-auto w-full"
            role="img"
            aria-label="tesser3TAKT HUD mit vier 7-mal-9-Feldern, Rösselsprung, sieben Lyra-Fasern, Hermes-Mast, Caduceus und Orange-Blau-Portalen"
          >
            <defs>
              <radialGradient id="hud-core-v2" cx="50%" cy="50%" r="52%">
                <stop offset="0%" stopColor="#f8fafc" stopOpacity="0.52" />
                <stop offset="28%" stopColor="#f59e0b" stopOpacity="0.2" />
                <stop offset="100%" stopColor="#09090b" stopOpacity="0" />
              </radialGradient>
              <linearGradient id="orange-portal-v2" x1="0" x2="1">
                <stop offset="0%" stopColor="#f59e0b" />
                <stop offset="100%" stopColor="#fb7185" />
              </linearGradient>
              <linearGradient id="blue-portal-v2" x1="0" x2="1">
                <stop offset="0%" stopColor="#22d3ee" />
                <stop offset="100%" stopColor="#3b82f6" />
              </linearGradient>
            </defs>

            <rect x="2" y="2" width="756" height="556" rx="24" fill="#050507" stroke="#27272a" />
            <ellipse
              cx="380"
              cy="278"
              rx="198"
              ry="220"
              fill="url(#hud-core-v2)"
              opacity={observerMode === 'INNER' ? 0.92 : 0.46}
            />

            {QUADRANT_ORIGINS.map((origin, quadrant) => (
              <g key={quadrant} opacity={observerMode === 'INNER' ? 0.36 : 0.78}>
                <rect
                  x={origin.x}
                  y={origin.y}
                  width={COLS * CELL_W}
                  height={ROWS * CELL_H}
                  rx="10"
                  fill="#09090b"
                  stroke="#3f3f46"
                />
                {Array.from({ length: ROWS + 1 }, (_, row) => (
                  <line
                    key={`r-${quadrant}-${row}`}
                    x1={origin.x}
                    y1={origin.y + row * CELL_H}
                    x2={origin.x + COLS * CELL_W}
                    y2={origin.y + row * CELL_H}
                    stroke="#27272a"
                    strokeWidth="0.8"
                  />
                ))}
                {Array.from({ length: COLS + 1 }, (_, column) => (
                  <line
                    key={`c-${quadrant}-${column}`}
                    x1={origin.x + column * CELL_W}
                    y1={origin.y}
                    x2={origin.x + column * CELL_W}
                    y2={origin.y + ROWS * CELL_H}
                    stroke="#27272a"
                    strokeWidth="0.8"
                  />
                ))}
                <text x={origin.x + 8} y={origin.y - 8} fill="#71717a" fontSize="11">
                  Q{quadrant + 1} · 7×9
                </text>
              </g>
            ))}

            <polyline
              points={trajectory.map((step) => `${step.x},${step.y}`).join(' ')}
              fill="none"
              stroke="#fbbf24"
              strokeWidth="3"
              strokeLinejoin="round"
              opacity="0.82"
            />

            {trajectory.map((step) => (
              <g key={step.id}>
                <circle
                  cx={step.x}
                  cy={step.y}
                  r={step.boundaryTransition ? 6 : 4}
                  fill={step.boundaryTransition ? '#f4f4f5' : '#f59e0b'}
                  stroke={step.boundaryTransition ? '#f59e0b' : '#09090b'}
                  strokeWidth="2"
                />
                {step.boundaryTransition && (
                  <text x={step.x + 8} y={step.y - 8} fill="#fbbf24" fontSize="9">
                    {step.boundaryTransition.half === 'EXIT' ? '½→' : '→½'}
                  </text>
                )}
              </g>
            ))}

            {FIBER_COLORS.map((color, index) => (
              <path
                key={color}
                d={fiberPath(index, torsion)}
                fill="none"
                stroke={color}
                strokeWidth={2.1 + torsion * 2.3}
                opacity={0.4 + torsion * 0.38}
                strokeLinecap="round"
              />
            ))}

            <line x1="380" y1="500" x2="380" y2="52" stroke="#f8fafc" strokeWidth="3" opacity="0.82" />
            <text x="390" y="64" fill="#e4e4e7" fontSize="12">
              z · orthogonaler Hermes-Mast
            </text>

            <path
              d={`M380 486 C${328 - zLayer * 2} 432 ${432 + zLayer * 2} 378 380 326 C${328 - zLayer * 2} 274 ${432 + zLayer * 2} 220 380 166 C${328 - zLayer * 2} 126 ${432 + zLayer * 2} 94 380 68`}
              fill="none"
              stroke="#22d3ee"
              strokeWidth="5"
              strokeLinecap="round"
            />
            <path
              d={`M380 486 C${432 + zLayer * 2} 432 ${328 - zLayer * 2} 378 380 326 C${432 + zLayer * 2} 274 ${328 - zLayer * 2} 220 380 166 C${432 + zLayer * 2} 126 ${328 - zLayer * 2} 94 380 68`}
              fill="none"
              stroke="#f59e0b"
              strokeWidth="5"
              strokeLinecap="round"
            />

            <g transform="translate(85 255)">
              <circle r="48" fill="#030712" stroke="url(#orange-portal-v2)" strokeWidth="5" />
              <circle r="28" fill="none" stroke="#f59e0b" strokeWidth="2" opacity="0.5" />
              <text x="0" y="4" fill="#fdba74" textAnchor="middle" fontSize="13">ORANGE</text>
              <text x="0" y="65" fill="#a1a1aa" textAnchor="middle" fontSize="10">+ Händigkeit</text>
            </g>

            <g transform="translate(675 255)">
              <circle r="48" fill="#030712" stroke="url(#blue-portal-v2)" strokeWidth="5" />
              <circle r="28" fill="none" stroke="#38bdf8" strokeWidth="2" opacity="0.5" />
              <text x="0" y="4" fill="#7dd3fc" textAnchor="middle" fontSize="13">BLUE</text>
              <text x="0" y="65" fill="#a1a1aa" textAnchor="middle" fontSize="10">− Händigkeit</text>
            </g>

            <circle
              cx="380"
              cy="278"
              r="18"
              fill="#09090b"
              stroke={portalCollision ? '#ef4444' : '#f8fafc'}
              strokeWidth="3"
            />
            <text
              x="380"
              y="282"
              fill={portalCollision ? '#fca5a5' : '#f8fafc'}
              textAnchor="middle"
              fontSize="11"
            >
              {portalCollision ? '0' : 'X'}
            </text>
            <text x="380" y="310" fill="#71717a" textAnchor="middle" fontSize="10">
              63 + X · unoccupied residual channel
            </text>

            {LYRA_CHANNELS.map((channel, index) => {
              const y = 510 - index * 13;
              return (
                <g key={channel.id}>
                  <line x1="300" y1={y} x2="460" y2={y} stroke={FIBER_COLORS[index]} strokeWidth="1.4" opacity="0.72" />
                  <text x="286" y={y + 3} fill="#a1a1aa" textAnchor="end" fontSize="9">
                    {index + 1} · {channel.note}
                  </text>
                </g>
              );
            })}

            {observerMode === 'INVERSE' && (
              <g>
                <rect x="250" y="20" width="260" height="32" rx="12" fill="#18181b" stroke="#a78bfa" strokeDasharray="6 4" />
                <text x="380" y="40" fill="#c4b5fd" textAnchor="middle" fontSize="12">
                  719° frozen frame · &gt;~&lt; · Rücken in 2D
                </text>
              </g>
            )}
          </svg>
        </div>

        <aside className="space-y-4">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/35 p-4">
            <h2 className="font-semibold text-zinc-100">Regime · keine Guard-Ableitung</h2>
            <label className="mt-4 block text-xs text-zinc-400">
              Landau control · {control.toFixed(2)}
              <input
                type="range"
                min="-1"
                max="1"
                step="0.02"
                value={control}
                onChange={(event) => setControl(Number(event.target.value))}
                className="mt-2 w-full"
              />
            </label>
            <svg viewBox="0 0 260 130" className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950/70">
              <line x1="20" y1="116" x2="242" y2="116" stroke="#52525b" />
              <line x1="130" y1="12" x2="130" y2="122" stroke="#52525b" />
              <path d={landauPath(control)} fill="none" stroke="#f59e0b" strokeWidth="3" />
              <circle cx={130 + frame.regime.orderParameter * 52} cy={112} r="4" fill="#22d3ee" />
            </svg>

            <label className="mt-4 block text-xs text-zinc-400">
              Loosen ↔ Tighten · {torsion.toFixed(2)}
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={torsion}
                onChange={(event) => setTorsion(Number(event.target.value))}
                className="mt-2 w-full"
              />
            </label>

            <label className="mt-4 block text-xs text-zinc-400">
              zN depth · {zLayer}
              <input
                type="range"
                min="1"
                max="9"
                step="1"
                value={zLayer}
                onChange={(event) => setZLayer(Number(event.target.value))}
                className="mt-2 w-full"
              />
            </label>

            <div className="mt-4 grid grid-cols-3 gap-2">
              {(['OUTER', 'INNER', 'INVERSE'] as const).map((mode) => (
                <button
                  key={mode}
                  type="button"
                  onClick={() => setObserverMode(mode)}
                  className={`rounded-lg border px-2 py-2 text-[11px] font-medium ${
                    observerMode === mode
                      ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300'
                      : 'border-zinc-700 bg-zinc-950/40 text-zinc-500'
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/35 p-4">
            <h2 className="font-semibold text-zinc-100">Portal-Antisymmetrie</h2>
            <p className="mt-2 text-xs leading-relaxed text-zinc-500">
              Der Nullfall ist ein formaler Kollisionshinweis. Er verändert nicht automatisch den Guard.
            </p>
            <button
              type="button"
              onClick={() =>
                setRightStateId((value) =>
                  value === PORTAL_LEFT_STATE_ID
                    ? PORTAL_DISTINCT_RIGHT_STATE_ID
                    : PORTAL_LEFT_STATE_ID,
                )
              }
              className={`mt-3 w-full rounded-xl border px-3 py-3 text-sm font-medium ${
                portalCollision
                  ? 'border-red-500/50 bg-red-500/10 text-red-300'
                  : 'border-sky-500/50 bg-sky-500/10 text-sky-300'
              }`}
            >
              {portalCollision ? 'Det Ψ = 0 · Kollision lösen' : 'Det Ψ ≠ 0 · Kollision simulieren'}
            </button>
            <p className="mt-2 break-all text-[10px] text-zinc-600">
              {frame.portal.leftStateId} ↔ {frame.portal.rightStateId}
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/35 p-4">
            <h2 className="font-semibold text-zinc-100">Guard-Ereignisse</h2>
            <label className="mt-3 flex items-center gap-3 text-xs text-zinc-400">
              <input
                type="checkbox"
                checked={claimPromotionRequested}
                onChange={(event) => setClaimPromotionRequested(event.target.checked)}
              />
              Claim-Promotion angefordert → HOLD
            </label>
            <label className="mt-3 flex items-center gap-3 text-xs text-zinc-400">
              <input
                type="checkbox"
                checked={consentFailed}
                onChange={(event) => setConsentFailed(event.target.checked)}
              />
              Consent-Fail → STOP
            </label>
          </div>
        </aside>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.25fr_.75fr]">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/25 p-4 md:p-5">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="font-semibold text-zinc-100">Kenogramm-Fransen</h2>
              <p className="mt-1 text-xs text-zinc-500">Lokalisieren, ohne durch Sichtbarkeit bereits zu schließen.</p>
            </div>
            <span className="rounded-full border border-zinc-700 px-3 py-1 text-xs text-zinc-400">
              {KENO_FRINGES.length} offen
            </span>
          </div>
          <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {KENO_FRINGES.map((fringe) => (
              <button
                key={fringe.id}
                type="button"
                onClick={() => setSelectedFringe(fringe.id)}
                className={`rounded-xl border p-3 text-left transition ${STATUS_STYLES[fringe.status]} ${
                  selectedFringe === fringe.id ? 'ring-2 ring-emerald-400/60' : ''
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-bold">{fringe.id}</span>
                  <span className="text-[10px] opacity-70">{fringe.status}</span>
                </div>
                <div className="mt-2 text-sm font-medium">{fringe.label}</div>
                <div className="mt-1 text-[10px] opacity-70">{fringe.layer}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/35 p-4 md:p-5">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold text-zinc-100">{selected.id}</h2>
            <span className={`rounded-full border px-2 py-1 text-[10px] ${STATUS_STYLES[selected.status]}`}>
              {selected.status}
            </span>
          </div>
          <p className="mt-3 text-sm font-medium text-zinc-300">{selected.label}</p>
          <dl className="mt-4 space-y-3 text-xs">
            <div>
              <dt className="text-zinc-600">Fehlender Operator</dt>
              <dd className="mt-1 text-zinc-300">{selected.missingOperator ?? 'mehrere konkurrierende Operatoren'}</dd>
            </div>
            <div>
              <dt className="text-zinc-600">Anker</dt>
              <dd className="mt-1 flex flex-wrap gap-1">
                {selected.anchors.map((anchor) => (
                  <span key={anchor} className="rounded bg-zinc-950/70 px-2 py-1 text-zinc-400">{anchor}</span>
                ))}
              </dd>
            </div>
            <div>
              <dt className="text-zinc-600">Provenienz</dt>
              <dd className="mt-1 space-y-1 text-zinc-400">
                {selected.provenance.map((reference, index) => (
                  <div key={`${reference.source}:${reference.locator}:${index}`}>
                    {reference.source} · {reference.locator}
                  </div>
                ))}
              </dd>
            </div>
            <div>
              <dt className="text-zinc-600">Resolution Gate</dt>
              <dd className="mt-1 text-zinc-300">
                human={String(selected.resolutionGate.needsHumanCommit)} · counterfixture={String(selected.resolutionGate.needsCounterfixture)} · claim-audit={String(selected.resolutionGate.needsClaimAudit)} · consent={String(selected.resolutionGate.needsConsent)}
              </dd>
            </div>
            <div>
              <dt className="text-zinc-600">Persistenter VOID</dt>
              <dd className="mt-1 text-emerald-300">zulässig</dd>
            </div>
          </dl>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/20 p-4 md:p-6">
          <h2 className="font-semibold text-zinc-100">HUD view + canonical transport</h2>
          <pre className="mt-4 max-h-96 overflow-auto rounded-xl border border-zinc-800 bg-zinc-950/80 p-3 text-[11px] leading-relaxed text-zinc-400">
            {JSON.stringify(frame, null, 2)}
          </pre>
        </div>

        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/20 p-4 md:p-6">
          <h2 className="font-semibold text-zinc-100">Optional semantic assist</h2>
          <p className="mt-3 text-sm leading-relaxed text-zinc-500">
            {frame.semanticAssist.modelRef} bleibt deaktiviert. Seine einzige erlaubte Rolle ist das Ranking möglicher Nachbarknoten; Kenogramme schließen und Claims promoten darf es nicht.
          </p>
          <div className="mt-4 grid gap-2 text-xs sm:grid-cols-2">
            <div className="rounded-lg border border-zinc-800 bg-zinc-950/60 p-3 text-zinc-400">enabled: false</div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950/60 p-3 text-zinc-400">persistence: none</div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950/60 p-3 text-zinc-400">resolve kenograms: false</div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950/60 p-3 text-zinc-400">promote claims: false</div>
          </div>
        </div>
      </section>
    </div>
  );
}
