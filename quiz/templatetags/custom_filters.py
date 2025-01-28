from django import template
from quiz.models import Points  # Импорт модели Points

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


@register.filter
def get_score(value, args):
    # args - строка вида "student_id:test_id"
    try:
        student_id, test_id = map(int, args.split(":"))
    except ValueError:
        return ''  # Если строка не в правильном формате

    # Получаем оценку для студента и теста
    score = Points.objects.filter(user__id=student_id, test__id=test_id).first()

    # Возвращаем score или None, если не найдено
    return score.score if score else None


