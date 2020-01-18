from CLI import CLI
from course import Course

class Logic():
    def __init__(self):
        self.interface = CLI(self)
        self.open = True
        self.course = None

        self.COMMANDS = {
            "exit": self.exit_command
        }

    def run(self):
        while self.open:
            self.interface.loop()

    def exit_command(self):
        self.open = False

    def set_course(self, name):
        course = Course(name)
        if course.exists:
            self.course = course
            return
