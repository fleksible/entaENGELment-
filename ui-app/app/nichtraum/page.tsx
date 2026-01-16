import { NichtraumZone } from '@/components/nichtraum/NichtraumZone';
import { NICHTRAUM_ZONES } from '@/lib/mock-data';

export default function NichtraumPage() {
  return (
    <div className="space-y-6 md:space-y-8">
      {/* Header */}
      <header className="pt-2 md:pt-4">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl opacity-50">◌</span>
          <h1 className="text-2xl md:text-3xl font-bold text-zinc-100">
            Nichtraum
          </h1>
        </div>
        <p className="text-sm md:text-base text-zinc-500">
          Der geschützte Bereich für Unentschiedenes (G2)
        </p>
      </header>

      {/* G2 Rule Box */}
      <div className="p-4 md:p-6 bg-zinc-900/30 rounded-xl border border-zinc-800/50">
        <div className="flex items-start gap-3">
          <span className="
            px-2 py-0.5
            bg-emerald-500/10 text-emerald-400
            rounded text-xs font-bold
            flex-shrink-0
          ">
            G2
          </span>
          <div>
            <h2 className="text-sm font-medium text-zinc-300 mb-2">
              Nichtraum-Schutz
            </h2>
            <ul className="text-xs text-zinc-500 space-y-1">
              <li>• Nicht optimieren, nicht aufräumen</li>
              <li>• Bei Unsicherheit: rein verschieben + ☐ markieren</li>
              <li>• Struktur: archive/, maybe/, quarantine/</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Zones Grid */}
      <div className="grid gap-4 md:grid-cols-3">
        {NICHTRAUM_ZONES.map((zone) => (
          <NichtraumZone
            key={zone.id}
            {...zone}
          />
        ))}
      </div>

      {/* Philosophy Box */}
      <div className="p-6 md:p-8 bg-zinc-950 rounded-2xl border border-zinc-900">
        <div className="max-w-2xl mx-auto text-center">
          <span className="text-5xl mb-6 block opacity-30">◌</span>

          <h3 className="text-lg font-medium text-zinc-400 mb-4">
            Über den Nichtraum
          </h3>

          <div className="space-y-4 text-sm text-zinc-600 leading-relaxed">
            <p>
              Der Nichtraum ist kein Fehler. Er ist ein Designprinzip.
            </p>
            <p>
              In einer Welt, die Optimierung fordert, ist der Nichtraum ein
              Rückzugsort für das Unentschiedene. Hier darf etwas sein, ohne
              sofort kategorisiert, bewertet oder gelöscht zu werden.
            </p>
            <p>
              <span className="text-zinc-500">G3 (Deletion-Verbot)</span> schützt
              diesen Raum: Was hier landet, wird nicht gelöscht, sondern bewahrt
              — bis eine bewusste Entscheidung getroffen wird.
            </p>
          </div>

          {/* Visual separator */}
          <div className="mt-8 flex justify-center gap-3 text-zinc-800">
            <span>●</span>
            <span>○</span>
            <span>●</span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="p-4 bg-zinc-900/20 rounded-xl border border-zinc-800/30">
        <h3 className="text-sm font-medium text-zinc-400 mb-3">
          Mögliche Aktionen
        </h3>
        <div className="grid gap-2 md:grid-cols-3">
          <button
            disabled
            className="
              p-3 rounded-lg
              bg-zinc-800/30 border border-zinc-700/30
              text-sm text-zinc-500
              cursor-not-allowed
            "
          >
            <span className="block mb-1">📥</span>
            Etwas hierher verschieben
            <span className="block text-xs text-zinc-600 mt-1">
              (Noch nicht implementiert)
            </span>
          </button>

          <button
            disabled
            className="
              p-3 rounded-lg
              bg-zinc-800/30 border border-zinc-700/30
              text-sm text-zinc-500
              cursor-not-allowed
            "
          >
            <span className="block mb-1">👁</span>
            Inhalt anzeigen
            <span className="block text-xs text-zinc-600 mt-1">
              (Noch nicht implementiert)
            </span>
          </button>

          <button
            disabled
            className="
              p-3 rounded-lg
              bg-zinc-800/30 border border-zinc-700/30
              text-sm text-zinc-500
              cursor-not-allowed
            "
          >
            <span className="block mb-1">✅</span>
            Entscheidung treffen
            <span className="block text-xs text-zinc-600 mt-1">
              (Noch nicht implementiert)
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
