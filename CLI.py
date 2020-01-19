from interface import Interface
from termcolor import colored
from CLIpresentation import CLIPresentation

class CLI(Interface):

    def __init__(self, logic):
        self.presentation = CLIPresentation()
        self.command_colour = "blue"
        self.next_command_text_colour = "red"
        self.logic = logic

        self.COMMANDS = {
            "help": [self.help_command, [], "Prints a list of available commands."],
            "exit": [self.exit_command, [], "Closes this interface."],
            "set": [self.set_course_command, ["course_name"], "Switches to the named course."],
            "course": [self.current_course_command, [], "Prints the name of the current course."]
        }

        self.BASIC_MESSAGE = colored("Please enter your next command: ", self.next_command_text_colour)

    def give_command(self, command):
        split_command = command.split(" ")
        command_name = split_command[0].lower()
        arguments = split_command[1:]

        if command_name in self.COMMANDS.keys():
            arguments_needed = len(self.COMMANDS[command_name][1])
            if len(arguments) != arguments_needed:
                self.wrong_number_of_arguments(command_name, len(arguments), arguments_needed)
            else:
                self.COMMANDS[command_name][0](*arguments)
        else:
            self.unknown_command(command)

    def exit_command(self):
        self.logic.exit_command()

    def help_command(self):
        for key, value in self.COMMANDS.items():
            param_string = "> <".join(value[1])
            if len(param_string) != 0:
                param_string = " <" + param_string + ">"
            self.presentation.tell(colored(key + param_string + ": ", self.command_colour) + value[2])

    def set_course_command(self, course_name):
        old_course = self.logic.course.name if self.logic.course else None
        self.logic.set_course(course_name)
        self.presentation.tell(self.correct_feedback_after_setting_course(self.logic.course, old_course, course_name))

    def correct_feedback_after_setting_course(self, current_course, old_course_name, given_name):
        if current_course:
            if old_course_name:
                if old_course_name != current_course.name:
                    return "Course switched from '" + old_course_name + "' to '" + current_course.name + "'."
                return "Unable to switch to '" + given_name + "', the current course is still '" + current_course.name + "'."
            return "Course set to '" + current_course.name + "'."
        return "Unable to set course to '" + given_name + "'."

    def current_course_command(self):
        if self.logic.course:
            self.presentation.tell("The current course is '" + self.logic.course.name + "'.")
        else:
            self.presentation.tell("No course has been selected.")

    def unknown_command(self, command):
        self.presentation.tell(colored("'" + command + "'", self.command_colour) + " is an unknown command. Type " + colored("'help'", self.command_colour) + " for a list of available commands.")

    def wrong_number_of_arguments(self, command, given_number, correct_number):
        given_arguments = " argument." if given_number == 1 else " arguments."
        correct_arguments = " argument." if correct_number == 1 else " arguments."
        self.presentation.tell("Command " + colored("'" + command + "'", self.command_colour) + " exists, but has " + str(correct_number) + correct_arguments)
        self.presentation.tell("You entered " + str(given_number) + given_arguments)

    def loop(self):
        command = self.presentation.ask(self.BASIC_MESSAGE)
        self.give_command(command)
