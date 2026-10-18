/* global jest, beforeEach, afterEach, test, expect */
import { act, createElement } from 'react';
import { createRoot } from 'react-dom/client';
import { FractalCanvas } from '../components/fractalsense/FractalCanvas';

let root;
let host;
let size;
let observers;
let context;

beforeEach(() => {
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  size = { width: 12, height: 8 };
  observers = [];
  globalThis.ResizeObserver = class {
    constructor(callback) {
      this.callback = callback;
      this.observe = jest.fn();
      this.disconnect = jest.fn();
      observers.push(this);
    }
  };
  jest.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(() => size);
  context = {
    createImageData: jest.fn((width, height) => {
      // Match the browser exception that caused the mobile crash.
      if (width <= 0 || height <= 0) throw new DOMException('Zero canvas size', 'IndexSizeError');
      return { data: new Uint8ClampedArray(width * height * 4) };
    }),
    putImageData: jest.fn(),
  };
  jest.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context);
  host = document.createElement('div');
  document.body.appendChild(host);
  root = createRoot(host);
});

afterEach(() => {
  act(() => root.unmount());
  host.remove();
  jest.restoreAllMocks();
  delete globalThis.ResizeObserver;
  delete globalThis.IS_REACT_ACT_ENVIRONMENT;
});

function mount() {
  act(() => root.render(createElement(FractalCanvas, { maxIterations: 2 })));
}

function resize(width, height) {
  size = { width, height };
  act(() => {
    window.dispatchEvent(new Event('resize'));
    for (const observer of observers) observer.callback();
  });
}

test.each([[0, 8], [12, 0], [0, 0], [0.5, 8]])(
  'hidden/subpixel canvas (%s × %s) skips allocation and recovers on show',
  (width, height) => {
    mount();
    context.createImageData.mockClear();
    context.putImageData.mockClear();

    expect(() => resize(width, height)).not.toThrow();
    expect(context.createImageData).not.toHaveBeenCalled();

    // Display changes can happen without a window resize (Controls → Canvas).
    size = { width: 10, height: 6 };
    act(() => {
      for (const observer of observers) observer.callback();
    });
    expect(context.createImageData).toHaveBeenLastCalledWith(10, 6);
    expect(context.putImageData).toHaveBeenCalledTimes(1);
  },
);

test('initially hidden canvas allocates only after becoming visible', () => {
  size = { width: 0, height: 0 };
  expect(mount).not.toThrow();
  expect(context.createImageData).not.toHaveBeenCalled();
  resize(12, 8);
  expect(context.createImageData).toHaveBeenCalledTimes(1);
});

test('observes the container, avoids duplicate renders and disconnects on unmount', () => {
  mount();
  expect(observers).toHaveLength(1);
  expect(observers[0].observe).toHaveBeenCalledWith(host.firstElementChild);
  context.createImageData.mockClear();
  resize(12, 8);
  expect(context.createImageData).not.toHaveBeenCalled();
  act(() => root.unmount());
  expect(observers[0].disconnect).toHaveBeenCalledTimes(1);
});
