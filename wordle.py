import random_word

WORDLE_SYMBOLS = {
    'ORANGE': '🟧',
    'GRAY': '⬛',
    'GREEN': '🟩'
}

TRIES = 6


async def wordle(update, context):
    if 'wordle_word' not in context.user_data:
        r = random_word.RandomWords()
        context.user_data['wordle_word'] = r.get_random_word()
        context.user_data['wordle_tries'] = []
        await update.message.reply_text(
            f'Wordle: слово {len(context.user_data["wordle_word"])} букв. {TRIES} попыток')
    return 1


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
    await update.message.reply_text(context.user_data['wordle_word'])
    if len(ans) != len(context.user_data['wordle_word']):
        await update.message.reply_text(f'В слове должно быть {len(context.user_data["wordle_word"])} букв')
        return 1
    context.user_data['wordle_tries'].append(ans)
    if ans == context.user_data['wordle_word']:
        await update.message.reply_text(f'Верно\n'
                                        f'Слово - {context.user_data["wordle_word"]}\n'
                                        f'Попыток - {len(context.user_data["wordle_tries"])}\\{TRIES}\n' +
                                        '\n'.join(format_word(word, context.user_data["wordle_word"]) for word in
                                                  context.user_data["wordle_tries"]))
        context.user_data['game'] = None
        return 1

    await update.message.reply_text(
        '\n'.join(format_word(word, context.user_data["wordle_word"]) for word in context.user_data["wordle_tries"]))
    if len(context.user_data['wordle_tries']) > TRIES:
        await update.message.reply_text('Вы не смогли угадать слово.\n'
                                        f'Слово: {context.user_data["wordle_word"]}\n'
                                        f'Попробовать еще раз? - /wordle')
        context.user_data['wordle_word'] = None
        context.user_data['wordle_tries'] = None
