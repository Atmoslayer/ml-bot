import vk_api
import os
import logging

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')

    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            logging.info('Новое сообщение:')
            if event.to_me:
                logging.info(f'Для меня от: {event.user_id}')
            else:
                logging.info(f'От меня для: {event.user_id}')
            logging.info(f'Текст: {event.text}')