# DexTracker Client

A Python library for listening to real-time DEX transactions using the DexTracker API.

## Installation

```bash
pip install websockets
```

## Usage

```python
import asyncio
from dex_tracker import DexTracker

async def main():
    tracker = DexTracker()

    def on_trade(trade):
        print(f"New trade: {trade}")

    tracker.set_on_trade(on_trade)
    await tracker.connect('TDxL4V5LE6TYSFXSCWJkkSsCYbgmrDnTer')

if __name__ == "__main__":
    asyncio.run(main())
```

## API

### Methods

- `connect(address, network='tron')` - Connect to track trades for a specific token
- `disconnect()` - Close the connection
- `is_connected()` - Check connection status
- `is_valid_network(network)` - Check if network is supported

### Event Handlers

Set event handlers using these methods:
- `set_on_connected(handler)` - Called when connection is established
- `set_on_trade(handler)` - Called when a new trade is received
- `set_on_error(handler)` - Called when an error occurs
- `set_on_disconnected(handler)` - Called when connection is lost
- `set_on_reconnecting(handler)` - Called during reconnection attempts

### Supported Networks

- `sol` - Solana
- `eth` - Ethereum
- `bsc` - Binance Smart Chain
- `base` - Base
- `tron` - Tron

## Trade Data Structure

```python
{
    'type': 'buy' | 'sell',
    'network': 'sol' | 'eth' | 'bsc' | 'base' | 'tron',
    'volume': float,  # USD amount
    'price': float,   # USD price
    'exchange': str,
    'txn': str,       # Transaction ID
    'walletAddress': str,
    'pool': str       # Pool address
}
```
