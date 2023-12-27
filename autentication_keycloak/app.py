from flask import Flask, g
from flask_oidc import OpenIDConnect
import json

app = Flask(__name__)

app.config.update(
        SECRET_KEY='',
        OIDC_CLIENT_SECRETS='keycloak.json',
        OIDC_INTROSPECTION_AUTH_METHOD='client_secret_post',
        OIDC_TOKEN_TYPE_HINT='access_token',
        OIDC_SCOPES=['openid','email','profile'],
        OIDC_OPENID_REALM='<name_realm>'
    )

oidc = OpenIDConnect(app)

@app.route('/')
def index():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(["preferred_username", "email", "sub"])
        return 'Welcome %s' % info.get("preferred_username")
    else:
        return '<h1>Not logged in</h1>'

@app.route('/login')
@oidc.require_login
def login():
    token = oidc.get_access_token()
    info = oidc.user_getinfo(["preferred_username", "email", "sub"])
    username = info.get("preferred_username")
    return "Token: " + token + "<br/><br/>  Username: " + username

@app.route('/logout')
def logout():
    oidc.logout()
    return '<h2>Hi, you have been logged out! <a href="/">Return</a></h2>'