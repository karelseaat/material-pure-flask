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

def random_device(device):
    fake = Faker()
    device.name = fake.name().split(" ")[0]
    device.created_at = fake.date_time_this_century()
    device.last_seen = fake.date_time_this_century()
    device.last_ip = fake.ipv4()
    device.soft_version = "1.1.2"
    device.hard_version = "2.1"
    device.mac = fake.text(max_nb_chars=12)
    return device

def random_group(group):
    faker = Faker()
    group.name = faker.name().split(" ")[0]
    return group

def random_tags(tag):
    faker = Faker()
    tag.name = faker.name().split(" ")[0]
    return tag

def random_device_type(device_type):
    fake = Faker()
    device_type.name = fake.name().split(" ")[0]
    device_type.soft_version = str(fake.pyfloat(min_value=0, max_value=5,right_digits=5))
    device_type.hard_version = str(fake.pyfloat(min_value=0, max_value=5,right_digits=5))
    return device_type

def random_node_schema(node_schema):
    fake = Faker()
    d = dict()
    d['first_name'] = fake.first_name()
    d['last_name'] = fake.last_name()
    d['personal_email'] =  fake.email()
    d['ssn'] = fake.ssn()
    node_schema.name = fake.name().split(" ")[0]
    node_schema.schema = json.dumps(d)
    node_schema.location = json.dumps(d)
    return node_schema

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



f = open("usernamesandpass.txt", "w")
longtxt = ""
for value in range(10):


    atag1 = random_tags(Tag())
    atag2 = random_tags(Tag())
    adevice_type = random_device_type(DeviceType())

    group = random_group(Group())
    message = random_message(Message())
    auser, sometext = random_user(User(), UserProfile())
    device = random_device(Device())
    longtxt += "{} - {}\n".format(*sometext)
    device.tags.append(atag1)
    device.tags.append(atag2)
    device.device_type = adevice_type
    anode_schema = random_node_schema(Node_schema())
    auser.node_schemas.append(anode_schema)
    auser.devices.append(device)
    auser.messages.append(message)
    auser.groups.append(group)
    session.add(auser)

f.write(longtxt)

session.commit()

session.close()
