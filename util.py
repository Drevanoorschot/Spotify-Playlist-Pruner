import json
from base64 import b64encode
from http.client import HTTPSConnection
from urllib.parse import urlencode

from config import config


class SpotifyActor:
    client_secret_pair = b64encode(
        "{id}:{sec}".format(id=config.get("client_id"), sec=config.get("client_secret")).encode("utf-8")).decode(
        "utf-8")
    # auth stuff
    auth_url = "accounts.spotify.com"
    api_url = "api.spotify.com"
    auth_headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + client_secret_pair
    }
    auth_params = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": config.get("refresh_token")
    })

    def __init__(self):
        self.access_token = self.get_access_token()
        self.playlist = self.get_playlist()
        self.mirror = self.get_mirror_playlist()

    def get_playlist(self) -> json:
        conn = HTTPSConnection(self.api_url)
        conn.request("GET",
                     "/v1/playlists/{id}".format(id=config.get("playlist_id")),
                     headers=self.generate_access_token_header())
        response = conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def get_mirror_playlist(self):
        conn = HTTPSConnection(self.api_url)
        conn.request("GET",
                     "/v1/playlists/{id}".format(id=config.get("mirror")),
                     headers=self.generate_access_token_header())
        response = conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def get_access_token(self) -> str:
        conn = HTTPSConnection(self.auth_url)
        conn.request("POST", "/api/token", self.auth_params, self.auth_headers)
        response = conn.getresponse()
        return json.loads(response.read().decode("utf-8"))["access_token"]

    def generate_access_token_header(self) -> dict:
        return {
            "Authorization": "Bearer {token}".format(token=self.access_token)
        }
