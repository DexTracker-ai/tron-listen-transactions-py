# DexTracker Client

A Node.js library for listening to real-time DEX transactions using the DexTracker API.

## Installation

```bash
npm install ws
```

## Usage

```javascript
const DexTracker = require('./dex-tracker');

const tracker = new DexTracker();

tracker.on('trade', (trade) => {
  console.log('New trade:', trade);
});

tracker.connect('4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R');
```

## API

### Methods

- `connect(network, address)` - Connect to track trades for a specific token
- `disconnect()` - Close the connection
- `isConnected()` - Check connection status

### Events

- `connected` - Fired when connection is established
- `trade` - Fired when a new trade is received
- `error` - Fired when an error occurs
- `disconnected` - Fired when connection is lost
- `reconnecting` - Fired during reconnection attempts

### Supported Networks

- `sol` - Solana
- `eth` - Ethereum
- `bsc` - Binance Smart Chain
- `base` - Base
- `tron` - Tron

## Trade Data Structure

```javascript
{
  type: 'buy' | 'sell',
  network: 'sol' | 'eth' | 'bsc' | 'base' | 'tron',
  volume: number, // USD amount
  price: number,  // USD price
  exchange: string,
  txn: string,    // Transaction ID
  walletAddress: string,
  pool: string    // Pool address
}
```
