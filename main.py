
from apscheduler.schedulers.asyncio import AsyncIOScheduler



from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from config import TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import random
import asyncio
import time
from aiogram.dispatcher import FSMContext
from keyboards import b1,b2,b3,ib1,ib2,b5,b6

from aiogram.utils.helper import Helper, HelperMode, ListItem
bot=Bot(TOKEN)
storage=MemoryStorage()
dp=Dispatcher(bot=bot, storage=storage)

async def shutdown(dp):
    await storage.close()
    await bot.close()


class Timer(StatesGroup):
    promez=State()
    napom=State()


stop=''

def get_cancel()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(b2)

    return kb

def get_kb()->ReplyKeyboardMarkup:
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(b3).add(b1)
    return kb

scheduler=AsyncIOScheduler()



data=0

@dp.message_handler(commands='start')
async def schedul(msg:types.Message):
    await msg.answer('Hi',reply_markup=get_kb())


@dp.message_handler(commands=['timer'],state=None)
async def cmd_create(message: types.Message):
    await message.reply('Отправь промежуток между сообщениями в секундах',reply_markup=get_kb())
    await Timer.promez.set()



@dp.message_handler(state=Timer.promez)
async def cms_promez(message: types.Message,state: FSMContext):
    try:
        if(int(message.text)<4):
            raise ValueError()
        promez=int(message.text)
        await state.update_data({
            'promez':promez

        })
        await message.reply('Отправь текст напоминания')
        await Timer.next()
    except(ValueError,TypeError):
        await message.answer('Что то пошло не так. Промежуток должен быть больше 4 секунд. Отправь корректное число')


async def send_msg_time(state: FSMContext, message: types.Message):
    global data
    await message.answer(data.get('napom'),reply_markup=get_cancel())


@dp.message_handler(state=Timer.napom)
async def load_photo(message: types.Message,state: FSMContext):

    await state.update_data({
        'napom': message.text
    })

    await message.reply('Thanks,bro',reply_markup=get_cancel())
    global data
    data = await state.get_data()
    scheduler.add_job(send_msg_time, "interval", seconds=data.get('promez'), args=(state, message),max_instances=5)
    scheduler.start()
    await state.finish()






@dp.message_handler(commands='cancel')
async def cancel(msg:types.Message):
    scheduler.shutdown()
    await msg.answer('Таймер отменен',reply_markup=get_kb())




async def on_startup(_):
    print('ALL GOOD')
if __name__=='__main__':
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True,on_shutdown=shutdown)


#
# class Shop(StatesGroup):
#     step1=State()
#     step2=State()
#
# class User(StatesGroup):
#     name=State()
#     age=State()
#     description=State()
#     studying=State()
#
# price1=100
# price2=500
#
# @dp.message_handler(commands='buy',state=None)
# async def shop(msg:types.Message):
#     await msg.answer('Введите товар 1 или 2')
#     await Shop.step1.set()
#
#
# @dp.message_handler(state=Shop.step1)
# async def shop(msg: types.Message,state:FSMContext):
#     item = msg.text
#     await state.update_data(
#         {
#             'item':item
#         }
#     )
#     await msg.answer('ведите волво')
#     await Shop.next()
#
#
# @dp.message_handler(state=Shop.step2)
# async def count(msg: types.Message,state:FSMContext):
#     data = await state.get_data()
#     item = data.get('item')
#     if item =='1':
#         p=price1
#     else:p=price2
#     count=int(msg.text)
#     await msg.answer(p*count)
#     await state.finish()
#
#
# @dp.message_handler(commands='reg',state=None)
# async def reg(msg: types.Message):
#     await msg.answer('Здарова, Напиши имя')
#     await User.name.set()
#
#
# @dp.message_handler(state=User.name)
# async def name(msg: types.Message,state:FSMContext):
#     name=msg.text
#     await state.update_data(
#         {
#             'name':name
#         }
#     )
#     await msg.answer('Напиши свой возраст')
#     await User.next()
#
#
#
# @dp.message_handler(state=User.age)
# async def age(msg: types.Message,state:FSMContext):
#     age=msg.text
#     await state.update_data({
#         'age':age
#     })
#     await msg.answer('Напиши о себе')
#     await User.next()
#
# @dp.message_handler(state=User.description)
# async def desc(msg: types.Message,state:FSMContext):
#     desc=msg.text
#     await state.update_data({
#         'desc':desc
#     })
#     await msg.answer('Где ты учишься')
#     await User.next()
#
# @dp.message_handler(state=User.studying)
# async def desc(msg: types.Message,state:FSMContext):
#     study=msg.text
#     await state.update_data({
#         'study':study
#     })
#     data = await state.get_data()
#     await msg.answer(f'Тебя зовут: {data.get("name")},\nВозраст: {data.get("age")},\nО Себе: {data.get("desc")},\nУчеба: {data.get("study")}')
#     await state.finish()




# async def send_msg_time(state:FSMContext,msg:types.Message):
#     data=await state.get_data()
#     await msg.answer(data.get('napom'))
#
# @dp.message_handler(commands=['timer'],state=None)
# async def cmd_create(message: types.Message):
#     await message.reply('Send me promez')
#     await Timer.promez.set()
#
# @dp.message_handler(state=Timer.promez)
# async def cms_promez(message: types.Message,state: FSMContext):
#     promez=message.text
#     await state.update_data({
#         'promez':promez
#
#     })
#     await message.reply('Send me your napom')
#     await Timer.next()
#
# @dp.message_handler(state=Timer.napom)
# async def load_photo(message: types.Message,state: FSMContext):
#     napom = message.text
#     await state.update_data({
#         'napom': napom
#     })
#     await message.reply('Send me your period')
#     await Timer.next()
#
#
#
#
# @dp.message_handler(state=Timer.period)
# async def load_name(message: types.Message,state: FSMContext):
#     period = int(message.text)
#     await state.update_data({
#         'period': period
#     })
#     await message.reply('Thanks,bro')
#     data = await state.get_data()
#
#     scheduler.every(10).minutes
#     await state.finish()

# ------------------


#
# @dp.callback_query_handler()
# async def callback_all(callback:types.CallbackQuery):
#     global count
#     global count2
#
#
# n=0
# m=0
# mes=''
# @dp.message_handler(commands=['start'])
# async def buttons(message:types.Message):
#     # await message.answer("Введите команду",reply_markup=kb)
#     await message.reply(MESSAGES['start'])
# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply(MESSAGES['help'])
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)
# #
# @dp.message_handler(commands=['timer'])
# async def buttons(message:types.Message):
#     global m
#
#
#     await message.answer('Напишите напоминание')
#     m=1
#
#
# @dp.message_handler()
# async def buttons(message: types.Message):
#     global m
#     if(m==1):
#         global mes
#         m=2
#         await message.answer('Напишите промежуток')
#
#     @dp.message_handler()
#     async def buttons(message: types.Message):
#         pass
