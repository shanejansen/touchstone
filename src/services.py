# parses services from config. can build and run dockerfile from each service

class Services(object):
    def __init__(self):
        self.temp = ''

    def __parse_services(self):
