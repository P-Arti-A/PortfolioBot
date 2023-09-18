from aiogram.dispatcher.filters.state import State, StatesGroup

# Machine State

class MachineState (StatesGroup):
    Start = State()
    About = State()
    Payment = State()
    List = State()
    Web = State()
    # FF = State()

class MachineState_1 (StatesGroup):
    List_main = State()
    List_create = State()