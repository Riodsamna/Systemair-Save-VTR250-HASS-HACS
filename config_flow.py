"""Systemair Modbus konfigūracijos vedlys. config_flow.py"""

from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN, LOGGER

DEFAULT_PORT = 502

class SystemairConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Systemair konfigūracijos vedlys."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Pirmas žingsnis – vartotojo įvestis."""
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            port = user_input["port"]

            # Galima pridėti testą, ar įrenginys pasiekiamas
            LOGGER.debug("Bandome prisijungti prie Systemair įrenginio %s:%s", host, port)

            return self.async_create_entry(title=host, data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("port", default=DEFAULT_PORT): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SystemairOptionsFlowHandler(config_entry)


class SystemairOptionsFlowHandler(config_entries.OptionsFlow):
    """Papildomų nustatymų vedlys (jei reikės ateityje)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Pradinis žingsnis – kol kas tuščias."""
        return self.async_create_entry(title="", data={})
