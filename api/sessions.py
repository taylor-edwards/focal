import os
from datetime import datetime
from random import SystemRandom
from time import sleep
from base64 import b64encode, b64decode
import bcrypt
import string

from utils import del_prop, load_config
from mailer import sendSignInMagicLink

# TODO: store sessions in a Manager instance to enable multiprocessing
unverified_sessions = {}
sessions = {}
session_insert_queue = []

def create_token():
    return ''.join([SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(128)])

def hash_text(text):
    return bcrypt.hashpw(text.encode(), bcrypt.gensalt(rounds=10)).decode()

def encode_bearer_token(email, token):
    return b64encode(f'{token}:{email}'.encode('utf-8')).decode('utf-8')

def decode_bearer_token(bearer_token):
    token_email_pair = b64decode(bearer_token).decode('utf-8')
    idx = token_email_pair.index(':')
    token = token_email_pair[0:idx]
    email = token_email_pair[idx + 1:len(token_email_pair)]
    return (email, token)

def create_htpasswd_line(email, token):
    return f"{token}:{hash_text(email)}\n"

def create_session(email):
    # TODO: no-op this function for suspicious and blocked email addresses
    # TODO: check if email looks valid before trying to send a sign-in link
    bearer_token = encode_bearer_token(email, create_token())
    sendSignInMagicLink(email, bearer_token)
    # if sending didn't fail, commit the temporary session to memory only
    now = datetime.now()
    unverified_sessions[bearer_token] = {
        'created_at': now,
        'verified_at': None,
        'last_seen_at': now,
        'account_email': email
    }
    # Do NOT return `unverified_token`! Users must receive their verification by email.

def verify_session(bearer_token):
    # TODO: no-op this function for blocked IPs
    if bearer_token in unverified_sessions:
        session = unverified_sessions[bearer_token]

        # "consume" this token and delete it now that it's being used to verify a session
        # TODO: allow retrying once or twice and ban senders with more than X failed attempts
        del unverified_sessions[bearer_token]

        token = create_token()
        # TODO: use account role and multiple htpasswd files to enable tiered authorization
        append_htpasswd(session['account_email'], token)

        # since the write succeeded, create the session in memory and return the usable token
        session['verified_at'] = datetime.now()
        sessions[token] = session

        # this is the token a client can use with the basic auth HTTP header
        # ```Authorization: Basic bearer <token>```
        bearer_token = encode_bearer_token(session['account_email'], token)
        return bearer_token

def delete_session(bearer_token):
    (email, token) = decode_bearer_token(bearer_token)
    if token in sessions and sessions[token]['account_email'] == email:
        omit_htpasswd(email, token)
        del_prop(sessions, token)

def append_htpasswd(email, token):
    line = create_htpasswd_line(email, token)
    config = load_config()
    if os.path.isfile(config['session_lockfile']):
        session_insert_queue.append(line)
        # stall the response until the line is consumed or it times out
        now = datetime.now()
        while line in session_insert_queue:
            if now - datetime.now() > config['htpasswd_timeout']:
                session_insert_queue.remove(l)
                raise TimeoutError('Timed out creating session')
            sleep(config['htpasswd_retry_interval'])
    else:
        with open(config['htpasswd_path'], 'a') as file:
            file.write(line)

def omit_htpasswd(email, token):
    # only omit one password at a time
    line = create_htpasswd_line(email, token)
    config = load_config()
    # stall the response until the line is consumed or it times out
    now = datetime.now()
    while os.path.isfile(config['session_lockfile']):
        if now - datetime.now() > config['htpasswd_timeout']:
            raise TimeoutError('Timed out deleting session')
        sleep(config['htpasswd_retry_interval'])

    with open(config['htpasswd_path'], 'r') as in_file:
        with open(config['session_lockfile'], 'w') as out_file:
            for l in in_file:
                if l != line:
                    out_file.write(l)
            for l in session_insert_queue:
                out_file.write(l)
            session_insert_queue = []

    # overwrite the "real" .htpasswd file by renaming the temporary one over it
    os.replace(config['session_lockfile'], config['htpasswd_path'])

