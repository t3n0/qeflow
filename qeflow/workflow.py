
from qeflow.logger import Logger


class Workflow(object):
    def __init__(self, inputs, logger = Logger()) -> None:
        self.logger = logger  

    def saveToFile(self):
        pass
