import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser

config = ConfigParser()         #почему иногда не реагирует на первые сообщения   как отключить изначально созданную клавиатуру
config.read('config.ini')

vk_session = vk_api.VkApi(token=config['VK']['token_new'])
longpoll = VkLongPoll(vk_session)
vk_session._auth_token()

def sender(id, text):
    vk_session.method('messages.send', {'user_id':id, 'message':text, 'random_id': 0})

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
                sender(id, 'Я не могу понять Ваше сообщение(\nСкоро админ ответит на все ваши вопросы)')

