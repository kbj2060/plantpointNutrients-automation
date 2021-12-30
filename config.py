from models.AutomationModels import NutrientSupply, SprayTerm, SprayTime, WaterSupply
from models.SwitchModels import LED, Valve, WaterPump

SECTION = 's1/d1'
ADDRESS = 'http://192.168.0.7:8000'
AUTOMATION_SUBJECTS = ['nutrientsupply', 'spraytime', 'sprayterm', 'watersupply']
AUTOMATION_MODELS = [SprayTerm, SprayTime, WaterSupply, NutrientSupply]
MACHINES_MODELS = [Valve, WaterPump, LED]
UNITS = {
    'nutrientsupply': 'mL',
    'watersupply': 'L',
    'spraytime': 'seconds',
    'sprayterm': 'minutes',
}
