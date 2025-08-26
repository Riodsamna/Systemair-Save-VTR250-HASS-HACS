"""Switch platforma Systemair Modbus įrenginio įjungimui/išjungimui."""

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

    def __init__(self, api: SystemairAPI):
        self._api = api
        self._attr_name = "Systemair Power"
        self._attr_unique_id = "systemair_power_switch"
        self._attr_is_on = None

    async def async_update(self):
        """Atnaujina būseną iš Modbus coil."""
        try:
            coils = await self._api.read_coil(HVAC_POWER_COIL)
            if coils:
                self._attr_is_on = coils[0]
                LOGGER.debug("Switch atnaujintas: %s", self._attr_is_on)
        except Exception as err:
            LOGGER.error("Nepavyko atnaujinti switch: %s", err)

    async def async_turn_on(self, **kwargs):
        """Įjungia įrenginį."""
        if await self._api.write_coil(HVAC_POWER_COIL, True):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Išjungia įrenginį."""
        if await self._api.write_coil(HVAC_POWER_COIL, False):
            self._attr_is_on = False
            self.async_write_ha_state()
