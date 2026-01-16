'use client';

import { FocusState } from '@/types';

interface FocusIndicatorProps {
  focusState: FocusState;
}

export function FocusIndicator({ focusState }: FocusIndicatorProps) {
  const { current, since, switchPending, proposedSwitch } = focusState;

  // Calculate duration
  const durationMs = Date.now() - since.getTime();
  const durationMin = Math.floor(durationMs / 60000);
  const durationHrs = Math.floor(durationMin / 60);

  const durationText = durationHrs > 0
    ? `${durationHrs}h ${durationMin % 60}m`
    : `${durationMin}m`;

  return (
    <div className={`
      relative
      p-6 md:p-8
      bg-zinc-900/50 rounded-2xl
      border-2
      transition-all duration-300
      ${switchPending
        ? 'border-red-500 animate-focus-switch'
        : 'border-emerald-500/30'
      }
    `}>
      {/* Fokus Label */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🎯</span>
        <span className={`
          text-sm font-medium uppercase tracking-wider
          ${switchPending ? 'text-red-400' : 'text-emerald-400'}
        `}>
          FOKUS
        </span>
        {switchPending && (
          <span className="
            px-2 py-0.5
            bg-red-500/20 text-red-400
            text-xs font-bold
            rounded-full
            animate-pulse
          ">
            SWITCH PENDING
          </span>
        )}
      </div>

      {/* Current Focus */}
      <h2 className="
        text-2xl md:text-3xl
        font-bold text-zinc-100
        leading-tight
      ">
        {current}
      </h2>

      {/* Duration */}
      <div className="mt-4 flex items-center gap-4 text-sm text-zinc-500">
        <div className="flex items-center gap-1.5">
          <span>⏱</span>
          <span>Seit {durationText}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>Stabil</span>
        </div>
      </div>

      {/* Switch Warning */}
      {switchPending && proposedSwitch && (
        <div className="
          mt-4 p-4
          bg-red-500/10 rounded-xl
          border border-red-500/30
        ">
          <div className="text-sm font-medium text-red-400 mb-2">
            Fokus-Switch erkannt
          </div>
          <div className="text-sm text-zinc-300 mb-3">
            Neuer vorgeschlagener Fokus: <strong>{proposedSwitch}</strong>
          </div>
          <div className="flex gap-2">
            <button className="
              flex-1 py-2.5 px-4
              bg-zinc-800 text-zinc-200
              rounded-lg text-sm font-medium
              touch-manipulation
              hover:bg-zinc-700
            ">
              Beim Fokus bleiben
            </button>
            <button className="
              flex-1 py-2.5 px-4
              bg-red-500/20 text-red-400
              rounded-lg text-sm font-medium
              border border-red-500/30
              touch-manipulation
              hover:bg-red-500/30
            ">
              Fokus wechseln
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
