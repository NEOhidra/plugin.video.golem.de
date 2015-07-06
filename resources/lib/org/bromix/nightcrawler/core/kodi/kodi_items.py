__author__ = 'bromix'

import xbmcgui
import xbmcplugin

from ...exception import NightcrawlerException
from ... import utils


def _do_info_labels(context, kodi_item, item):
    def _process_not_none_value(_info_labels, name, value):
        if value is not None:
            _info_labels[name] = value
            pass
        pass

    info_labels = {}
    item_type = item['type']

    if item_type in ['video', 'movie']:
        # 'plot' = '...' (string)
        _process_not_none_value(info_labels, 'plot', item.get('plot', None))

        # 'artist' = [] (list)
        #_process_not_none_value(info_labels, 'artist', item.get('artist', None))

        # studio
        _process_not_none_value(info_labels, 'studio', item.get('studio', None))

        # tvshowtitle
        _process_not_none_value(info_labels, 'tvshowtitle', item.get('format', None))

        if 'published' in item:
            published_date = utils.datetime.parse(item['published'])

            # 'aired' = '2013-12-12' (string)
            info_labels['aired'] = published_date.strftime('%Y-%m-%d')

            # 'premiered' = '2013-12-12' (string)
            info_labels['premiered'] = published_date.strftime('%Y-%m-%d')

            # 'dateadded' = '2014-08-11 13:08:56' (string) will be taken from 'date'
            info_labels['dateadded'] = published_date.strftime('%Y-%m-%d %H:%M:%S')

            # fallback
            if item_type == 'video':
                info_labels['season'] = published_date.year
                info_labels['episode'] = published_date.timetuple().tm_yday
                pass
            pass

        if item_type == 'video':
            if 'season' or 'episode' in item:
                # 'episode' = 12 (int)
                _process_not_none_value(info_labels, 'episode', item.get('episode', None))

                # 'season' = 12 (int)
                _process_not_none_value(info_labels, 'season', item.get('season', None))
                pass
            pass

        if info_labels:
            kodi_item.setInfo(type=u'video', infoLabels=info_labels)
            pass

        # 'rating' = 4.5 (float)
        #_process_video_rating(info_labels, base_item.get_rating())

        # 'director' = 'Steven Spielberg' (string)
        #_process_string_value(info_labels, 'director', base_item.get_director())

        # 'code' = 'tt3458353' (string) - imdb id
        #_process_string_value(info_labels, 'code', base_item.get_imdb_id())

        # 'cast' = [] (list)
        #_process_list_value(info_labels, 'cast', base_item.get_cast())
        pass
    pass


def _do_context_menu(context, kodi_item, item):
    if item.get('context-menu', {}).get('items', None):
        kodi_item.addContextMenuItems(item['context-menu']['items'],
                                      replaceItems=item['context-menu'].get('replace', False))
        pass
    pass


def _do_fanart(context, kodi_item, item):
    fanart = item.get('images', {}).get('fanart', u'')
    if fanart and context.get_settings().show_fanart():
        kodi_item.setProperty(u'fanart_image', fanart)
        pass
    pass


def _create_kodi_item(context, item):
    icon_image_map = {'folder': u'DefaultFolder.png',
                       'video': u'DefaultVideo.png',
                       'movie': u'DefaultVideo.png',
                       'audio': u'DefaultAudio.png',
                       'music': u'DefaultAudio.png',
                       'image': u'DefaultFile.png',
                       'uri': u''}

    item_type = item['type']
    if item_type == 'uri':
        kodi_item = xbmcgui.ListItem(path=item['uri'])
        pass
    else:
        kodi_item = xbmcgui.ListItem(label=item.get('title', item['uri']),
                                      iconImage=icon_image_map.get(item_type, u''),
                                      thumbnailImage=item.get('images', {}).get('thumbnail', u''))
        pass

    # set playable
    if item_type in ['video', 'movie', 'audio', 'music', 'uri']:
        kodi_item.setProperty(u'IsPlayable', u'true')
        pass

    # set the duration
    if item_type in ['video', 'movie'] and 'duration' in item:
        kodi_item.addStreamInfo('video', {'duration': '%d' % item['duration']})
        pass

    return kodi_item


def process_item(context, item):
    kodi_item = _create_kodi_item(context, item)
    _do_fanart(context, kodi_item, item)
    _do_context_menu(context, kodi_item, item)
    _do_info_labels(context, kodi_item, item)

    if item['type'] == 'uri':
        xbmcplugin.setResolvedUrl(context.get_handle(), succeeded=True, listitem=kodi_item)
        pass
    else:
        if not xbmcplugin.addDirectoryItem(handle=context.get_handle(), url=item['uri'], listitem=kodi_item,
                                           isFolder=item['type'] == 'folder'):
            raise NightcrawlerException('Failed to add folder item')
        pass
    pass


def to_audio_item(context, audio_item):
    context.log_debug('Converting AudioItem')
    item = xbmcgui.ListItem(label=audio_item.get_name(),
                            iconImage=u'DefaultAudio.png',
                            thumbnailImage=audio_item.get_image())

    # only set fanart is enabled
    settings = context.get_settings()
    if audio_item.get_fanart() and settings.show_fanart():
        item.setProperty(u'fanart_image', audio_item.get_fanart())
        pass
    if audio_item.get_context_menu() is not None:
        item.addContextMenuItems(audio_item.get_context_menu(), replaceItems=audio_item.replace_context_menu())
        pass

    item.setProperty(u'IsPlayable', u'true')

    item.setInfo(type=u'music', infoLabels=info_labels.create_from_item(context, audio_item))
    return item