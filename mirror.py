import base64
import json
from http.client import HTTPSConnection

import requests

from config import config
from pruner import Pruner
from util import SpotifyActor


class Mirror(SpotifyActor):

    def update_image(self):
        image = self.get_base_64_cover_image()
        config.get("mirror")
        conn = HTTPSConnection(self.api_url)
        headers = self.generate_access_token_header()
        headers.update(
            {"Content-Type": "image/jpeg"}
        )
        conn.request("PUT", "/v1/playlists/{id}/images".format(id=config.get("mirror")), image, headers)
        response = conn.getresponse().read()

    def update_title(self):
        name = self.playlist["name"].replace(" (private)", "")
        conn = HTTPSConnection(self.api_url)
        headers = self.generate_access_token_header()
        headers.update(
            {"Content-Type": "application/json"}
        )
        body = json.dumps({
            "name": name
        })
        conn.request("PUT", "/v1/playlists/{id}".format(id=config.get("mirror")), body, headers)
        response = conn.getresponse().read()

    def get_base_64_cover_image(self) -> str:
        conn = HTTPSConnection(self.api_url)
        headers = self.generate_access_token_header()
        conn.request("GET", "/v1/playlists/{id}/images".format(id=config.get("playlist_id")), headers=headers)
        response = conn.getresponse()
        img_url = json.loads(response.read().decode("utf-8"))[0]["url"]
        return str(base64.b64encode(requests.get(img_url).content), "utf-8")

    def update_tracks(self):
        # generate track uri set of playlist:
        playlist_uris = set()
        for track in self.playlist["tracks"]["items"]:
            playlist_uris.add(track["track"]["uri"])
        # generate track uri set of mirror:
        mirror_uris = set()
        for track in self.mirror["tracks"]["items"]:
            mirror_uris.add(track["track"]["uri"])
        # add new tracks to mirror
        for uri in playlist_uris - mirror_uris:
            self.add_mirror_track(uri)
        # remove old tracks from mirror
        for uri in mirror_uris - playlist_uris:
            self.remove_mirror_track(uri)

    def remove_mirror_track(self, uri: str):
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
        conn.request("DELETE", "/v1/playlists/{id}/tracks".format(id=config.get("mirror")), body, headers)
        response = conn.getresponse().read()

    def add_mirror_track(self, uri: str):
        conn = HTTPSConnection(self.api_url)
        headers = self.generate_access_token_header()
        headers.update(
            {"Content-Type": "application/json"}
        )
        body = json.dumps({
            "uris": [uri]
        })
        conn.request("POST", "/v1/playlists/{id}/tracks".format(id=config.get("mirror")), body, headers)


m = Mirror()

