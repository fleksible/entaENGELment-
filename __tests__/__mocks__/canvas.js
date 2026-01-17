/**
 * Canvas 2D Context Mock
 * Provides a mock implementation of the Canvas 2D API for testing
 */

class MockCanvasRenderingContext2D {
  constructor(canvas) {
    this.canvas = canvas;
    this._imageData = null;
  }

  createImageData(width, height) {
    return {
      data: new Uint8ClampedArray(width * height * 4),
      width,
      height
    };
  }

  putImageData(imageData, dx, dy) {
    this._imageData = imageData;
  }

  getImageData(sx, sy, sw, sh) {
    return this.createImageData(sw, sh);
  }

  fillRect(x, y, width, height) {}
  clearRect(x, y, width, height) {}
  strokeRect(x, y, width, height) {}

  beginPath() {}
  closePath() {}
  moveTo(x, y) {}
  lineTo(x, y) {}
  stroke() {}
  fill() {}

  arc(x, y, radius, startAngle, endAngle, counterclockwise) {}
  rect(x, y, width, height) {}

  save() {}
  restore() {}
  translate(x, y) {}
  rotate(angle) {}
  scale(x, y) {}

  fillText(text, x, y, maxWidth) {}
  strokeText(text, x, y, maxWidth) {}
  measureText(text) {
    return { width: text.length * 10 };
  }

  drawImage() {}
}

/**
 * Creates a mock canvas element
 * @param {number} width - Canvas width
 * @param {number} height - Canvas height
 * @returns {Object} Mock canvas element
 */
function createMockCanvas(width = 800, height = 600) {
  const canvas = {
    width,
    height,
    style: {},
    parentElement: {
      clientWidth: width,
      clientHeight: height
    },
    getContext: jest.fn(function(contextType) {
      if (contextType === '2d') {
        return new MockCanvasRenderingContext2D(canvas);
      }
      return null;
    }),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    getBoundingClientRect: jest.fn(() => ({
      left: 0,
      top: 0,
      right: width,
      bottom: height,
      width,
      height
    }))
  };
  return canvas;
}

/**
 * Sets up canvas mocking for document.getElementById
 */
function setupCanvasMock() {
  const mockCanvas = createMockCanvas();

  jest.spyOn(document, 'getElementById').mockImplementation((id) => {
    if (id.includes('canvas') || id === 'fractalCanvas') {
      return mockCanvas;
    }
    return null;
  });

  return mockCanvas;
}

module.exports = {
  MockCanvasRenderingContext2D,
  createMockCanvas,
  setupCanvasMock
};
