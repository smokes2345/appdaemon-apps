#!/usr/bin/env python3
from pip.commands import install
from psutil import process_iter
from os import path
from sys import argv
from requests import get
from hashlib import sha512sha512
import logging

url_base = 'https://raw.githubusercontent.com/smokes2345/appdaemon-apps/master/'
app_url_base = 'http://kinolien.github.io/gitzip/?download=' + \
    url_base + 'apps/{app}/{app}.py'
req_url_base = url_base + 'apps/{app}/requirements.txt'
sha_url_base = url_base + 'apps/{app}/sha512.txt'

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.INFO)

path_reqs = [
    {'name': 'appdaemon.yaml', 'desc': 'appdaemon config file', 'filter': path.isfile},
    {'name': 'apps.yaml', 'desc': 'app config file', 'filter': path.isfile},
    {'name': 'apps', 'desc': 'app directory', 'filter': path.isdir}
]


def get_conf_dir():
    for p in process_iter():
        log.debug("Checking process {}".format(p))
        if len(p.cmdline()) >= 2 and 'appdaemon' in p.cmdline()[1]:
            data = p.cmdline()
            ad_dir = str(data[data.index('-c') + 1])
            reqs_met = 0
            for req in path_reqs:
                fqp = path.join(ad_dir, req['name'])
                if req['filter'](fqp):
                    reqs_met += 1
                    log.debug("Located {} at {}".format(req['desc'], fqp))
            if reqs_met == len(path_reqs):
                log.info("Located appdaemon config at {}".format(ad_dir))
                return ad_dir
    return None


def get_file(url, name, **kwargs):
    resp = get(url, stream=True, **kwargs)
    resp.raise_for_code()
    with open(name, 'wb') as fh:
        for chunk in resp:
            fh.write(chunk)
    return True


def app_installed(name):
    if path.isfile(path.join(get_conf_dir(), 'apps', name)):
        return True
    return False


def install_app(name):
    fname = path.join(get_conf_dir(), 'apps', name)
    if get_file(app_url_base.format(app=name), fname):


def update_app(name):
    install_app(name)


conf_dir = get_conf_dir()
if conf_dir:
    for app in argv[1:]:
        if app_installed(name):
            update_app(name)
        else:
            install_app(name)
