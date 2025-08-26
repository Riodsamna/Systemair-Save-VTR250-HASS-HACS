"""Binary sensor platform for Systemair Modbus. binary_sensor.py"""

from datetime import timedelta
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, LOGGER
from .api import SystemairAPI

SCAN_INTERVAL = timedelta(seconds=30)

BINARY_SENSOR_TYPES = [
    {
        "name": "Filter Alarm",
        "coil": 10,
        "device_class": BinarySensorDeviceClass.PROBLEM,
    },
    {
        "name": "Unit Running",
        "coil": 11,
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up binary sensors from a config entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entities = [
        SystemairBinarySensor(api, sensor["name"], sensor["coil"], sensor["device_class"])
        for sensor in BINARY_SENSOR_TYPES
    ]

    async_add_entities(entities, update_before_add=True)


class SystemairBinarySensor(BinarySensorEntity):
    """Representation of a Systemair Modbus binary sensor."""

    def __init__(self, api, name, coil, device_class):
        self._api = api
        self._attr_name = f"Systemair {name}"
        self._coil = coil
        self._attr_device_class = device_class
        self._attr_unique_id = f"systemair_coil_{coil}"
        self._attr_is_on = None

    async def async_update(self):
        """Fetch new state data from the Modbus device."""
        try:
            coils = await self._api.read_coil(self._coil)
            if coils:
                self._attr_is_on = coils[0]
                LOGGER.debug("Updated %s: %s", self._attr_name, self._attr_is_on)
        except Exception as err:
            LOGGER.error("Failed to update %s: %s", self._attr_name, err)
