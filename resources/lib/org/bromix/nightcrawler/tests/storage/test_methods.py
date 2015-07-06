# -*- coding: utf-8 -*-
__author__ = 'bromix'

import platform
import unittest


class TestMethods(unittest.TestCase):
    def test_get_platform(self):
        pf = platform.python_version()
        pass

    def test_find_best_fit(self):
        fit = 1080

        def _compare(item):
            return fit - item['format']['h']

        data = [{'url': '...', 'format': {'w': 1280, 'h': 720}},
                {'url': '...', 'format': {'w': 640, 'h': 480}},
                {'url': '...', 'format': {'w': 320, 'h': 160}},
                {'url': '...', 'format': {'w': 1920, 'h': 1080}}, ]

        best_fit = kodion.utils.find_best_fit(data, _compare)
        pass

    def test_get_select_stream(self):
        stream_data = [
            {
                "title": "720p@5000",
                "sort": [720, 5000],
                "video": {"height": 720, "width": 1280, "bandwidth": 5000}
            },
            {
                "title": "720p@10000",
                "sort": [720, 10000],
                "video": {"height": 720, "width": 1280, "bandwidth": 10000}
            },
            {
                "title": "480p@5000",
                "sort": [480, 5000],
                "video": {"height": 480, "width": 640, "bandwidth": 5000}
            },
            {
                "title": "1080p@5000", "sort": [1080, 5000],
                "video": {"height": 1080, "width": 1920, "bandwidth": 5000}
            },
            {
                "title": "1080p@10000", "sort": [1080, 10000],
                "video": {"height": 1080, "width": 1920, "bandwidth": 10000}
            }
        ]

        context = kodion.Context()
        quality_map_override = {0: 480, 1: 720, 2: 1080}
        stream = kodion.utils.select_stream(context, stream_data, quality_map_override=quality_map_override)
        pass

    pass
