from extensions import db
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer, String
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import fields, reqparse, marshal_with


class UserModel(db.Model):
    __tablename__ = 'user'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password:Mapped[str] = mapped_column(String, nullable=False)
    pnumber:Mapped[str]

    olddaychick =relationship('OldDayChickModel', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(password=password)


class OldDayChickModel(db.Model):
    __tablename__ = 'oldday'

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    order_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    preffered_date: Mapped[datetime] = mapped_column(nullable=False)
    chick_type: Mapped[str] = mapped_column(String, nullable=False)
    breed_type: Mapped[str] = mapped_column(String, nullable=False) 

    user = relationship('UserModel', back_populates='olddaychick')

