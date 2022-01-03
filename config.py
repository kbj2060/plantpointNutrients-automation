SECTION = 's1/d1'
ADDRESS = 'http://192.168.0.7:8000'
#ADDRESS = 'http://127.0.0.1:8000'

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
