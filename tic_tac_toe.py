import os
from random import choice, randint

from PIL import Image, ImageDraw
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

start_keyboard = [
    ['/tic_tac_toe Крестики нолики', '/wordle Wordle', '/guess_city Угадай город', '/tic_tac_toe_online ']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

tic_tac_toe_field_keyboard = [["1_1  ", "1_2  ", "1_3  "],
                              ["2_1  ", "2_2  ", "2_3  "],
                              ["3_1  ", "3_2  ", "3_3  "]]

tic_tac_toe_markup = ReplyKeyboardMarkup(tic_tac_toe_field_keyboard, one_time_keyboard=False)

exit_keyboard = [['/start_again', '/exit']]
exit_markup = ReplyKeyboardMarkup(exit_keyboard, one_time_keyboard=True)

only_exit_keyboard = [['/exit']]
only_exit_markup = ReplyKeyboardMarkup(only_exit_keyboard, one_time_keyboard=True)

POOL = []
GAMES = {}


async def tic_tac_toe(update, context):
    context.user_data["game"] = ["tic_tac_toe"]

    s = [["  ", "  ", "  "], ["  ", "  ", "  "], ["  ", "  ", "  "]]
    context.user_data["game"].append(s)
    board(s, update.message.from_user)
    await context.bot.send_photo(
        update.message.chat_id,
        f"{update.message.from_user}.png",
        caption='Вы играете крестиками, а бот ноликами.'
    )
    os.remove(f'{update.message.from_user}.png')


    await update.message.reply_text("Ваш ход",
                                    reply_markup=tic_tac_toe_markup)

    return 1


async def tic_tac_toe_online(update, context):
    user_id = update.message.from_user['id']
    if user_id in POOL:
        return await context.bot.send_message(user_id, 'Вы уже в очереди', reply_markup=tic_tac_toe_markup)
    if POOL:
        s = [["  ", "  ", "  "], ["  ", "  ", "  "], ["  ", "  ", "  "]]
        match = POOL.pop()
        board(s, user_id)
        x = choice((user_id, match))
        o = user_id if x == match else match

        game = {'users': (user_id, match), 'x': x, 'o': o, 'turn': 'x', 'board': s}
        GAMES[o] = GAMES[x] = game

        await context.bot.send_message(match, f'Пара найдена. Вы - {"x" if game["x"] == match else "0"}',
                                       reply_markup=tic_tac_toe_markup)
        await context.bot.send_message(user_id, f'Пара найдена. Вы - {"x" if game["x"] == user_id else "0"}',
                                       reply_markup=tic_tac_toe_markup)

    else:
        POOL.append(user_id)
        await update.message.reply_text('Мы сообщим, когда найдем вам пару.', reply_markup=only_exit_markup)
    return 1


async def tic_tac_toe_online_message(update, context):
    update.message.reply_text('Online message')
    user_id = update.message.from_user['id']
    game = GAMES[user_id]
    field = game['board']
    match = tuple(filter(lambda x: x != user_id, game['users']))[0]
    user_symb = 'x' if game['x'] == user_id else 'o'
    if check_end_of_tic_tac_toe(field):
        return 1
    if user_symb != game['turn']:
        await update.message.reply_text('Не ваш ход.')
        return 1

    text = update.message.text
    try:
        text = text[0:3].split("_")
        if field[int(text[0]) - 1][int(text[1]) - 1] == "  ":
            field[int(text[0]) - 1][int(text[1]) - 1] = game['turn']
        else:
            await update.message.reply_text("Данное поле уже занято")
            return 1
    except Exception:
        await update.message.reply_text("Вы ввели поле в неправильном формате или поле уже занято")
        return 1

    board(field, update.message.from_user)
    await context.bot.send_photo(
        user_id,
        f"{update.message.from_user}.png"
    )
    await context.bot.send_photo(
        match,
        f"{update.message.from_user}.png"
    )
    os.remove(f'{update.message.from_user}.png')


    game['turn'] = 'x' if game['turn'] == 'o' else 'o'

    if check_end_of_tic_tac_toe(field):
        await update.message.reply_text("Вы победили", reply_markup=exit_markup)
        await context.bot.send_message(match, 'Вы проиграли', reply_markup=exit_markup)
        context.user_data.clear()

    draw = 0
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] == "  ":
                draw += 1

    if draw == 0:
        await update.message.reply_text("Ничья", reply_markup=exit_markup)
        await context.bot.send_message(match, 'Ничья', reply_markup=exit_markup)
        context.user_data.clear()

    return 1


async def tic_tac_toe_message(update, context):
    field = context.user_data["game"][1]
    text = update.message.text
    try:
        text = text[0:3].split("_")
        if field[int(text[0]) - 1][int(text[1]) - 1] == "  ":
            field[int(text[0]) - 1][int(text[1]) - 1] = "x"
        else:
            await update.message.reply_text("Данное поле уже занято")
            return 1
    except Exception:
        await update.message.reply_text("Вы ввели поле в неправильном формате или поле уже занято")
        return 1
    await update.message.reply_text("Ваш ход",
                                    reply_markup=tic_tac_toe_markup)
    board(field, update.message.from_user)
    await context.bot.send_photo(
        update.message.chat_id,
        f"{update.message.from_user}.png"
    )
    os.remove(f'{update.message.from_user}.png')

    if check_end_of_tic_tac_toe(field):
        await update.message.reply_text("Вы победили")
        await tic_tac_toe(update, context)
        return ConversationHandler.END
    draw = 0
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] == "  ":
                draw += 1
    if draw == 0:
        await update.message.reply_text("Ничья")
        await tic_tac_toe(update, context)
        return ConversationHandler.END
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
    os.remove(f'{update.message.from_user}.png')
    if check_end_of_tic_tac_toe(field):
        await update.message.reply_text("Бот победил")
        await tic_tac_toe(update, context)
        return ConversationHandler.END
    return 1


def check_end_of_tic_tac_toe(field):
    for i in field:
        if i[0] == i[1] == i[2] != "  ":
            return True
    for i in range(3):
        if field[0][i] == field[1][i] == field[2][i] != "  ":
            return True
    if field[0][0] == field[1][1] == field[2][2] != "  ":
        return True
    if field[0][2] == field[1][1] == field[2][0] != "  ":
        return True
    return False


def board(field, user):
    size = 60
    new_image = Image.new("RGB", (3 * size, 3 * size), (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    for i1, i in enumerate(field):
        for j1, j in enumerate(i):
            if j == "x":
                draw.line((j1 * size, i1 * size, (j1 + 1) * size, (i1 + 1) * size), fill=(255, 0, 0), width=4)
                draw.line((j1 * size, (i1 + 1) * size, (j1 + 1) * size, i1 * size), fill=(255, 0, 0), width=4)
            if j == "o":
                draw.ellipse(
                    (j1 * size + 3, i1 * size + 3, (j1 + 1) * size - 2, (i1 + 1) * size - 2),
                    fill=(255, 255, 255), outline=(0, 0, 255), width=4)
    for i in range(4):
        draw.line(((i + 1) * 60, 0, (i + 1) * 60, 180), fill=(0, 0, 0), width=2)
    for i in range(4):
        draw.line((0, (i + 1) * 60, 180, (i + 1) * 60), fill=(0, 0, 0), width=2)
    new_image.save(f'{user}.png', "PNG")


async def tic_tac_toe_exit(update, context):
    await update.message.reply_text('Вышли из крестиков ноликов', reply_markup=start_markup)
    if update.message.chat_id in POOL:
        POOL.remove(update.message.chat_id)
    context.user_data.clear()
    return ConversationHandler.END
