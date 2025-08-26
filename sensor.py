"""Systemair temperatūros jutikliai: išorės ir vidaus. sensor.py"""

from datetime import timedelta
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER, OUTDOOR_TEMP_REGISTER, INDOOR_TEMP_REGISTER
from .api import SystemairAPI

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Sukuria temperatūros jutiklius iš Config Entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entities = [
        SystemairTemperatureSensor(api, "Outdoor Temperature", OUTDOOR_TEMP_REGISTER),
        SystemairTemperatureSensor(api, "Indoor Temperature", INDOOR_TEMP_REGISTER),
    ]

    async_add_entities(entities, update_before_add=True)

class SystemairTemperatureSensor(SensorEntity):
    """Systemair temperatūros jutiklis."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "°C"
    _attr_should_poll = True

    def __init__(self, api: SystemairAPI, name: str, register: int):
        self._api = api
        self._register = register
        self._attr_name = name
        self._attr_unique_id = f"systemair_temp_{register}"
        self._attr_native_value = None
        self._available = True

    async def async_update(self) -> None:
        """Skaito temperatūrą iš Modbus registro."""
        try:
            value = await self._api.read_register(self._register)
            if value is not None:
                self._attr_native_value = value / 10.0
                self._available = True
                LOGGER.debug("Temperatūra %s: %.1f°C", self._attr_name, self._attr_native_value)
            else:
                self._available = False
        except Exception as err:
            self._available = False
            LOGGER.error("Klaida skaitant temperatūrą %s: %s", self._attr_name, err)