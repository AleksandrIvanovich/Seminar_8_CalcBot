import telebot, time, re
# from telebot import types
from config import TOCKEN

BOT_TOKEN = TOCKEN # Токен бота
BOT_NAME = '' # Имя для бота. Нужно в том случае, если вы хотите обращаться к боту по имени
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5 # Таймаут переподключения

# Сообщение при старте
START_MESSAGE = """Отправь мне выражение, а я тебе скажу ответ"""
# Сообщение поддержки
HELP_MESSAGE = """Мной пользоваться очень просто. Вы мне отправляете выражение, а я вам возвращаю его результат.
***Операторы***:
    + - сложение;
    - - вычитание;
    \* - умножение;
    / - деление;
    \*\* - возведение в степнь."""


пи = п = p = pi = 3.141592653589793238462643 # число Пи asd 

# Обработчик сообщений-команд
@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    if message.text.lower() == '/start':
        msg = bot.send_message(message.chat.id, START_MESSAGE, parse_mode='markdown')

    elif message.text.lower() == '/help':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')
        
    if (msg):
        print('Бот: %s'%msg.text)

# Обработчик всех сообщений
@bot.message_handler(func = lambda message: True)
def answer_to_user(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    user_message = message.text.lower()

    if BOT_NAME:
        regex = re.compile(BOT_NAME.lower())
        print(regex.search(user_message))
        if regex.search(user_message) == None:
            return

        regex = re.compile('%s[^a-z]'%(BOT_NAME.lower()))
        user_message = regex.sub("", user_message)

    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    
    print(user_message)

    if user_message == 'привет':
        msg = bot.send_message(message.chat.id, '*Привет, %s*'%(message.chat.first_name), parse_mode='markdown')

    elif user_message == 'помощь':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')

    else:
        try:
            answer = str(eval(user_message.replace(' ', '')))
            msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)
                
        except SyntaxError:
            msg = bot.send_message(message.chat.id, 'Похоже, что вы написали что-то не так. \nПопробуйте ещё раз')
        except NameError:
            msg = bot.send_message(message.chat.id, 'Переменную которую вы спрашиваете я не знаю. \nПопробуйте ещё раз')
        except ZeroDivisionError:
            msg = bot.send_message(message.chat.id, 'В выражении вы делите на ноль. \nПопробуйте ещё раз')

    if (msg):
        print('Бот: %s'%msg.text)

# Вход в программу
if (__name__ == '__main__'):
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print ('Ошибка подключения. Попытка подключения через %s сек.'%TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)