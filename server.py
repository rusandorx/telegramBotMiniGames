import logging
from random import randint

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler

from config import BOT_TOKEN
from tic_tac_toe import tic_tac_toe, check_end_of_tic_tac_toe, board
from wordle import wordle, wordle_answer, wordle_difficulty, wordle_exit

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

start_keyboard = [['/tic_tac_toe Крестики нолики', '/wordle Wordle']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text("Выберите миниигру",
                                    reply_markup=start_markup)


async def mini_games(update, context):
    if 'game' not in context.user_data:
        return
    text = update.message.text
    if context.user_data["game"][0] == "tic_tac_toe":
        field = context.user_data["game"][1]
        try:
            text = text[0:3].split("_")
            if field[int(text[0]) - 1][int(text[1]) - 1] == "  ":
                field[int(text[0]) - 1][int(text[1]) - 1] = "x"
            else:
                await update.message.reply_text("Данное поле уже занято")
                return 0
        except Exception:
            await update.message.reply_text("Вы ввели поле в неправильном формате или поле уже занято")
            return 0
        tic_tac_toe_field_keyboard = [[f"1_1 {field[0][0]}", f"1_2 {field[0][1]}", f"1_3 {field[0][2]}"],
                                      [f"2_1 {field[1][0]}", f"2_2 {field[1][1]}", f"2_3 {field[1][2]}"],
                                      [f"3_1 {field[2][0]}", f"3_2 {field[2][1]}", f"3_3 {field[2][2]}"]]
        tic_tac_toe_markup = ReplyKeyboardMarkup(tic_tac_toe_field_keyboard,
                                                 one_time_keyboard=True)
        await update.message.reply_text("Ваш ход",
                                        reply_markup=tic_tac_toe_markup)
        board(field, update.message.from_user)
        await context.bot.send_photo(
            update.message.chat_id,
            f"{update.message.from_user}.png"
        )
        if check_end_of_tic_tac_toe(field):
            await update.message.reply_text("Вы победили")
            await tic_tac_toe(update, context)
            return 0
        draw = 0
        for i in range(len(field)):
            for j in range(len(field)):
                if field[i][j] == "  ":
                    draw += 1
        if draw == 0:
            await update.message.reply_text("Ничья")
            await tic_tac_toe(update, context)
            return 0
        Ai_tic_tac_toe = []
        for i in range(len(field)):
            for j in range(len(field)):
                if field[i][j] == "  ":
                    Ai_tic_tac_toe.append(i * 3 + j)
        s = Ai_tic_tac_toe[randint(0, len(Ai_tic_tac_toe) - 1)]
        field[s // 3][s % 3] = "o"
        await update.message.reply_text("Ход бота",
                                        reply_markup=tic_tac_toe_markup)
        board(field, update.message.from_user)
        await context.bot.send_photo(
            update.message.chat_id,
            f"{update.message.from_user}.png"
        )
        if check_end_of_tic_tac_toe(field):
            await update.message.reply_text("Бот победил")
            await tic_tac_toe(update, context)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tic_tac_toe", tic_tac_toe))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('wordle', wordle)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, wordle_difficulty)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, wordle_answer)]
        },
        fallbacks=[CommandHandler('exit', wordle_exit)]
    ))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, mini_games)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
