from abc import ABC, abstractmethod

class Interface(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def give_command(self, command, *args):
        pass
