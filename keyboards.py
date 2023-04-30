from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from config import TOKEN
import random

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1=KeyboardButton('/timer')
b2=KeyboardButton('/cancel')
b3=KeyboardButton('/start ')
b4=KeyboardButton('/back ')
b5=KeyboardButton('/location ')
b6=KeyboardButton('/timer ')



ikb=InlineKeyboardMarkup(row_width=2)
ib1=InlineKeyboardButton('*',callback_data='*')
ib2=InlineKeyboardButton('/',callback_data='/')
