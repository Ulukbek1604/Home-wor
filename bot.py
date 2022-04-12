from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from decouple import config
import random

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
ADMIN = 1155154067
# '🎲', '🎰', "🎯", "🏀", "🎳"

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, f"Салам хозяин {message.from_user.full_name}")

# @dp.message_handler(commands=['help'])
# async def help(message: types.Message):
#     await bot.send_message(message.chat.id, )



@dp.message_handler(commands=['mem'])
async def problem_1(message: types.Message):
    photo = open('media/photo_2022-04-09_15-00-02.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=photo)


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    question = "Какого типа данных не существует в Python?"
    answers = ['int', 'str', 'elif', 'tuple']
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2
                        )


@dp.message_handler(commands=['problem'])
async def problem_1(message: types.Message):
    murkup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "NEXT",
        callback_data="button_call_1"
    )
    murkup.add(button_call_1)

    photo = open("media/img.png", "rb")
    await bot.send_photo(message.chat.id, photo=photo)

    question = "Output:"
    answers = ["[2, 4]", '[2, 4, 6]', '[2]', '[4]', '[0]', "Error"]
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=5,
                        open_period=5,
                        reply_markup=murkup
                        )



@dp.callback_query_handler(lambda func: func.data == "button_call_1")
async def problem_2(call: types.CallbackQuery):
    photo = open("media/photo_2022-04-06_19-41-01.jpg", "rb")
    await bot.send_photo(call.message.chat.id, photo=photo)

    question = "Output:"
    answers = "Error 4,2 2,4".split()
    await bot.send_poll(call.message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2,
                        open_period=5,
                        )
@dp.callback_query_handler(lambda func: func.data == "button_call_1")
async def problem_2(call: types.CallbackQuery):
    photo = open("media/img_1.png", "rb")
    await bot.send_photo(call.message.chat.id, photo=photo)

    question = "Output:"
    answers = "Error 4,2 2,4".split()
    await bot.send_poll(call.message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2,
                        open_period=5,
                        )

@dp.message_handler(content_types=["text"])
async def echo_message(message: types.Message):

    # Check bad words
    bad_words = "java bitch дурак балбес эшек".split()

    for i in bad_words:
        if i in message.text.lower():
            await message.delete()
            await bot.send_message(message.chat.id,
                           f"{message.from_user.full_name}, сам ты {i}!!!"
                           )

    # Send dice
    if message.text.lower() == 'dice':
        await bot.send_dice(message.chat.id, "🎲")


    # pin message
    if message.text.startswith('!pin'):
        if not message.reply_to_message:
            await message.reply('Команда должна быть ответом на сообщение!')
        else:
            await bot.pin_chat_message(message.chat.id, message.message_id)
    # Send game
    if message.text.lower() == 'game':
        result1: message = await bot.send_dice("🎲")
        result2: message = await bot.send_dice("🎲")
        if result1 == result2:
            await bot.send_message(message.chat.id, 'Ничья')
        elif result1 < result2:
            await bot.send_message(message.chat.id, f'You loose')
        else:
            await bot.send_message(message.chat.id, f'{message.from_user.full_name} Win')


@dp.message_handler(commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id != ADMIN:
            await message.reply("Ты не мой БОСС!")

        if not message.reply_to_message:
            await message.reply("Команда должна быть ответом на сообщение!")

        else:
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.bot.kick_chat_member(message.chat.id, user_id=message.reply_to_message.from_user.id)
            await bot.send_message(
                message.chat.id,
                f"{message.reply_to_message.from_user.full_name} забанен по воле {message.from_user.full_name}")


    else:
        await message.answer("Это работает только в группах!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
