import ipaddress
import os
import re

from dataclasses import dataclass
from typing import Optional
from typing import Union
import pymysql
import pynetbox
import urllib3
from environs import Env
from requests import request
from sqlalchemy.engine.url import URL

urllib3.disable_warnings()

commands = (
    ("start", "See if the ship is sailing"),
    ("help", "Get the command list"),
    ("id", "Get the command list"),
    # ("ip", "Проверка по IP адресу"),
    # ("file", "Загрузка фото на сервер"),
)

USERS = {52384439, 539181195, 345467127, 252810436, 347748319, 494729634, 1016868504, 361955359, 1292364914, 449155597,
         233703468, 842525963, 564569131, 1034083048, 224825221, 1369644834, 150862960, 1134721808, 1285798322,
         700520296, 700520296}

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
}


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    user_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = list(map(int, env.list("ADMINS")))
        user_ids = list(map(int, USERS))
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, user_ids=user_ids, use_redis=use_redis)


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
    netbox_url : str, optional

        A string used to hold other various parameters as required (default is None).
    """

    other_params: str = None
    netbox_url: str = None
    netbox_api: str = None
    upload_dir_photo: str = None
    upload_dir_data: str = None
    upload_dir_rack: str = None

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """

        netbox_url = env.str("NETBOX_URL")
        netbox_api = env.str("NETBOX_API")
        upload_dir_photo = os.path.dirname(os.path.realpath(__file__)) + "/_Photos/"
        upload_dir_data = os.path.dirname(os.path.realpath(__file__)) + "/_Data/"
        upload_dir_rack = os.path.dirname(os.path.realpath(__file__)) + "/_Rack/"

        return Miscellaneous(
            netbox_url=netbox_url,
            netbox_api=netbox_api,
            upload_dir_photo=upload_dir_photo,
            upload_dir_data=upload_dir_data,
            upload_dir_rack=upload_dir_rack
        )


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        db=DbConfig.from_env(env),
        redis=RedisConfig.from_env(env),
        misc=Miscellaneous.from_env(env),
    )


# nb = pynetbox.api(url=Config.misc.netbox_url, token=Config.misc.netbox_api)
# nb.http_session.verify = False


class Switch:
    """Заполняет данные по свичам"""
    db: None
    id: int
    nid: int
    name: str
    device_type: str
    rack: str
    status: str
    ip: ipaddress
    address: str
    msg = Union[str, int]
    json = str
    url = str
    comments = str
    images: list

    def __init__(self, db):
        self.db = db
        self.cfg = load_config(".env")

    def __call__(self, msg: str):
        url = self.cfg.misc.netbox_url + "api/dcim/devices/" + str(msg) + "/"
        response = request("GET", url, headers=HEADERS, data='')

        json = response.json()

        # devices = nb.dcim.devices.filter(id=msg)  # asset_tag__ic='авантел', role_id=4, status='offline'
        # for device in devices:

        # pprint(json['count'])
        self.nid = json['id']
        self.name = json['name'].lower()
        self.device_type = json['device_type']['display']
        self.address = json['site']['display']

        if json['asset_tag']:
            asset_tag = re.findall(r"(?<!\d)\d{5}(?!\d)", json['asset_tag'])
            self.id = int(asset_tag[0])
        else:
            self.id = 0

        if json['rack'] is not None:
            self.rack = json['rack']['name']
        else:
            self.rack = ' '

        self.status = json['status']['label']

        if json['primary_ip'] is not None:
            ip = json['primary_ip']['address'].split('/')
            self.ip = ip[0]
        else:
            self.ip = None
        self.url = json['url'].replace('/api/', '/')
        self.comments = json['comments']
        self.images = self.get_photo_in_netbox()
        self.images2 = self.get_photo_in_base()

        return self

    def get_photo_in_netbox(self):
        url = self.cfg.misc.netbox_url + "api/extras/image-attachments/?object_id=" + str(self.nid)
        response = request("GET", url, headers=HEADERS, data='')
        json = response.json()

        # img = nb.extras.image_attachments.filter(
        #     object_id=self.nid)  # asset_tag__ic='авантел', role_id=4, status='offline'

        photos = list()
        if json['count'] > 0:
            for iterator in json['results']:
                photos.append({
                    'pid': iterator['id'],
                    'image': iterator['image'],
                    'name': iterator['name'],
                    'object_id': iterator['object_id']}
                )
            return photos
        else:
            return None

    def get_photo_in_base(self):
        with self.db.cursor() as cursor:
            select_all_rows = f"SELECT `sid` as pid, `name`, `file_id` as image FROM `bot_photo` WHERE sid='{self.id}'"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None


def query_select(query):
    try:
        base = pymysql.connect(host="jok.su",
                               user="joker",
                               password="Mrj0keer155",
                               database="test",
                               cursorclass=pymysql.cursors.DictCursor
                               )
        base.autocommit(True)
        try:
            with base.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
        finally:
            base.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)
    return rows


def query_insert(query):
    is_true = None

    try:
        base = pymysql.connect(host="jok.su",
                               user="joker",
                               password="Mrj0keer155",
                               database="test",
                               cursorclass=pymysql.cursors.DictCursor
                               )
        base.autocommit(True)
        try:
            with base.cursor() as cursor:
                cursor.execute(query)
                base.commit()
                is_true = True
                base.close()
        except Exception as ex:
            print(ex)
            is_true = False

    except Exception as ex:
        print("Connection refused...")
        print(ex)

    return is_true


config = load_config(".env")
