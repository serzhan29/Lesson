from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item2(value, index):
    """Возвращает элемент из списка по индексу"""
    try:
        return value[int(index)]  # Пытаемся получить элемент по индексу
    except (IndexError, ValueError):
        return ''  # Если индекс некорректен или нет данных, возвращаем пустую строку