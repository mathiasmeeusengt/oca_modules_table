import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Flask-WTF
    # Flask-WTF can give protection against CSRF attacks if:
    #  a SECRET_KEY is in the config and a hidden tag in the template
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

