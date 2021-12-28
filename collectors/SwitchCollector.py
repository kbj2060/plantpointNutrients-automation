import asyncio
from api import get_last_switches, get_machines, post_report, post_switch
from models.SwitchModels import SwitchBase
from config import MACHINES_MODELS
from utils import get_arr_diffs


class SwitchCollector:
    def _classify_machine_model(self, switches: dict, machines: dict) -> SwitchBase:
        results = {}
        for machine in machines:
            found_switch = next(s for s in switches if s['machine_id'] == machine['id'])
            m_object = next(m for m in MACHINES_MODELS if m.get_name() in machine['name'])
            m_object = m_object(**machine)
            m_object.set_switch_info(status=found_switch['status'], poweredAt=found_switch['createdAt'])
            results[m_object.name] = m_object
        return results

    def _get_machines(self):
        machines = asyncio.run(get_machines())
        return sorted(machines, key=lambda k: k['id'])

    def _get_switches(self):
        switches = asyncio.run(get_last_switches())
        return sorted(switches, key=lambda k: k['machine_id'])

    async def post_excepted_switch(self, name, machine_id):
        asyncio.run(
                    post_switch(
                        name=name,
                        machine_id=machine_id,
                        status=0,
                        controlledBy='auto'
                    )
                )

    def get(self):
        machines = self._get_machines()
        switches = self._get_switches()
        if not (len(machines) == len(switches)):
            try:
                machine_ids = [ machine['id'] for machine in machines]
                switch_machine_id = [ _switch['machine_id'] for _switch in switches]
                diffs = get_arr_diffs(machine_ids, switch_machine_id)
                for diff_machine_id in diffs:
                    name = next(item for item in machines if item['id'] == diff_machine_id)['name']
                    self.post_excepted_switch(name=name, machine_id=diff_machine_id)
                    print(f'Machine과 Switch가 맞지 않아 {name}에 OFF를 명령했습니다.')
            except:
                self.error_handling('Machine과 Switches 데이터 검증')
        switch_models = self._classify_machine_model(switches=switches, machines=machines)
        return switch_models