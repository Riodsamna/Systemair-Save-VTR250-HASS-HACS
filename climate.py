"""Systemair klimato (beta) platforma. climate.py"""

from homeassistant.components.climate import ClimateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, LOGGER, PRESET_MODES
from .api import SystemairAPI

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entity = SystemairClimate(api)
    async_add_entities([entity], update_before_add=True)

class SystemairClimate(ClimateEntity):
    """Systemair climate entity."""

    _attr_hvac_modes = ["off", "heat", "cool", "auto"]
    _attr_preset_modes = PRESET_MODES
    _attr_should_poll = True
    _attr_temperature_unit = "°C"  # <- pridėta!

    def __init__(self, api: SystemairAPI):
        self._api = api
        self._attr_name = "Systemair Climate"
        self._attr_unique_id = "systemair_climate"
        self._attr_temperature = None
        self._attr_preset_mode = None

    async def async_update(self):
        """Čia skaitoma temperatūra ir režimai iš Modbus."""
        # Pritaikyk pagal savo logiką, pvz., skaityk registrus per api.read_register(...)
        pass

    async def async_set_preset_mode(self, preset_mode: str):
        """Keičia preset režimą."""
        # Rašyk į preset mode register
        pass