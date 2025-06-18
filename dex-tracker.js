const WebSocket = require('ws');
const EventEmitter = require('events');

class DexTracker extends EventEmitter {
  constructor(options = {}) {
    super();
    this.socket = null;
    this.isReconnecting = false;
    this.reconnectAttempts = 0;
    this.network = null;
    this.address = null;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
    this.reconnectDelay = options.reconnectDelay || 1000;
  }

  connect(network, address) {
    if (!['sol', 'eth', 'bsc', 'base', 'tron'].includes(network)) {
      throw new Error('Unsupported network');
    }

    const url = `wss://api.cryptoscan.pro/dex?network=${network}&address=${address}`;
    this.network = network;
    this.address = address;

    this.socket = new WebSocket(url);

    this.socket.on('open', () => {
      this.reconnectAttempts = 0;
      this.emit('connected', { network, address });
    });

    this.socket.on('message', (data) => {
      try {
        const trade = JSON.parse(data);
        this.emit('trade', trade);
      } catch (error) {
        this.emit('error', error);
      }
    });

    this.socket.on('close', (code, reason) => {
      this.emit('disconnected', { code, reason: reason || 'Connection closed' });
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
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
    this.emit('reconnecting', { attempt: this.reconnectAttempts });

    setTimeout(() => {
      this.isReconnecting = false;
      this.connect(this.network, this.address);
    }, this.reconnectDelay);
  }

  isValidNetwork(network) {
    return ['sol', 'eth', 'bsc', 'base', 'tron'].includes(network);
  }
}

module.exports = DexTracker;
