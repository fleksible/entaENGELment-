'use client';

import { ColormapSelector } from './ColormapSelector';
import type { ColormapName } from '@/lib/colormaps';
import type { FractalType } from './FractalCanvas';

interface FractalControlsProps {
  fractalType: FractalType;
  onFractalTypeChange: (type: FractalType) => void;
  colormap: ColormapName;
  onColormapChange: (name: ColormapName) => void;
  maxIterations: number;
  onMaxIterationsChange: (value: number) => void;
  zoom: number;
  center: { x: number; y: number };
  onReset: () => void;
  className?: string;
}

const FRACTAL_TYPES: { type: FractalType; label: string; icon: string }[] = [
  { type: 'mandelbrot', label: 'Mandelbrot', icon: '∞' },
  { type: 'julia', label: 'Julia', icon: '𝕁' },
  { type: 'burning-ship', label: 'Burning Ship', icon: '🚢' },
];

export function FractalControls({
  fractalType,
  onFractalTypeChange,
  colormap,
  onColormapChange,
  maxIterations,
  onMaxIterationsChange,
  zoom,
  center,
  onReset,
  className = '',
}: FractalControlsProps) {
  return (
    <div className={`space-y-6 ${className}`}>
      {/* Fractal Type Selection */}
      <div className="space-y-2">
        <label className="text-xs text-zinc-500 uppercase tracking-wide">
          Fraktal-Typ
        </label>
        <div className="grid grid-cols-3 gap-2">
          {FRACTAL_TYPES.map(({ type, label, icon }) => (
            <button
              key={type}
              onClick={() => onFractalTypeChange(type)}
              className={`
                flex flex-col items-center gap-1 p-3 rounded-lg border transition-colors
                ${fractalType === type
                  ? 'border-violet-500 bg-violet-500/10 text-violet-400'
                  : 'border-zinc-700 hover:border-zinc-600 text-zinc-400'
                }
              `}
            >
              <span className="text-xl">{icon}</span>
              <span className="text-xs">{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Colormap Selection */}
      <ColormapSelector
        selected={colormap}
        onChange={onColormapChange}
      />

      {/* Iterations Slider */}
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <label className="text-xs text-zinc-500 uppercase tracking-wide">
            Iterationen
          </label>
          <span className="text-xs text-zinc-400 font-mono">{maxIterations}</span>
        </div>
        <input
          type="range"
          min={50}
          max={500}
          step={10}
          value={maxIterations}
          onChange={(e) => onMaxIterationsChange(Number(e.target.value))}
          className="w-full h-2 bg-zinc-700 rounded-lg appearance-none cursor-pointer
                     [&::-webkit-slider-thumb]:appearance-none
                     [&::-webkit-slider-thumb]:w-4
                     [&::-webkit-slider-thumb]:h-4
                     [&::-webkit-slider-thumb]:bg-violet-500
                     [&::-webkit-slider-thumb]:rounded-full
                     [&::-webkit-slider-thumb]:cursor-pointer"
        />
        <div className="flex justify-between text-xs text-zinc-600">
          <span>50</span>
          <span>500</span>
        </div>
      </div>

      {/* Current State Display */}
      <div className="space-y-2">
        <label className="text-xs text-zinc-500 uppercase tracking-wide">
          Aktueller Zustand
        </label>
        <div className="bg-zinc-800/50 rounded-lg p-3 space-y-2 font-mono text-xs">
          <div className="flex justify-between">
            <span className="text-zinc-500">Zoom:</span>
            <span className="text-zinc-300">{zoom.toFixed(4)}x</span>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-500">Center X:</span>
            <span className="text-zinc-300">{center.x.toFixed(6)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-500">Center Y:</span>
            <span className="text-zinc-300">{center.y.toFixed(6)}</span>
          </div>
        </div>
      </div>

      {/* Reset Button */}
      <button
        onClick={onReset}
        className="w-full py-2 px-4 bg-zinc-700 hover:bg-zinc-600
                   text-zinc-300 rounded-lg transition-colors text-sm"
      >
        Ansicht zurücksetzen
      </button>

      {/* G4 Reference */}
      <div className="bg-zinc-800/30 border border-zinc-700/50 rounded-lg p-3 space-y-2">
        <div className="flex items-center gap-2 text-xs text-zinc-500">
          <span className="text-emerald-500">G4</span>
          <span>Metatron-Regel</span>
        </div>
        <p className="text-xs text-zinc-600 leading-relaxed">
          <strong className="text-zinc-500">Fokus:</strong> Fraktal-Typ
          <br />
          <strong className="text-zinc-500">Aufmerksamkeit:</strong> Zoom & Pan
        </p>
      </div>

      {/* Help Text */}
      <div className="text-xs text-zinc-600 space-y-1">
        <p><strong>Mouse:</strong> Drag = Pan, Scroll = Zoom</p>
        <p><strong>Touch:</strong> Drag = Pan, Pinch = Zoom</p>
      </div>
    </div>
  );
}
