# My website

This is a website project host on my raspberry

### Objectives

Present my work (like CV), and developpe my skill in:

- Python
- REST API
- Flask
- Fast API

### Task

- [ ] FLASK API
  - [x] Change api to gunicorn
  - [ ] Update logs in api gunicorn
  - [ ] Automatisation deploy
  - [x] Manage Identity with token
  - [ ] Secret Santa DB
  - [ ] Secret Santa managing

### Technology

- Docker
- Python 3.10

### Development Env

#### vs code debuger

```sh
mkdir .vscode && touch launch.json
```

Puis copier et adapter le contenue suivant:

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
        "DB_HOST": "jeremiehenrion.eu"
      },
      "args": [
        "--chdir",
        "${workspaceFolder}/apis/flask/app",
        "--bind",
        "127.0.0.1:5000",
        "app:app"
      ],
      "cwd": "${workspaceFolder}/apis/flask/"
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
        "DB_HOST": "jeremiehenrion.eu"
      },
      "args": [
        "--chdir",
        "${workspaceFolder}/apis/flask/app",
        "--reload",
        "--bind",
        "127.0.0.1:5000",
        "app:app"
      ],
      "cwd": "${workspaceFolder}/apis/flask/"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "env": {
        "ROOT_DB": "${workspaceFolder}/apis/fastAPI"
      },
      "args": [
        "--app-dir",
        "${workspaceFolder}/apis/fastAPI",
        "--reload",
        "app.app:app"
      ],
      "cwd": "${workspaceFolder}/apis/fastAPI/"
    }
  ]
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
