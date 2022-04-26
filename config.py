SECTION = 's1'
#ADDRESS = 'http://mudeulro29.iptime.org:9100'
ADDRESS = 'http://127.0.0.1:8000'
MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1883
CLIENT_ID = 'auto'
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
WATER_TANK_MAX_MINUTES = 3
CURRENT_LIMIT = 3500
WATERTANK_HEIGHT = 63 # cm
WATERTANK_LIMIT = WATERTANK_HEIGHT * 0.1
WATERTANK_VOLUMNE = 60000 # ml
NUTRIENT_AMOUNT = WATERTANK_VOLUMNE * 50 / 20000
AUTOMATION_TABLES = ['automation_ac', 'automation_fan', 'automation_rooffan', 'automation_led', 'sprayterm', 'spraytime', 'watersupply', 'nutrientsupply']
DB_CONFIG = {
    "database": "nutrient",
    "user": "root", 
    "port": 3306,
    "password": "01055646565", 
    "host": "127.0.0.1"
}