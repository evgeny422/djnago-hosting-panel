import git
#
# try:
#     git.Repo.clone_from('https://github.com/Jokend23/test.git', '/home/evgeny/dir3')
#
# except git.GitCommandError as exception:
#
#     print(exception)
#
#     if exception.stdout:
#         print('!! stdout was:')
#         print(exception.stdout)
#
#     if exception.stderr:
#         print('!! stderr was:')
#         print(exception.stderr)


repo = git.Repo('/home/evgeny/dir3')
origin = repo.remote('origin')
origin.pull()