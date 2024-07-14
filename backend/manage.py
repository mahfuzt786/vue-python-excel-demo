from flask_script import Manager
from flask_migrate import Migrate
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', migrate.init_app(app, db))

if __name__ == '__main__':
    manager.run()