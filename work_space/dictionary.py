from bot import report


greeting = {
    'ru' : "Привет, {}!",
    'en' : "Hello, {}!"
}

lot_of_reports = {
    'ru' : "Пользователь {} получил {}/{} репортов!\nДа прибудет с ним сила!",
    'en' : "User {} received {}/{} reports!\nMay the Force be with him!"
}

new_report = {
    'ru' : "Пользователь {} получил {}/{} репортов!",
    'en' : "User {} received {}/{} reports!"
}

farewell = {
    'ru' : "Пользователь {} забанен\nДа прибудет с ним сила!",
    'en' : "The user {} is banned\nMay the Force be with him!"
}

problems_with_the_procedure = {
    'ru' : "Эта команда должна быть ответом на сообщение",
    'en' : "This command should be a reply to the message"
}

please_enter_value = {
    'ru' : "Пожалуйста, введите новое значение!",
    'en' : "Please enter a new value!"
}

you_cant_ban_me = {
    'ru' : "Хаха, меня так просто не забанить! 😁",
    'en' : "Haha, I can't be banned so easily! 😁"
}

you_cant_ban = {
    'ru' : "Я не могу удалять администраторов чата! 😐",
    'en' : "I can't delete chat admins! 😐"
}

change_settings = {
    'ru' : "Настройки успешно сменены!",
    'en' : "Setting is changed!"
}

cant_change_settings = {
    'ru' : "Вы допустили ошибку в запросе!",
    'en' : "You made a mistake in the request!"
}

help = {
    'ru' : "Помощь",
    'en' : "Helping",
}

so_small_user = {
    'ru' : "Для отправления ссылок вы должны состоять в группе более {} дней",
    'en' : "To send links, you must be in a group for more than {} days"
}

next_time = {
    'ru' : "Если вы будете изпользовать команды ещё раз, то используйте такой шаблон:\n \\`команда` `новое значение`",
    'en' : "If you will use the commands again, then use this template:\n \\`command` `new_value`"
}

stupid_user = {
    'ru' : "Пожалуйста, просто нажмите на кнопку!",
    'en' : "Please just click on the button!"
}

data_is_out_range = {
    'ru' : "Время нахождения новых пользователей в Black листе может находиться в промежутке от 0 до 365!\nВводите ТОЛЬКО новое значение",
    'en' : "The time spent by new users in the Black List can be in the range from 0 to 365!\nEnter ONLY the new value"
}

reports_is_out_range = {
    'ru' : "Необходимое количество репортов для бана пользователя должно варьироваться от 1 до 100!\nВводите ТОЛЬКО новое значение",
    'en' : "The required number of reports to ban a user should vary from 1 to 100!\nEnter ONLY the new value"
}

already_sent = {
    "ru" : "Вы уже отправили репорт на этого участника чата",
    'en' : 'Нou have already sent a report to this chat member'
}

more_day = {
    'ru' : "Для отправления репортов вы должны состоять в группе более {} дней",
    'en' : 'To send reports, you must be in a group for more than {} days'
}

languages = ['ru', 'en']