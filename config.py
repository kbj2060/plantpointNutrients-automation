from models.AutomationModels import NutrientSupply, SprayTerm, SprayTime, WaterSupply
from models.SensorModels import DHT22, Current, WaterLevel
from models.SwitchModels import LED, Valve, WaterPump

SECTION = 's1/d1'
# ADDRESS = 'http://192.168.0.7:8000'
ADDRESS = 'http://127.0.0.1:8000'
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
