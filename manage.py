from flask_script import Manager
from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True)

if __name__ == '__main__':
    manager.run()
