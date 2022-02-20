from pprint import pprint
import sqlalchemy as sq
from sqlalchemy import exists
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from datetime import datetime

from VKinder_class import token, VKinder

db = 'postgresql://postgres:ChobaniukBogdan1994@localhost:5432/VKinder_v1'
engine = sq.create_engine(db)
Session = sessionmaker(bind=engine)
connection = engine.connect()
session = Session()
# session.close()

Base = declarative_base()


class Candidate(Base):
    __tablename__ = 'candidate'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    second_name = sq.Column(sq.String)
    first_name = sq.Column(sq.String)
    bday = sq.Column(sq.String)  # настроить декоратор
    sex = sq.Column(sq.Integer)
    city = sq.Column(sq.String)
    status = sq.Column(sq.Integer)
    profile_url = sq.Column(sq.String)
    input_date = sq.Column(sq.Date)
    sent_to_user = sq.Column(sq.String)
    photos = relationship('Photo', back_populates='candidate', cascade='all, delete, delete-orphan')


class Photo(Base):
    __tablename__ = 'photo'

    id = sq.Column(sq.Integer, primary_key=True)
    photo = sq.Column(sq.String)
    likes = sq.Column(sq.Integer)
    id_candidate = sq.Column(sq.Integer, sq.ForeignKey('candidate.id'))
    candidate = relationship('Candidate', back_populates='photos')


Base.metadata.create_all(engine)

vk = VKinder(token, '5.130')
candidates_list = vk.candidates_list()
for candidate in candidates_list:
    stmt = session.query(exists().where(Candidate.vk_id == candidate['vk_id'])).scalar()
    if stmt == True:
        continue
    else:
        new_candidate = Candidate(
            vk_id=candidate['vk_id'],
            second_name=candidate['last_name'],
            first_name=candidate['first_name'],
            bday=candidate['bdate'],
            sex=candidate['sex'],
            city=candidate['city'],
            status=candidate['status'],
            profile_url=candidate['profile_url'],
            input_date=datetime.today(),
            sent_to_user='No')
        photos_list = []
        for photo in candidate['photos']:
            new_photo = Photo(
                photo=photo['url'],
                likes=photo['likes']
            )
            photos_list.append(new_photo)
        new_candidate.photos = photos_list
        session.add(new_candidate)
    session.commit()

# session.delete(session.get(Candidate, 34))
# session.commit()
# print(session.query(Candidate).first().second_name)

