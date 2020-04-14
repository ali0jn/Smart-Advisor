import json
import requests
import os
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flaskr.testimonials import fetch_testifiers
from oauthlib.oauth2 import WebApplicationClient
from flaskr.user import Student
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

GOOGLE_CLIENT_ID = '738133434886-hj1r4tuge60dcvb59aaid713v1740ah1.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'M_hqsHXkj3fLmC2whuCUiIbb'
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@bp.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@bp.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code)
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),)

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["name"]
    else:
        return "User email not available or not verified by Google.", 400

    std = Student(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not Student.get(unique_id):
        Student.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    session['user_id'] = std.id
    return redirect(url_for('profile.profile'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cursor = db.cursor()
        query = cursor.execute('SELECT * FROM student WHERE student_google_id = {}'.format(user_id))
        g.user = cursor.fetchall()[0]

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
