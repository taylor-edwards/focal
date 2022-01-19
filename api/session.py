import os
import string
from datetime import datetime
from random import SystemRandom
from utils import load_config
from mailer import sendSignInMagicLink

unverified_sessions = {}
sessions = {}
session_insert_queue = []

def create_token(length=192):
    return ''.join([SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(length)])

def create_session(account_email):
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
