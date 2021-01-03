# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Text, text, Table, Boolean, BigInteger,Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import time
from sqlalchemy.orm.session import Session
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import mapper
from sqlalchemy import event
import datetime

Base = declarative_base()
metadata = Base.metadata
from sqlalchemy.dialects import postgresql, mysql, sqlite
from sqlalchemy_utils import get_hybrid_properties
from sqlalchemy.ext.hybrid import hybrid_property

class DictSerializableMixin(Base):
    __abstract__ = True

    def _asdict(self):
        result = dict()

        for key in self.__mapper__.c.keys() + list(get_hybrid_properties(self).keys()):
            result[key] = getattr(self, key)
        return result

    def _asattrs(self, adict, filter):
        for key, val in adict.items():
            if hasattr(self, key) and key in filter:
                setattr(self, key, val)

# class RevokedTokenModel(DictSerializableMixin):
#     __tablename__ = 'revoked_tokens'
#     id = Column(Integer, primary_key = True)
#     jti = Column(String(120))
#
#     def add(self):
#         db.session.add(self)
#         db.session.commit()
#
#     @classmethod
#     def is_jti_blacklisted(self, jti):
#         query = self.query.filter_by(jti = jti).first()
#         return bool(query)


# user_group = Table('user_group', Base.metadata,
#     Column('user_id', BigInteger, ForeignKey('User.id')),
#     Column('group_id', BigInteger, ForeignKey('Group.id'))
# )
#
# tag_all = Table('tag_all', Base.metadata,
#     Column('tag_id', Integer, ForeignKey('tag.id')),
#     Column('device_id', Integer, ForeignKey('Device.id')),
#     Column('node_schema_id', Integer, ForeignKey('Node_schema.id'))
# )
#
# device_node_schema = Table('device_node_schema', Base.metadata,
#     Column('device_id', BigInteger, ForeignKey('Device.id')),
#     Column('node_schema_id', BigInteger, ForeignKey('Node_schema.id'))
# )
#
class User():
    pass

class UserSetting(DictSerializableMixin):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), index=True)
    user = relationship('User', back_populates="setting")



# class Node_schema(DictSerializableMixin):
#     __tablename__ = 'Node_schema'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     schema = Column(Text())
#     locations = Column(Text())
#     user_id = Column(ForeignKey('User.id'), index=True)
#     device_type_id = Column(ForeignKey('device_type.id'), nullable=False, index=True)
#     device_type = relationship('DeviceType', back_populates="node_schema")
#     user = relationship('User', back_populates="node_schemas")
#     devices = relationship("Device", secondary=device_node_schema, back_populates="node_schemas")
#     tags = relationship("Tag", secondary=tag_all, back_populates="node_schemas")

class UserProfile(DictSerializableMixin):
    __tablename__ = 'UserProfile'

    id = Column(Integer, primary_key=True)
    pic_hash = Column(String(100))
    first_name = Column(String(100))
    sur_name = Column(String(100))
    user_id = Column(ForeignKey('User.id'), index=True)
    user = relationship('User', back_populates="profile")

    def user_image(self):
        return self.pic_hash.decode('utf-8')


class User(DictSerializableMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    developper = Column(Boolean)
    super_user = Column(Boolean)
    user_name = Column(String(100), nullable=False)
    password_hash = Column(String(100), nullable=False)
    last_seen = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    verified_at = Column(TIMESTAMP)
    last_ip = Column(String(18))
    email = Column(String(100))
    is_active = True
    # node_schemas = relationship('Node_schema', back_populates="user")
    messages = relationship('Message', cascade="all, delete-orphan", back_populates="user", lazy='joined')
    setting = relationship('UserSetting', cascade="all, delete-orphan", back_populates="user")
    # devices = relationship('Device', back_populates="user")
    # leading = relationship('Group', cascade="all, delete-orphan", back_populates="leader")
    # groups = relationship("Group", secondary=user_group, back_populates="members")
    profile = relationship('UserProfile', cascade="all, delete-orphan", back_populates="user", lazy='joined')

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


# class DeviceType(DictSerializableMixin):
#     __tablename__ = 'device_type'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     soft_version = Column(String(100))
#     hard_version = Column(String(100))
#     device = relationship('Device', back_populates="device_type")
#     node_schema = relationship('Node_schema', back_populates="device_type")
#
#
# class Tag(DictSerializableMixin):
#     __tablename__ = 'tag'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     devices = relationship("Device", secondary=tag_all, back_populates="tags")
#     node_schemas = relationship("Node_schema", secondary=tag_all, back_populates="tags")
#
#
# # from sqlalchemy.orm import column_property
#
# class Device(DictSerializableMixin):
#     __tablename__ = 'Device'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     created_at = Column(TIMESTAMP)
#     last_seen = Column(TIMESTAMP)
#     last_ip = Column(String(18))
#     mac = Column(String(12))
#     user_id = Column(ForeignKey('User.id'), index=True)
#     device_type_id = Column(ForeignKey('device_type.id'), nullable=False, index=True)
#     device_type = relationship('DeviceType', back_populates="device")
#     user = relationship('User', back_populates="devices")
#     node_schemas = relationship("Node_schema", secondary=device_node_schema, back_populates="devices")
#     tags = relationship("Tag", secondary=tag_all, back_populates="devices")

    # @hybrid_property
    # def created_at_unix(self):
    #     return self.created_at.timestamp()

    # @hybrid_property
    # def last_seen_unix(self):
    #     return self.created_at.timestamp()

class Message(DictSerializableMixin):
    __tablename__ = 'Message'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    created = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    user_id = Column(ForeignKey('User.id'), index=True)
    user = relationship('User', back_populates="messages", lazy='joined')
#
#
# class Group(DictSerializableMixin):
#     __tablename__ = 'Group'
#
#     id = Column(Integer, primary_key=True)
#     leader_id = Column(ForeignKey('User.id'), index=True)
#     name = Column(String(100))
#     leader = relationship("User", back_populates="leading")
#     members = relationship("User", secondary=user_group, back_populates="groups")
