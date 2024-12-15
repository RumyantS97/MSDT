#!/usr/bin/env python3

import os
import json
import re
import subprocess
import uuid
import base64
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    filename='script.log',  # Имя файла для записи логов
    filemode='w'  # Режим записи в файл (перезапись)
)

# Проверка наличия файла repos.json
if not os.path.isfile('repos.json'):
    logging.error('No repos.json found, please create one')
    print('No repos.json found, please create one')
    quit()

# Загрузка конфигурации из repos.json
try:
    repos = json.load(open('repos.json'))
    logging.info('Successfully loaded repos.json')
except Exception as e:
    logging.error(f'Failed to load repos.json: {e}')
    quit()

origWD = os.getcwd()  # Запоминаем оригинальную рабочую директорию

def init():
    logging.info("Initializing repository...")  # Логирование инициализации репозитория
    subprocess.call([
        'git',
        'init'
    ])
    try:
        readme = open(repo['dummy_repo'] + os.path.sep + 'README.md', 'w+')
        readme.write(repo['dummy_readme'])
        readme.close()
        logging.info("Created README.md")
    except Exception as e:
        logging.error(f"Failed to create README.md: {e}")

    try:
        ignore = open(repo['dummy_repo'] + os.path.sep + '.gitignore', 'w+')
        ignore.write(".DS_Store\n")
        ignore.close()
        logging.info("Created .gitignore")
    except Exception as e:
        logging.error(f"Failed to create .gitignore: {e}")

    try:
        subprocess.call([
            'git',
            'add',
            '-A'
        ])
        subprocess.call([
            'git',
            'commit',
            '-m',
            'README'
        ])
        subprocess.call([
            'git',
            'remote',
            'add',
            'origin',
            repo['remote']
        ])
        subprocess.call([
            'git',
            'push',
            '-u',
            'origin',
            'master'
        ])
        logging.info("Pushed initial commit to remote repository")
    except Exception as e:
        logging.error(f"Failed to push initial commit: {e}")

for repo in repos:
    logging.info(f"Processing repository: {repo['dummy_repo']}")  # Логирование обработки репозитория
    commits = []

    if os.path.isdir(repo['dummy_repo']):
        logging.info(f"Directory {repo['dummy_repo']} already exists")
        os.chdir(repo['dummy_repo'])

        if not os.path.isdir(repo['dummy_repo_data']):
            os.mkdir(repo['dummy_repo_data'])
            logging.info(f"Created directory: {repo['dummy_repo_data']}")
        if not os.path.isdir(repo['dummy_repo'] + os.path.sep + '.git'):
            logging.info("Repository not initialized yet, initializing...")
            init()
    else:
        logging.info(f"Directory {repo['dummy_repo']} does not exist, creating...")
        os.mkdir(repo['dummy_repo'])
        os.mkdir(repo['dummy_repo_data'])
        os.chdir(repo['dummy_repo'])
        init()

    since = ''
    if os.path.isfile(repo['dummy_repo'] + os.path.sep + '.gitdummy'):
        try:
            dotgitdummy = open(repo['dummy_repo'] + os.path.sep + '.gitdummy', 'r')
            since = dotgitdummy.read()
            dotgitdummy.close()
            logging.info(f"Loaded .gitdummy with value: {since}")
        except Exception as e:
            logging.error(f"Failed to read .gitdummy: {e}")

    commits = []

    for targetrepo in repo['target_repo']:
        os.chdir(targetrepo)  # Переключаемся на целевой репозиторий
        logging.info(f"Switched to target repository: {targetrepo}")

        print('since: ' + since)
        try:
            if since == '':
                log_output = subprocess.check_output([
                    'git',
                    'log',
                    '--reverse',
                    '--pretty=format:%an||||%ae||||%ad||||%s||||%f-%h'
                ])
            else:
                log_output = subprocess.check_output([
                    'git',
                    'log',
                    '--since',
                    since,
                    '--reverse',
                    '--pretty=format:%an||||%ae||||%ad||||%s||||%f-%h'
                ])
            log_split = log_output.decode('utf-8').split('\n')
            logging.info(f"Log Split Length: {len(log_split)}")
        except Exception as e:
            logging.error(f"Failed to fetch git log from {targetrepo}: {e}")
            continue

        if len(log_split) > 1:
            line_re = re.compile(r'^(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)(?:\|\|\|\|)(.+)', re.DOTALL)

            for line in log_split:
                if '||||||||' in line: continue
                if '||||||||||||' in line: continue
                if '||||||||||||||||' in line: continue
                if '||||||||||||||||||||' in line: continue

                try:
                    commit_line = line_re.search(line).groups()
                    commits.append({
                        'name': commit_line[0],
                        'email': commit_line[1],
                        'date': commit_line[2],
                        'message': commit_line[3],
                        'filename': commit_line[4]
                    })
                except Exception as e:
                    logging.error(f"Failed to parse commit line: {line}, error: {e}")

    if len(commits) > 0:
        require_push = False
        for commit in commits:
            private_commit_message = 'Commit message is private'
            if 'dummy_commit_message' in repo:
                private_commit_message = repo['dummy_commit_message']

            if len(commit['filename']) > 200:
                fullStr = commit['filename']
                commit['filename'] = fullStr[:200]

            if repo['random_file_name']:
                commit['filename'] = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('UTF-8').replace('=', '').replace('-', '').replace('_', '')

            os.chdir(repo['dummy_repo_data'])
            if not os.path.isfile(repo['dummy_repo_data'] + os.path.sep + commit['filename'] + repo['dummy_ext']):
                emailcheck = False
                for email in repo['target_email']:
                    if email == commit['email']:
                        emailcheck = True

                if emailcheck:
                    if repo['hide_commits'] is not True:
                        private_commit_message = commit['filename'] + "\n" + commit['message'].replace("@", "[at]")
                    logging.info(f"PRIVATE COMMIT MESSAGE: {private_commit_message}")
                    dummyfile = repo['dummy_repo_data'] + os.path.sep + commit['filename'][:120] + repo['dummy_ext']
                    try:
                        dummyfile = open(dummyfile, 'w+')
                        dummyfile.write(repo['dummy_code'])
                        dummyfile.close()
                        subprocess.call([
                            'git',
                            'add',
                            '--',
                            commit['filename'] + repo['dummy_ext']
                        ])
                        dotgitdummy = open(repo['dummy_repo'] + os.path.sep + '.gitdummy', 'w+')
                        dotgitdummy.write(commit['date'])
                        dotgitdummy.close()
                        subprocess.call([
                            'git',
                            'add',
                            '--',
                            repo['dummy_repo'] + os.path.sep + '.gitdummy'
                        ])
                        os.environ['GIT_COMMITTER_DATE'] = commit['date']
                        subprocess.call([
                            'git',
                            'commit',
                            '-m',
                            private_commit_message,
                            '--date',
                            commit['date']
                        ])
                        require_push = True
                    except Exception as e:
                        logging.error(f"Failed to process commit: {e}")

        if repo['auto_push'] is True and require_push is True:
            try:
                if repo['force'] is True:
                    subprocess.call([
                        'git',
                        'push',
                        '-u',
                        'origin',
                        'master',
                        '--force'
                    ])
                else:
                    subprocess.call([
                        'git',
                        'push',
                        '-u',
                        'origin',
                        'master'
                    ])
                logging.info("Successfully pushed changes to remote repository")
            except Exception as e:
                logging.error(f"Failed to push changes: {e}")

        try:
            del os.environ['GIT_COMMITTER_DATE']
        except:
            pass
    else:
        logging.info("Length of commits was zero, nothing to update")

os.chdir(origWD)
