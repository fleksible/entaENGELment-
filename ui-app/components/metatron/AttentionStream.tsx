'use client';

import { useEffect, useRef, useState } from 'react';
import { AttentionItem } from '@/types';
import { MOCK_ATTENTION_ITEMS, generateAttentionItem } from '@/lib/mock-data';

function getTypeStyles(type: AttentionItem['type']) {
  switch (type) {
    case 'exploration':
      return {
        bg: 'bg-blue-500/10',
        border: 'border-blue-500/20',
        text: 'text-blue-400',
        icon: '🔍',
      };
    case 'context':
      return {
        bg: 'bg-zinc-500/10',
        border: 'border-zinc-500/20',
        text: 'text-zinc-400',
        icon: '📎',
      };
    case 'warning':
      return {
        bg: 'bg-amber-500/10',
        border: 'border-amber-500/20',
        text: 'text-amber-400',
        icon: '⚠️',
      };
    case 'switch':
      return {
        bg: 'bg-red-500/10',
        border: 'border-red-500/20',
        text: 'text-red-400',
        icon: '🔄',
      };
  }
}

export function AttentionStream() {
  const [items, setItems] = useState<AttentionItem[]>(MOCK_ATTENTION_ITEMS);
  const [isLive, setIsLive] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Simulate live stream
  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      const newItem = generateAttentionItem();
      setItems(prev => [newItem, ...prev].slice(0, 50)); // Keep last 50
    }, 3000 + Math.random() * 2000); // Random 3-5 seconds

    return () => clearInterval(interval);
  }, [isLive]);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">👁</span>
          <h3 className="text-sm font-medium text-zinc-300">
            Aufmerksamkeit-Stream
          </h3>
        </div>
        <button
          onClick={() => setIsLive(!isLive)}
          className={`
            flex items-center gap-1.5
            px-3 py-1.5
            rounded-full text-xs font-medium
            touch-manipulation
            ${isLive
              ? 'bg-emerald-500/20 text-emerald-400'
              : 'bg-zinc-700 text-zinc-400'
            }
          `}
        >
          <span className={`w-2 h-2 rounded-full ${isLive ? 'bg-emerald-500 animate-pulse' : 'bg-zinc-500'}`} />
          {isLive ? 'Live' : 'Paused'}
        </button>
      </div>

      {/* Stream */}
      <div
        ref={scrollRef}
        className="
          flex-1 space-y-2
          overflow-y-auto
          max-h-[400px] md:max-h-[500px]
          scrollbar-thin
        "
      >
        {items.map((item, index) => {
          const styles = getTypeStyles(item.type);
          const isNew = index === 0;

          return (
            <div
              key={item.id}
              className={`
                flex items-start gap-3
                p-3 rounded-lg
                ${styles.bg} border ${styles.border}
                ${isNew ? 'animate-in' : ''}
              `}
            >
              <span className="text-base flex-shrink-0">{styles.icon}</span>
              <div className="flex-1 min-w-0">
                <p className={`text-sm ${styles.text}`}>
                  {item.content}
                </p>
                <span className="text-[10px] text-zinc-600 mt-1 block">
                  {item.timestamp.toLocaleTimeString('de-DE')}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-4 pt-4 border-t border-zinc-800/50">
        <div className="flex flex-wrap gap-3 text-[10px] text-zinc-500">
          <span className="flex items-center gap-1">
            <span>🔍</span> Exploration
          </span>
          <span className="flex items-center gap-1">
            <span>📎</span> Context
          </span>
          <span className="flex items-center gap-1">
            <span>⚠️</span> Warning
          </span>
        </div>
      </div>
    </div>
  );
}
