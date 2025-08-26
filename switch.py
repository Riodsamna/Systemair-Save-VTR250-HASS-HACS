"""Switch platforma Systemair Modbus įrenginio įjungimui/išjungimui. switch.py"""

from datetime import timedelta
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER, HVAC_POWER_COIL
from .api import SystemairAPI

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Sukuria įjungimo/išjungimo switch iš Config Entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entity = SystemairPowerSwitch(api)
    async_add_entities([entity], update_before_add=True)

class SystemairPowerSwitch(SwitchEntity):
    """Systemair įrenginio įjungimo/išjungimo jungiklis."""

    _attr_should_poll = True

    def __init__(self, api: SystemairAPI):
        self._api = api
        self._attr_name = "Systemair Power"
        self._attr_unique_id = "systemair_power"
        self._is_on = False

    async def async_update(self):
        """Skaito įrenginio būseną iš coil."""
        try:
            result = await self._api.read_coil(HVAC_POWER_COIL)
            if result is not None:
                self._is_on = result[0]
                self._attr_is_on = self._is_on
                LOGGER.debug("Systemair Power: %s", self._is_on)
            else:
                self._attr_is_on = False
        except Exception as err:
            self._attr_is_on = False
            LOGGER.error("Klaida skaitant Systemair Power: %s", err)

    async def async_turn_on(self, **kwargs):
        """Įjungia įrenginį."""
        await self._api.write_coil(HVAC_POWER_COIL, True)
        await self.async_update()

    async def async_turn_off(self, **kwargs):
        """Išjungia įrenginį."""
        await self._api.write_coil(HVAC_POWER_COIL, False)
        await self.async_update()