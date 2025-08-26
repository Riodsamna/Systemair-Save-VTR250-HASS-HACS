"""Modbus parameters for Systemair VTR250 ventilation unit and helper functions. modbus.py"""

from dataclasses import dataclass
from enum import Enum
from pymodbus.client import ModbusTcpClient

# --- ENUMAI ---
class IntegerType(Enum):
    UINT = "UINT"
    INT = "INT"

class RegisterType(Enum):
    Input = "Input"
    Holding = "Holding"

# --- PARAMETRO STRUKTŪRA ---
@dataclass(kw_only=True, frozen=True)
class ModbusParameter:
    register: int
    sig: IntegerType
    reg_type: RegisterType
    short: str
    description: str
    min_value: int | None = None
    max_value: int | None = None
    boolean: bool | None = None
    scale_factor: int | None = None
    combine_with_32_bit: int | None = None

# --- PARAMETRŲ SĄRAŠAS ---
parameters_list = [
    # Demand control
    ModbusParameter(register=1001, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_DEMC_RH_HIGHEST", description="Highest value of all RH sensors", min_value=0, max_value=100),

    # User modes
    ModbusParameter(register=1101, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_HOLIDAY_TIME", description="Holiday mode delay (days)", min_value=1, max_value=365),
    ModbusParameter(register=1102, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_AWAY_TIME", description="Away mode delay (hours)", min_value=1, max_value=72),
    ModbusParameter(register=1103, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_FIREPLACE_TIME", description="Fireplace mode delay (min)", min_value=1, max_value=60),
    ModbusParameter(register=1104, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_REFRESH_TIME", description="Refresh mode delay (min)", min_value=1, max_value=240),
    ModbusParameter(register=1111, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_USERMODE_REMAINING_TIME_L", description="Remaining time L"),
    ModbusParameter(register=1112, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_USERMODE_REMAINING_TIME_H", description="Remaining time H"),
    ModbusParameter(register=1131, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF", description="Manual SAF airflow level", min_value=0, max_value=4),
    ModbusParameter(register=1161, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_USERMODE_MODE", description="Active user mode", min_value=0, max_value=8),
    ModbusParameter(register=1162, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_USERMODE_HMI_CHANGE_REQUEST", description="Requested user mode", min_value=0, max_value=7),

    # Airflow control
    ModbusParameter(register=12401, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_SENSOR_RPM_SAF", description="SAF RPM", min_value=0, max_value=5000),
    ModbusParameter(register=12402, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_SENSOR_RPM_EAF", description="EAF RPM", min_value=0, max_value=5000),
    ModbusParameter(register=14001, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_OUTPUT_SAF", description="SAF speed", min_value=0, max_value=100),
    ModbusParameter(register=14002, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_OUTPUT_EAF", description="EAF speed", min_value=0, max_value=100),

    # Temperature control
    ModbusParameter(register=2001, sig=IntegerType.INT, reg_type=RegisterType.Holding, short="REG_TC_SP", description="Supply air temp setpoint", scale_factor=10, min_value=120, max_value=300),

    # Heater
    ModbusParameter(register=3113, sig=IntegerType.INT, reg_type=RegisterType.Input, short="REG_FUNCTION_ACTIVE_HEATER_COOL_DOWN", description="Heater cool down active", boolean=True),
    ModbusParameter(register=14381, sig=IntegerType.INT, reg_type=RegisterType.Input, short="REG_OUTPUT_TRIAC", description="TRIAC control", boolean=True),
    ModbusParameter(register=2149, sig=IntegerType.INT, reg_type=RegisterType.Input, short="REG_PWM_TRIAC_OUTPUT", description="TRIAC override", min_value=0, max_value=100),
    ModbusParameter(register=14101, sig=IntegerType.INT, reg_type=RegisterType.Input, short="REG_OUTPUT_Y1_ANALOG", description="Heater AO", min_value=0, max_value=100),
    ModbusParameter(register=14102, sig=IntegerType.INT, reg_type=RegisterType.Input, short="REG_OUTPUT_Y1_DIGITAL", description="Heater DO", boolean=True),

    # ECO mode
    ModbusParameter(register=2505, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_ECO_MODE_ON_OFF", description="Eco mode enabled", boolean=True),

    # Filter replacement
    ModbusParameter(register=7005, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_FILTER_REMAINING_TIME_L", description="Filter time L", combine_with_32_bit=7006),
    ModbusParameter(register=7006, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_FILTER_REMAINING_TIME_H", description="Filter time H", combine_with_32_bit=7005),

    # Sensors
    ModbusParameter(register=12102, sig=IntegerType.INT, reg_type=RegisterType.Holding, short="REG_SENSOR_OAT", description="Outdoor temp", scale_factor=10, min_value=-400, max_value=800),
    ModbusParameter(register=12103, sig=IntegerType.INT, reg_type=RegisterType.Holding, short="REG_SENSOR_SAT", description="Supply temp", scale_factor=10, min_value=-400, max_value=800),
    ModbusParameter(register=12105, sig=IntegerType.INT, reg_type=RegisterType.Holding, short="REG_SENSOR_EAT", description="Extract temp", scale_factor=10, min_value=-400, max_value=800),
    ModbusParameter(register=12108, sig=IntegerType.INT, reg_type=RegisterType.Holding, short="REG_SENSOR_OHT", description="Overheat temp", scale_factor=10, min_value=-400, max_value=800),
    ModbusParameter(register=12109, sig=IntegerType.UINT, reg_type=RegisterType.Holding, short="REG_SENSOR_RHS", description="Humidity sensor", min_value=0, max_value=100),

    # Alarms
    ModbusParameter(register=15016, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_FROST_PROT_ALARM", description="Frost protection", min_value=0, max_value=3),
    ModbusParameter(register=15030, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_SAF_RPM_ALARM", description="SAF RPM alarm", min_value=0, max_value=3),
    ModbusParameter(register=15037, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_EAF_RPM_ALARM", description="EAF RPM alarm", min_value=0, max_value=3),
    ModbusParameter(register=15072, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_SAT_ALARM", description="SAT alarm", min_value=0, max_value=3),
    ModbusParameter(register=15086, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_EAT_ALARM", description="EAT alarm", min_value=0, max_value=3),
    ModbusParameter(register=15142, sig=IntegerType.UINT, reg_type=RegisterType.Input, short="REG_ALARM_FILTER_ALARM", description="Filter alarm", min_value=0, max_value=3),
]

         # --- ŽEMĖLAPIAI ---
parameter_map = {param.short: param for param in parameters_list}

operation_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_TC_SP",
        "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_MODE",
        "REG_ECO_MODE_ON_OFF",
        "REG_SENSOR_RPM_SAF",
        "REG_SENSOR_RPM_EAF",
        "REG_OUTPUT_SAF",
        "REG_OUTPUT_EAF",
    ]
}

sensor_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_SENSOR_OAT",
        "REG_SENSOR_SAT",
        "REG_SENSOR_EAT",
        "REG_SENSOR_OHT",
        "REG_SENSOR_RHS",
    ]
}

config_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_USERMODE_HOLIDAY_TIME",
        "REG_USERMODE_AWAY_TIME",
        "REG_USERMODE_FIREPLACE_TIME",
        "REG_USERMODE_REFRESH_TIME",
        "REG_USERMODE_REMAINING_TIME_L",
        "REG_USERMODE_REMAINING_TIME_H",
        "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_HMI_CHANGE_REQUEST",
    ]
}

alarm_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_ALARM_FROST_PROT_ALARM",
        "REG_ALARM_SAF_RPM_ALARM",
        "REG_ALARM_EAF_RPM_ALARM",
        "REG_ALARM_SAT_ALARM",
        "REG_ALARM_EAT_ALARM",
        "REG_ALARM_FILTER_ALARM",
    ]
}

# --- Modbus TCP helperiai Systemair įrenginiui ---
MODBUS_HOST = "192.168.0.60"   # pakeisk į savo IP
MODBUS_PORT = 502

_client = None

def _get_client() -> ModbusTcpClient:
    """Grąžina aktyvų arba sukuria naują Modbus TCP klientą."""
    global _client
    if _client is None:
        _client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    if not _client.connect():
        raise ConnectionError(f"Nepavyko prisijungti prie Modbus serverio {MODBUS_HOST}:{MODBUS_PORT}")
    return _client

def read_holding_register(address: int) -> int:
    """Skaito vieną holding registrą."""
    client = _get_client()
    rr = client.read_holding_registers(address, count=1, slave=1)
    if rr.isError():
        raise IOError(f"Klaida skaitant holding registrą {address}: {rr}")
    return rr.registers[0]

def write_register(address: int, value: int) -> None:
    """Įrašo reikšmę į holding registrą."""
    client = _get_client()
    rq = client.write_register(address, value, slave=1)
    if rq.isError():
        raise IOError(f"Klaida rašant į registrą {address}: {rq}")
