from PIL import Image, ImageDraw
from telegram import ReplyKeyboardMarkup


async def tic_tac_toe(update, context):
    context.user_data["game"] = ["tic_tac_toe"]
    s = [["  ", "  ", "  "], ["  ", "  ", "  "], ["  ", "  ", "  "]]
    context.user_data["game"].append(s)
    tic_tac_toe_field_keyboard = [["/1_1  ", "/1_2  ", "/1_3  "],
                                  ["/2_1  ", "/2_2  ", "/2_3  "],
                                  ["/3_1  ", "/3_2  ", "/3_3  "]]
    tic_tac_toe_markup = ReplyKeyboardMarkup(tic_tac_toe_field_keyboard, one_time_keyboard=True)
    board(s, update.message.from_user)
    await context.bot.send_photo(
        update.message.chat_id,
        "res.png",
        caption='Вы играете крестиками, а бот ноликами.'
    )
    await update.message.reply_text("Ваш ход",
                                    reply_markup=tic_tac_toe_markup)


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
