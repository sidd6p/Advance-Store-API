from flask_restful import Resource
from flask import g

from app.oa import github


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:5000/login/github/authorized"
        )


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        g.access_token = resp["access_token"]
        github_user = github.get(
            "user"
        )  # this uses the access_token from the tokengetter function
        github_username = github_user.data["login"]
        return github_username
