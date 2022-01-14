import requests
from config import ADDRESS


async def get_last_automations(label):
    response = requests.post(
        f"{ADDRESS}/{label}",
        json={ 'data': { 'limit': 1 } }
    )
    return response.json()[0]

async def get_last_switches():
    response = requests.post(
        f"{ADDRESS}/switch",
        json={ 'data': { 'autoEachLast': True }}
    )
    return response.json()

async def get_machines():
    response = requests.get(f"{ADDRESS}/machines")
    return response.json()

async def get_sensors():
    response = requests.get(f"{ADDRESS}/sensor")
    return response.json()
    
async def get_last_automation_date(subject, isCompleted):
    response = requests.post(f"{ADDRESS}/automation_history", json={ 'data': { 'subject__eq': subject, 'isCompleted': isCompleted }})
    return response.json()

async def post_automation_history(subject, start, isCompleted):
    requests.post(
        f"{ADDRESS}/automation_history/create", 
        json={ 'data': { 
                    'subject': subject, 
                    'start': start,
                    'isCompleted': isCompleted 
                }
            }
        )

async def post_report(lv, problem):
    requests.post(
        f"{ADDRESS}/report/create",
        json={ 'data': { 'level': lv, 'problem': problem } }
    )

async def post_switch(name, machine_id, status, controlledBy):
    requests.post(
        f"{ADDRESS}/switch/create",
        json={ 'data': { 'name': name, 'machine_id': machine_id, 'status': status, 'controlledBy': controlledBy } }
    )

async def post_temperature(value):
    requests.post(
        f"{ADDRESS}/temperature/create",
        json={ 'data': { 'value': value } }
    )

async def post_humidity(value):
    requests.post(
        f"{ADDRESS}/humidity/create",
        json={ 'data': { 'value': value } }
    )
