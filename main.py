import telebot
from telebot import types
import openai
from openai import OpenAI
import requests
from deep_translator import GoogleTranslator

token = '6859864173:AAHOQlg-Amjvth-tK8hr8jvaRKNS1UrRh4g'
bot = telebot.TeleBot(token)
client = OpenAI(
    api_key="sk-Wt_ftNYg9TNJcnFJ3jfAmgT5lyqiifi0ThC7kYgrbQT3BlbkFJ8JQdimGrtKrNuiiE_dmeozWY8tOZbJpbvKiuroD_QA")
global messages
messages = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    global messages
    global id
    id = message.from_user.id
    if not message.from_user.id in messages:
        messages[message.from_user.id] = []
    keyboard = types.InlineKeyboardMarkup()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новая игра")
    markup.row(item1)
    bot.send_message(message.chat.id,
                     'Здравствуйте! Я бот-помощник для проведения D&D партий. Для запуска новой игры, нажмите кнопку "Новая игра". Для добавления нового события, напишите команду /new_event и опишите событие',
                     reply_markup=markup)
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system",
                   "content": "You are a D&D game master. Each of your messages should be based on the following points: What the players see and What's going on around the players. Use no more than 100 characters for each stage.  The players will name their actions."},
                  {"role": "user", "content": "Describe start position"}]
    )
    messages[message.from_user.id] = [{"role": "system",
                                       "content": "You are a D&D game master. Each of your messages should be based on the following points. What the players see and What's going on around the players. Use no more than 100 characters for each stage.  The players will name their actions."},
                                      {"role": "user", "content": "Describe start position"}]
    response = client.images.generate(
        prompt=completion.choices[0].message.content,
        n=1,
        size="256x256",
    )
    image_url = response.data[0].url
    bot.send_message(message.chat.id,
                     GoogleTranslator(source='auto', target='russian').translate(completion.choices[0].message.content),
                     reply_markup=keyboard)
    bot.send_photo(message.chat.id, image_url)
    messages[message.from_user.id].append({"role": "assistant", "content": completion.choices[0].message.content})


@bot.message_handler(content_types=['text'])
def message_reply(message):
    keyboard = types.InlineKeyboardMarkup()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text[0:10] == "/new_event":
        print("cmdjkcvnedjvndf")
        messages[message.from_user.id].append({"role": "assistant", "content": GoogleTranslator(source='russian', target='english').translate(message.text[10:])})
        bot.send_message(message.from_user.id,
                         "Теперь напишите действия игроков",
                         reply_markup=keyboard)
        return
    if message.text == "Новая игра":
        keyboard = types.InlineKeyboardMarkup()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        messages[id].clear()
        print(messages)
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "system",
                       "content": "You are a D&D game master. Each of your messages should be based on the following points. What the players see and What's going on around the players. Use no more than 100 characters for each stage.  The players will name their actions."},
                      {"role": "user", "content": "Describe start position"}]
        )
        messages[message.from_user.id] = [{"role": "system",
                                           "content": "You are a D&D game master. Each of your messages should be based on the following points. What the players see and What's going on around the players. Use no more than 100 characters for each stage.  The players will name their actions."},
                                          {"role": "user", "content": "Describe start position"}]
        response = client.images.generate(
            prompt=completion.choices[0].message.content,
            n=1,
            size="256x256",
        )
        image_url = response.data[0].url
        bot.send_message(message.from_user.id,
                         GoogleTranslator(source='auto', target='russian').translate(
                             completion.choices[0].message.content),
                         reply_markup=keyboard)
        bot.send_photo(message.from_user.id, image_url)
        messages[message.from_user.id].append({"role": "assistant", "content": completion.choices[0].message.content})
        return
    messages[message.from_user.id].append(
        {"role": "user", "content": GoogleTranslator(source='russian', target='english').translate(message.text)})
    print(messages)
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages[message.from_user.id]
    )

    chat_response = completion.choices[0].message.content
    response = client.images.generate(
        prompt=chat_response,
        n=1,
        size="256x256",
    )
    image_url = response.data[0].url
    bot.send_message(message.chat.id,
                     GoogleTranslator(source='auto', target='russian').translate(chat_response),
                     reply_markup=keyboard)
    bot.send_photo(message.chat.id, image_url)
    messages[message.from_user.id].append({"role": "assistant", "content": completion.choices[0].message.content})


@bot.message_handler(commands=['new_ivent'])
def new_event(message):
    print(message)

bot.infinity_polling()
