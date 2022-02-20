from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from db_requests import Candidate, Photo


with open('VK_token.txt', 'r') as file_object:
    token = file_object.read().strip()

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

db = 'postgresql://postgres:ChobaniukBogdan1994@localhost:5432/VKinder_v1'
engine = sq.create_engine(db)
Session = sessionmaker(bind=engine)
connection = engine.connect()
session = Session()


def write_msg(user_id, message, attachment):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment, 'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}", None)
            elif request == "пришли кандидатов":
                write_msg(event.user_id, "Лови:", None)
                q = session.query(Candidate).order_by(Candidate.id)
                for c in q:
                    p = session.query(Photo).filter_by(id_candidate=c.id).first()
                    write_msg(event.user_id, f"{c.first_name} {c.second_name} \n {c.profile_url}", f'{p.photo}')
            elif request == "пока":
                write_msg(event.user_id, "Пока((", None)
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", None)
