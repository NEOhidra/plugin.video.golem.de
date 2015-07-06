__author__ = 'bromix'

__all__ = ['create_path', 'create_uri_path', 'strip_html_from_text', 'print_items', 'find_best_fit', 'to_utf8',
           'to_unicode', 'select_stream']

import urllib
import re
from ..constants import localize


def find_best_fit(data, compare_method=None):
    result = None

    last_fit = -1
    if isinstance(data, dict):
        for key in data.keys():
            item = data[key]
            fit = abs(compare_method(item))
            if last_fit == -1 or fit < last_fit:
                last_fit = fit
                result = item
                pass
            pass
        pass
    elif isinstance(data, list):
        for item in data:
            fit = abs(compare_method(item))
            if last_fit == -1 or fit < last_fit:
                last_fit = fit
                result = item
                pass
            pass
        pass

    return result


def select_stream(context, stream_data_list, quality_map_override=None):
    # sort - best stream first
    def _sort_stream_data(_stream_data):
        return _stream_data.get('sort', 0)

    video_quality = context.get_settings().get_video_quality(quality_map_override=quality_map_override)

    def _find_best_fit_video(_stream_data):
        return video_quality - _stream_data.get('video', {}).get('height', 0)

    sorted_stream_data_list = sorted(stream_data_list, key=_sort_stream_data, reverse=True)

    context.log_debug('selectable streams: %d' % len(sorted_stream_data_list))
    for sorted_stream_data in sorted_stream_data_list:
        context.log_debug('selectable stream: %s' % sorted_stream_data)
        pass

    selected_stream_data = None
    if context.get_settings().ask_for_video_quality() and len(sorted_stream_data_list) > 0:
        items = []
        for sorted_stream_data in sorted_stream_data_list:
            items.append((sorted_stream_data['title'], sorted_stream_data))
            pass

        result = context.get_ui().on_select(context.localize(localize.SELECT_VIDEO_QUALITY), items)
        if result != -1:
            selected_stream_data = result
        pass
    else:
        selected_stream_data = find_best_fit(sorted_stream_data_list, _find_best_fit_video)
        pass

    if selected_stream_data is not None:
        context.log_debug('selected stream: %s' % selected_stream_data)
        pass

    return selected_stream_data