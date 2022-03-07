"""
problems

асинхронные запросы к бд!
"""



from work_space import config
from work_space import dictionary
from work_space import filters
from work_space import findURL
from work_space.utils import States

import bd.bd as cucumber

import re
import logging
import time
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot (token = config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.filters_factory.bind (filters.IsAdmin)

def create_keyboard (buttons):

    #Функция создаёт клавиатуру для пользователя 
    #Как параметр передаём текстовый массив

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.add (KeyboardButton(button))
    return keyboard

#Admin functions

@dp.message_handler(is_admin = True, commands=['ban'], commands_prefix ='!/')
async def ban_for_user (message: types.Message):

    #Банит людей)

    try:
        lang = cucumber.get_base (message.chat.id)[3]
    except:
        cucumber.add_new_base (message.chat.id)
        lang = cucumber.get_base (message.chat.id)[3]
    
    if (not message.reply_to_message):
        await message.reply (dictionary.problems_with_the_procedure[lang])
        return
    
    if (int(message.reply_to_message.from_user.id) == int(config.BOT_ID)):
        await message.reply (dictionary.you_cant_ban_me[lang])
        return
    
    member = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if (member.is_chat_admin()):
        await message.reply (dictionary.you_cant_ban[lang])
        return

    cucumber.delete_entry (message.chat.id, message.reply_to_message.from_user.id)
    await message.bot.kick_chat_member (chat_id= message.chat.id, user_id= message.reply_to_message.from_user.id)
    await message.answer (dictionary.farewell[lang].format(message.reply_to_message.from_user.full_name))
    await message.delete ()

@dp.message_handler(is_admin = True, commands=['help'], commands_prefix ='!/')
async def send_help (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]

    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return
        
    await message.answer (dictionary.help[lang])

#States

@dp.message_handler(state=States.waiting_new_lang)
async def first_test_state_case_met(message: types.Message):
    if (not message.text in dictionary.languages):
        #Подумать, как лучше реализовать нахождение языка без лишних запросов в бд
        lang = cucumber.get_base (message.chat.id)[3]
        return await message.answer (dictionary.stupid_user[lang])
    
    state = dp.current_state(chat=message.chat.id)
    await state.reset_state ()

    current_state = list(cucumber.get_base (message.chat.id))
    current_state[3] = message.text
    cucumber.update_base (*current_state)

    await message.answer (dictionary.change_settings[current_state[3]])
    await message.answer (dictionary.next_time[current_state[3]], reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=States.waiting_new_rep)
async def second_test_state_case_met(message: types.Message):
    if (len(message.text.split()) == 1 and "".join(message.text.split()).isdigit()):
        if (1 < int("".join(message.text.split())) and int("".join(message.text.split())) < 100):
            current_state = list(cucumber.get_base (message.chat.id))
            current_state[2] = "".join(message.text.split())
            cucumber.update_base (*current_state)

            state = dp.current_state(chat=message.chat.id)  
            await state.reset_state ()

            lang = current_state[3]
            await message.answer (dictionary.change_settings[lang])
            return await message.answer (dictionary.next_time[current_state[3]])
    lang = cucumber.get_base (message.chat.id)[3]
    return await message.answer (dictionary.reports_is_out_range[lang])

@dp.message_handler(state=States.waiting_new_lim)
async def third_test_state_case_met(message: types.Message):
    if (len(message.text.split()) == 1 and "".join(message.text.split()).isdigit()):
        if (0 < int("".join(message.text.split())) and int("".join(message.text.split())) < 365):
            current_state = list(cucumber.get_base (message.chat.id))
            current_state[1] = "".join(message.text.split())
            cucumber.update_base (*current_state)

            state = dp.current_state(chat=message.chat.id)  
            await state.reset_state ()

            lang = current_state[3]
            await message.answer (dictionary.change_settings[lang])
            return await message.answer (dictionary.next_time[current_state[3]])
    lang = cucumber.get_base (message.chat.id)[3]
    return await message.answer (dictionary.data_is_out_range[lang])
    
#User functions

@dp.message_handler(content_types=['text'])
async def report (message: types.Message):
    match = re.findall(findURL.URL_REGEX, message.text)
    if (len(match) < 1):
        return
    
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]

    user = cucumber.get_user (message.chat.id, message.from_user.id)

    if (user != None):
        if (cucumber.how_many_days(user[2]) < data[1]):
            await message.delete ()
            ms = await message.answer (dictionary.so_small_user[lang].format (data[1]))
            await asyncio.sleep(4)
            await ms.delete()


@dp.message_handler(commands=['report'], commands_prefix ='!/')
async def report (message: types.Message):

    #Кидает репорты)

    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    
    #Сообщение должно быть ответом

    if (not message.reply_to_message):
        await message.reply (dictionary.problems_with_the_procedure[lang])
        return
    
    #нельзя забанить самого себя

    if (int(message.reply_to_message.from_user.id) == int(config.BOT_ID)):
        await message.reply (dictionary.you_cant_ban_me[lang])
        return
    
    #нельзя забанить админа

    member = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if (member.is_chat_admin()):
        await message.reply (dictionary.you_cant_ban[lang])
        return

    try:
        people = list(cucumber.get_user (message.chat.id, message.reply_to_message.from_user.id))
        report = []
        if (people[3] != None):
            report = people[3].split()
    except:
        cucumber.add_new_user (message.chat.id, message.reply_to_message.from_user.id)
        cucumber.normalizetime(message.chat.id, message.reply_to_message.from_user.id)
        people = list(cucumber.get_user (message.chat.id, message.reply_to_message.from_user.id))
        report = []
        if (people[3] != None):
            report = people[3].split()
    
    if (message.from_user.id in report):
        return await message.answer (dictionary.already_sent[lang])
    '''
    judge = cucumber.get_user (message.chat.id, message.from_user.id)

    if (judge != None):
        if (cucumber.how_many_days(judge[2]) < data[1]):
            return await message.answer (dictionary.more_day[lang].format(data[1]))
    '''
    report.append (message.from_user.id)
    if (len(report) >= data[2]):
        cucumber.delete_entry (message.chat.id, message.reply_to_message.from_user.id)
        await message.bot.kick_chat_member (chat_id= message.chat.id, user_id= message.reply_to_message.from_user.id)
        await message.answer (dictionary.lot_of_reports[lang].format(message.reply_to_message.from_user.full_name, data[2], data[2]))
        await message.delete ()
    else:
        people[3] = " ".join(list(map(str, report)))
        cucumber.update_user(message.chat.id, message.reply_to_message.from_user.id, people[3])
        await message.answer (dictionary.new_report[lang].format(message.reply_to_message.from_user.full_name, len(report), data[2]))
        await message.delete ()


# Admin settings

@dp.message_handler(is_admin = True, commands=['change_language'], commands_prefix ='!/')
async def change_language (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]

    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return

    arg = message.get_args ()
    if (len(arg.split()) == 1 and "".join(arg.split()) in dictionary.languages):
        pass
    else:
        markup = create_keyboard (dictionary.languages)
        state = dp.current_state(chat=message.chat.id)

        await message.answer (dictionary.please_enter_value[lang], reply_markup= markup)
        await state.set_state(States.waiting_new_lang)
        return

    data[3] = "".join(arg.split())
    cucumber.update_base (*data)

    await message.answer (dictionary.change_settings[data[3]])

@dp.message_handler(is_admin = True, commands=['change_anti_bot_time_limit'], commands_prefix ='!/')
async def change_anti_spam_limitation (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    
    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return
    
    arg = message.get_args ()
    if (len(arg.split()) == 1 and "".join(arg.split()).isdigit()):
        if (0 > int("".join(arg.split())) or int("".join(arg.split())) > 365):
            return await message.answer (dictionary.data_is_out_range[lang])
        data[1] = int("".join(arg.split()))
        cucumber.update_base (*data)

        await message.answer (dictionary.change_settings[lang])
    else:
        state = dp.current_state(chat=message.chat.id)

        await message.answer (dictionary.please_enter_value[lang])
        await message.answer (dictionary.data_is_out_range[lang])
        await state.set_state(States.waiting_new_lim)


@dp.message_handler(is_admin = True, commands=['change_count_reports_for_ban'], commands_prefix ='!/')
async def change_reports_for_ban (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    
    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return

    arg = message.get_args ()
    if (len(arg.split()) == 1 and "".join(arg.split()).isdigit()):
        if (1 > int("".join(arg.split())) or int("".join(arg.split())) > 100):
            return await message.answer (dictionary.reports_is_out_range[lang])
        data[2] = int("".join(arg.split()))
        cucumber.update_base (*data)

        await message.answer (dictionary.change_settings[lang])
    else:
        state = dp.current_state(chat=message.chat.id)

        await message.answer (dictionary.please_enter_value[lang])
        await message.answer (dictionary.reports_is_out_range[lang])
        await state.set_state(States.waiting_new_rep)

@dp.message_handler(is_admin = True, commands=['need_to_appeal_on'], commands_prefix ='!/')
async def on (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    
    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return
    data[4] = True
    cucumber.update_base (*data)
    await message.answer (dictionary.change_settings[lang])

@dp.message_handler(is_admin = True, commands=['need_to_appeal_off'], commands_prefix ='!/')
async def off (message: types.Message):
    try:
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    except:
        cucumber.add_new_base (message.chat.id)
        data = list (cucumber.get_base (message.chat.id))
        lang = data[3]
    
    if(bool(data[4])):
        if (not config.BOT_NAME in message.text):
            return
    
    data[4] = False
    cucumber.update_base (*data)
    await message.answer (dictionary.change_settings[lang])

@dp.message_handler(content_types=['new_chat_members'])
async def new_members_handler(message: types.Message):
    for member in message.new_chat_members:
        cucumber.add_new_user (message.chat.id, member.id)
    await message.delete ()



if (__name__ == '__main__'):
    executor.start_polling(dp, skip_updates=True)