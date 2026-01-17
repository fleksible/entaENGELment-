'use client';

import { useState, useCallback } from 'react';
import Link from 'next/link';
import { FractalCanvas, FractalControls, type FractalType } from '@/components/fractalsense';
import type { ColormapName } from '@/lib/colormaps';

const DEFAULT_CENTER = { x: -0.5, y: 0 };
const DEFAULT_ZOOM = 1;
const DEFAULT_ITERATIONS = 100;

export default function FractalsensePage() {
  const [fractalType, setFractalType] = useState<FractalType>('mandelbrot');
  const [colormap, setColormap] = useState<ColormapName>('resonant');
  const [maxIterations, setMaxIterations] = useState(DEFAULT_ITERATIONS);
  const [zoom, setZoom] = useState(DEFAULT_ZOOM);
  const [center, setCenter] = useState(DEFAULT_CENTER);
  const [showControls, setShowControls] = useState(false);

  // Key for forcing canvas remount on reset
  const [canvasKey, setCanvasKey] = useState(0);

  const handleReset = useCallback(() => {
    setZoom(DEFAULT_ZOOM);
    setCenter(DEFAULT_CENTER);
    setCanvasKey((k) => k + 1);
  }, []);

  const handleFractalTypeChange = useCallback((type: FractalType) => {
    setFractalType(type);
    // Reset view when changing fractal type
    if (type === 'julia') {
      setCenter({ x: 0, y: 0 });
    } else if (type === 'burning-ship') {
      setCenter({ x: -0.4, y: -0.6 });
    } else {
      setCenter(DEFAULT_CENTER);
    }
    setZoom(DEFAULT_ZOOM);
    setCanvasKey((k) => k + 1);
  }, []);

  return (
    <div className="h-[calc(100vh-2rem)] md:h-[calc(100vh-3rem)] flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between py-3 md:py-4">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            ← Dashboard
          </Link>
          <div className="h-4 w-px bg-zinc-700" />
          <h1 className="text-lg md:text-xl font-semibold text-zinc-100 flex items-center gap-2">
            <span>🌀</span>
            <span>FractalSense</span>
          </h1>
        </div>

        {/* Mobile controls toggle */}
        <button
          onClick={() => setShowControls(!showControls)}
          className="md:hidden px-3 py-1.5 bg-zinc-800 border border-zinc-700
                     rounded-lg text-sm text-zinc-300"
        >
          {showControls ? 'Canvas' : 'Controls'}
        </button>
      </header>

      {/* Main content */}
      <div className="flex-1 flex gap-4 min-h-0">
        {/* Canvas area */}
        <div className={`flex-1 min-w-0 ${showControls ? 'hidden md:block' : ''}`}>
          <FractalCanvas
            key={canvasKey}
            fractalType={fractalType}
            colormap={colormap}
            maxIterations={maxIterations}
            initialZoom={zoom}
            initialCenter={center}
            onZoomChange={setZoom}
            onCenterChange={setCenter}
          />
        </div>

        {/* Controls panel */}
        <aside
          className={`
            w-full md:w-80 flex-shrink-0 overflow-y-auto
            ${showControls ? '' : 'hidden md:block'}
          `}
        >
          <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 h-full">
            <FractalControls
              fractalType={fractalType}
              onFractalTypeChange={handleFractalTypeChange}
              colormap={colormap}
              onColormapChange={setColormap}
              maxIterations={maxIterations}
              onMaxIterationsChange={setMaxIterations}
              zoom={zoom}
              center={center}
              onReset={handleReset}
            />
          </div>
        </aside>
      </div>
    </div>
  );
}
