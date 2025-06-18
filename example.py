import asyncio
from dex_tracker import DexTracker

async def main():
    tracker = DexTracker()

    # Set event handlers
    def on_trade(trade):
        print(f"New trade: {trade}")

    def on_connected(data):
        print(f"Connected to DexTracker: {data}")

    def on_error(error):
        print(f"DexTracker error: {error}")

    def on_disconnected(data):
        print(f"Disconnected: {data}")

    def on_reconnecting(data):
        print(f"Reconnecting attempt {data['attempt']}")

    tracker.set_on_trade(on_trade)
    tracker.set_on_connected(on_connected)
    tracker.set_on_error(on_error)
    tracker.set_on_disconnected(on_disconnected)
    tracker.set_on_reconnecting(on_reconnecting)

    # Connect to track TRON address
    await tracker.connect('TDxL4V5LE6TYSFXSCWJkkSsCYbgmrDnTer')

    # Optional: Disconnect after 60 seconds
    await asyncio.sleep(60)
    await tracker.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
