import os
import string
from datetime import datetime
from random import SystemRandom
from utils import load_config
from mailer import sendSignInMagicLink
# from multiprocessing import Process, Manager
# from time import sleep

# TODO: it'll be easier to scale with uWSGI if this file were built
#       as its own image and container run with only 1 replica
# TODO: store sessions in a Manager instance to enable multiprocessing
# TODO: load sessions from disk on startup

unverified_sessions = {}
sessions = {}
session_insert_queue = []

def create_token(length=192):
    return ''.join([SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(length)])

def create_session(account_email):
    # TODO: no-op this function for suspicious and blocked email addresses
    # TODO: check if email looks valid before trying to send a sign-in link
    token = create_token()
    sendSignInMagicLink(account_email, token)
    now = datetime.now()
    unverified_sessions[token] = {
        'created_at': now,
        'verified_at': None,
        'last_seen_at': now,
        'account_email': account_email,
    }
    return None

def authenticate_session(tmp_token):
    if tmp_token in unverified_sessions:
        session = unverified_sessions[tmp_token]
        token = create_token()
        session['verified_at'] = datetime.now()
        sessions[token] = session
        del unverified_sessions[tmp_token]
        return token
    return None

def refresh_session(prev_token):
    if prev_token in sessions:
        token = create_token()
        sessions[token] = sessions[prev_token]
        del unverified_sessions[prev_token]
        return token
    return None

def verify_session(token):
    return token in sessions

def get_session(token):
    if token in sessions:
        return sessions[token]
    return None

def delete_session(token):
    if token in sessions:
        del sessions[token]
    return None

# This creates a desync between actual unverified sessions and those in shared memory.
# Must wrap this file in the `with Manager()` call in order to share state.
# def truncate_expired_sessions(wrapper):
#     while True:
#         now = datetime.now()
#         config = load_config()
#         for k, v in wrapper['unverified_sessions'].items():
#             if v['verified_at'] is None and now - v['created_at'] > config['magic_link_max_age']:
#                 del wrapper['unverified_sessions'][k]
#         sleep(config['session_recycle_interval'])

# with Manager() as manager:
#     wrapper = manager.dict()
#     wrapper['unverified_sessions'] = unverified_sessions
#     loop = Process(target=truncate_expired_sessions, args=(wrapper))
#     loop.start()
#     loop.join()
