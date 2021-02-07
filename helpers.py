import flask_login
from flask import  get_flashed_messages
from urllib.parse import urlparse, parse_qs
from flask import request
from flask import session as bsession


def pageparameters(pagename=None):

    themenu = [
        ('/', 'UI', 'view_comfy', True ),
        ('/device-cards', 'Devices', 'view_comfy', True),
        ('/message-tables', 'MessageTable', 'view_comfy', True),
        ('/login', 'Login', 'multiline_chart', False),
        ('index', 'Index', 'multiline_chart', False)
    ]

    params = {
        'loggedin': bool(flask_login.current_user.get_id()),
        'sitename': 'lolzor',
        'pagename': 'defaultname'
    }

    params.update({'menu': themenu, 'flashmessages': get_flashed_messages()})

    hist = historykeep(pagename)

    if flask_login.current_user.get_id():
        params.update({
            'history': hist,
            'useremail': flask_login.current_user.email,
            'userimage': flask_login.current_user.profile[0].pic_hash.decode('utf-8'),
            'username': flask_login.current_user.user_name,
            'messages': flask_login.current_user.messages,
            'messagelen': len(flask_login.current_user.messages),
            'profile': flask_login.current_user.profile[0]
        })
    return params

def historykeep(pagename):
    parsed = urlparse(request.url, '.')
    if 'history' in bsession:
        myses = bsession['history']
        baseurl = "{}://{}{}".format(parsed.scheme, parsed.netloc, parsed.path)
        if not myses or myses[-1:][0][0] != baseurl and pagename:
            myses.append((baseurl, pagename))
        if len(myses) > 6:
            myses = myses[1:]
        bsession['history'] = myses
    else:
        bsession['history'] = []

    return bsession['history'][:-1]
