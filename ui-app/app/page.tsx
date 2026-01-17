import Link from 'next/link';
import { getVoidStats } from '@/lib/voidmap-parser';
import { GUARD_DEFINITIONS } from '@/lib/guard-definitions';

export default function HomePage() {
  const stats = getVoidStats();

  return (
    <div className="space-y-6 md:space-y-8">
      {/* Header */}
      <header className="pt-2 md:pt-4">
        <h1 className="text-2xl md:text-3xl font-bold text-zinc-100">
          Dashboard
        </h1>
        <p className="text-sm md:text-base text-zinc-500 mt-1">
          EntaENGELment Guard & Void Overview
        </p>
      </header>

      {/* Quick Stats Grid */}
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
        {/* Total VOIDs */}
        <div className="bg-zinc-900/50 rounded-xl p-4 md:p-5 border border-zinc-800">
          <div className="text-2xl md:text-3xl font-bold text-zinc-100">
            {stats.total}
          </div>
          <div className="text-xs md:text-sm text-zinc-500 mt-1">
            Total VOIDs
          </div>
        </div>

        {/* Open */}
        <div className="bg-zinc-900/50 rounded-xl p-4 md:p-5 border border-zinc-800">
          <div className="text-2xl md:text-3xl font-bold text-amber-400">
            {stats.open}
          </div>
          <div className="text-xs md:text-sm text-zinc-500 mt-1">
            ☐ Open
          </div>
        </div>

        {/* Closed */}
        <div className="bg-zinc-900/50 rounded-xl p-4 md:p-5 border border-zinc-800">
          <div className="text-2xl md:text-3xl font-bold text-green-500">
            {stats.closed}
          </div>
          <div className="text-xs md:text-sm text-zinc-500 mt-1">
            ✓ Closed
          </div>
        </div>

        {/* Critical */}
        <div className="bg-zinc-900/50 rounded-xl p-4 md:p-5 border border-zinc-800">
          <div className="text-2xl md:text-3xl font-bold text-red-500">
            {stats.critical}
          </div>
          <div className="text-xs md:text-sm text-zinc-500 mt-1">
            Critical Open
          </div>
        </div>
      </section>

      {/* Navigation Cards */}
      <section className="space-y-3 md:space-y-4">
        <h2 className="text-lg md:text-xl font-semibold text-zinc-200">
          Quick Navigation
        </h2>

        <div className="grid gap-3 md:grid-cols-2 md:gap-4">
          {/* Metatron HUD */}
          <Link
            href="/metatron"
            className="
              flex items-start gap-4 p-4 md:p-5
              bg-zinc-900/50 rounded-xl border border-zinc-800
              hover:bg-zinc-800/50 hover:border-zinc-700
              transition-colors duration-150
              touch-manipulation
            "
          >
            <span className="text-3xl">🎯</span>
            <div>
              <h3 className="font-semibold text-zinc-100">Metatron HUD</h3>
              <p className="text-sm text-zinc-500 mt-1">
                Fokus & Aufmerksamkeit Monitor
              </p>
            </div>
          </Link>

          {/* VOIDMAP Explorer */}
          <Link
            href="/voidmap"
            className="
              flex items-start gap-4 p-4 md:p-5
              bg-zinc-900/50 rounded-xl border border-zinc-800
              hover:bg-zinc-800/50 hover:border-zinc-700
              transition-colors duration-150
              touch-manipulation
            "
          >
            <span className="text-3xl">☐</span>
            <div>
              <h3 className="font-semibold text-zinc-100">VOIDMAP Explorer</h3>
              <p className="text-sm text-zinc-500 mt-1">
                {stats.open} offene VOIDs durchsuchen
              </p>
            </div>
          </Link>

          {/* Guard Dashboard */}
          <Link
            href="/guards"
            className="
              flex items-start gap-4 p-4 md:p-5
              bg-zinc-900/50 rounded-xl border border-zinc-800
              hover:bg-zinc-800/50 hover:border-zinc-700
              transition-colors duration-150
              touch-manipulation
            "
          >
            <span className="text-3xl">🛡️</span>
            <div>
              <h3 className="font-semibold text-zinc-100">Guard Dashboard</h3>
              <p className="text-sm text-zinc-500 mt-1">
                G0-G6 Status überwachen
              </p>
            </div>
          </Link>

          {/* FractalSense */}
          <Link
            href="/fractalsense"
            className="
              flex items-start gap-4 p-4 md:p-5
              bg-gradient-to-br from-violet-500/10 to-amber-500/10
              rounded-xl border border-violet-500/30
              hover:from-violet-500/20 hover:to-amber-500/20
              transition-colors duration-150
              touch-manipulation
            "
          >
            <span className="text-3xl">🌀</span>
            <div>
              <h3 className="font-semibold text-zinc-100">FractalSense</h3>
              <p className="text-sm text-zinc-400 mt-1">
                Resonante Fraktal-Visualisierung
              </p>
              <span className="inline-block mt-2 px-2 py-0.5 bg-amber-500/20 text-amber-400 text-xs rounded">
                NEU
              </span>
            </div>
          </Link>

          {/* Nichtraum */}
          <Link
            href="/nichtraum"
            className="
              flex items-start gap-4 p-4 md:p-5
              bg-zinc-900/50 rounded-xl border border-zinc-800
              hover:bg-zinc-800/50 hover:border-zinc-700
              transition-colors duration-150
              touch-manipulation
            "
          >
            <span className="text-3xl">◌</span>
            <div>
              <h3 className="font-semibold text-zinc-100">Nichtraum</h3>
              <p className="text-sm text-zinc-500 mt-1">
                Bereich für Unentschiedenes
              </p>
            </div>
          </Link>
        </div>
      </section>

      {/* Guards Overview */}
      <section className="space-y-3 md:space-y-4">
        <h2 className="text-lg md:text-xl font-semibold text-zinc-200">
          Guards (G0-G6)
        </h2>

        <div className="grid gap-2 md:gap-3">
          {GUARD_DEFINITIONS.map((guard) => (
            <div
              key={guard.id}
              className="
                flex items-center gap-3 p-3 md:p-4
                bg-zinc-900/30 rounded-lg border border-zinc-800/50
              "
            >
              <span className="
                w-10 h-10 flex items-center justify-center
                bg-emerald-500/10 text-emerald-400
                rounded-lg text-sm font-bold
              ">
                {guard.id}
              </span>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-zinc-200 text-sm md:text-base">
                  {guard.name}
                </div>
                <div className="text-xs md:text-sm text-zinc-500 truncate">
                  {guard.shortRule}
                </div>
              </div>
              <span className="text-emerald-500">✓</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
