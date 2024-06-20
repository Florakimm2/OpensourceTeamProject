#!/usr/bin/env python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, filters, Application, ContextTypes
from telegram.error import (TelegramError, BadRequest,
                            TimedOut, ChatMigrated, NetworkError, Forbidden)
import logging
import person_db
import face_classifier
import io
import cv2
from datetime import datetime
from datetime import timedelta
import humanize


class CmdDefault():
    def __init__(self, telegram_bot):
        self.name = self.__class__.__name__[3:].lower()
        self.vatb = telegram_bot

    def usage(self):
        return '/' + self.name

    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        # dummy method - echo
        chat_id = update.effective_chat.id
        reply = update.message.text
        await context.bot.send_message(chat_id=chat_id, text=reply)


class CmdRename(CmdDefault):
    def usage(self):
        return '/' + self.name + ' old_name new_name'

    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        args = update.message.text.split()
        if len(args) == 3:
            if self.vatb.pdb.rename(args[1], args[2]) == 0:
                reply = 'Name changed: ' + args[1] + ' -> ' + args[2]
            else:
                reply = 'Cannot change the person with name ' + args[1]
        else:
            reply = 'usage: ' + self.usage()
        await context.bot.send_message(chat_id=chat_id, text=reply)

class CmdList(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if len(self.vatb.pdb.persons) == 0:
            reply = 'No persons in DB'
            await context.bot.send_message(chat_id=chat_id, text=reply)
            return
        for person in self.vatb.pdb.persons:
            reply = "%s with %d faces" % (person.name, len(person.faces))
            image = person.get_montage(3, 2)
            is_success, buf = cv2.imencode(".png", image)
            bio = io.BytesIO(buf)
            bio.seek(0)
            await context.bot.send_photo(chat_id=chat_id, photo=bio, caption=reply)

class CmdStatus(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        reply = 'In person DB, ' + self.vatb.pdb.__repr__()
        reply += '\n' + self.vatb.fc.status_string
        if self.vatb.fc.running is True:
            reply += '\n' + self.vatb.fc.source_info_string
        await context.bot.send_message(chat_id=chat_id, text=reply)

class CmdStart(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if self.vatb.fc.running:
            reply = 'Face classifier is already running.'
        else:
            reply = 'OK. Starting face classifier.'
        if chat_id != self.vatb.alarm_receiver:
            reply += '\nVisitor alarm will be sent to you.'
            self.vatb.alarm_receiver = chat_id
        await context.bot.send_message(chat_id=chat_id, text=reply)
        if not self.vatb.fc.running:
            self.vatb.fc.start_running()

class CmdStop(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        reply = self.vatb.fc.settings.__repr__()
        if self.vatb.fc.running:
            reply = 'OK. Stopping face classifier.'
        else:
            reply = 'Face classifier is not running now.'
        await context.bot.send_message(chat_id=chat_id, text=reply)
        if self.vatb.fc.running:
            self.vatb.fc.stop_running()

class CmdSettings(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        reply = self.vatb.str_settings()
        await context.bot.send_message(chat_id=chat_id, text=reply)

class CmdShot(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if self.vatb.fc.running:
            image = self.vatb.fc.last_frame
            is_success, buf = cv2.imencode(".png", image)
            bio = io.BytesIO(buf)
            bio.seek(0)
            await context.bot.send_photo(chat_id=chat_id, photo=bio)
        else:
            reply = 'Face classifier is not running now.'
            await context.bot.send_message(chat_id=chat_id, text=reply)

class CmdHelp(CmdDefault):
    async def method(self, update: Updater, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        usages = [cmd.usage() for cmd in self.vatb.commands]
        reply = '\n'.join(usages)
        await context.bot.send_message(chat_id=chat_id, text=reply)


class VisitorAlarmTelegramBot(face_classifier.Observer):
    def __init__(self, face_classifier, person_db, settings):
        self.fc = face_classifier
        self.pdb = person_db
        self.settings = settings
        self.alarm_receiver = None

        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO)

        # create Telegram Bot
        self.core = telegram.Bot(settings.token)
        self.application = Application.builder().token(settings.token).build()

        # add command handlers
        self.commands = []
        self.add_command(CmdHelp(self))
        self.add_command(CmdSettings(self))
        self.add_command(CmdStart(self))
        self.add_command(CmdStop(self))
        self.add_command(CmdStatus(self))
        self.add_command(CmdShot(self))
        self.add_command(CmdRename(self))
        self.add_command(CmdList(self))

        # unknown handler should be added last
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.unknown))

        # error handler
        # self.application.add_error_handler(self.error_callback)

    def add_command(self, handlerObj):
        self.commands.append(handlerObj)
        self.application.add_handler(CommandHandler(handlerObj.name, handlerObj.method))

    async def start_polling(self):
        print("Visitor Alarm Telegram Bot is started.")
        print(self.str_settings())
        print("press ^C to stop...")
        await self.application.start_polling()

    def stop(self):
        self.application.stop()

    async def idle(self):
        await self.application.idle()
        print("Visitor Alarm Telegram Bot is finished.")

    async def unknown(self, update, context):
        chat_id = update.effective_chat.id
        print(update.message.text)
        reply = "Sorry, I didn't understand that command."
        reply += "\nTry /help for available commands."
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def on_new_person(self, person):
        chat_id = self.alarm_receiver
        reply = person.name + " appeared for the first time"
        image = person.get_montage(2, 1)
        is_success, buf = cv2.imencode(".png", image)
        bio = io.BytesIO(buf)
        bio.seek(0)
        await self.core.send_photo(chat_id=chat_id, photo=bio, caption=reply)
        logging.info(reply)

    async def on_person(self, person):
        now = datetime.now()
        td = timedelta(seconds=self.settings.appearance_interval)
        if person.last_face_time + td > now:
            return
        # this person is detected again after for a while
        chat_id = self.alarm_receiver
        ago = now - person.last_face_time
        reply = person.name + ' appeared again in ' + humanize.naturaldelta(ago)
        reply += ' since ' + person.last_face_time.strftime('%Y-%m-%d %H:%M:%S')
        image = person.get_montage(2, 1)
        is_success, buf = cv2.imencode(".png", image)
        bio = io.BytesIO(buf)
        bio.seek(0)
        await self.core.send_photo(chat_id=chat_id, photo=bio, caption=reply)
        logging.info(reply)

    async def on_start(self, fc):
        chat_id = self.alarm_receiver
        reply = 'Face classifier is started.'
        reply += '\n' + fc.source_info_string
        await self.core.send_message(chat_id=chat_id, text=reply)
        logging.info(reply)

    async def on_stop(self, fc):
        chat_id = self.alarm_receiver
        reply = 'Face classifier is stopped.'
        await self.core.send_message(chat_id=chat_id, text=reply)
        logging.info(reply)
        self.alarm_receiver = None

    def str_settings(self):
        s = '* srcfile = ' + self.settings.srcfile
        if self.settings.srcfile == '0':
            s += ' (webcam)'
        s += '\n* resize_ratio = ' + str(self.settings.resize_ratio)
        s += '\n* sbf (second between frame processed) = ' + str(self.settings.sbf)
        s += '\n* similarity threshold = ' + str(self.settings.threshold)
        s += '\n* appearance_interval = ' + str(self.settings.appearance_interval)
        return s
    
    


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True,
                    help="Telegram Bot Token")
    ap.add_argument("--srcfile", type=str, default='0',
                    help="Video file to process. If not specified, web cam is used.")
    ap.add_argument("--threshold", default=0.42, type=float,
                    help="threshold of the similarity (default=0.42)")
    ap.add_argument("--sbf", default=0.5, type=float,
                    help="second between frame processed (default=0.5)")
    ap.add_argument("--resize-ratio", default=1.0, type=float,
                    help="resize the frame to process (less time, less accuracy)")
    ap.add_argument("--appearance-interval", default=10, type=int,
                    help="alarm interval second between appearance (default=10)")
    args = ap.parse_args()

    dir_name = "result"
    pdb = person_db.PersonDB()
    pdb.load_db()

    fc = face_classifier.FaceClassifier(pdb, args)
    vatb = VisitorAlarmTelegramBot(fc, pdb, args)
    fc.register_observer(vatb)

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(vatb.start_polling())
    loop.run_until_complete(vatb.idle())
    fc.stop_running()