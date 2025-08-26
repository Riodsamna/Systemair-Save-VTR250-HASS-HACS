"""Systemair climate platforma su veikimo režimais (preset)."""

from __future__ import annotations
from typing import Optional
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    PRESET_MODES,
    PRESET_REGISTER_READ,
    PRESET_REGISTER_WRITE,
    LOGGER,
)
from .api import SystemairAPI


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Sukuria climate entitetą iš Config Entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 502)

    api = SystemairAPI(host, port)
    await api.connect()

    entity = SystemairClimate(api)
    async_add_entities([entity], update_before_add=True)


class SystemairClimate(ClimateEntity):
    """Systemair ClimateEntity su veikimo režimais."""

    _attr_supported_features = ClimateEntityFeature.PRESET_MODE
    _attr_should_poll = True
    _attr_preset_modes = PRESET_MODES
    _attr_temperature_unit = None  # Nenaudojama

    def __init__(self, api: SystemairAPI):
        self._api = api
        self._attr_name = "Systemair Mode"
        self._attr_unique_id = "systemair_climate"
        self._attr_preset_mode: Optional[str] = None
        self._available = True

    @property
    def available(self) -> bool:
        return self._available

    async def async_update(self) -> None:
        """Atnaujina veikimo režimą iš Modbus."""
        try:
            value = await self._api.read_register(PRESET_REGISTER_READ)
            if value is not None and 0 <= value < len(PRESET_MODES):
                self._attr_preset_mode = PRESET_MODES[value]
                self._available = True
                LOGGER.debug("Preset mode atnaujintas: %s", self._attr_preset_mode)
            else:
                self._available = False
        except Exception as err:
            LOGGER.error("Klaida skaitant preset mode: %s", err)
            self._available = False

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Nustato naują veikimo režimą."""
        if preset_mode in PRESET_MODES:
            idx = PRESET_MODES.index(preset_mode)
            success = await self._api.write_register(PRESET_REGISTER_WRITE, idx)
            if success:
                self._attr_preset_mode = preset_mode
                self.async_write_ha_state()
