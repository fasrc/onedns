import time

from onedns import api


class OneMonitor(api.OneDNS):
    """
    Daemon that syncs OpenNebula VMs with SkyDNS
    """
    def run(self, interval=60):
        while True:
            self.sync()
            time.sleep(interval)
