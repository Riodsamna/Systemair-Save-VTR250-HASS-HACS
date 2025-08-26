"""Modbus parameters for Systemair VTR250 ventilation unit and helper functions. modbus_device.py"""
from __future__ import annotations

from .api import SystemairAPI


class MyModbusDevice:
    """Adapteris, suderinantis ankstesnį MyModbusDevice pavadinimą su esamu SystemairAPI."""

    def __init__(self, host: str, port: int = 502) -> None:
        self._api = SystemairAPI(host, port)

    async def connect(self) -> None:
        """Užmezga ryšį, jei API turi connect metodą."""
        connect = getattr(self._api, "connect", None)
        if callable(connect):
            await connect()

    async def close(self) -> None:
        """Uždaro ryšį, jei API turi close/disconnect metodą."""
        close = getattr(self._api, "close", None) or getattr(self._api, "disconnect", None)
        if callable(close):
            await close()

    async def read_register(self, address: int):
        """Skaito vieną registro reikšmę per API."""
        if not hasattr(self._api, "read_register"):
            raise NotImplementedError("SystemairAPI neturi read_register metodo")
        return await self._api.read_register(address)

    async def write_register(self, address: int, value: int):
        """Rašo į registrą, jei API tai palaiko."""
        write = getattr(self._api, "write_register", None)
        if not callable(write):
            raise NotImplementedError("SystemairAPI neturi write_register metodo")
        return await write(address, value)

    async def read_coil(self, address: int):
        """Skaito coil, jei API tai palaiko; priešingu atveju grąžina None."""
        read = getattr(self._api, "read_coil", None)
        if callable(read):
            return await read(address)
        return None

    async def write_coil(self, address: int, value: bool):
        """Rašo coil, jei API tai palaiko."""
        write = getattr(self._api, "write_coil", None)
        if not callable(write):
            raise NotImplementedError("SystemairAPI neturi write_coil metodo")
        return await write(address, value)
