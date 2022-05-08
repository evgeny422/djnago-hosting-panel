import os
import datetime

from myproject.settings import BASE_DIR


class HistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        params = {i: request.GET.get(i) for i in request.GET.keys()}

        with open(os.path.join(BASE_DIR, 'data_list.log'), 'a') as f:
            f.write(
                f'TIME:{datetime.datetime.now()} - USER:{request.user.username} - URL:{request.path} {params if params else " "}\n')

        return response
