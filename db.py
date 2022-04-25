import pymysql
from config import DB_CONFIG

class MysqlController:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG, charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_user_id(self, user_id: int):
        sql = (f"SELECT * FROM user WHERE name = \"{user_id}\";")
        self.curs.execute(sql)
        return self.curs.fetchone()

    def insert_switch(self, machine_id: int, status:bool, controlledBy: str):
        user_id = self.get_user_id(controlledBy)['id']
        sql = (f"INSERT INTO switch VALUES (NULL, {machine_id}, {status}, {user_id}, NULL);")
        self.curs.execute(sql)
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
        sql = (f"SELECT switch.id AS switch_id, switch.machine_id AS switch_machine_id, switch.status AS switch_status, switch.`controlledBy_id` AS `switch_controlledBy_id`, switch.`createdAt` AS `switch_createdAt` FROM switch INNER JOIN (SELECT max(switch.id) AS maxid, user.name AS name FROM switch INNER JOIN user ON user.id = switch.`controlledBy_id` WHERE user.name = 'auto' GROUP BY switch.machine_id) AS t2 ON switch.id = t2.maxid")
        self.curs.execute(sql)
        return self.curs.fetchall()

    def select_last_automations(self, automation: str):
        sql = f"SELECT {automation}.id AS {automation}_id, {automation}.quantity AS {automation}_quantity, {automation}.`createdAt` AS `{automation}_createdAt` FROM {automation} ORDER BY {automation}.id DESC LIMIT 1"
        self.curs.execute(sql)
        self.conn.commit()
        return self.curs.fetchone()

    def select_ac_automation(self):
        sql = (f"SELECT automation_ac.id AS id, automation_ac.start AS start, automation_ac.end AS end, automation_ac.active AS active, automation_ac.`createdAt` AS `createdAt` FROM automation_ac ORDER BY automation_ac.id DESC LIMIT 1")
        self.curs.execute(sql)
        return self.curs.fetchone()

    def select_led_automation(self):
        sql = (f"SELECT automation_led.id AS id, automation_led.start AS start, automation_led.end AS end, automation_led.active AS active, automation_led.`createdAt` AS `createdAt` FROM automation_led ORDER BY automation_led.id DESC LIMIT 1")
        self.curs.execute(sql)
        return self.curs.fetchone()

    def select_fan_automation(self):
        sql = (f"SELECT automation_fan.id AS id, automation_fan.term AS term, automation_fan.active AS active, automation_fan.`createdAt` AS `createdAt` FROM automation_fan ORDER BY automation_fan.id DESC LIMIT 1")
        self.curs.execute(sql)
        return self.curs.fetchone()

    def select_rooffan_automation(self):
        sql = (f"SELECT automation_rooffan.id AS id, automation_rooffan.term AS term, automation_rooffan.active AS active, automation_rooffan.`createdAt` AS `createdAt` FROM automation_rooffan ORDER BY automation_rooffan.id DESC LIMIT 1")
        self.curs.execute(sql)
        return self.curs.fetchone()

    def select_current_state(self, _machine):
        sql = (f"SELECT switch.id AS id, switch.machine_id AS machine_id, switch.status AS status, switch.`controlledBy_id` AS `controlledBy_id`, switch.`createdAt` AS `createdAt` FROM switch INNER JOIN (SELECT max(switch.id) AS maxid FROM switch INNER JOIN machine ON machine.id = switch.`machine_id` WHERE machine.name = '{_machine}' GROUP BY switch.machine_id) AS t2 ON switch.id = t2.maxid")
        self.curs.execute(sql)
        return self.curs.fetchone()