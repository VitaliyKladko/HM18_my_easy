from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns


def create_app(config: Config) -> Flask:
    """
    Функция создает приложение, конфигурирует его (из объекта Конфиг), применяет конфигурацию(app.app_context().push())
    и отдает обратно приложение
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    return app


def configure_app(app: Flask):
    """
    Функция, которая конфигурирует приложение: подключает приложение к БД
    """
    # подключаем БД
    db.init_app(app)
    # создаем API
    api = Api(app)
    # добавляем namespace к API
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)


if __name__ == '__main__':
    # создаем экземляр класса конфиг с нашими настройками и передаем этот конфиг в качестве аргумента в
    # функцию create_app()
    application_config = Config()
    # создаем приложение, которое грузит экземпляр класса Конфиг в качестве конфигурации
    application = create_app(application_config)
    # конфигурируем приложение
    configure_app(application)
    # запускаем приложение
    application.run()
