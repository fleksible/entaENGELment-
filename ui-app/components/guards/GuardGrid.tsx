'use client';

import { useState, useEffect } from 'react';
import { Guard } from '@/types';
import { GuardStatusCard } from './GuardStatus';
import { getGuardsWithStatus } from '@/lib/guard-definitions';

export function GuardGrid() {
  const [guards, setGuards] = useState<Guard[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  // Initialize guards
  useEffect(() => {
    setGuards(getGuardsWithStatus());
  }, []);

  // Simulate real-time updates (every 10 seconds)
  useEffect(() => {
    const interval = setInterval(() => {
      setGuards(getGuardsWithStatus());
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // Count statuses
  const okCount = guards.filter(g => g.status === 'ok').length;
  const warningCount = guards.filter(g => g.status === 'warning').length;
  const errorCount = guards.filter(g => g.status === 'error').length;

  return (
    <div className="space-y-4 md:space-y-6">
      {/* Summary */}
      <div className="flex items-center gap-4 p-4 bg-zinc-900/30 rounded-xl">
        <div className="flex items-center gap-2">
          <span className="text-emerald-400 text-xl">✓</span>
          <span className="text-emerald-400 font-bold">{okCount}</span>
          <span className="text-zinc-500 text-sm">OK</span>
        </div>
        {warningCount > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-amber-400 text-xl">⚠</span>
            <span className="text-amber-400 font-bold">{warningCount}</span>
            <span className="text-zinc-500 text-sm">Warning</span>
          </div>
        )}
        {errorCount > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-red-400 text-xl">✗</span>
            <span className="text-red-400 font-bold">{errorCount}</span>
            <span className="text-zinc-500 text-sm">Error</span>
          </div>
        )}
        <div className="flex-1" />
        <div className="text-xs text-zinc-600">
          Auto-refresh: 10s
        </div>
      </div>

      {/* Guard Cards */}
      <div className="space-y-3">
        {guards.map((guard) => (
          <GuardStatusCard
            key={guard.id}
            guard={guard}
            expanded={expandedId === guard.id}
            onToggle={() => setExpandedId(
              expandedId === guard.id ? null : guard.id
            )}
          />
        ))}
      </div>
    </div>
  );
}
