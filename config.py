SECTION = 's1/d1'
ADDRESS = 'http://mudeulro29.iptime.org:9100'
#ADDRESS = 'http://127.0.0.1:8000'

UNITS = {
    'nutrientsupply': 'mL',
    'watersupply': 'L',
    'spraytime': 'seconds',
    'sprayterm': 'minutes',
}
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

CURRENT_LIMIT = 3500
WATERTANK_HEIGHT = 63 # cm
WATERTANK_LIMIT = WATERTANK_HEIGHT * 0.1
WATERTANK_VOLUMNE = 60000 # ml
NUTRIENT_AMOUNT = WATERTANK_VOLUMNE * 50 / 20000
