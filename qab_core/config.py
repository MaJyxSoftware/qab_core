import os
import json
import multiprocessing

from qab_core.exception import ConfigNotFoundError, ConfigParseFailureError

CONFIG_DEFAULT = {
    'server': {
        'port': os.environ.get('LISTEN_PORT', '8443'),
        'address': os.environ.get('LISTEN_ADDRESS', '0.0.0.0'),
        'cors_enabled': os.environ.get('CORS_ENABLED', 'false').lower() == "true",
        'cors_domains': os.environ.get('CORS_DOMAINS', "").split(','),
        'certificate': os.environ.get('CERTIFICATE', 'certs/fullchain.pem'),
        'private_key': os.environ.get('PRIVKEY', 'certs/privkey.pem'),
        'generate_ssl': str(os.environ.get('GENERATE_SSL', 'false')).lower() == "true",
        'workers': int(os.environ.get('WORKERS', str(multiprocessing.cpu_count() - 1))),
        'threads': int(os.environ.get('THREADS', str(multiprocessing.cpu_count() - 1))),
    },
    'console': {
        'quiet': str(os.environ.get('QUIET', 'false')).lower() == "true",
        'nolog': str(os.environ.get('NOLOG', 'false')).lower() == "true",
        'debug': str(os.environ.get('DEBUG', 'false')).lower() == "true",
        'log_dir': os.environ.get('LOG_DIR', 'logs/')
    }
}


def load_config(*files):
    '''
    Parse a configuration file to override and complete the default configuration
    '''

    config = CONFIG_DEFAULT.copy()

    for file in files:
        if not os.path.exists(file):
            raise ConfigNotFoundError(
                "Configuration file {} not found".format(file))

        with open(file) as config_file:
            try:
                config.update(json.load(config_file))
            except Exception:
                raise ConfigParseFailureError(
                    "Couldn't parse configuration file {}".format(file))

    return config
