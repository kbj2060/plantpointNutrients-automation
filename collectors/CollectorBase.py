import asyncio
from api import post_report

class CollectorBase:
    def error_handling(self, point) -> None:
        asyncio.run(post_report(lv=3, problem=f'[Automation] {point}에 문제가 생겼습니다.'))   
        raise Exception(f'[Automation] {point}에 문제가 생겼습니다.')