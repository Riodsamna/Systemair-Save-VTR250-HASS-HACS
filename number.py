"""Systemair Modbus skaitiniai parametrai: temperatūros ir ventiliatoriaus setpoint'ai. number.py"""

from datetime import timedelta
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER, MIN_TEMP, MAX_TEMP
from .api import SystemairAPI

SCAN_INTERVAL = timedelta(seconds=30)

# Registrai
SUPPLY_TEMP_REGISTER = 2001  # REG_TC_SP
FAN_SPEED_REGISTER = 1131    # REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Sukuria skaitinius entitetus iš Config Entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entities = [
        SystemairNumber(api, "Supply Air Setpoint", SUPPLY_TEMP_REGISTER, "°C", MIN_TEMP, MAX_TEMP, 0.1),
        SystemairNumber(api, "Fan Speed Level", FAN_SPEED_REGISTER, "", 0, 4, 1),
    ]

    async_add_entities(entities, update_before_add=True)


class SystemairNumber(NumberEntity):
    """Systemair Modbus skaitinis entitetas."""

    _attr_should_poll = True

    def __init__(
        self,
        api: SystemairAPI,
        name: str,
        register: int,
        unit: str,
        min_value: float,
        max_value: float,
        scale: float,
    ):
        self._api = api
        self._register = register
        self._scale = scale

        self._attr_name = name
        self._attr_unique_id = f"systemair_number_{register}"
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_value = None

    async def async_update(self):
        """Skaito dabartinę reikšmę iš Modbus registro."""
        try:
            value = await self._api.read_register(self._register)
            if value is not None:
                self._attr_native_value = value * self._scale
                LOGGER.debug("Atnaujinta %s: %.1f%s", self._attr_name, self._attr_native_value, self._attr_native_unit_of_measurement)
        except Exception as err:
            LOGGER.error("Klaida skaitant %s: %s", self._attr_name, err)

    async def async_set_native_value(self, value: float):
        """Nustato naują reikšmę į Modbus registrą."""
        scaled = int(value / self._scale)
        success = await self._api.write_register(self._register, scaled)
        if success:
            self._attr_native_value = value
            self.async_write_ha_state()
