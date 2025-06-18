const WebSocket = require('ws');
const EventEmitter = require('events');

class DexTracker extends EventEmitter {
  constructor(options = {}) {
    super();
    this.socket = null;
    this.isReconnecting = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
    this.reconnectTimeout = options.reconnectTimeout || 5000;
  }

  connect(network, address) {
    if (!['sol', 'eth', 'bsc', 'base', 'tron'].includes(network)) {
      throw new Error('Unsupported network');
    }

    const url = `wss://api.dextracker.com/ws/${network}/${address}`;

    this.socket = new WebSocket(url);

    this.socket.on('open', () => {
      this.reconnectAttempts = 0;
      this.emit('connected');
    });

    this.socket.on('message', (data) => {
      try {
        const trade = JSON.parse(data);
        this.emit('trade', trade);
      } catch (error) {
        this.emit('error', error);
      }
    });

    this.socket.on('close', (hadError) => {
      this.emit('disconnected');
      if (!hadError && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnect();
      }
    });

    this.socket.on('error', (error) => {
      this.emit('error', error);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  isConnected() {
    return this.socket !== null && this.socket.readyState === WebSocket.OPEN;
  }

  reconnect() {
    if (this.isReconnecting) return;
    
    this.isReconnecting = true;
    this.reconnectAttempts++;
    this.emit('reconnecting', this.reconnectAttempts);

    setTimeout(() => {
      this.isReconnecting = false;
      this.connect(this.network, this.address);
    }, this.reconnectTimeout);
  }
}

module.exports = DexTracker;
