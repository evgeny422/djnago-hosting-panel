import os
import datetime

from config.settings import BASE_DIR


class LogWriter:
    def __init__(self, request):
        self.request = request
        self.params = {i: request.GET.get(i) for i in request.GET.keys()}

    def write_log(self, ):
        with open(os.path.join(BASE_DIR, 'data_list.log'), 'a') as f:
            f.write(
                f'TIME:{datetime.datetime.now()} - USER:{self.request.user.username} - URL:{self.request.path} {self.params if self.params else " "}\n')
