from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate()

cache = Cache(config={
    'CACHE_TYPE': 'redis',
   # 'CACHE_KEY_PREFIX': 'token',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    #'CACHE_REDIS_URL': 'redis://localhost:6379',
    "CACHE_REDIS_DB": 0
})


def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cache.init_app(app=app)