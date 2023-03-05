import time
from threading import Thread
from googletrans import Translator
from revChatGPT.V1 import Chatbot
from base.models import Chapter, Setting, ChatGPTCredentials
from background_task import background


translator = Translator()
packets_dict = dict()


def packet_division(text: str) -> dict:
    print(text)
    chunks = text.split('\n')

    packets = {}
    counter = 0
    current_packet = ''
    for chunk in chunks:
        if len(current_packet) > 450:
            packets[counter] = current_packet
            current_packet = ''
            counter += 1
        current_packet += chunk
    packets[counter] = current_packet
    return packets


def ask_question(chat_bot, prompt: str):
    final_text = ''
    prev_text = ""
    for data in chat_bot.ask(prompt):
        message = data["message"][len(prev_text):]
        final_text += message
        prev_text = data["message"]
    return final_text


def translate(target_text, chat_bot) -> str:
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


def packets_translate(packets: list, chat_bot) -> None:
    print('Поток пошёл')
    global packets_dict
    for packet in packets:

        print(f'Елемент - {packet} в работе!')
        try:
            try:
                packets_dict[packet] = translate(packets_dict[packet], chat_bot)
            except KeyError:
                continue
        except Exception as e:
            print(e)
            time.sleep(30)
            packets_dict[packet] = translate(packets_dict[packet], chat_bot)
        print(packets_dict)


@background
def translate_chapter(chapter_id):
    global packets_dict
    try:
        settings = Setting.objects.get(id=1)
    except Setting.DoesNotExist:
        return False
    try:
        chapter = Chapter.objects.get(id=chapter_id)
    except Chapter.DoesNotExist:
        return False

    thread_num = settings.threads

    account_counter = 0
    account_list = []
    for account in ChatGPTCredentials.objects.all():
        if len(account_list) >= thread_num:
            break
        account_counter += 1

        account_list.append(Chatbot(config={
          "email": account.login,
          "password": account.password
        }))

    if thread_num > len(account_list):
        print('Критическая ошибка! Аккаунтов меньше чем потоков!')
        return False

    packets_dict = packet_division(chapter.text)
    print(packets_dict)
    count_thread_packets = len(packets_dict) // thread_num
    count_thread_packets += 1

    threads = []

    for i, account in zip(range(thread_num), account_list):
        print(i)
        th = Thread(target=packets_translate,
                    args=(
                        list(packets_dict.keys())[i * count_thread_packets:(i + 1) * count_thread_packets], account
                    )
                    )
        th.start()
        threads.append(th)

    for t in threads:
        t.join()

    result_text = ''
    for i in packets_dict.values():
        result_text += i
    print('----------------')
    print(result_text)

    if len(chapter.text) // 2 < len(result_text):
        chapter.text = result_text
        chapter.save()
