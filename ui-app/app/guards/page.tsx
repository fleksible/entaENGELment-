import { GuardGrid } from '@/components/guards/GuardGrid';

export default function GuardsPage() {
  return (
    <div className="space-y-6 md:space-y-8">
      {/* Header */}
      <header className="pt-2 md:pt-4">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">🛡️</span>
          <h1 className="text-2xl md:text-3xl font-bold text-zinc-100">
            Guard Dashboard
          </h1>
        </div>
        <p className="text-sm md:text-base text-zinc-500">
          Überwachung der G0-G6 Guards aus CLAUDE.md
        </p>
      </header>

      {/* Guard Reference */}
      <div className="p-4 bg-zinc-900/30 rounded-xl border border-zinc-800/50">
        <h2 className="text-sm font-medium text-zinc-300 mb-3">
          Quick Reference
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span>
            <span className="text-zinc-400">OK - Guard aktiv</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-amber-400">⚠</span>
            <span className="text-zinc-400">Warning - Aufmerksamkeit</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-red-400">✗</span>
            <span className="text-zinc-400">Error - Verletzt</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-zinc-500">●</span>
            <span className="text-zinc-400">Simulated Data</span>
          </div>
        </div>
      </div>

      {/* Guard Grid */}
      <GuardGrid />

      {/* Info Box */}
      <div className="p-4 bg-zinc-900/20 rounded-xl border border-zinc-800/30">
        <h3 className="text-sm font-medium text-zinc-400 mb-2">
          Über die Guards
        </h3>
        <p className="text-xs text-zinc-500 leading-relaxed">
          Die G0-G6 Guards sind die Kernregeln für die Arbeit mit EntaENGELment.
          Sie schützen die Integrität des Projekts und definieren klare Grenzen
          für Änderungen. In diesem MVP werden die Statuswerte simuliert.
          In einer Produktionsversion würden sie aus echten CI/CD-Checks,
          Linter-Ergebnissen und Audit-Logs gespeist.
        </p>
      </div>
    </div>
  );
}
