'use client';

import { useRef, useEffect, useState, useCallback } from 'react';
import { getColormap, interpolateColor, type ColormapName, type ColorPalette } from '@/lib/colormaps';

export type FractalType = 'mandelbrot' | 'julia' | 'burning-ship';

interface FractalCanvasProps {
  fractalType?: FractalType;
  colormap?: ColormapName;
  maxIterations?: number;
  initialZoom?: number;
  initialCenter?: { x: number; y: number };
  onZoomChange?: (zoom: number) => void;
  onCenterChange?: (center: { x: number; y: number }) => void;
}

// Julia set constant
const JULIA_C = { re: -0.7, im: 0.27 };

export function FractalCanvas({
  fractalType = 'mandelbrot',
  colormap = 'resonant',
  maxIterations = 100,
  initialZoom = 1,
  initialCenter = { x: -0.5, y: 0 },
  onZoomChange,
  onCenterChange,
}: FractalCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const [zoom, setZoom] = useState(initialZoom);
  const [center, setCenter] = useState(initialCenter);
  const [isDragging, setIsDragging] = useState(false);
  const [lastPos, setLastPos] = useState({ x: 0, y: 0 });
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  // Get color palette
  const palette = useCallback(() => getColormap(colormap, 256), [colormap]);

  // Calculate fractal iteration count
  const calculateIteration = useCallback(
    (px: number, py: number, width: number, height: number): number => {
      // Map pixel to complex plane
      const scale = 3.5 / (zoom * Math.min(width, height));
      const x0 = (px - width / 2) * scale + center.x;
      const y0 = (py - height / 2) * scale + center.y;

      let za: number, zb: number, ca: number, cb: number;

      if (fractalType === 'julia') {
        // Julia: z starts at pixel, c is constant
        za = x0;
        zb = y0;
        ca = JULIA_C.re;
        cb = JULIA_C.im;
      } else {
        // Mandelbrot/Burning Ship: z starts at 0, c is pixel
        za = 0;
        zb = 0;
        ca = x0;
        cb = y0;
      }

      let i = 0;
      while (i < maxIterations) {
        // Burning Ship: take absolute values
        if (fractalType === 'burning-ship') {
          za = Math.abs(za);
          zb = Math.abs(zb);
        }

        // z = z² + c
        const za2 = za * za;
        const zb2 = zb * zb;

        // Escape condition
        if (za2 + zb2 > 4) {
          // Smooth coloring
          const log_zn = Math.log(za2 + zb2) / 2;
          const nu = Math.log(log_zn / Math.log(2)) / Math.log(2);
          return i + 1 - nu;
        }

        // z = z² + c
        zb = 2 * za * zb + cb;
        za = za2 - zb2 + ca;
        i++;
      }

      return -1; // In the set
    },
    [fractalType, zoom, center, maxIterations]
  );

  // Render fractal
  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { width, height } = dimensions;
    canvas.width = width;
    canvas.height = height;

    const imageData = ctx.createImageData(width, height);
    const data = imageData.data;
    const colors = palette();

    for (let py = 0; py < height; py++) {
      for (let px = 0; px < width; px++) {
        const iter = calculateIteration(px, py, width, height);
        const idx = (py * width + px) * 4;

        if (iter < 0) {
          // Point is in the set - black
          data[idx] = 0;
          data[idx + 1] = 0;
          data[idx + 2] = 0;
          data[idx + 3] = 255;
        } else {
          // Color based on iteration count
          const normalized = (iter % maxIterations) / maxIterations;
          const color = interpolateColor(colors, normalized);
          data[idx] = color.r;
          data[idx + 1] = color.g;
          data[idx + 2] = color.b;
          data[idx + 3] = 255;
        }
      }
    }

    ctx.putImageData(imageData, 0, 0);
  }, [dimensions, palette, calculateIteration, maxIterations]);

  // Resize handler
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setDimensions({
          width: Math.floor(rect.width),
          height: Math.floor(rect.height),
        });
      }
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  // Render on state change
  useEffect(() => {
    render();
  }, [render]);

  // Notify parent of changes
  useEffect(() => {
    onZoomChange?.(zoom);
  }, [zoom, onZoomChange]);

  useEffect(() => {
    onCenterChange?.(center);
  }, [center, onCenterChange]);

  // Mouse handlers
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setLastPos({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;

    const dx = e.clientX - lastPos.x;
    const dy = e.clientY - lastPos.y;

    const scale = 3.5 / (zoom * Math.min(dimensions.width, dimensions.height));
    setCenter((prev) => ({
      x: prev.x - dx * scale,
      y: prev.y - dy * scale,
    }));
    setLastPos({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    // Calculate point under mouse in complex plane
    const scale = 3.5 / (zoom * Math.min(dimensions.width, dimensions.height));
    const pointX = (mouseX - dimensions.width / 2) * scale + center.x;
    const pointY = (mouseY - dimensions.height / 2) * scale + center.y;

    // Zoom factor
    const factor = e.deltaY > 0 ? 0.8 : 1.25;
    const newZoom = zoom * factor;

    // Adjust center to zoom towards mouse position
    const newScale = 3.5 / (newZoom * Math.min(dimensions.width, dimensions.height));
    const newCenterX = pointX - (mouseX - dimensions.width / 2) * newScale;
    const newCenterY = pointY - (mouseY - dimensions.height / 2) * newScale;

    setZoom(newZoom);
    setCenter({ x: newCenterX, y: newCenterY });
  };

  // Touch handlers
  const touchRef = useRef<{ x: number; y: number; dist: number } | null>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      const touch = e.touches[0];
      setIsDragging(true);
      setLastPos({ x: touch.clientX, y: touch.clientY });
    } else if (e.touches.length === 2) {
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const dist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
      const cx = (t1.clientX + t2.clientX) / 2;
      const cy = (t1.clientY + t2.clientY) / 2;
      touchRef.current = { x: cx, y: cy, dist };
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    e.preventDefault();

    if (e.touches.length === 1 && isDragging) {
      const touch = e.touches[0];
      const dx = touch.clientX - lastPos.x;
      const dy = touch.clientY - lastPos.y;

      const scale = 3.5 / (zoom * Math.min(dimensions.width, dimensions.height));
      setCenter((prev) => ({
        x: prev.x - dx * scale,
        y: prev.y - dy * scale,
      }));
      setLastPos({ x: touch.clientX, y: touch.clientY });
    } else if (e.touches.length === 2 && touchRef.current) {
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const dist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);

      // Pinch zoom
      const factor = dist / touchRef.current.dist;
      setZoom((prev) => prev * factor);

      touchRef.current.dist = dist;
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    touchRef.current = null;
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full min-h-[300px] bg-black rounded-lg overflow-hidden"
    >
      <canvas
        ref={canvasRef}
        className="w-full h-full cursor-grab active:cursor-grabbing touch-none"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      />

      {/* Zoom overlay */}
      <div className="absolute top-2 left-2 px-2 py-1 bg-black/60 rounded text-xs text-zinc-300 font-mono">
        {zoom.toFixed(2)}x
      </div>

      {/* Fractal type overlay */}
      <div className="absolute top-2 right-2 px-2 py-1 bg-black/60 rounded text-xs text-zinc-300">
        {fractalType === 'mandelbrot' && 'Mandelbrot'}
        {fractalType === 'julia' && 'Julia'}
        {fractalType === 'burning-ship' && 'Burning Ship'}
      </div>
    </div>
  );
}
