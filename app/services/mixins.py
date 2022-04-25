import os
from subprocess import Popen, PIPE


class ShellConnection:
    def script_apply(self, path=None, param=None, url: str = None, branch=None):
        try:
            # result = os.popen(f'bash {path}  {param} {url} {branch}').read()
            p = Popen(f'bash {path}  {param} {url} {branch}', shell=True, stdout=PIPE,
                      stderr=PIPE, bufsize=1, universal_newlines=True)
            stdout, stderr = p.communicate()
            if stderr:
                return stderr

            return stdout
        except:
            raise Exception
