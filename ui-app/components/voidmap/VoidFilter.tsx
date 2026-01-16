'use client';

import { VoidStatus, VoidPriority, VoidFilters } from '@/types';

interface VoidFilterProps {
  filters: VoidFilters;
  onFilterChange: (filters: VoidFilters) => void;
  stats: {
    total: number;
    open: number;
    inProgress: number;
    closed: number;
  };
}

const STATUS_OPTIONS: { value: VoidStatus | 'ALL'; label: string; icon: string }[] = [
  { value: 'ALL', label: 'Alle', icon: '○' },
  { value: 'OPEN', label: 'Open', icon: '☐' },
  { value: 'IN_PROGRESS', label: 'In Progress', icon: '🔄' },
  { value: 'CLOSED', label: 'Closed', icon: '✓' },
];

const PRIORITY_OPTIONS: { value: VoidPriority | 'ALL'; label: string }[] = [
  { value: 'ALL', label: 'Alle' },
  { value: 'critical', label: 'Critical' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
];

export function VoidFilter({ filters, onFilterChange, stats }: VoidFilterProps) {
  return (
    <div className="space-y-4">
      {/* Status Filter - Chips */}
      <div className="flex flex-wrap gap-2">
        {STATUS_OPTIONS.map((option) => {
          const isActive = filters.status === option.value;
          const count = option.value === 'ALL' ? stats.total
            : option.value === 'OPEN' ? stats.open
            : option.value === 'IN_PROGRESS' ? stats.inProgress
            : stats.closed;

          return (
            <button
              key={option.value}
              onClick={() => onFilterChange({ ...filters, status: option.value })}
              className={`
                flex items-center gap-2
                px-4 py-2.5 md:px-3 md:py-2
                rounded-full
                text-sm font-medium
                touch-manipulation
                transition-colors duration-150
                ${isActive
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-zinc-800/50 text-zinc-400 border border-zinc-700/50 hover:bg-zinc-800'
                }
              `}
            >
              <span>{option.icon}</span>
              <span>{option.label}</span>
              <span className={`
                text-xs px-1.5 py-0.5 rounded-full
                ${isActive ? 'bg-emerald-500/20' : 'bg-zinc-700/50'}
              `}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Priority Filter - Dropdown on mobile, chips on desktop */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-zinc-500">Priority:</span>

        {/* Mobile: Dropdown */}
        <select
          value={filters.priority}
          onChange={(e) => onFilterChange({ ...filters, priority: e.target.value as VoidPriority | 'ALL' })}
          className="
            md:hidden
            flex-1
            bg-zinc-800 border border-zinc-700
            rounded-lg px-3 py-2.5
            text-sm text-zinc-200
            touch-manipulation
          "
        >
          {PRIORITY_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        {/* Desktop: Chips */}
        <div className="hidden md:flex gap-1.5">
          {PRIORITY_OPTIONS.map((option) => {
            const isActive = filters.priority === option.value;
            return (
              <button
                key={option.value}
                onClick={() => onFilterChange({ ...filters, priority: option.value })}
                className={`
                  px-2.5 py-1.5
                  rounded-md
                  text-xs font-medium
                  transition-colors duration-150
                  ${isActive
                    ? 'bg-zinc-700 text-zinc-100'
                    : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50'
                  }
                `}
              >
                {option.label}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
