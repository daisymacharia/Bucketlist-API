import os
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from bucketlist.app import create_app
# from run import app
from bucketlist.app.models import db

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def dbinit():
        db.create_all()
        print('All tables created.')


@manager.command
def dropdb():
        db.drop_all()
        print('All tables deleted.')


if __name__ == '__main__':
    manager.run()
