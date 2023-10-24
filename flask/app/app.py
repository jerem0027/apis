from controllers.email_controller import *
from controllers.home_users_controller import *
from controllers.identity_controller import *
from controllers.secret_santa_controller import *
from controllers.tests_controller import *
from errors.handlers import *
from server.instance import server
from server.logging import *

if __name__ == "__main__":
    server.run()