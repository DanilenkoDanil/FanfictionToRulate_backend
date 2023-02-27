import time

from threading import Thread
from googletrans import Translator
from revChatGPT.V1 import Chatbot

thread_num = 2
translator = Translator()

account_list = list()

account_list.append(Chatbot(config={
  "email": "gtaforilona@gmail.com",
  "password": "Game45666"
}))
account_list.append(Chatbot(config={
  "email": "danilenkodanil.fb05@gmail.com",
  "password": "Game45666"
}))

if thread_num > len(account_list):
    print('Критическая ошибка! Аккаунтов меньше чем потоков!')
    input()


def packet_division(path: str) -> dict:
    with open(path, "r") as file:
        text = file.read()

    chunks = text.split('\n\n')

    packets = {}
    counter = 0
    current_packet = ''
    for chunk in chunks:
        if len(current_packet) > 450:
            packets[counter] = current_packet
            current_packet = ''
            counter += 1
        current_packet += chunk
    return packets


def ask_question(chat_bot, prompt: str):
    final_text = ''
    prev_text = ""
    for data in chat_bot.ask(prompt):
        message = data["message"][len(prev_text):]
        final_text += message
        prev_text = data["message"]
    return final_text


def translate(target_text, chat_bot):
    timer = time.time()
    prompt = f'Edit and improve the text, remove the tautology by replacing it with synonyms, remove lexical and grammatical errors, keeping the meaning without cutting or deleting anything:\n'
    prompt += target_text
    try:
        completion = ask_question(chat_bot, prompt)
    except Exception as e:
        print(e)
        print('ChatGPT Error!')
        time.sleep(63)
        completion = ask_question(chat_bot, prompt)
    if len(prompt) / 2 > len(completion):
        time.sleep(63)
        completion = ask_question(chat_bot, prompt)
    print(time.time() - timer)
    return translator.translate(dest='ru', text=completion).text


def packets_translate(packets: list, chat_bot):
    print('Поток пошёл')
    global packets_dict
    for packet in packets:
        try:
            print(f'Елемент - {packet} в работе!')
            try:
                packets_dict[packet] = translate(packets_dict[packet], chat_bot)
            except KeyError:
                continue
        except Exception as e:
            print(e)
            time.sleep(60)
            packets_dict[packet] = translate(packets_dict[packet], chat_bot)
        print(packets_dict)


packets_dict = packet_division('1.txt')
count_thread_packets = len(packets_dict) // thread_num
count_thread_packets += 1
result_list = []
for i, account in zip(range(thread_num), account_list):
    th = Thread(target=packets_translate,
                args=(
                    list(packets_dict.keys())[i * count_thread_packets:(i + 1) * count_thread_packets], account
                )
                )
    th.start()

result_text = ''
for i in packets_dict.values():
    result_text += i

with open("firstt.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
