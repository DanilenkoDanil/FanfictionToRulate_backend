﻿from urllib import request
import requests
import os
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from tg_bot_key import get_tg_api_key, get_login_data
from requests.auth import HTTPBasicAuth

login, password = get_login_data()
#data = {
#    "url": 'dat'
#}

#resp = requests.post('http://185.26.96.154/api/check_book/', json=data, auth=HTTPBasicAuth('Lazair', '9baY2jHszz3XqUy'))
#print(resp.json())

bot = Bot(token=get_tg_api_key())
dp = Dispatcher(bot, storage=MemoryStorage())

# books_lst = ['book1', 'book2', 'book3']
chapters = ['chap1', 'chap2', 'chap3']
books_state = ['chap1', 'chap2', 'chap3']
fandom = ['fandom1', 'fandom2', 'fandom3']
genre = ['genre1', 'genre2', 'genre3']
text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

but_parser = KeyboardButton('Спарсить')
but_translate = KeyboardButton('Перевести')  
but_download = KeyboardButton('Скачать')  
but_cancel = KeyboardButton('Отмена')
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(but_cancel)
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.row(but_parser, but_translate).add(but_download)


class TranslateFSM(StatesGroup):
    choose_book = State()
    choose_chapter = State()
    pars_book = State()
    fandom = State()
    genre = State()
    book_status = State()
    translate_chapter_num = State()
    send_chapter_text = State()


def dec_permission(func):
    async def user(message, state):
        if message.from_user.id not in [999]:
            print('Доступ получен')
            await func(message, state)
        else:
            print('Доступ запрещен')
            return False
    return user


@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
@dec_permission
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'OK', reply_markup=kb_main)


@dp.message_handler(Text(equals=['Перевести', 'Скачать'], ignore_case=True))
@dec_permission
async def choose_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['status'] = message.text
    books = requests.get('http://185.26.96.154/api/books/', auth=HTTPBasicAuth(login, password)).json()
    save_name_book = {}
    list_of_books = ''
    for book in books:
        list_of_books += f'{book["id"]}. {book["name"]} --- {book["genre"]} --- {book["fandom"]} --- {book["status"]}\n'
        save_name_book[str(book["id"])] = book["name"]
    async with state.proxy() as data:
        data['book_name'] = save_name_book
    if data['status'] == 'Перевести' or data['status'] == 'Скачать':
        await TranslateFSM.choose_chapter.set()
    await bot.send_message(message.from_user.id, f'Введи номер книги:\n\n{list_of_books}', reply_markup=kb_cancel)


@dp.message_handler(state=TranslateFSM.translate_chapter_num)
@dec_permission
async def send_translate_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['book'] = message.text[0]
    # books_state = get_book_state(data['book'])
    list_of_chapters = ''
    for i in books_state:
        list_of_chapters += f'{i}\n'
    await bot.send_message(message.from_user.id, f'Отправлено на перевод', reply_markup=kb_main)
    await state.finish()


@dp.message_handler(state=TranslateFSM.choose_chapter)
@dec_permission
async def choose_chapter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['book'] = message.text
    chapters = requests.get(f"http://185.26.96.154/api/chapters/{data['book']}/", auth=HTTPBasicAuth(login, password)).json()
    list_of_chapters = ''
    save_id = {}
    save_chapter_name = {}
    i = 1
    for chapter in chapters:
        list_of_chapters +=f'{i}. {chapter["name"]} --- {chapter["status"]} \n'       
        save_id[str(i)] = chapter["id"]
        save_chapter_name[str(i)] = chapter["name"]
        i += 1
        #list_of_chapters += f'{chapter["number"]}. {chapter["name"]} --- {chapter["status"]} \n'
        #save_id[chapter["number"]] = chapter["id"])
    async with state.proxy() as data:
        data['save_id'] = save_id
        data['chapter_name'] = save_chapter_name
    if data['status'] == 'Перевести':
        await TranslateFSM.translate_chapter_num.set()
    if data['status'] == 'Скачать':
        await TranslateFSM.send_chapter_text.set()
    await bot.send_message(message.from_user.id, f'Введи номер главы\n\n{list_of_chapters}')


@dp.message_handler(state=TranslateFSM.send_chapter_text)
@dec_permission
async def send_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chapter'] = message.text
    index = data['save_id'][data['chapter']]
    text_request = requests.get(f"http://185.26.96.154/api/chapter_text/{index}/", auth=HTTPBasicAuth(login, password)).json()
    text = text_request['text']
    index_book = data['book_name'][data['book']]
    index_chapter = data['chapter_name'][data['chapter']]
    file_name = f"{index_book}_{index_chapter}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)
    await bot.send_document(message.from_user.id, open(file_name, 'rb'))
    await bot.send_message(message.from_user.id, f'Вот твоя глава', reply_markup=kb_main)
    os.remove(file_name)
    await state.finish()


@dp.message_handler(Text(equals='Спарсить', ignore_case=True))
@dec_permission
async def translate_state(message: types.Message, state: FSMContext):
    await TranslateFSM.pars_book.set()
    await bot.send_message(message.from_user.id, f'Введи ссылку', reply_markup=kb_cancel)


@dp.message_handler(state=TranslateFSM.pars_book)
@dec_permission
async def download_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['book_link'] = message.text
    # check = check_book_in_bd(data[0])
    # if check is True:
    #     await bot.send_message(message.from_user.id, f'Эта книга уже есть!', reply_markup=kb_main)
    #     await state.finish()
    # else:
    list_of_fandom = ''
    for i in fandom:
        list_of_fandom += f'{i}\n'
    await TranslateFSM.fandom.set()
    await bot.send_message(message.from_user.id, f'{list_of_fandom}\nВведи номер фендома')


@dp.message_handler(state=TranslateFSM.fandom)
@dec_permission
async def choose_fandom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fandom'] = message.text
    list_of_genre = ''
    for i in genre:
        list_of_genre += f'{i}\n'
    await TranslateFSM.genre.set()
    await bot.send_message(message.from_user.id, f'{list_of_genre}\nВведи номер жанра')


@dp.message_handler(state=TranslateFSM.genre)
@dec_permission
async def choose_fandom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['genre'] = message.text
    await state.finish()
    await bot.send_message(message.from_user.id, f'Сделано ^^', reply_markup=kb_main)


@dp.message_handler(commands=['start'])
@dec_permission
async def start(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Started", reply_markup=kb_main)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
