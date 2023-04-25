from random_word import Wordnik
from telegram import ReplyKeyboardMarkup

WORDLE_SYMBOLS = {
    'ORANGE': '🟧',
    'GRAY': '⬛',
    'GREEN': '🟩'
}

DIFFICULTIES = {
    'easy': (4, 5, 6),
    'normal': (6, 7, 5),
    'hard': (7, 8, 5),
}

diff_keyboard = [['easy', 'normal', 'hard']]
diff_markup = ReplyKeyboardMarkup(diff_keyboard, one_time_keyboard=True)


async def wordle(update, context):
    await update.message.reply_text('Выберите сложность', reply_markup=diff_markup)
    return 1


async def wordle_difficulty(update, context):
    difficulty = DIFFICULTIES.get(update.message.text)
    if not difficulty:
        await update.message.reply_text(
            f'Нет сложности {difficulty}')
        return 1
    await update.message.reply_text(f'Выбрана сложность {update.message.text}')
    context.user_data["difficulty"] = difficulty

    if 'wordle_word' not in context.user_data:
        r = Wordnik()
        context.user_data['wordle_word'] = r.get_random_word(minLength=context.user_data["difficulty"][0],
                                                             maxLength=context.user_data["difficulty"][1])
        context.user_data['wordle_tries'] = []
        await update.message.reply_text(
            f'Wordle: слово {len(context.user_data["wordle_word"])} букв. {context.user_data["difficulty"][2]} попыток')

    return 2


def format_word(word, correct):
    new_word = ''
    for i, char in enumerate(word):
        if char == correct[i]:
            new_word += WORDLE_SYMBOLS['GREEN']
        elif char in correct:
            new_word += WORDLE_SYMBOLS['ORANGE']
        else:
            new_word += WORDLE_SYMBOLS['GRAY']
    return new_word


async def wordle_answer(update, context):
    ans = update.message.text
    if len(ans) != len(context.user_data['wordle_word']):
        await update.message.reply_text(f'В слове должно быть {len(context.user_data["wordle_word"])} букв')
        return 2
    context.user_data['wordle_tries'].append(ans)
    if ans == context.user_data['wordle_word']:
        await update.message.reply_text(f'Верно\n'
                                        f'Слово - {context.user_data["wordle_word"]}\n'
                                        f'Попыток - {len(context.user_data["wordle_tries"])}\\{context.user_data["difficulty"][2]}\n' +
                                        '\n'.join(format_word(word, context.user_data["wordle_word"]) for word in
                                                  context.user_data["wordle_tries"]))
        context.user_data['game'] = None
        return 2

    await update.message.reply_text(
        '\n'.join(format_word(word, context.user_data["wordle_word"]) for word in context.user_data["wordle_tries"]))
    if len(context.user_data['wordle_tries']) > context.user_data['difficulty'][2]:
        await update.message.reply_text('Вы не смогли угадать слово.\n'
                                        f'Слово: {context.user_data["wordle_word"]}\n'
                                        f'Попробовать еще раз? - /wordle')
        context.user_data['wordle_word'] = None
        context.user_data['wordle_tries'] = None
