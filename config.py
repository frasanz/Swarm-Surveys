# -*- coding: utf-8 -*-
# ...
# available languages

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JMETER = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_ENABLED = True
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    LANGUAGES = {
        'en': 'English',
        'es': 'Español'
    }
    LOCALES = ['en', 'es']
    OPENID_PROVIDERS = [
        { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
        { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
        { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
        { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
        { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class Jmeter(Config):
    JMETER = True
    SEQUENCE = [5, 6, 7, 8, 9, 10, 17, 16, 12, 23, 22, 32, 33, 40, 41, 42, 49, 50, 51, 46, 47, 48, 14, 15]
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('JMETER_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-jmeter.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler
        # credentials = None
        # secure = None
        # if getattr(cls, 'MAIL_USERNAME', None) is not None:
        #     credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        #     if getattr(cls, 'MAIL_USE_TLS', None):
        #         secure = ()
        # mail_handler = SMTPHandler(
        #     mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        #     fromaddr=cls.FLASKY_MAIL_SENDER,
        #     toaddrs=[cls.FLASKY_ADMIN],
        #     subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
        #     credentials=credentials,
        #     secure=secure)
        # mail_handler.setLevel(logging.ERROR)
        # app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog unix machine
        # import logging
        # from logging.handlers import SysLogHandler
        # syslog_handler = SysLogHandler()
        # syslog_handler.setLevel(logging.WARNING)
        # app.logger.addHandler(syslog_handler)

        # file log
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('temp/swarms.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('swarms startup')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
