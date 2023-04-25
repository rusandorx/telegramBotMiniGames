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
    await update.message.reply_text(f"|{s[0][0]}|{s[0][1]}|{s[0][2]}|\n"
                                    f"|{s[1][0]}|{s[1][1]}|{s[1][2]}|\n"
                                    f"|{s[2][0]}|{s[2][1]}|{s[2][2]}|\nВы играете крестиками, а бот ноликами.",
                                    reply_markup=tic_tac_toe_markup)
    await update.message.reply_text("Ваш ход")


def check_end_of_tic_tac_toe(field):
    for i in field:
        if i[0] == i[1] == i[2] != "  ":
            return True
    for i in range(3):
        if field[0][i] == field[1][i] == field[1][i] != "  ":
            return True
    if field[0][0] == field[1][1] == field[2][2] != "  ":
        return True
    if field[0][2] == field[1][1] == field[2][0] != "  ":
        return True
    return False


def board(field):
    size = 60
    new_image = Image.new("RGB", (3 * size, 3 * size), (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    for i in field:
        for j in i:
            if j == "x":
                draw.line((i, 0, i, 200), fill=(r, g, b), width=1)
    new_image.save('res.png', "PNG")
