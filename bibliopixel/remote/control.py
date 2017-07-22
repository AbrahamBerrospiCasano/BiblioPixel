import multiprocessing
import inspect
from .. animation import BaseAnimation
from .. animation.animation import STATE
from . import server
from .. import log


DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'display': None,
    'valid': True
}

DEFAULT_SERVER_CONFIG = {
    'title': 'BiblioPixel Remote',
    'bgcolor': '#000000',
    'font_color': '#ffffff',
    'external_access': False,
    'port': 5000
}


class RemoteControl:
    def __init__(self, config, animations):
        # These start with the defaults
        self.config = dict(DEFAULT_SERVER_CONFIG, **config)

        self.ui_config = {
            'bgcolor': self.config['bgcolor'],
            'title': self.config['title']
        }

        self.q_send = multiprocessing.Queue()
        self.q_recv = multiprocessing.Queue()

        server_args = (
            self.config['external_access'],
            self.config['port'],
            self.q_send,
            self.q_recv
        )

        self.server = multiprocessing.Process(target=server.run_server,
                                              args=server_args)
        if not isinstance(animations, list):
            raise ValueError('animations must be a list!')

        self.current_animation_name = None
        self.current_animation_obj = None
        self.animations = animations
        self.animation_objs = {}
        self.animations = [self._load_animation(a) for a in self.animations]

        self.handlers = {
            'run_animation': self.run_animation,
            'stop_animation': self.stop_animation,
            'get_config': self.get_config
        }

        self.default = config['default']
        if issubclass(type(self.default), BaseAnimation):
            self.animation_objs[DEFAULT_OFF] = self.default
            self.default = DEFAULT_OFF

        if self.default not in self.animation_objs:
            raise ValueError(('`{}` is not a valid default! '
                              'It must be one of the configured animation names.').format(self.default))

    def _load_animation(self, anim):
        anim_cfg = dict(DEFAULT_ANIM_CONFIG, **anim)

        if not anim_cfg['display']:
            anim_cfg['display'] = anim_cfg['name']
        anim_cfg['name'] = ''.join(e for e in anim['name'] if e.isalnum())

        if anim_cfg['loaded']:
            anim_cfg['animation'].on_completion = self.on_completion
            self.animation_objs[anim_cfg['name']] = anim_cfg['animation']
        else:
            anim_cfg['display'] = 'LOAD FAILED: ' + anim_cfg['display']
            anim_cfg['valid'] = False
            anim_cfg['bgcolor'] = 'rgb(48, 48, 48)'

        # no longer need here
        del anim_cfg['animation']
        del anim_cfg['loaded']

        return anim_cfg

    def cleanup(self, clean_layout=True):
        self.q_recv.close()
        self.q_send.close()
        self.server.terminate()

    def on_completion(self, reason):
        if reason != STATE.canceled:
            self._start_default()

    def _start_default(self):
        self._run_anim(self.default)

    def _stop_anim(self):
        if self.current_animation_obj:
            self.current_animation_obj.cleanup(clean_layout=False)

    def _start_anim(self, name):
        self._stop_anim()
        self._run_anim(name)

    def _run_anim(self, name):
        log.info('Running animation: {}'.format(name))
        self.current_animation_name = name
        self.current_animation_obj = self.animation_objs[name]
        self.current_animation_obj.start()

    # API Handlers
    def run_animation(self, name):
        if name not in self.animation_objs:
            return False, 'Invalid animation name: {}'.format(name)

        self._start_anim(name)
        return True, None

    def stop_animation(self, data):
        self._stop_anim()
        self._start_default()
        return True, None

    def get_config(self, data):
        resp = {
            'ui': self.ui_config,
            'animations': list(self.animations)
        }
        return True, resp

    def start(self):
        self._start_default()
        self.server.start()
        while True:
            recv = self.q_recv.get()
            req = recv['req']
            if req not in self.handlers:
                resp = False, '{} is not a valid request!'.format(req)
            else:
                resp = self.handlers[req](recv['data'])
            self.q_send.put(resp)