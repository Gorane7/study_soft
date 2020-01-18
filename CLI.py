from interface import Interface
from termcolor import colored

class CLI(Interface):

    def __init__(self, brain):
        print("Welcome to the basic command line interface.")
        self.command_colour = "blue"
        self.next_command_text_colour = "red"
        self.brain = brain

        self.COMMANDS = {
            "help": [self.help_command, [], "Prints a list of available commands."],
            "exit": [self.exit_command, [], "Closes this interface."],
            "set": [self.set_course_command, ["course_name"], "Switches to the named course."]
        }
        self.BASIC_MESSAGE = colored("Please enter your next command: ", self.next_command_text_colour)

    def give_command(self, command):
        command_lower = command.lower()
        split_command = command_lower.split(" ")
        if split_command[0] in self.COMMANDS.keys():
            if len(split_command) - 1 != len(self.COMMANDS[split_command[0]][1]):
                self.wrong_number_of_arguments(split_command[0], len(split_command[1:], len(self.COMMANDS[split_command[0][1]])))
            else:
                self.COMMANDS[command_lower][0](*split_command[1:])
        else:
            self.unknown_command(command)

    def exit_command(self):
        self.brain.exit_command()

    def help_command(self):
        for key, value in self.COMMANDS.items():
            param_string = "> <".join(value[1])
            if len(param_string) != 0:
                param_string = " <" + param_string + ">"
            print(colored(key + param_string + ": ", self.command_colour) + value[2])
        self.command_to_brain = None

    def set_course_command(self, course_name):
        pass

    def unknown_command(self, command):
        print(colored("'" + command + "'", self.command_colour) + " is an unknown command. Type " + colored("'help'", self.command_colour) + " for a list of available commands.")

    def wrong_number_of_arguments(self, command, given_number, correct_number):
        print("Command " + colored("'" + command + "'", self.command_colour) + " exists, but has " + str(correct_number) + " arguments.")
        print("You entered " + str(given_number) + " arguments.")

    def loop(self):
        command = input(self.BASIC_MESSAGE)
        self.give_command(command)
