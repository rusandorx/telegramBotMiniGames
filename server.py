import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler

from config import BOT_TOKEN
from guess_city import guess_city
from guess_city import guess_city_message
from tic_tac_toe import tic_tac_toe
from tic_tac_toe import tic_tac_toe_online, tic_tac_toe_exit, \
    tic_tac_toe_message, tic_tac_toe_online_message
from wordle import wordle, wordle_answer, wordle_difficulty, wordle_exit

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

start_keyboard = [
    ['/tic_tac_toe Крестики нолики', '/wordle Wordle', '/guess_city Угадай город', '/tic_tac_toe_online ']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text("Выберите миниигру",
                                    reply_markup=start_markup)


async def mini_games(update, context):
    await update.message.reply_text("Mini games")
    if 'game' not in context.user_data:
        return


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('wordle', wordle)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, wordle_difficulty)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, wordle_answer)]
        },
        fallbacks=[CommandHandler('exit', wordle_exit)]
    ))

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('tic_tac_toe', tic_tac_toe)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, tic_tac_toe_message)]
        },
        fallbacks=[]
    ))

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('tic_tac_toe_online', tic_tac_toe_online)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, tic_tac_toe_online_message),
                CommandHandler('start_again', tic_tac_toe_online)]
        },
        fallbacks=[CommandHandler('exit', tic_tac_toe_exit)]
    ))

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('guess_city', guess_city)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, guess_city_message), ]
        },
        fallbacks=[]
    ))
    application.run_polling()

if __name__ == '__main__':
    main()
