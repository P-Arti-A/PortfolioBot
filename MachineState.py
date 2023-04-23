from aiogram.dispatcher.filters.state import State, StatesGroup

# Machine State

class MachineState (StatesGroup):
    About = State()
    Payment = State()
    List = State()
    Excel = State()
    FF = State()