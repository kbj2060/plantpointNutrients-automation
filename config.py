from models.AutomationModels import NutrientSupply, SprayTerm, SprayTime, WaterSupply
from models.SensorModels import DHT22, Current, WaterLevel
from models.SwitchModels import LED, Valve, WaterPump

SECTION = 's1/d1'
ADDRESS = 'http://mudeulro29.iptime.org:9100'
# ADDRESS = 'http://127.0.0.1:8000'
AUTOMATION_SUBJECTS = ['nutrientsupply', 'spraytime', 'sprayterm', 'watersupply']
AUTOMATION_MODELS = [SprayTerm, SprayTime, WaterSupply, NutrientSupply]
SENSOR_MODELS = [Current, WaterLevel, DHT22]
MACHINES_MODELS = [Valve, WaterPump, LED]
UNITS = {
    'nutrientsupply': 'mL',
    'watersupply': 'L',
    'spraytime': 'seconds',
    'sprayterm': 'minutes',
}
CSPIN = 8
MISOPIN = 9
MOSIPIN = 10
CLOCKPIN = 11

WATERTANK_HEIGHT = 63 # cm
WATERTANK_VOLUMNE = 60000 # ml
NUTRIENT_AMOUNT = WATERTANK_VOLUMNE * 50 / 20000
