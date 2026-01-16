'use client';

import { Guard, GuardStatus as GuardStatusType } from '@/types';

interface GuardStatusProps {
  guard: Guard;
  expanded?: boolean;
  onToggle?: () => void;
}

function getStatusStyles(status: GuardStatusType) {
  switch (status) {
    case 'ok':
      return {
        bg: 'bg-emerald-500/10',
        border: 'border-emerald-500/30',
        text: 'text-emerald-400',
        icon: '✓',
        label: 'OK',
      };
    case 'warning':
      return {
        bg: 'bg-amber-500/10',
        border: 'border-amber-500/30',
        text: 'text-amber-400',
        icon: '⚠',
        label: 'Warning',
      };
    case 'error':
      return {
        bg: 'bg-red-500/10',
        border: 'border-red-500/30',
        text: 'text-red-400',
        icon: '✗',
        label: 'Error',
      };
  }
}

export function GuardStatusCard({ guard, expanded = false, onToggle }: GuardStatusProps) {
  const styles = getStatusStyles(guard.status);

  return (
    <div
      className={`
        rounded-xl border transition-all duration-200
        ${styles.bg} ${styles.border}
        ${expanded ? 'ring-1 ring-emerald-500/20' : ''}
      `}
    >
      {/* Header */}
      <button
        onClick={onToggle}
        className="
          w-full p-4 md:p-5
          flex items-center gap-4
          text-left touch-manipulation
        "
      >
        {/* Guard ID Badge */}
        <div className={`
          w-12 h-12 md:w-10 md:h-10
          flex items-center justify-center
          rounded-lg
          ${styles.bg} ${styles.text}
          text-lg md:text-base font-bold
        `}>
          {guard.id}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-zinc-100 text-base md:text-sm">
            {guard.name}
          </h3>
          <p className="text-sm md:text-xs text-zinc-500 mt-0.5">
            {guard.shortRule}
          </p>
        </div>

        {/* Status Icon */}
        <div className={`
          flex items-center gap-2
          ${styles.text}
        `}>
          <span className="text-2xl md:text-xl">{styles.icon}</span>
        </div>
      </button>

      {/* Expanded Content */}
      {expanded && (
        <div className="px-4 pb-4 md:px-5 md:pb-5 animate-in">
          {/* Full Rule */}
          <div className="p-3 md:p-4 bg-zinc-900/50 rounded-lg">
            <div className="text-xs font-medium text-zinc-400 mb-2">
              Vollständige Regel
            </div>
            <p className="text-sm text-zinc-300 leading-relaxed">
              {guard.fullRule}
            </p>
          </div>

          {/* Last Check */}
          {guard.lastCheck && (
            <div className="mt-3 text-xs text-zinc-500">
              Letzter Check: {guard.lastCheck.toLocaleTimeString('de-DE')}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
