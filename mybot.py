from aiogram import Dispatcher, executor

from init import dp
import callback, message, payment

##################################################################

callback.register_handlers(dp)
message.register_handlers(dp)
payment.register_handlers(dp)

##################################################################

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

executor.start_polling(dp, on_shutdown=shutdown(dp), skip_updates=True)