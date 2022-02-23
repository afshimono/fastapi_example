from dataclasses import dataclass
import os


@dataclass
class EnvVariables:
    db_url: str
    db_password: str
    db_login: str
    db_name: str
    jwt_secret: str
    admin_email: str
    admin_pwd: str

    def __init__(self) -> None:
        self.db_url = os.environ["DATABASE_URL"]
        self.db_login = os.environ["DATABASE_LOGIN"]
        self.db_password = os.environ["DATABASE_PASSWORD"]
        self.db_name = os.environ["DATABASE_NAME"]
        self.jwt_secret = os.environ["JWT_SECRET"]
        self.admin_email = os.environ["ADMIN_MAIL"]
        self.admin_pwd = os.environ["ADMIN_PWD"]


env_vars = EnvVariables()
