# 🌬️ Systemair Modbus integracija Home Assistant

Ši integracija leidžia prijungti Systemair vėdinimo įrenginį prie Home Assistant per Modbus TCP protokolą.

---

## ⚙️ Funkcionalumas

- 📡 Skaitymas:
  - Tiekiamo oro temperatūra
  - Ištraukiamo oro temperatūra
- 🎛️ Valdymas:
  - Tiekiamo oro temperatūros setpoint
  - Ventiliatoriaus greitis (rankinis režimas)
  - Bypass režimas (įjungti/išjungti)
- 🌡️ Klimato entitetas (beta): leidžia keisti režimus ir temperatūrą

---

## 🛠️ Diegimas

1. Nukopijuokite katalogą `systemair` į `custom_components` katalogą:
/config/custom_components/systemair/

2. Įsitikinkite, kad turite `pymodbus==3.5.2` biblioteką:
```bash
pip install pymodbus==3.5.2
3. Perkraukite Home Assistant.

4. ikite į Settings → Devices & Services → Add Integration ir pasirinkite Systemair Modbus.

5. Įveskite IP adresą ir (jei reikia) Modbus TCP prievadą (numatytas: 502).

🧪 Testavimas
Patikrinkite, ar entitetai atsirado:

sensor.supply_air_temp

number.supply_air_setpoint

switch.bypass

climate.systemair_climate

Naudokite Developer Tools → Services, jei norite testuoti rašymą į registrus.

📚 Naudojami Modbus registrai
Parametras	Registras	Tipas	Skalė	Aprašymas
Tiekiamo oro setpoint	2001	Number	0.1	REG_TC_SP
Ventiliatoriaus greitis	1131	Number	1	REG_USERMODE_MANUAL_AIRFLOW
Bypass režimas	1105	Switch	1	REG_BYPASS_ACTIVATE
Oro temperatūros jutikliai	1001, 1002	Sensor	0.1	REG_TEMP_SUPPLY / REG_TEMP_EXTRACT
🧑‍💻 Autorius
Sukurta su 💙 Lietuvoje. GitHub: @raimis