import asyncio
import websockets
import json
import logging
from typing import Optional, Callable, Dict, Any
from enum import Enum

class Network(Enum):
    SOLANA = "sol"
    ETHEREUM = "eth"
    BSC = "bsc"
    BASE = "base"
    TRON = "tron"

class DexTracker:
    def __init__(self, max_reconnect_attempts: int = 5, reconnect_delay: float = 1.0):
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.is_reconnecting = False
        self.reconnect_attempts = 0
        self.network: Optional[str] = None
        self.address: Optional[str] = None
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.is_running = False
        
        # Event handlers
        self.on_connected: Optional[Callable] = None
        self.on_trade: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_reconnecting: Optional[Callable] = None
        
        self.logger = logging.getLogger(__name__)

    def set_on_connected(self, handler: Callable[[Dict[str, str]], None]):
        """Set handler for connection events"""
        self.on_connected = handler

    def set_on_trade(self, handler: Callable[[Dict[str, Any]], None]):
        """Set handler for trade events"""
        self.on_trade = handler

    def set_on_error(self, handler: Callable[[Exception], None]):
        """Set handler for error events"""
        self.on_error = handler

    def set_on_disconnected(self, handler: Callable[[Dict[str, Any]], None]):
        """Set handler for disconnection events"""
        self.on_disconnected = handler

    def set_on_reconnecting(self, handler: Callable[[Dict[str, int]], None]):
        """Set handler for reconnection events"""
        self.on_reconnecting = handler

    def is_valid_network(self, network: str) -> bool:
        """Check if network is supported"""
        return network in [n.value for n in Network]

    async def connect(self, address: str, network: str = "tron"):
        """Connect to DexTracker WebSocket API"""
        if not self.is_valid_network(network):
            raise ValueError(f"Unsupported network: {network}")

        self.network = network
        self.address = address
        self.is_running = True

        url = f"wss://api.cryptoscan.pro/dex?network={network}&address={address}"
        
        try:
            self.websocket = await websockets.connect(url)
            self.reconnect_attempts = 0
            
            if self.on_connected:
                self.on_connected({"network": network, "address": address})
            
            await self._listen()
            
        except Exception as e:
            if self.on_error:
                self.on_error(e)
            await self._handle_disconnect()

    async def _listen(self):
        """Listen for incoming messages"""
        try:
            async for message in self.websocket:
                try:
                    trade_data = json.loads(message)
                    if self.on_trade:
                        self.on_trade(trade_data)
                except json.JSONDecodeError as e:
                    if self.on_error:
                        self.on_error(e)
        except websockets.exceptions.ConnectionClosed as e:
            await self._handle_disconnect(e.code, str(e))
        except Exception as e:
            if self.on_error:
                self.on_error(e)
            await self._handle_disconnect()

    async def _handle_disconnect(self, code: Optional[int] = None, reason: str = "Connection closed"):
        """Handle disconnection and attempt reconnection"""
        if self.on_disconnected:
            self.on_disconnected({"code": code, "reason": reason})
        
        if self.is_running and self.reconnect_attempts < self.max_reconnect_attempts:
            await self._reconnect()

    async def _reconnect(self):
        """Attempt to reconnect"""
        if self.is_reconnecting or not self.is_running:
            return
        
        self.is_reconnecting = True
        self.reconnect_attempts += 1
        
        if self.on_reconnecting:
            self.on_reconnecting({"attempt": self.reconnect_attempts})
        
        await asyncio.sleep(self.reconnect_delay)
        
        self.is_reconnecting = False
        await self.connect(self.address, self.network)

    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    def is_connected(self) -> bool:
        """Check if WebSocket is connected"""
        return self.websocket is not None and not self.websocket.closed

    async def run_forever(self):
        """Keep the connection alive"""
        while self.is_running:
            await asyncio.sleep(1)
