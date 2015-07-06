import re

__author__ = 'bromix'

import unittest

from resources.lib.de import golem


class TestClient(unittest.TestCase):
    def test_get_videos(self):
        client = golem.Client()
        videos = client.get_videos()
        pass

    def test_get_stream(self):
        client = golem.Client()
        videos = client.get_videos(limit=10)
        self.assertGreater(len(videos['items']), 0)

        video = videos['items'][0]
        video_stream = client.get_video_stream(video['uri'], quality='medium')
        video_stream = client.get_video_stream(video['uri'], quality='high')
        pass

    def test_get_streams(self):
        client = golem.Client()
        videos = client.get_videos(limit=10)
        self.assertGreater(len(videos['items']), 0)

        video = videos['items'][0]
        video_streams = client.get_video_streams(video['uri'])
        pass

    pass
