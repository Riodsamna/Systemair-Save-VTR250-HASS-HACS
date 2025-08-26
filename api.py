"""API Systemair Modbus integracijai. api.py"""

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from .const import LOGGER

class SystemairAPI:
    def __init__(self, host: str, port: int = 502, unit_id: int = 1):
        self._host = host
        self._port = port
        self._unit_id = unit_id
        self._client: AsyncModbusTcpClient | None = None

    async def connect(self) -> bool:
        """Prisijungia prie Modbus įrenginio."""
        self._client = AsyncModbusTcpClient(self._host, port=self._port)
        connected = await self._client.connect()
        if connected:
            LOGGER.debug("Prisijungta prie Systemair Modbus %s:%s", self._host, self._port)
        else:
            LOGGER.error("Nepavyko prisijungti prie Systemair Modbus %s:%s", self._host, self._port)
        return connected

    async def close(self):
        """Atsijungia nuo Modbus įrenginio."""
        if self._client:
            await self._client.close()
            LOGGER.debug("Atsijungta nuo Systemair Modbus")

    async def read_register(self, register: int) -> int | None:
        """Skaito vieną holding registrą."""
        if not self._client:
            LOGGER.error("Modbus klientas neprisijungęs")
            return None
        try:
            rr = await self._client.read_holding_registers(register, 1, unit=self._unit_id)
            if rr.isError():
                LOGGER.warning("Klaida skaitant registrą %s", register)
                return None
            return rr.registers[0]
        except Exception as err:
            LOGGER.error("Modbus išimtis skaitant registrą %s: %s", register, err)
            return None

    async def write_register(self, register: int, value: int) -> bool:
        """Rašo reikšmę į holding registrą."""
        if not self._client:
            LOGGER.error("Modbus klientas neprisijungęs")
            return False
        try:
            rq = await self._client.write_register(register, value, unit=self._unit_id)
            if rq.isError():
                LOGGER.warning("Klaida rašant į registrą %s", register)
                return False
            LOGGER.debug("Įrašyta %s į registrą %s", value, register)
            return True
        except Exception as err:
            LOGGER.error("Modbus išimtis rašant į registrą %s: %s", register, err)
            return False

    async def read_coil(self, coil: int) -> list[bool] | None:
        """Skaito coil būseną."""
        if not self._client:
            LOGGER.error("Modbus klientas neprisijungęs")
            return None
        try:
            rr = await self._client.read_coils(coil, 1, unit=self._unit_id)
            if rr.isError():
                LOGGER.warning("Klaida skaitant coil %s", coil)
                return None
            return rr.bits
        except Exception as err:
            LOGGER.error("Modbus išimtis skaitant coil %s: %s", coil, err)
            return None

    async def write_coil(self, coil: int, value: bool) -> bool:
        """Rašo į coil būseną."""
        if not self._client:
            LOGGER.error("Modbus klientas neprisijungęs")
            return False
        try:
            rq = await self._client.write_coil(coil, value, unit=self._unit_id)
            if rq.isError():
                LOGGER.warning("Klaida rašant į coil %s", coil)
                return False
            LOGGER.debug("Įrašyta %s į coil %s", value, coil)
            return True
        except Exception as err:
            LOGGER.error("Modbus išimtis rašant į coil %s: %s", coil, err)
            return False