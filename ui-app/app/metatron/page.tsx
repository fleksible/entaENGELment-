'use client';

import { useState } from 'react';
import { FocusIndicator } from '@/components/metatron/FocusIndicator';
import { AttentionStream } from '@/components/metatron/AttentionStream';
import { FocusSwitchAlert } from '@/components/metatron/FocusSwitchAlert';
import { MOCK_FOCUS_STATE } from '@/lib/mock-data';
import { FocusState } from '@/types';

export default function MetatronPage() {
  const [focusState, setFocusState] = useState<FocusState>(MOCK_FOCUS_STATE);
  const [showSwitchAlert, setShowSwitchAlert] = useState(false);

  // Simulate focus switch trigger
  const triggerSwitch = () => {
    setFocusState(prev => ({
      ...prev,
      switchPending: true,
      proposedSwitch: 'Bug in Receipt-Validierung fixen',
    }));
    setShowSwitchAlert(true);
  };

  const handleStay = () => {
    setFocusState(prev => ({
      ...prev,
      switchPending: false,
      proposedSwitch: undefined,
    }));
    setShowSwitchAlert(false);
  };

  const handleSwitch = () => {
    setFocusState({
      current: focusState.proposedSwitch || focusState.current,
      since: new Date(),
      switchPending: false,
    });
    setShowSwitchAlert(false);
  };

  return (
    <div className="space-y-6 md:space-y-8">
      {/* Header */}
      <header className="pt-2 md:pt-4">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">🎯</span>
          <h1 className="text-2xl md:text-3xl font-bold text-zinc-100">
            Metatron HUD
          </h1>
        </div>
        <p className="text-sm md:text-base text-zinc-500">
          Fokus & Aufmerksamkeit Monitor (G4: Metatron-Regel)
        </p>
      </header>

      {/* Main Layout */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Focus Indicator */}
        <div>
          <FocusIndicator focusState={focusState} />

          {/* Demo Button */}
          <div className="mt-4">
            <button
              onClick={triggerSwitch}
              disabled={focusState.switchPending}
              className="
                w-full py-3 px-4
                bg-amber-500/10 text-amber-400
                border border-amber-500/30
                rounded-xl text-sm font-medium
                touch-manipulation
                hover:bg-amber-500/20
                disabled:opacity-50 disabled:cursor-not-allowed
              "
            >
              🎭 Demo: Fokus-Switch simulieren
            </button>
          </div>
        </div>

        {/* Attention Stream */}
        <div className="bg-zinc-900/30 rounded-2xl p-4 md:p-6 border border-zinc-800/50">
          <AttentionStream />
        </div>
      </div>

      {/* G4 Rule Reference */}
      <div className="p-4 md:p-6 bg-zinc-900/20 rounded-xl border border-zinc-800/30">
        <h3 className="text-sm font-medium text-zinc-400 mb-3 flex items-center gap-2">
          <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded text-xs font-bold">
            G4
          </span>
          Metatron-Regel
        </h3>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="font-medium text-zinc-300 mb-1">Fokus</div>
            <p className="text-xs text-zinc-500">
              Das Task-Ziel, der Nullpunkt. Stabil, definiert, unverrückbar während der Session.
            </p>
          </div>
          <div>
            <div className="font-medium text-zinc-300 mb-1">Aufmerksamkeit</div>
            <p className="text-xs text-zinc-500">
              Freie Exploration der Peripherie. Wandernd, neugierig, sammelnd.
            </p>
          </div>
          <div>
            <div className="font-medium text-zinc-300 mb-1">Fokus-Switch</div>
            <p className="text-xs text-zinc-500">
              Wenn Exploration neue Aufgabe anfordert → STOP → fragen → dokumentieren.
            </p>
          </div>
        </div>
      </div>

      {/* Focus Switch Alert Modal */}
      <FocusSwitchAlert
        isActive={showSwitchAlert}
        currentFocus={focusState.current}
        proposedFocus={focusState.proposedSwitch || ''}
        onStay={handleStay}
        onSwitch={handleSwitch}
        onDismiss={handleStay}
      />
    </div>
  );
}
