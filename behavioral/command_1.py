# command, a behavioral design pattern
# reference: https://medium.com/@rrfd/strategy-and-command-design-patterns-wizards-and-sandwiches-applications-in-python-d1ee1c86e00f
import abc


class Command(metaclass=abc.ABCMeta):
    """
    The command interface that declares a method (execute) for a particular
    action.
    """
    @abc.abstractmethod
    def execute(self):
        pass


class Sandwich:
    """
    The receiver class, which holds the specifc method to be called to
    perform the specific action.
    This will be called by the Invoker object.
    """

    def make_sandwich(self):
        print("A sandwich is being made")


class Salad:
    """
    The receiver class, which holds the specific method to be called.
    This will be called by the Invoker object.
    """

    def make_salad(self):
        print("A salad is being made")


class Taco:
    """
    The receiver class, which holds the specific method to be called.
    This will be called by the Invoker object.
    """

    def make_taco(self):
        print("A taco is being made")


class SandwichCommand(Command):
    """
    A concrete / specific Command class, implementing exectue()
    which calls a specific or an appropriate action of a method
    from a Receiver class.
    Args:
        lunch (Lunch): Receiver class to be attached to the command
    """

    def __init__(self, sandwich: Sandwich):
        self._sandwich = sandwich

    def execute(self):
        self._sandwich.make_sandwich()


class SaladCommand(Command):
    def __init__(self, salad: Salad):
        self._salad = salad

    def execute(self):
        self._salad.make_salad()


class TacoCommand(Command):
    def __init__(self, taco: Taco):
        self._taco = taco

    def execute(self):
        self._taco.make_taco()


class MealInvoker:
    """
    Has a reference to the Command, and can execute the method.
    Notice how the command.execute() is never directly called,
    but always through the invoker.
    The action invoked is decoupled from the action performed
    by the Receiver.
    The Invoker (self) invokes a Command (LunchCommand),
    and the Command executes the appropriate action (command.execute())
    """

    def __init__(self, command: Command):
        self._command = command
        self._command_list = []  # type: List[Command]

    def set_command(self, command: Command):
        self.command = command

    def get_command(self):
        print(self.command.__class__.__name__)

    def add_command_to_list(self, command: Command):
        self._command_list.append(command)

    def execute_commands(self):
        """
        Execute all the saved commands, then empty the list.
        """
        for cmd in self._command_list:
            cmd.execute()

        self._command_list.clear()

    def invoke(self):
        self._command.execute()