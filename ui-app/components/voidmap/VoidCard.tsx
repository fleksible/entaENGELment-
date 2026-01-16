'use client';

import { Void } from '@/types';
import { getStatusIcon, getPriorityColor, getStatusColor } from '@/lib/voidmap-parser';

interface VoidCardProps {
  void_item: Void;
  expanded?: boolean;
  onToggle?: () => void;
}

export function VoidCard({ void_item, expanded = false, onToggle }: VoidCardProps) {
  const statusIcon = getStatusIcon(void_item.status);
  const priorityColor = getPriorityColor(void_item.priority);
  const statusColor = getStatusColor(void_item.status);

  return (
    <div
      className={`
        bg-zinc-900/50 rounded-xl border border-zinc-800
        transition-all duration-200
        ${expanded ? 'ring-1 ring-emerald-500/30' : ''}
      `}
    >
      {/* Header - Always visible */}
      <button
        onClick={onToggle}
        className="
          w-full p-4 md:p-5
          flex items-start gap-3 md:gap-4
          text-left touch-manipulation
        "
      >
        {/* Status Icon */}
        <span className={`text-2xl md:text-xl flex-shrink-0 ${statusColor}`}>
          {statusIcon}
        </span>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* ID and Priority */}
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-zinc-500">
              {void_item.id}
            </span>
            <span className={`text-xs font-medium ${priorityColor}`}>
              {void_item.priority}
            </span>
            {void_item.domain && (
              <span className="text-xs text-zinc-600">
                {void_item.domain}
              </span>
            )}
          </div>

          {/* Title */}
          <h3 className="text-base md:text-sm font-medium text-zinc-100 leading-snug">
            {void_item.title}
          </h3>

          {/* Symptom preview (truncated) */}
          {!expanded && void_item.symptom && (
            <p className="text-sm text-zinc-500 mt-1 line-clamp-1">
              {void_item.symptom}
            </p>
          )}
        </div>

        {/* Expand indicator */}
        <span className={`
          text-zinc-500 transition-transform duration-200
          ${expanded ? 'rotate-180' : ''}
        `}>
          ▼
        </span>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="px-4 pb-4 md:px-5 md:pb-5 space-y-3 animate-in">
          {/* Symptom */}
          {void_item.symptom && (
            <div>
              <div className="text-xs font-medium text-zinc-400 mb-1">
                Symptom
              </div>
              <p className="text-sm text-zinc-300">
                {void_item.symptom}
              </p>
            </div>
          )}

          {/* Closing Path */}
          {void_item.closing_path && (
            <div>
              <div className="text-xs font-medium text-zinc-400 mb-1">
                Closing Path
              </div>
              <p className="text-sm text-zinc-300">
                {void_item.closing_path}
              </p>
            </div>
          )}

          {/* Dates */}
          <div className="flex gap-4 text-xs text-zinc-500">
            <span>Created: {void_item.created}</span>
            {void_item.closed && (
              <span className="text-green-500">Closed: {void_item.closed}</span>
            )}
          </div>

          {/* Evidence */}
          {void_item.evidence && (
            <div>
              <div className="text-xs font-medium text-zinc-400 mb-1">
                Evidence
              </div>
              <div className="text-xs font-mono text-zinc-500">
                {Array.isArray(void_item.evidence)
                  ? void_item.evidence.join(', ')
                  : void_item.evidence
                }
              </div>
            </div>
          )}

          {/* Notes */}
          {void_item.notes && (
            <div>
              <div className="text-xs font-medium text-zinc-400 mb-1">
                Notes
              </div>
              <p className="text-xs text-zinc-500 whitespace-pre-line">
                {void_item.notes}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
