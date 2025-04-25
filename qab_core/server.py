import inspect
import os
import socket
from datetime import datetime
from collections import OrderedDict
from itertools import chain, combinations

from bottle import Bottle, RouteBuildError, redirect, request, response

from qab_core.config import load_config
from qab_core.console import Console
from qab_core.exception import ServerCertificateError
from qab_core.plugins import GzipPlugin
from qab_core.scheduler import Scheduler

def _gen_cryptography():
    import datetime
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend())
    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, socket.gethostname())]))
    builder = builder.issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, socket.gethostname())]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day*365*5))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(socket.gethostname()),
            x509.DNSName(f'*.{socket.gethostname()}'),
            x509.DNSName('localhost'),
            x509.DNSName('*.localhost'),
        ]),
        critical=False)
    builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend())

    return certificate.public_bytes(serialization.Encoding.PEM), private_key.private_bytes(serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption())

def all_subsets(ss):
    if not ss:
        return []

    if len(ss) == 1:
        return [ss]

    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))

def gen_routes(base_route, method):
    map_method = {}
    method_spec = inspect.getfullargspec(method)

    default_c = len(method_spec.defaults) if method_spec.defaults else 0
    args_c = len(method_spec.args)

    args = method_spec.args.copy()
    opts_args = args[args_c - default_c:]
    required_args = args[0:args_c - default_c]
    required_args.remove("self") 

    # gen default route params
    default_route_params = "/".join([f"<{a}>" for a in required_args])
    if default_route_params:
        default_route_params = f"/{default_route_params}"

    for subset in all_subsets(opts_args):
        route_params = []
        for arg in subset:
            # Manage optional params
            route_params.append(f"{arg}/<{arg}>")
            map_method.update({f"{base_route}/{method.__name__.replace('_', '/')}{default_route_params}/{'/'.join(route_params)}": method})
            map_method.update({f"{base_route}/{method.__name__.replace('_', '/')}{default_route_params}/{'/'.join(route_params)}/": method})                

    # Manage index as base route
    if method.__name__ == "index" and not required_args and not opts_args:
        map_method.update({f"{base_route}": method})
        map_method.update({f"{base_route}/": method})

    map_method.update({f"{base_route}/{method.__name__.replace('_', '/')}{default_route_params}": method})

    return map_method


class Server(Bottle):

    def __init__(self):
        super(Server, self).__init__()
              
        config_files = []
        if os.path.exists('/etc/qab/app.json'):
            config_files.append('/etc/qab/app.json')

        if os.path.exists(os.path.expanduser('~/.qab.json')):
            config_files.append(os.path.expanduser('~/.qab.json'))
    
        if os.path.exists('config.json'):
            config_files.append('config.json')

        self.config.update(load_config(*config_files))

        self.hostname = socket.gethostname()
        self.map = []

        self.catchall = True

        self.__console = Console(**self.config['console'])

        self.__scheduler = Scheduler(self, **self.config['scheduler'])
        self.__scheduler.add("0 0 * * *", self.__console.compress)
        self.__scheduler.add("0 0 * * *", self.__console.rotate, self.__console.access_log)

        self.__init_hook()
        self.__init_plugin()

    def __init_hook(self):
        self.add_hook('after_request', self.enable_cors)

    def __init_plugin(self):
        self.install(GzipPlugin())

    def __register(self, route, method):
        self.route(route, method=['GET', 'POST'])(method)
        self.route(route, method=['OPTIONS'])(self.__options)
        self.map.append(route)
        self.console.log(f"Registering route {route} => {method.__module__}.{method.__name__}")

    def __redirect_home(self):
        redirect(self.routes[0].rule)

    def __options(self, *args, **kargs):
        return "OK"

    @property
    def scheduler(self):
        return self.__scheduler

    @property
    def console(self):
        return self.__console

    def enable_cors(self):
        '''
        Allow `cors_domains` to do AJAX request
        To enable CORS, 

        Don't use the wildcard '*' for Access-Control-Allow-Origin in production.

        Domaine can be set using either configuration file `server.cors_domains` as an array or environment variable `CORS_DOMAINS` as a list of domain seperated by a `,`
        '''
        if self.config['server'].get('cors_enabled') and request.headers.get('X-Requested-With') == "XMLHttpRequest":
            self.console.debug("CORS enabled, adding headers")
            cors_domain = '*'

            cors_domains = self.config['server'].get('cors_domains')
            if cors_domains:
                if request.headers['host'] in cors_domains:
                    cors_domain = request.headers.get('origin')
                else:
                    cors_domain = None     

            if cors_domain:
                response.headers['Access-Control-Allow-Origin'] = cors_domain
                response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, Cache-Control, X-CSRF-Token, X-Auth'

    def check_certificate(self):
        if not os.path.exists(self.config['server']['certificate']) and not os.path.exists(self.config['server']['private_key']):
            self.console.error("Couldn't find certificate files!")
            return self.generate_certificate()

        with open(self.config['server']['certificate']) as crt_file:
            from OpenSSL import crypto
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, crt_file.read())

            expiration_date = datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
            if expiration_date < datetime.now():
                self.console.error("Certificate is expired!")
                return self.generate_certificate()

        return True

    def generate_certificate(self):
        '''
        Create SSL PEM Files
        '''

        self.console.log("Attempting to generate self-signed certificate")

        if not self.config['server']['generate_ssl']:
            self.console.error("Self-signed certificate generation has been disabled")
            return False
        
        if not os.path.exists(os.path.dirname(self.config['server']['certificate'])):
            os.makedirs(os.path.dirname(self.config['server']['certificate']))

        if not os.path.exists(os.path.dirname(self.config['server']['private_key'])):
            os.makedirs(os.path.dirname(self.config['server']['private_key']))

        pub = None
        priv = None
        try:
            pub, priv = _gen_cryptography()
        except Exception:
            self.console.error("Couldn't generate self-signed certificate!!!")
            return False
        
        with open(self.config['server']['certificate'], 'wb') as pub_file, open(self.config['server']['private_key'], 'wb') as priv_file:
            pub_file.write(pub)
            priv_file.write(priv)

        self.console.log("Self-signed certificate generated")
        return True

    def register(self, obj):
        '''
        Allow you to register object by introspection of their method
        '''
        if hasattr(obj, 'base_route'):
            base_route = obj.base_route
        else:
            base_route = f"/{obj.__class__.__name__.lower().replace('controller', '')}"

        map_method = {}
        for attr in dir(obj):
            elem = getattr(obj, attr)
            if inspect.ismethod(elem):
                method = elem

                if attr in obj.pass_method or attr.startswith('_') or method.__module__ == "qab_core.controller":
                    continue

                map_method.update(gen_routes(base_route, method))

        map_method = OrderedDict(sorted(map_method.items()))

        if '/' not in map_method.keys():
            self.__register("/", self.__redirect_home)

        for new_route in map_method.keys():
            self.__register(new_route, map_method[new_route])

        self.map.sort()

    def start(self):
        '''
        Start server/listener
        '''        
        if self.check_certificate():
            self.console.log("Server started on port {} (debug: {})".format(self.config['server']['port'], self.console.is_debug))

            if not self.scheduler.is_running:
                self.scheduler.start()

            try:
                self.run(
                    host=self.config['server']['address'],
                    port=self.config['server']['port'],
                    quiet=self.console.quiet,
                    debug=self.console.is_debug,
                    server='gunicorn',
                    certfile=self.config['server']['certificate'],
                    keyfile=self.config['server']['private_key'],
                    workers=self.config['server']['workers'],
                    threads=self.config['server']['threads'],
                    worker_tmp_dir="/dev/shm",
                    accesslog=self.console.access_log,
                    errorlog=self.console.console_log
                )
            except Exception as ex:
                self.console.error(str(ex))
            finally:
                if self.scheduler.is_running:
                    self.scheduler.stop()

        else:
            self.console.error("Invalid cetificates, please check error above!")
            self.console.error("Exiting!")
            raise ServerCertificateError("Invalid cetificates, please check logs")
