import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USERNAME = os.environ.get('mail_username')
	MAIL_PASSWORD = os.environ.get('mail_password')
	FLASKY_MAIL_SUBJECT_PREFIX = 'TAO'
	FLASKY_MAIL_SENDER = 'beardtao@163.com'
	FLASKY_AMDIN = os.environ.get('FLASKY_AMDIN', 'TAO')

	SQLCHRMERY_TRACK_MODIFICATION = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

class TestingConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite://')

class ProductConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.sqlite'))

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductConfig,
	'default': DevelopmentConfig
}	