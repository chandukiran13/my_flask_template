from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_caching import Cache


db = SQLAlchemy(engine_options={"pool_size": 50, "max_overflow": 20})
migrate = Migrate()
cache = Cache()
