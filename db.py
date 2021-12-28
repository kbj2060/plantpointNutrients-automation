import pymysql
from config import db_config

class MysqlController:
    def __init__(self):
        self.conn = pymysql.connect(**db_config, charset='utf8')
        self.curs = self.conn.cursor()

    def insert_switch(self, machine_id: int, status:bool, controlledBy_id: int):
        sql = (f"INSERT INTO switch (machine_id, status, `controlledBy_id`)" 
                f"VALUES (%s, %s, %s)")
        self.curs.execute(sql, (machine_id, status, controlledBy_id))
        self.conn.commit()

    def insert_report(self, lv: str, problem: str):
        sql = (f"INSERT INTO report (level, problem)" 
                f"VALUES (%s, %s)")
        self.curs.execute(sql, (lv, problem))
        self.conn.commit()

    def select_machines(self):
        sql = (f"SELECT machine.id AS machine_id, machine.pin AS machine_pin, machine.name AS machine_name, machine.`createdAt` AS `machine_createdAt`" 
                "FROM machine")
        self.curs.execute(sql)
        return self.curs.fetchall()

    def select_last_switches(self):
        sql = (f"SELECT switch.id AS switch_id, switch.machine_id AS switch_machine_id, switch.status AS switch_status, switch.`controlledBy_id` AS `switch_controlledBy_id`, switch.`createdAt` AS `switch_createdAt`"
                "FROM switch INNER JOIN (SELECT max(switch.id) AS maxid, user.name AS name"
                "FROM switch INNER JOIN user ON user.id = switch.`controlledBy_id`"
                "WHERE user.name = 'auto' GROUP BY switch.machine_id) AS t2 ON switch.id = t2.maxid")
        self.curs.execute(sql)
        return self.curs.fetchall()

    def select_last_automations(self, automation: str):
        sql = f"SELECT {automation}.id AS {automation}_id, {automation}.quantity AS {automation}_quantity, {automation}.`createdAt` AS `{automation}_createdAt` FROM {automation} ORDER BY {automation}.id DESC LIMIT 1"
        self.curs.execute(sql)
        self.conn.commit()
        return self.curs.fetchone()