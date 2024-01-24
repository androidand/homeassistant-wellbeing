# api_models.py refactored from api.py
from enum import Enum
from custom_components.wellbeing.const import SENSOR, FAN, BINARY_SENSOR

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE, CONCENTRATION_PARTS_PER_MILLION, \
    CONCENTRATION_PARTS_PER_BILLION, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

FILTER_TYPE = {
    48: "BREEZE Complete air filter",
    51: "CARE Ultimate protect filter",
    64: "Breeze 360 filter",
    96: "Breeze 360 filter",
    99: "Breeze 360 filter",
    192: "FRESH Odour protect filter",
    0: "Filter"
}

class Mode(str, Enum):
    OFF = "PowerOff"
    AUTO = "Auto"
    MANUAL = "Manual"
    UNDEFINED = "Undefined"


class ApplianceEntity:
    entity_type: int = None

    def __init__(self, name, attr, device_class=None) -> None:
        self.attr = attr
        self.name = name
        self.device_class = device_class
        self._state = None

    def setup(self, data):
        self._state = data[self.attr]
        return self

    def clear_state(self):
        self._state = None

    @property
    def state(self):
        return self._state


class ApplianceSensor(ApplianceEntity):
    entity_type: int = SENSOR

    def __init__(self, name, attr, unit="", device_class=None) -> None:
        super().__init__(name, attr, device_class)
        self.unit = unit


class ApplianceFan(ApplianceEntity):
    entity_type: int = FAN

    def __init__(self, name, attr) -> None:
        super().__init__(name, attr)


class ApplianceBinary(ApplianceEntity):
    entity_type: int = BINARY_SENSOR

    def __init__(self, name, attr, device_class=None) -> None:
        super().__init__(name, attr, device_class)

    @property
    def state(self):
        return self._state in ['enabled', True, 'Connected']

class Appliance:
    serialNumber: str
    brand: str
    device: str
    firmware: str
    mode: Mode
    entities: []

    def __init__(self, name, pnc_id, model) -> None:
        self.model = model
        self.pnc_id = pnc_id
        self.name = name

class Appliances:
    def __init__(self, appliances) -> None:
        self.appliances = appliances

    def get_appliance(self, pnc_id):
        return self.appliances.get(pnc_id, None)


    @staticmethod
    def _create_entities(data):
        a7_entities = [
            ApplianceSensor(
                name="eCO2",
                attr='ECO2',
                unit=CONCENTRATION_PARTS_PER_MILLION,
                device_class=SensorDeviceClass.CO2
            ),
            ApplianceSensor(
                name=f"{FILTER_TYPE[data.get('FilterType_1', 0)]} Life",
                attr='FilterLife_1',
                unit=PERCENTAGE
            ),
            ApplianceSensor(
                name=f"{FILTER_TYPE[data.get('FilterType_2', 0)]} Life",
                attr='FilterLife_2',
                unit=PERCENTAGE
            ),
            ApplianceSensor(
                name='State',
                attr='State'
            ),
            ApplianceBinary(
                name='PM Sensor State',
                attr='PMSensState'
            )
        ]

        a9_entities = [
            ApplianceSensor(
                name=f"{FILTER_TYPE.get(data.get('FilterType', 0), 'Filter')} Life",
                attr='FilterLife',
                unit=PERCENTAGE
            ),
            ApplianceSensor(
                name="CO2",
                attr='CO2',
                unit=CONCENTRATION_PARTS_PER_MILLION,
                device_class=SensorDeviceClass.CO2
            ),
        ]

        common_entities = [
            ApplianceFan(
                name="Fan Speed",
                attr='Fanspeed',
            ),
            ApplianceSensor(
                name="Temperature",
                attr='Temp',
                unit=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE
            ),
            ApplianceSensor(
                name="TVOC",
                attr='TVOC',
                unit=CONCENTRATION_PARTS_PER_BILLION
            ),
            ApplianceSensor(
                name="PM1",
                attr='PM1',
                unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                device_class=SensorDeviceClass.PM1
            ),
            ApplianceSensor(
                name="PM2.5",
                attr='PM2_5',
                unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                device_class=SensorDeviceClass.PM25
            ),
            ApplianceSensor(
                name="PM10",
                attr='PM10',
                unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                device_class=SensorDeviceClass.PM10
            ),
            ApplianceSensor(
                name="Humidity",
                attr='Humidity',
                unit=PERCENTAGE,
                device_class=SensorDeviceClass.HUMIDITY
            ),
            ApplianceSensor(
                name="Mode",
                attr='Workmode'
            ),
            ApplianceBinary(
                name="Ionizer",
                attr='Ionizer'
            ),
            ApplianceBinary(
                name="UI Light",
                attr='UILight'
            ),
            ApplianceBinary(
                name="Connection State",
                attr='connectionState',
                device_class=BinarySensorDeviceClass.CONNECTIVITY
            ),
            ApplianceBinary(
                name="Status",
                attr='status'
            ),
            ApplianceBinary(
                name="Safety Lock",
                attr='SafetyLock',
                device_class=BinarySensorDeviceClass.LOCK
            )
        ]

        return common_entities + a9_entities + a7_entities