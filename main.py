import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from configparser import ConfigParser

config = ConfigParser()  # почему иногда не реагирует на первые сообщения   как отключить изначально созданную клавиатуру
config.read('config.ini')

vk_session = vk_api.VkApi(token=config['VK']['token_new'])
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def sender(id, text):
    print(id, text)
    vk.messages.send(
        user_id=id,
        random_id=0,
        keyboard=VkKeyboard.get_empty_keyboard(),
        message=text
    )


def adder(x):
    file = open('data.txt', 'a', encoding='utf-8')
    file.write(f'{x}\n')
    file.close()


def check(a):
    file = open('data.txt', 'r', encoding='utf-8')
    if str(a) not in file.read():
        return True
    file.close()


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            # print(event.__dict__)
            mess = event.text.lower()
            id = event.user_id
            if mess.lower() == 'привет':
                sender(id, 'hi')
                if check(id):
                    adder(id)
            else:
                sender(id,
                       'Я не могу понять Ваше сообщение(\nСкоро админ ответит на все ваши вопросы)')
