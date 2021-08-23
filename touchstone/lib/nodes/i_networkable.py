import abc

from touchstone.lib.networking.i_network import INetwork


class INetworkable(object):
    @abc.abstractmethod
    def get_network(self) -> INetwork:
        pass
