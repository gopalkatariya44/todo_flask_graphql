from urllib.parse import urlencode, quote_plus

import sqlalchemy
from flask import Blueprint, session, render_template, abort, redirect, url_for

from main import oauth, appConf
from main.features.auth.auth_models import User
from main.features.auth.auth_services import AuthServices

router = Blueprint('auth', __name__)


@router.route('/loginr')
def loginr():
    if "user" in session:
        abort(404)
    return render_template("auth/login.html")


@router.route("/login")
def login():
    # check if session already present
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))


@router.route("/callback")
def callback():
    auth_services = AuthServices()
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    try:
        user = User()
        user.id = session['user']['userinfo']['sub']
        auth_services.create_user(user)
    except sqlalchemy.exc.IntegrityError:
        return redirect(url_for("todos.home"))

    return redirect(url_for("todos.home"))


@router.route("/logout")
def logout():
    # https://stackoverflow.com/a/72011979/2746323
    id_token = session["user"]["id_token"]
    session.clear()
    logout_redirect = redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("auth.logout", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )
    return logout_redirect
