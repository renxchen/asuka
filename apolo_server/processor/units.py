class TriggerException(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass

    def __str__(self):
        return self.msg


class FunctionException(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass

    def __str__(self):
        return self.msg
