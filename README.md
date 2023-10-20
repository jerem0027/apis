# My website

This is a website project host on my raspberry

### Objectives

Present my work (like CV), and developpe my skill in:

- HTML/CSS
- JS
- PHP
- NETWORK

### Task

- [x] Connection to Raspberry Pi
- [x] Update + installation docker
- [x] Check to open ports
- [x] Contenerised website
  - [x] PHP apache -> updated to nginx
  - [x] Python Flask
  - [x] Mysql -> change to mariadb
  - [x] Phpmyadmin
- [x] Change api to gunicorn
- [x] Fix phpmyadmin redirection + block outside connection
- [x] Fix managing password for mail and DB access
- [ ] Move certificats to other repository
- [ ] Update logs in api gunicorn
- [ ] Clear docker-compose file
  - [ ] Remove useless port
  - [x] Add auto restart
  - [ ] See for more parameter
- [ ] Fix connection Home
- [x] Templatisation
- [ ] Auto save and deploy database
- [ ] Automatisation deploy
- [ ] Auto save Database
- [ ] FLASK API
  - [x] Manage Identity with token
  - [ ] Secret Santa DB
  - [ ] Secret Santa managing
- [ ] Secret santa Pages

### Technology

- HTML 5
- CSS 3
- JS
- PHP 7
- Docker
- Docker-compose
- Handlebars
- Python 3.10
- Node 10

### Templating

Use Handlabars and Yaml with js-yaml

```sh
sudo npm install -g npm to update
npm install js-yaml
```

### Development Env

#### vs code debuger
launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask DEBUG",
      "type": "python",
      "request": "launch",
      "module": "gunicorn",
      "env": {
        "PATH_ROOT": "/home/jeremie/realtemp",
        "FLASK_DEBUG": "True",
        "DB_PASSWORD": "Check in env file",
        "MAILPASS": "Check in env file",
        "DB_HOST": "jeremiehenrion.serveblog.net"
      },
      "args": [
        "--chdir",
        "${workspaceFolder}/web_site/apis/flask/app",
        "--bind",
        "127.0.0.1:5000",
        "app:app"
      ],
      "cwd": "${workspaceFolder}/web_site/apis/flask/"
    },
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "gunicorn",
      "env": {
        "PATH_ROOT": "/home/jeremie/realtemp",
        "FLASK_DEBUG": "False",
        "ENV": "develop",
        "DB_PASSWORD": "Check in env file",
        "MAILPASS": "Check in env file",
        "DB_HOST": "jeremiehenrion.serveblog.net"
      },
      "args": [
        "--chdir",
        "${workspaceFolder}/web_site/apis/flask/app",
        "--reload",
        "--bind",
        "127.0.0.1:5000",
        "app:app"
      ],
      "cwd": "${workspaceFolder}/web_site/apis/flask/"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "env": {
        "ROOT_DB": "${workspaceFolder}/web_site/apis/fastAPI"
      },
      "args": [
        "--app-dir",
        "${workspaceFolder}/web_site/apis/fastAPI",
        "--reload",
        "app.app:app"
      ],
      "cwd": "${workspaceFolder}/web_site/apis/fastAPI/"
    }
  ]
}
```

settings.json

```json
{
  "python.pythonPath": "./virtualenv/bin/python3.10"
}
```

#### virtual env python

```sh
virtualenv -p python3.10 virtualenv/
source virtualenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Contribution

- Jérémie Henrion
