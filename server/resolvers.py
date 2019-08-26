from functools import reduce

"""
Если изменить механизм инициализации INSTALLED_APPS
можно попробовать сделать динамическую загрузку модулей, наподобии плагинов
"""
from settings import INSTALLED_APPS

from decorators import log_call_info

"""
Добавил декоратор для теста
"""

@log_call_info
def get_server_action():
    # импортируем файл routes из каждого модуля
    applications = reduce(
        lambda value, item: value + [__import__(f'{item}.routes')],
        INSTALLED_APPS,
        []
    )
    # создаем словарь всех routes как объектов
    routes = reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        applications,
        []
    )
    # cоздаем словать всех actionmapping определенных в routes
    return reduce(
        lambda value, item: value + getattr(item, 'actionmapping', None),
        routes,
        []
    )

def resolve(action):
    """
    Герерирует на лету список обработчиков и находит нужный
    """
    actionmapping = {
        item.get('action'): item.get('controller')
        for item in get_server_action()
        if item is not None
    }
    return actionmapping.get(action)