from django.conf import settings as django_settings

from attrdict import AttrDict


DEFAULTS = {
    'DEFAULT_THROTTLING_VALIDATORS_PATH': 'security.default_validators',
    'THROTTLING_FAILURE_VIEW': 'security.views.throttling_failure_view',
    'LOG_REQUEST_IGNORE_IP': (),
    'LOG_REQUEST_IGNORE_URL_PATHS': (),
    'LOG_REQUEST_BODY_LENGTH': 1000,
    'LOG_RESPONSE_BODY_LENGTH': 1000,
    'LOG_RESPONSE_BODY_CONTENT_TYPES':  (
        'application/json', 'application/xml', 'text/xml', 'text/csv', 'text/html', 'application/xhtml+xml'
    ),
    'LOG_JSON_STRING_LENGTH': 250,
    'COMMAND_LOG_EXCLUDED_COMMANDS': (
        'runserver', 'makemigrations', 'migrate', 'sqlmigrate', 'showmigrations', 'shell', 'shell_plus', 'test',
        'help', 'reset_db', 'compilemessages', 'makemessages', 'dumpdata', 'loaddata'
    ),
    'HIDE_SENSITIVE_DATA_PATTERNS': {
        'BODY': (
            r'"password"\s*:\s*"((?:\\"|[^"])*)',
            r'<password>([^<]*)',
            r'password=([^&]*)',
            r'csrfmiddlewaretoken=([^&]*)',
            r'(?i)content-disposition: form-data; name="password"\r\n\r\n.*',
            r'"access_key": "([^"]*)',
        ),
        'HEADERS': (
            r'Authorization',
            r'X_Authorization',
            r'Cookie',
            r'.*token.*',
        ),
        'QUERIES': (
            r'.*token.*',
        ),
    },
    'SENSITIVE_DATA_REPLACEMENT': '[Filtered]',
    'APPEND_SLASH': True,
}


class Settings:

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid Security setting: "{}"'.format(attr))

        value = getattr(django_settings, 'SECURITY_{}'.format(attr), DEFAULTS[attr])

        if isinstance(value, dict):
            value = AttrDict(value)

        return value


settings = Settings()
