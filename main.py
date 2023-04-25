import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.ext import CommandHandler
from random import randint

from tg.tic_tac_toe import tic_tac_toe, check_end_of_tic_tac_toe, board

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

start_keyboard = [['/tic_tac_toe Крестики нолики']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text("Выберите миниигру",
                                    reply_markup=start_markup)


async def mini_games(update, context):
    text = update.message.text
    if context.user_data["game"][0] == "tic_tac_toe":
        field = context.user_data["game"][1]
        tic_tac_toe_field_keyboard = [[f"/1_1 {field[0][0]}", f"/1_2 {field[0][1]}", f"/1_3 {field[0][2]}"],
                                      [f"/2_1 {field[1][0]}", f"/2_2 {field[1][1]}", f"/2_3 {field[1][2]}"],
                                      [f"/3_1 {field[2][0]}", f"/3_2 {field[2][1]}", f"/3_3 {field[2][2]}"]]
        tic_tac_toe_markup = ReplyKeyboardMarkup(tic_tac_toe_field_keyboard, one_time_keyboard=True)
        try:
            text = text[1:4].split("_")
            if field[int(text[0]) - 1][int(text[1]) - 1] == "  ":
                field[int(text[0]) - 1][int(text[1]) - 1] = "x"
            else:
                await update.message.reply_text("Данное поле уже занято")
            await update.message.reply_text(f"|{field[0][0]}|{field[0][1]}|{field[0][2]}|\n"
                                            f"|{field[1][0]}|{field[1][1]}|{field[1][2]}|\n"
                                            f"|{field[2][0]}|{field[2][1]}|{field[2][2]}|\n",
                                            reply_markup=tic_tac_toe_markup)
        except Exception:
            await update.message.reply_text("Вы ввели поле в неправильном формате или поле уже занято")
        await update.message.reply_text("Ваш ход")
        if check_end_of_tic_tac_toe(field):
            await update.message.reply_text("Вы Победили")
        board(field)
        await context.bot.send_photo(
            update.message.chat_id,
            "res.png"
        )


def main():
    application = Application.builder().token("6183870254:AAH2HrtJcJaeD_3wQBso2WeFrTWZTlvNja4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tic_tac_toe", tic_tac_toe))
    text_handler = MessageHandler(filters.TEXT, mini_games)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
