import os

from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    "github",
    consumer_key=os.getenv("GITHUB_CONSUMER_KEY"),
    consumer_secret=os.getenv("GITHUB_CONSUMER_KEY"),
    request_token_params={"scope": "user:email"},
    base_url="https://api.githun.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
)
