"""Konstantos Systemair Modbus integracijai. const.py"""

import logging

# Bendras logger objektas integracijai
LOGGER = logging.getLogger(__name__)

# Pagrindiniai duomenys
DOMAIN = "systemair"
LOGGER_NAME = "systemair"

# Veikimo režimai (preset modes)
PRESET_MODES = [
    "Auto",        # 0
    "Manual",      # 1
    "Crowded",     # 2
    "Refresh",     # 3
    "Fireplace",   # 4
    "Away",        # 5
    "Holiday",     # 6
]

# Modbus registrai
PRESET_REGISTER_READ = 1161   # REG_USERMODE_MODE (skaitymas)
PRESET_REGISTER_WRITE = 1162  # REG_USERMODE_HMI_CHANGE_REQUEST (rašymas)

HVAC_POWER_COIL = 21          # Įjungti/išjungti įrenginį

# Temperatūros registrai
OUTDOOR_TEMP_REGISTER = 12102  # REG_SENSOR_OAT
INDOOR_TEMP_REGISTER = 12105   # REG_SENSOR_EAT

# Temperatūros ribos (naudojamos jei norėsi keisti setpoint)
MIN_TEMP = 10
MAX_TEMP = 30

# Atribucija
ATTRIBUTION = "Duomenis pateikė Systemair Modbus"
