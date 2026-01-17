/**
 * Web Audio API Mock
 * Provides mock implementations for testing audio-related functionality
 */

class MockAudioParam {
  constructor(defaultValue = 0) {
    this.value = defaultValue;
    this.defaultValue = defaultValue;
  }

  setValueAtTime(value, startTime) {
    this.value = value;
    return this;
  }

  linearRampToValueAtTime(value, endTime) {
    this.value = value;
    return this;
  }

  exponentialRampToValueAtTime(value, endTime) {
    this.value = value;
    return this;
  }

  setTargetAtTime(target, startTime, timeConstant) {
    this.value = target;
    return this;
  }

  cancelScheduledValues(startTime) {
    return this;
  }
}

class MockOscillatorNode {
  constructor(context) {
    this.context = context;
    this.frequency = new MockAudioParam(440);
    this.detune = new MockAudioParam(0);
    this.type = 'sine';
    this._started = false;
    this._stopped = false;
  }

  connect(destination) {
    return destination;
  }

  disconnect() {}

  start(when = 0) {
    this._started = true;
  }

  stop(when = 0) {
    this._stopped = true;
  }
}

class MockGainNode {
  constructor(context) {
    this.context = context;
    this.gain = new MockAudioParam(1);
  }

  connect(destination) {
    return destination;
  }

  disconnect() {}
}

class MockBiquadFilterNode {
  constructor(context) {
    this.context = context;
    this.frequency = new MockAudioParam(350);
    this.Q = new MockAudioParam(1);
    this.gain = new MockAudioParam(0);
    this.type = 'lowpass';
  }

  connect(destination) {
    return destination;
  }

  disconnect() {}
}

class MockDelayNode {
  constructor(context, options = {}) {
    this.context = context;
    this.delayTime = new MockAudioParam(options.delayTime || 0);
  }

  connect(destination) {
    return destination;
  }

  disconnect() {}
}

class MockAudioBuffer {
  constructor(options) {
    this.numberOfChannels = options.numberOfChannels || 2;
    this.length = options.length || 0;
    this.sampleRate = options.sampleRate || 44100;
    this.duration = this.length / this.sampleRate;
    this._channels = [];

    for (let i = 0; i < this.numberOfChannels; i++) {
      this._channels.push(new Float32Array(this.length));
    }
  }

  getChannelData(channel) {
    return this._channels[channel] || new Float32Array(this.length);
  }

  copyFromChannel(destination, channelNumber, startInChannel = 0) {
    const source = this._channels[channelNumber];
    if (source) {
      destination.set(source.subarray(startInChannel, startInChannel + destination.length));
    }
  }

  copyToChannel(source, channelNumber, startInChannel = 0) {
    const dest = this._channels[channelNumber];
    if (dest) {
      dest.set(source, startInChannel);
    }
  }
}

class MockAudioBufferSourceNode {
  constructor(context) {
    this.context = context;
    this.buffer = null;
    this.playbackRate = new MockAudioParam(1);
    this.loop = false;
    this.loopStart = 0;
    this.loopEnd = 0;
    this._started = false;
    this._stopped = false;
  }

  connect(destination) {
    return destination;
  }

  disconnect() {}

  start(when = 0, offset = 0, duration) {
    this._started = true;
  }

  stop(when = 0) {
    this._stopped = true;
  }
}

class MockAudioDestinationNode {
  constructor(context) {
    this.context = context;
    this.maxChannelCount = 2;
    this.numberOfInputs = 1;
    this.numberOfOutputs = 0;
  }
}

class MockAudioContext {
  constructor() {
    this.sampleRate = 44100;
    this.currentTime = 0;
    this.state = 'running';
    this.destination = new MockAudioDestinationNode(this);
  }

  createOscillator() {
    return new MockOscillatorNode(this);
  }

  createGain() {
    return new MockGainNode(this);
  }

  createBiquadFilter() {
    return new MockBiquadFilterNode(this);
  }

  createDelay(maxDelayTime = 1) {
    return new MockDelayNode(this, { delayTime: 0 });
  }

  createBuffer(numberOfChannels, length, sampleRate) {
    return new MockAudioBuffer({ numberOfChannels, length, sampleRate });
  }

  createBufferSource() {
    return new MockAudioBufferSourceNode(this);
  }

  decodeAudioData(audioData) {
    return Promise.resolve(new MockAudioBuffer({
      numberOfChannels: 2,
      length: 44100,
      sampleRate: 44100
    }));
  }

  resume() {
    this.state = 'running';
    return Promise.resolve();
  }

  suspend() {
    this.state = 'suspended';
    return Promise.resolve();
  }

  close() {
    this.state = 'closed';
    return Promise.resolve();
  }
}

/**
 * Sets up Web Audio API mocking on the global window object
 */
function setupWebAudioMock() {
  global.AudioContext = MockAudioContext;
  global.webkitAudioContext = MockAudioContext;
  window.AudioContext = MockAudioContext;
  window.webkitAudioContext = MockAudioContext;
}

module.exports = {
  MockAudioContext,
  MockOscillatorNode,
  MockGainNode,
  MockBiquadFilterNode,
  MockDelayNode,
  MockAudioBuffer,
  MockAudioBufferSourceNode,
  MockAudioParam,
  setupWebAudioMock
};
