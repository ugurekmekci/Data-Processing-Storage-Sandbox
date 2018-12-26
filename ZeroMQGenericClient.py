from library.ConfigProvider.ConfigProvider import ConfigProvider
from library.ProcessCommunication.ProcessCommunication import ZeroMQProvider


class connectZeroMQ(object):

    def __init__(self):
        self.process_communication = ZeroMQProvider()
        self.config_file = ConfigProvider().configReplicationFile()

    def zeroMQServer(self):
        zeroMQServer = self.process_communication.initializeServer(
            protocol=self.config_file['AppManagerStart']['AppManagerStartServer']['protocol'],
            bind_port=self.config_file['AppManagerStart']['AppManagerStartServer']['bind_port'],
            url=self.config_file['AppManagerStart']['AppManagerStartServer']['url']
        )
        return zeroMQServer

    def zeroMQClient(self):
        zeroMQClient = self.process_communication.initializeCli(
            protocol=self.config_file['AppManagerStart']['AppManagerStartClient']['protocol'],
            bind_port=self.config_file['AppManagerStart']['AppManagerStartClient']['bind_port'],
            url=self.config_file['AppManagerStart']['AppManagerStartClient']['url']
        )
        return zeroMQClient
