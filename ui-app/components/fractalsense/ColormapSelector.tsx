'use client';

import { useMemo } from 'react';
import {
  getColormap,
  rgbToCss,
  COLORMAP_NAMES,
  COLORMAP_LABELS,
  type ColormapName,
} from '@/lib/colormaps';

interface ColormapPreviewProps {
  name: ColormapName;
  size?: number;
  className?: string;
}

/**
 * Shows a gradient preview of a colormap
 */
export function ColormapPreview({ name, size = 32, className = '' }: ColormapPreviewProps) {
  const gradient = useMemo(() => {
    const palette = getColormap(name, size);
    const stops = palette.map((color, i) => {
      const percent = (i / (palette.length - 1)) * 100;
      return `${rgbToCss(color)} ${percent.toFixed(1)}%`;
    });
    return `linear-gradient(to right, ${stops.join(', ')})`;
  }, [name, size]);

  return (
    <div
      className={`h-4 rounded ${className}`}
      style={{ background: gradient }}
      title={COLORMAP_LABELS[name]}
    />
  );
}

interface ColormapSelectorProps {
  selected: ColormapName;
  onChange: (name: ColormapName) => void;
  className?: string;
}

/**
 * Grid selector for all colormaps
 */
export function ColormapSelector({ selected, onChange, className = '' }: ColormapSelectorProps) {
  return (
    <div className={`space-y-2 ${className}`}>
      <label className="text-xs text-zinc-500 uppercase tracking-wide">
        Colormap
      </label>
      <div className="grid gap-2">
        {COLORMAP_NAMES.map((name) => (
          <button
            key={name}
            onClick={() => onChange(name)}
            className={`
              flex flex-col gap-1 p-2 rounded-lg border transition-colors
              ${selected === name
                ? 'border-violet-500 bg-violet-500/10'
                : 'border-zinc-700 hover:border-zinc-600 bg-zinc-800/50'
              }
            `}
          >
            <ColormapPreview name={name} />
            <span className="text-xs text-zinc-400 text-left truncate">
              {COLORMAP_LABELS[name]}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
