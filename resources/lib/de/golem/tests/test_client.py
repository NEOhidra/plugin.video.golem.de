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
        data = client.get_video_stream(video_id='14856', url='http://video.golem.de/handy/14856/alcatel-onetouch-idol-3-hands-on-mwc-2015.html')
        pass

    def test_get_stream_not_exists(self):
        client = Client()
        data = client.get_video_stream(video_id='148560000', url='http://video.golem.de/handy/14856/alcatel-onetouch-idol-3-hands-on-mwc-2015.html')
        pass

    pass
