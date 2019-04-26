import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USERNAME = os.environ.get('user_name')
	MAIL_PASSWORD = os.environ.get('user_password')
	FLASKY_SUBJECT_PREFIX = 'TAO'
	FLASKY_SUBJECT_SENDER = 'beardtao@163.com'
	FLASKY_AMDIN = os.environ.get('FLASKY_AMDIN', 'TAO')

	SQLCHRMERY_TRACK_MODIFICATION = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLCHEMERY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

class TestingConfig(Config):
	DEBUG = True
	SQLCHEMERY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite://')

class ProductionConfig(Config):
	SQLCHEMERY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.sqlite'))

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}