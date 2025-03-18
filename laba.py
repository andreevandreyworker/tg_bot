import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Вопросы и ответы
questions = [
    {
        "question": "Какой цвет на флаге России?",
        "options": ["Оранжевый", "Чёрный", "Синий", "Зеленый"],
        "answer": 2  # Индекс правильного ответа (синий)
    },
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["8", "9", "7", "10"],
        "answer": 0
    },
    {
        "question": "Какой ученый разработал теорию относительности?",
        "options": ["Ньютона", "Эйнштейна", "Коперника", "Галилея"],
        "answer": 1
    },
    {
        "question": "Какой элемент имеет химический символ O?",
        "options": ["Золото", "Кислород", "Серебро", "Олово"],
        "answer": 1
    },
    {
        "question": "Какой континент является самым большим?",
        "options": ["Австралия", "Евразия", "Африка", "Северная Америка"],
        "answer": 1
    },
]


# Начало игры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Добро пожаловать в игру 'Кто хочет стать миллионером?!'.\n"
        "Нажмите /play, чтобы начать!"
    )


# Запуск игры
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['score'] = 0
    context.user_data['question_index'] = 0
    await ask_question(update, context)


# Задание вопроса
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question_index = context.user_data['question_index']

    if question_index >= len(questions):  # Защита от выхода за пределы массива
        await update.callback_query.message.reply_text("Нет доступных вопросов.")
        return

    question_data = questions[question_index]

    options = question_data['options']
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=str(i)) for i, opt in enumerate(options)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверка на наличие у update.message или у update.callback_query.message
    if update.callback_query:
        await update.callback_query.message.reply_text(question_data['question'], reply_markup=reply_markup)
    else:
        await update.message.reply_text(question_data['question'], reply_markup=reply_markup)


# Обработка ответа
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    question_index = context.user_data['question_index']
    question_data = questions[question_index]

    if int(query.data) == question_data['answer']:
        context.user_data['score'] += 1
        await query.edit_message_text(text=f"Правильно! Ваш текущий счёт: {context.user_data['score']}")
    else:
        await query.edit_message_text(
            text=f"Неправильно! Правильный ответ: {question_data['options'][question_data['answer']]}\n"
                 f"Ваш окончательный счёт: {context.user_data['score']}"
        )
        return  # Завершение игры

    context.user_data['question_index'] += 1
    if context.user_data['question_index'] < len(questions):
        await ask_question(update, context)  # Здесь мы передаём update
    else:
        await query.edit_message_text(
            text=f"Игра окончена! Вы МИЛЛИОНЕР!! Ваш окончательный счёт: {context.user_data['score']}"
        )


def main():
    # Вставьте свой токен Telegram бота
    token = "7575730429:AAGbg258ShMFDnlSfRQH1GkrJeK96gzCW-0"  # Замените на ваш токен
    application = ApplicationBuilder().token(token).build()

    # Определяем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CallbackQueryHandler(answer))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()