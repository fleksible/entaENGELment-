'use client';

interface FocusSwitchAlertProps {
  isActive: boolean;
  currentFocus: string;
  proposedFocus: string;
  onStay: () => void;
  onSwitch: () => void;
  onDismiss: () => void;
}

export function FocusSwitchAlert({
  isActive,
  currentFocus,
  proposedFocus,
  onStay,
  onSwitch,
  onDismiss,
}: FocusSwitchAlertProps) {
  if (!isActive) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
        onClick={onDismiss}
      />

      {/* Alert */}
      <div className="
        fixed z-50
        inset-x-4 bottom-24
        md:inset-auto md:top-1/2 md:left-1/2
        md:-translate-x-1/2 md:-translate-y-1/2
        md:w-full md:max-w-md
      ">
        <div className="
          bg-zinc-900 rounded-2xl
          border-2 border-red-500
          animate-focus-switch
          shadow-2xl shadow-red-500/20
        ">
          {/* Header */}
          <div className="p-4 md:p-6 border-b border-zinc-800">
            <div className="flex items-center gap-3">
              <span className="text-3xl animate-pulse">⚠️</span>
              <div>
                <h2 className="text-lg font-bold text-red-400">
                  FOKUS-SWITCH RISK
                </h2>
                <p className="text-sm text-zinc-500">
                  G4: Metatron-Regel verletzt
                </p>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-4 md:p-6 space-y-4">
            {/* Current Focus */}
            <div className="p-3 bg-zinc-800/50 rounded-lg">
              <div className="text-xs text-zinc-500 mb-1">Aktueller Fokus</div>
              <div className="text-sm font-medium text-zinc-200">
                {currentFocus}
              </div>
            </div>

            {/* Arrow */}
            <div className="flex justify-center text-zinc-600">
              ↓
            </div>

            {/* Proposed Focus */}
            <div className="p-3 bg-red-500/10 rounded-lg border border-red-500/20">
              <div className="text-xs text-red-400 mb-1">Vorgeschlagener Fokus</div>
              <div className="text-sm font-medium text-zinc-200">
                {proposedFocus}
              </div>
            </div>

            {/* Explanation */}
            <p className="text-xs text-zinc-500 leading-relaxed">
              Ein Fokus-Switch wurde erkannt. Nach G4 (Metatron-Regel) sollte
              der Fokus stabil bleiben. Aufmerksamkeit darf wandern, aber ein
              Wechsel des Hauptziels erfordert explizite Entscheidung.
            </p>
          </div>

          {/* Actions */}
          <div className="p-4 md:p-6 pt-0 flex flex-col md:flex-row gap-3">
            <button
              onClick={onStay}
              className="
                flex-1 py-3 px-4
                bg-emerald-500/20 text-emerald-400
                border border-emerald-500/30
                rounded-xl text-sm font-medium
                touch-manipulation
                hover:bg-emerald-500/30
                active:scale-[0.98]
              "
            >
              Beim Fokus bleiben
            </button>
            <button
              onClick={onSwitch}
              className="
                flex-1 py-3 px-4
                bg-zinc-800 text-zinc-300
                rounded-xl text-sm font-medium
                touch-manipulation
                hover:bg-zinc-700
                active:scale-[0.98]
              "
            >
              Fokus wechseln
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
