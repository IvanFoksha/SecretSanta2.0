import json
from django.http import JsonResponse
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MassageHandler, Filters


from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
bot = bot.set_webhook(url='http://127.0.0.1:8000/')
