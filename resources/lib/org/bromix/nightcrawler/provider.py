__author__ = 'bromix'

import json

from .core.nightcrawler_decorators import register_path, register_context_value, register_path_value
from .core.view_manager import ViewManager
from .exception import NightcrawlerException


class Provider(object):
    LOCAL_SETUP_WIZARD_EXECUTE = 30030

    LOCAL_PLEASE_WAIT = 30119

    LOCAL_FAVORITES = 30100
    LOCAL_FAVORITES_ADD = 30101
    LOCAL_FAVORITES_REMOVE = 30108

    LOCAL_WATCH_LATER = 30107
    LOCAL_WATCH_LATER_ADD = 30107
    LOCAL_WATCH_LATER_REMOVE = 30108

    LOCAL_SEARCH = 30102
    LOCAL_SEARCH_TITLE = 30102
    LOCAL_SEARCH_NEW = 30110
    LOCAL_SEARCH_RENAME = 30113
    LOCAL_SEARCH_REMOVE = 30108
    LOCAL_SEARCH_CLEAR = 30120

    LOCAL_CONFIRM_DELETE = 30114
    LOCAL_CONFIRM_REMOVE = 30115
    LOCAL_DELETE_CONTENT = 30116
    LOCAL_REMOVE_CONTENT = 30117

    LOCAL_SELECT_VIDEO_QUALITY = 30010

    LOCAL_SETUP_VIEW_DEFAULT = 30027
    LOCAL_SETUP_VIEW_VIDEOS = 30028

    LOCAL_LIBRARY = 30103
    LOCAL_HIGHLIGHTS = 30104
    LOCAL_ARCHIVE = 30105
    LOCAL_NEXT_PAGE = 30106

    LOCAL_LATEST_VIDEOS = 30109

    LOCAL_SETUP_OVERRIDE_VIEW = 30037

    PATH_SEARCH = 'search/list'
    PATH_SEARCH_QUERY = 'search/query'
    PATH_SEARCH_INPUT = 'search/input'
    PATH_SEARCH_CLEAR = 'search/clear'
    PATH_SEARCH_RENAME = 'search/rename'
    PATH_SEARCH_REMOVE = 'search/remove'

    PATH_FAVORITES_ADD = 'favorites/add'
    PATH_FAVORITES_LIST = 'favorites/list'
    PATH_FAVORITES_REMOVE = 'favorites/remove'

    PATH_WATCH_LATER_ADD = 'watch_later/add'
    PATH_WATCH_LATER_LIST = 'watch_later/list'
    PATH_WATCH_LATER_REMOVE = 'watch_later/remove'

    def __init__(self):
        pass

    def _process_addon_setup(self, context):
        settings = context.get_settings()

        # exit if the setup isn't enabled
        if not settings.is_setup_wizard_enabled():
            return

        # exit if the setup shouldn't be executed
        if not context.get_ui().on_yes_no_input(context.get_name(), context.localize(self.LOCAL_SETUP_WIZARD_EXECUTE)):
            return

        view_manager = ViewManager(context, self)
        view_manager.setup()

        self.on_setup(mode='setup')

        # disable the setup
        settings.set_bool(settings.ADDON_SETUP, False)
        pass

    def on_setup(self, mode):
        if mode == 'content-types':
            return ['default']

        return None

    def get_wizard_steps(self, context):
        # can be overridden by the derived class
        return []

    def navigate(self, context):
        self._process_addon_setup(context)

        method_names = dir(self)
        for method_name in method_names:
            method = getattr(self, method_name)
            if hasattr(method, 'nightcrawler_registered_path'):
                result = method(context)
                if result is not None:
                    return result
                pass
            pass

        raise NightcrawlerException('Missing method for path "%s"' % context.get_path())

    def get_fanart(self, context):
        """
        Can be overriden by the derived class to return an alternate image
        :param context: the current image
        :return: full path to the fanart image
        """
        return context.get_fanart()

    def on_search(self, context, search_text):
        """
        The derived class has to implement this method in case of support for search
        :param context: the current context
        :param search_text: the search term in unicode
        :return: a list of items or False if something went wrong
        """
        raise NotImplementedError()

    @register_path('/favorites/(?P<method>add|remove)/')
    @register_path_value('method', unicode)
    @register_context_value('item', dict, required=True)
    def _internal_favorites_with_item(self, context, method, item):
        # context.add_sort_method(constants.sort_method.LABEL_IGNORE_THE)

        if method == 'add':
            context.get_favorite_list().add(item)
            return True

        if method == 'remove':
            context.get_favorite_list().remove(item)
            context.get_ui().refresh_container()
            return True

        return False

    @register_path('/favorites/list/')
    def _internal_favorites_list(self, context):
        # context.add_sort_method(constants.sort_method.LABEL_IGNORE_THE)

        result = context.get_favorite_list().list()
        for directory_item in result:
            context_menu = [(context.localize(self.LOCAL_WATCH_LATER_REMOVE),
                             'RunPlugin(%s)' % context.create_uri(self.PATH_FAVORITES_REMOVE,
                                                                  {'item': json.dumps(directory_item)}))]
            directory_item['context-menu'] = {'items': context_menu}
            pass

        return result

    @register_path('/watch_later/(?P<method>add|remove)/')
    @register_path_value('method', unicode)
    @register_context_value('item', dict, required=True)
    def _internal_watch_later_with_item(self, context, method, item):
        if method == 'add':
            context.get_watch_later_list().add(item)
            return True

        if method == 'remove':
            context.get_watch_later_list().remove(item)
            context.get_ui().refresh_container()
            return True

        return False

    @register_path('/watch_later/list/')
    def _internal_watch_later_list(self, context):
        video_items = context.get_watch_later_list().list()

        for video_item in video_items:
            context_menu = [(context.localize(self.LOCAL_WATCH_LATER_REMOVE),
                             'RunPlugin(%s)' % context.create_uri(self.PATH_WATCH_LATER_REMOVE,
                                                                  {'item': json.dumps(video_item)}))]
            video_item['context-menu'] = {'items': context_menu}
            pass

        return video_items

    @register_path('/search/(?P<method>(remove|rename|query))/')
    @register_path_value('method', unicode)
    @register_context_value('q', unicode, alias='query', required=True)
    def _internal_search_with_query(self, context, method, query):
        search_history = context.get_search_history()
        if method == 'remove':
            search_history.remove(query)
            context.get_ui().refresh_container()
            return True

        if method == 'rename':
            result, new_query = context.get_ui().on_keyboard_input(context.localize(self.LOCAL_SEARCH_RENAME), query)
            if result:
                search_history.rename(query, new_query)
                context.get_ui().refresh_container()
                pass
            return True

        if method == 'query':
            search_history.update(query)
            return self.on_search(context, query)

        return False

    @register_path('/search/(?P<method>(list|input|clear))/')
    @register_path_value('method', unicode)
    def _internal_search_without_query(self, context, method):
        search_history = context.get_search_history()
        if method == 'clear':
            search_history.clear()
            context.get_ui().refresh_container()
            return True

        if method == 'input':
            result, query = context.get_ui().on_keyboard_input(context.localize(self.LOCAL_SEARCH_TITLE))
            if result:
                context.execute(
                    'Container.Update(%s)' % context.create_uri(self.PATH_SEARCH_QUERY, {'q': query}))
                pass

            return True

        if method == 'list':
            # add new search
            result = [{'type': 'folder',
                       'title': '[B]%s[/B]' % context.localize(30102),
                       'uri': context.create_uri(self.PATH_SEARCH_INPUT),
                       'images': {'thumbnail': context.create_resource_path('media/new_search.png'),
                                  'fanart': self.get_fanart(context)}}]

            for query in search_history.list():
                # we create a new instance of the SearchItem
                context_menu = [(context.localize(30108),
                                 'RunPlugin(%s)' % context.create_uri(self.PATH_SEARCH_REMOVE, {'q': query})),
                                (context.localize(30113),
                                 'RunPlugin(%s)' % context.create_uri(self.PATH_SEARCH_RENAME, {'q': query})),
                                (context.localize(30120),
                                 'RunPlugin(%s)' % context.create_uri(self.PATH_SEARCH_CLEAR))]
                item = {'type': 'folder',
                        'title': query,
                        'uri': context.create_uri(self.PATH_SEARCH_QUERY, {'q': query}),
                        'images': {'thumbnail': context.create_resource_path('media/search.png'),
                                   'fanart': self.get_fanart(context)},
                        'context-menu': {'items': context_menu}}
                result.append(item)
                pass

            if search_history.is_empty():
                context.execute('RunPlugin(%s)' % context.create_uri(self.PATH_SEARCH_INPUT))
                pass

            return result

        return False

    def handle_exception(self, context, exception_to_handle):
        """
        Can be overridden by the derived class to handle exceptions
        :param context: the current context
        :param exception_to_handle: the caught excaption
        :return: None if nothing can be done. True exception can be handled, False if not. A list of items is also possible.
        """
        return None

    def tear_down(self, context):
        """
        Can be overridden by the derived class to free resources or write some stuff to disk/cache
        :param context: the current context
        """
        pass

    pass