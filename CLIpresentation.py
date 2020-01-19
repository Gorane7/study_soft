
class CLIPresentation():
    def __init__(self):
        print("Welcome to the basic command line interface.")

    def tell(self, msg):
        print(msg)

    def ask(self, inp_msg):
        return input(inp_msg)
