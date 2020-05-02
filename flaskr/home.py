from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from flaskr.testimonials import fetch_testifiers

bp = Blueprint('home', __name__)


@bp.route('/home')
def home():
    user_id = session.get('user_id')
    if user_id is not None:
        return redirect(url_for('profile.profile', current_user=user_id))
    else:
        block, radio, label = fetch_testifiers()
        return render_template('home/home.html', testifiers=block, radio_buttons=radio, labels=label)

@bp.route('/faq')
def faqs():
    return render_template('home/faq.html')

