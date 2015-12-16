import os
from fabric.api import *

RIAK_VERSION            = "2.1.3"
RIAK_DOWNLOAD_URL       = "http://s3.amazonaws.com/downloads.basho.com/riak/2.1/2.1.3/osx/10.8/riak-2.1.3-OSX-x86_64.tar.gz"

NUM_NODES = 4

def fetch_riak():
    if(not os.path.exists('riak-{0}'.format(RIAK_VERSION))):
        local('curl -L {0} | tar xz -'.format(RIAK_DOWNLOAD_URL))

def copy_riak():
    for i in range(1, NUM_NODES):
        local('cp -nr riak-{0}/ riak{1}'.format(RIAK_VERSION, i))

def ping():
    for i in range(1, NUM_NODES):
        local('riak{0}/bin/riak ping'.format(i))

def join():
    for i in range(2, NUM_NODES):
        local('./riak{0}/bin/riak-admin join -f riak1@127.0.0.1 || true'.format(i))

def stop():
    for i in range(1, NUM_NODES):
        local('ulimit -n 65536; ./riak{0}/bin/riak stop || true'.format(i))

def start():
    for i in range(1, NUM_NODES):
        local('ulimit -n 65536; ./riak{0}/bin/riak start || true'.format(i))

    print("========================================")
    print("Riak Dev Cluster Started")
    print("\n")
    print("HTTP API: http://localhost:8098/")
    print("Admin UI: http://localhost:8098/admin")
    print("========================================")

def restart():
    stop()
    start()
