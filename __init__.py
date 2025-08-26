"""Systemair Modbus integracijos paleidimas Home Assistant'e."""

from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Tik reikalingos platformos
PLATFORMS: list[str] = ["switch", "climate", "sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Įkelia Systemair platformas iš Config Entry."""
    _LOGGER.debug("Systemair integracija paleidžiama: %s", entry.data)
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Pašalina Systemair platformas."""
    _LOGGER.debug("Systemair integracija šalinama")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
