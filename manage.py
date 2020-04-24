from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from settings import app, db
import models.user
import models.instance

from models.user import User
from models.instance import Instance


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
