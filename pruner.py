# put this script in cron job for best constant monitoring of a playlist

import json
from http.client import HTTPSConnection

from config import config
from util import SpotifyActor


class Pruner(SpotifyActor):

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
