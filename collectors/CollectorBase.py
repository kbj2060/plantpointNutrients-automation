import asyncio
from api import post_report
from db import MysqlController
from entities.error import CollectorException

class CollectorBase(MysqlController):
    def error_handling(self, point) -> None:
        asyncio.run(post_report(lv=3, problem=f'[Automation] {point}에 문제가 생겼습니다.'))   
        raise CollectorException(f'[Automation] {point}에 문제가 생겼습니다.')