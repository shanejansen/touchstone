from typing import List

from touchstone.lib.listeners.i_services_available_listener import IServicesAvailableListener


class TsContext(object):
    def __init__(self):
        self.__services_available_listeners: List[IServicesAvailableListener] = []
        self.__triggered_services_available: bool = False

    def register_services_available_listener(self, listener: IServicesAvailableListener):
        self.__services_available_listeners.append(listener)

    def trigger_services_available(self):
        if not self.__triggered_services_available:
            self.__triggered_services_available = True
            for listener in self.__services_available_listeners:
                listener.services_available()
