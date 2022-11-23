from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_redis import FlaskRedis


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
redis_cache = FlaskRedis()