import datetime
from datetime import date
import logging

import telegram
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - \
                    %(message)s", level=logging.INFO)

class TelegramDailyBot:
    # Bot sends new messages to user every day at scheduled time
    # You should pass a dict to bot with prepared messages in values
    # and dates formatted in str(dd.mm) in keys
    # Hours and minutes are the time when messages would be sent
    
    def __init__(self, token, hours, minutes, input_dict):
        self.token = token
        self.hours = hours
        self.minutes = minutes
        self.input_dict = input_dict
        self.bot = telegram.Bot(token=self.token)
        self.updater = Updater(bot=self.bot, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self, *handlers):
        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def start(self, update, context):
        # /Start command that subscribe user to daily messages
        chat_id = update.message.chat_id
        new_job = context.job_queue.run_daily(
                    self.daily_routine, 
                    datetime.time(hour=self.hours, 
                    minute=self.minutes), 
                    context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text("You're subscribed to daily messages")
            
    def daily_routine(self, context):
        # Bot supposes that you pass the dict with keys-days formatted 
        # in str(dd.mm)
        job = context.job
        current_date = date.today().strftime("%d.%m")
        context.bot.send_message(job.context, text=i[current_date])

    def init_handlers(self):
        start_handler = CommandHandler("start", self.start, 
                                       pass_args=True,
                                       pass_job_queue=True, 
                                       pass_chat_data=True)
        self.add_handlers(start_handler)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
        
if __name__ == "__main__":
    t = TelegramDailyBot(token, hours, minutes, input_dict)
    t.init_handlers()
    t.run()  
