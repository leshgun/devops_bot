"""Module create the Telegram Bot."""

import logging
import os
import re
from tkinter import END

from telegram import Update
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, Updater)

from host import Host

BASE_URL = "https://api.telegram.org/bot"

COMMANDS = {
    '/start':               'Показать стартовое сообщение',
    '/help':                'Показать справку по командам',
    '/find_email':          'Поиск всех Email-адресов в тексте',
    '/find_phone_numbers':  'Поиск всех российских телефонных номеров в тексте',
    '/verify_password':     'Введите пароль для проверки на сложность',
    '/help_host':           'Показать информацию о доступных хостах и возможных действиях с ними'
}

HOST_COMMANDS = {
    '/get_release':         ('cat /etc/*release', 'Информация о релизе операционной системы'),
    '/get_uname':           ('uname -a', 
                             'Информацию об архитектуры процессора, имени хоста системы '
                               + 'и версии ядра'),
    '/get_uptime':          ('uptime', 'Информация о времени работы'),
    '/get_df':              ('df -h', 'Информация о состоянии файловой системы'),
    '/get_free':            ('free -h', 'Информация о состоянии оперативной памяти'),
    '/get_mpstat':          ('mpstat', 'Информация о производительности системы'),
    '/get_w':               ('w -f', 'Информация о работающих в данной системе пользователях'),
    '/get_auths':           ('tail -n 10 /var/log/auth.log', 
                             'Информация о последних 10 входах в систему'),
    '/get_critical':        ('journalctl -p 2 -n 5', 
                             'Информация о последних 5 критических событиях'),
    '/get_ps':              ('ps -aux', 'Информация о запущенных процессах'),
    '/get_ss':              ('ss -tnlp', 'Информация об используемых портах'),
    '/get_app_list':        ('apt list --installed', 'Информация об установленных пакетах'),
    '/get_services':        ('service --status-all', 'Информация о запущенных сервисах'),
    '/get_repl_logs':       ('grep "repl" /var/log/postgresql/*.log', 
                             'Журнал событий репликации базы данных'),
    '/get_emails':          ('psql -c "select * from email" telegram_bot', 
                             'Список всех почтовых адресов'),
    '/get_phone_numbers':   ('psql -c "select * from phone" telegram_bot', 
                             'Список всех телефонных номеров'),
}

DB_COMMANDS = ['insert_to_db']

class Bot:
    """ Creating Bot class """

    MAX_MESSAGE_LENGTH = 500

    def __init__(self, token: str, host: Host):
        self._token = token
        self._host = host
        logging.basicConfig(
            filename='logfile.txt',
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self._logger = logging.getLogger(__name__)
        self.updater = Updater(self._token, use_context=True)
        self.dp = self.updater.dispatcher

    def _simple_conversation_handler(self, ep, ep_c, st, st_c) -> ConversationHandler:
        """Some docstrings..."""
        return ConversationHandler(
            entry_points=[CommandHandler(ep, ep_c)],
            states={st: [MessageHandler(Filters.text & ~Filters.command, st_c)]},
            fallbacks=[]
        )

    def start_botting(self):
        """Some docstrings..."""
        if not self.dp:
            return
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help_command))
        self.dp.add_handler(CommandHandler("help_host", self.help_host_command))
        self.dp.add_handler(self._simple_conversation_handler(
            ep = 'verify_password', ep_c = self.verify_password_command,
            st = 'verify_password_state', st_c = self.verify_password_state
        ))
        self.dp.add_handler(ConversationHandler(
            entry_points=[CommandHandler('find_email', self.find_email_command)],
            states={
                'find_email_state': [MessageHandler(Filters.text & ~Filters.command, 
                                                    self.find_email_state)],
                'save_to_db': [MessageHandler(
                    Filters.text & ~Filters.command,
                    self.save_to_db
                )]
            },
            fallbacks=[]
        ))
        self.dp.add_handler(ConversationHandler(
            entry_points=[CommandHandler('find_phone_numbers', self.find_phone_numbers_command)],
            states={
                'find_phone_numbers_state': [MessageHandler(Filters.text & ~Filters.command, 
                                                            self.find_phone_numbers_state)],
                'save_to_db': [MessageHandler(
                    Filters.regex(re.compile('да', re.I)) & ~Filters.command,
                    self.save_to_db
                )]
            },
            fallbacks=[]
        ))
        self.dp.add_handler(ConversationHandler(
                entry_points=[
                    MessageHandler(
                        Filters.regex(r'/get_\w+(?:\s\w+)?'),
                        self.send_to_host_state
                    )
                ],
                states={
                    'send_to_host_state': [
                        MessageHandler(
                            Filters.text & ~Filters.command,
                            self.send_to_host_state
                        )
                    ]
                },
                fallbacks=[]
        ))
        self.updater.start_polling()
        self.updater.idle()

    def echo(self, update: Update, context):
        """Some docstrings..."""
        update.message.reply_text(update.message.text)

    def find_email(self, text: str) -> list:
        """Searching for email addresses in the text."""
        regex = re.compile(r'([\w\.-]+@[\w\.-]+(\.[\w]+)+)')
        email_list = regex.findall(text)
        if not email_list:
            return []
        return [i[0] for i in email_list]

    def find_email_command(self, update: Update, context):
        """Requesting text from the user to search for emails"""
        update.message.reply_text('Введите текст для поиска Email-адресов')
        return 'find_email_state'

    def find_email_state(self, update: Update, context):
        """Some docstrings..."""
        user_input = update.message.text
        answer = self.find_email(user_input)
        if not answer:
            update.message.reply_text('Почтовые адреса не найдены')
            return ConversationHandler.END
        context.user_data['data_list'] = answer
        context.user_data['data_table'] = 'email'
        context.user_data['data_column'] = 'email'
        update.message.reply_text(
            'Найдены следующие адреса:\n'
            + self.list_to_numbered_list(answer)
        )
        update.message.reply_text('Вы хотите сохранить данные в БД? (Да/нет)')
        return 'save_to_db'

    def find_phone_numbers(self, text: str) -> list:
        """text -> list(numbers)"""
        regex = re.compile(r"(?:8|\+7)(?:[\s\(-]{0,2})(?:\d{3})(?:[\s\)-]{0,2})"
                           + r"(?:\d{3})(?:(?:[\s-]?)(?:\d{2})){2}")
        phone_num_list = regex.findall(text)
        if not phone_num_list:
            return []
        return phone_num_list

    def find_phone_numbers_command(self, update: Update, context) -> str:
        """Some docstrings..."""
        update.message.reply_text('Введите текст для поиска телефонных номеров:')
        return 'find_phone_numbers_state'

    def find_phone_numbers_state(self, update: Update, context):
        """Some docstrings..."""
        user_input = update.message.text
        answer = self.find_phone_numbers(user_input)
        if not answer:
            update.message.reply_text('Телефонные номера не найдены.')
            return ConversationHandler.END
        context.user_data['data_list'] = answer
        context.user_data['data_table'] = 'phone'
        context.user_data['data_column'] = 'phone'
        update.message.reply_text(
            'Найдены следующие номера:\n'
            + self.list_to_numbered_list(answer)
        )
        update.message.reply_text('Вы хотите сохранить данные в БД? (Да/нет)')
        return 'save_to_db'

    def help_command(self, update: Update, context):
        """Some docstrings..."""
        message = ''
        for item in COMMANDS.items():
            message += f'{item[0]} - {item[1]} \n'
        update.message.reply_text(message)

    def help_host_command(self, update: Update, context):
        """Some docstrings..."""
        if not self._host or not self._host.host:
            update.message.reply_text('Ни один из хостов не доступен.')
            return
        update.message.reply_text(f"*** {self._host.host} ***")
        message = ''
        for item in HOST_COMMANDS.items():
            message += f'{item[0]} - {item[1][1]} \n'
        update.message.reply_text(message)

    def list_to_numbered_list(self, l: list) -> str:
        """Conver python list to human-readable numbered list"""
        answer = ''
        for i, text in enumerate(l):
            answer += f'{i+1}. {text}\n'
        return answer

    def save_to_db(self, update: Update, context):
        """Some docstrings..."""
        if not re.match(r'да', update.message.text, re.I):
            return ConversationHandler.END
        data = context.user_data['data_list']
        table = context.user_data['data_table']
        column = context.user_data['data_column']
        if not data:
            return ConversationHandler.END
        try:
            for i in data:
                res = self.send_to_host(
                    'insert_to_db', 
                    request = f'psql -c "INSERT INTO {table} ({column}) VALUES (\'{i}\') '
                                + ' ON CONFLICT DO NOTHING;" telegram_bot'
                )
            update.message.reply_text('Обновление базы данных прошло успешно.')
        except Exception as exeption:
            update.message.reply_text(f'Обновление базы данных произошло с ошибкой:\n{exeption}')
        return ConversationHandler.END

    def send_to_host(self, command: str, grep='', request=''):
        """Some docstrings..."""
        if not command:
            return 'Команда введена неверно.'
        if command in HOST_COMMANDS:
            req = HOST_COMMANDS[command][0]
        elif command in DB_COMMANDS and request:
            req = request
        else:
            return 'Команда введена неверно.'
            
        
        grep = re.sub(r'\W', '', grep)
        if grep:
            req += f' | grep {grep}'
        self._host.connect()
        res = self._host.exec(req)
        self._host.close()
        return res

    def send_to_host_state(self, update: Update, context):
        """Some docstrings..."""
        inp = update.message.text
        inp = inp.split(' ')
        if len(inp) == 1:
            answer = self.send_to_host(inp[0])
        elif len(inp) == 2:
            answer = self.send_to_host(inp[0], grep=inp[1])
        else:
            answer = 'Команда введена неверно...'
            update.message.reply_text(answer)
            return ConversationHandler.END
        if len(answer) > self.MAX_MESSAGE_LENGTH:
            caption = (answer[:self.MAX_MESSAGE_LENGTH] + '\n...'
                       + '\nВывод слишком большой для отображения')
            try:
                file = open('tmp', 'a+', encoding="utf-8")
            except Exception:
                update.message.reply_text(caption)
            else:
                with file:
                    file.writelines(answer)
                    file.seek(0)
                    update.message.reply_document(
                        file,
                        filename='output.txt',
                        caption=caption
                    )
                    file.close()
                    os.remove('tmp')
        else:
            update.message.reply_text(answer)
        return ConversationHandler.END

    def start(self, update: Update, context):
        """Some docstrings..."""
        user = update.effective_user
        update.message.reply_text(f'Привет {user.full_name}!') # type: ignore
        update.message.reply_text('/help - показать возможности этого бота')

    def verify_password(self, text: str) -> str:
        """Some docstrings..."""
        if len(text.strip()) < 8:
            return 'Пароль простой - должен состоять как минимуим из 8 символов'
        if text == re.sub(r'[a-zA-Z]', '', text):
            return 'Пароль простой - должен содержать хотябы 1 букву'
        if text == re.sub(r'\d', '', text):
            return 'Пароль простой - должен содержать хотябы 1 цифру'
        if text == re.sub(r'[!@#$%^&*\(\)]', '', text):
            return 'Пароль простой - должен содержать хотябы 1 из следующих символов: !@#$%^&*()'
        if text in (text.upper(), text.lower()):
            return 'Пароль простой - должен содержать не менее 1 строчной и 1 заглавной буквы'
        return 'Пароль сложный'

    def verify_password_command(self, update: Update, context) -> str:
        """Some docstrings..."""
        update.message.reply_text('Введите пароль для проверки на сложность')
        return 'verify_password_state'

    def verify_password_state(self, update: Update, context):
        """Some docstrings..."""
        user_input = update.message.text
        answer = self.verify_password(user_input)
        update.message.reply_text(answer)
        return ConversationHandler.END
