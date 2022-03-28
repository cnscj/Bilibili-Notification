#!/usr/bin/python

import time
from servers import service
from configs import services_config

class SleepCpuService(service.Service):
    def __init__(self):
        super().__init__()

    def _onUpdate(self):
        time.sleep(services_config.INTERVALS_SECOND)