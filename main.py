import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.ext import CommandHandler
from random import randint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

start_keyboard = [['/tic_tac_toe Крестики нолики']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

reply_keyboard_1 = [['/1_1 ']]
markup_1 = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True)

game = {}


def check_end_of_tic_tac_toe(field):
    for i in field:
        if i[0] == i[1] == i[2]:
            return True
    for i in range(3):
        if field[0][i] == field[1][i] == field[1][i]:
            return True
    if field[0][0] == field[1][1] == field[1][2]:
        return True
    if field[0][2] == field[1][1] == field[1][0]:
        return True
    return False


async def start(update, context):
    await update.message.reply_text("Выберите миниигру",
                                    reply_markup=start_markup)


async def tic_tac_toe(update, context):
    game[update.message.from_user] = ["tic_tac_toe"]
    s = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    game[update.message.from_user].append(s)
    await update.message.reply_text(f"|{s[0][0]}|{s[0][1]}|{s[0][2]}|\n"
                                    f"|{s[1][0]}|{s[1][1]}|{s[1][2]}|\n"
                                    f"|{s[2][0]}|{s[2][1]}|{s[2][2]}|\nВы играете крестиками, а бот ноликами.")


async def mini_games(update, context):
    global game
    if game["update.message.from_user"][0] == "tic_tac_toe":

    await update.message.reply_text("Ваш ход")


def main():
    application = Application.builder().token("6183870254:AAH2HrtJcJaeD_3wQBso2WeFrTWZTlvNja4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tic_tac_toe", tic_tac_toe))
    text_handler = MessageHandler(filters.TEXT, mini_games)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
