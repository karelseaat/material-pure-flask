#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import create_engine
from models import *
from faker import Faker
import os
from dbsession import sqlitefilename
import base64
import requests
import time

if os.path.exists(sqlitefilename):
    os.remove(sqlitefilename)

from dbsession import make_session
import json

def random_message(message):
    faker = Faker()
    message.title = faker.name().split(" ")[0]
    message.created = faker.date_time_this_century()
    message.content = faker.text()
    return message

def random_user(user, profile):
    faker = Faker()
    user.pic_hash = faker.md5()
    user.developper = faker.boolean()
    user.super_user = faker.boolean()
    user.user_name = faker.name().split(" ")[0]
    password = faker.password(length=6, special_chars=False, digits=True, upper_case=False, lower_case=True)

    user.password_hash = User.generate_hash(password)
    profile.first_name = faker.name().split(" ")[0]
    user.last_seen = faker.date_time_this_century()
    user.created_at = faker.date_time_this_century()
    user.verified_at = faker.date_time_this_century()
    user.last_ip = faker.ipv4()
    profile.sur_name = faker.name().split(" ")[1]
    response = requests.get('https://placeimg.com/80/80/any')
    encoded_string = base64.b64encode(response.content)
    profile.pic_hash = encoded_string
    user.profile.append(profile)
    user.email = faker.email()
    time.sleep(1)
    return user, (user.email, password)



session = make_session()

# test = session.query(User).all()

# group = random_group(Group())

f = open("usernamesandpass.txt", "w")
longtxt = ""
for value in range(10):

    # for value in range(10):
    #     atag = random_tags(Tag())
    #     session.add(atag)

    message = random_message(Message())
    auser, sometext = random_user(User(), UserProfile())
    longtxt += "{} - {}\n".format(*sometext)

    auser.messages.append(message)
    session.add(auser)

f.write(longtxt)

session.commit()

session.close()
