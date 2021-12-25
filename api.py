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