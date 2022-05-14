import functools
import traceback

from django.http import JsonResponse


def ret(json_object, status=200):
    """Отдает JSON с правильными HTTP заголовками в читаемом виде (кириллица)"""
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params={'ensure_ascii': False},
    )


def error_response(exception):
    """Форматирует HTTP ответ с описанием ошибки"""
    res = {
        'errorMessage': str(exception),
        'traceback': traceback.format_exc(),
    }
    return ret(res, status=400)


def base_view(fn):
    """Декоратор для всех view, обрабатывает исключения"""

    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)

    return inner
