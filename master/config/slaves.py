import os
import config
from buildbot.plugins import worker

def create_slave(name, *args, **kwargs):
    password = config.options.get("Worker Passwords", name)
    return worker.Worker(name, password=password, *args, **kwargs)

def get_build_workers():
    return [
        # Fedora 25
        create_slave("llvm-worker")
    ]

