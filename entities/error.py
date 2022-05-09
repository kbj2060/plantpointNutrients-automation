class UnknownException(Exception):
    pass

class SprayExcpetion(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return f"[스프레이 오류] {self.msg}"

class WaterException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return f"[물공급 오류] {self.msg}"

class CollectorException(Exception):
    def __init__(self, msg):
        self.msg = msg
        logger.error(msg)
    
    def __str__(self):
        return f"[정보 수집 오류] {self.msg}"
