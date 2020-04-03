# put this script in cron job for best constant monitoring of a playlist

import json
from base64 import b64encode
from http.client import HTTPSConnection
from urllib.parse import urlencode

from config import config


class Pruner:
    # auth stuff
    client_secret_pair = b64encode(
        "{id}:{sec}".format(id=config.get("client_id"), sec=config.get("client_secret")).encode("utf-8")).decode(
        "utf-8")
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

    def get_access_token(self) -> str:
        conn = HTTPSConnection(self.auth_url)
        conn.request("POST", "/api/token", self.auth_params, self.auth_headers)
        response = conn.getresponse()
        return json.loads(response.read().decode("utf-8"))["access_token"]

    def generate_access_token_header(self) -> dict:
        return {
            "Authorization": "Bearer {token}".format(token=self.access_token)
        }

    def get_playlist(self) -> json:
        conn = HTTPSConnection(self.api_url)
        conn.request("GET",
                     "/v1/playlists/{id}".format(id=config.get("playlist_id")),
                     headers=self.generate_access_token_header())
        response = conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def prune_playlist(self):
        # get list of track objects for each allowed user
        # if user is not an allowed user, delete track
        user_tracks = dict()
        for user in config.get("allowed_users"):
            user_tracks.update({user: []})
        for track in self.playlist["tracks"]["items"]:
            user = track["added_by"]["id"]
            if user not in config.get("allowed_users"):
                self.remove_track(track["track"]["uri"])
            else:
                user_tracks.get(user).append(track)
        # remove latest tracks if >user_limit
        for user in config.get("allowed_users"):
            if len(user_tracks.get(user)) > config.get("user_song_limit"):
                user_tracks.get(user).sort(key=lambda t: t["added_at"])
                to_be_removed = len(user_tracks.get(user)) - config.get("user_song_limit")
                for i in range(0, to_be_removed):
                    uri = user_tracks.get(user)[i]["track"]["uri"]
                    self.remove_track(uri)

    def remove_track(self, uri: str):
        conn = HTTPSConnection(self.api_url)
        headers = self.generate_access_token_header()
        headers.update(
            {"Content-Type": "application/json"}
        )
        body = json.dumps({
            "tracks":
                [{
                    "uri": uri
                }]
        })
        conn.request("DELETE", "/v1/playlists/{id}/tracks".format(id=config.get("playlist_id")), body, headers)
        response = conn.getresponse().read()


def callback():
    print("pruning playlist...")
    Pruner().prune_playlist()
    print("pruning completed")


callback()
