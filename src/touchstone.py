from mocks.mocks import Mocks
from services import Services


class Touchstone(object):
    # start_mocks(), run_tests(), load_defaults(), exit()

    def __init__(self):
        self.services: Services = Services()
        self.mocks: Mocks = Mocks()

    def start_mocks(self):

# def __init__(self, services: List[Service], root: str = os.path.abspath('./')):
#     self.services: List[Service] = services
#     TouchstoneConfig.instance().set_root(root)
#     with open(os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json'), 'r') as file:
#         TouchstoneConfig.instance().merge(json.load(file))
#     self.mocks: Mocks = Mocks()
#
# def run(self):
#     try:
#         self.__run()
#     except (Exception, KeyboardInterrupt) as e:
#         print('\nTouchstone tests were interrupted. Cleaning up...')
#         DockerManager.instance().cleanup()
#         raise e
#
# def __run(self):
#     print(figlet_format('Touchstone', font='larry3d'))
#
#     self.mocks.start()
#
#     if TouchstoneConfig.instance().config['dev'] is True:
#         self.mocks.load_defaults()
#         self.mocks.print_available_mocks()
#         self.__accept_user_command()
#     else:
#         self.__exit(self.__run_all_service_tests())
#
# def __run_all_service_tests(self) -> bool:
#     results = []
#     for service in self.services:
#         results.append(service.run_tests(self.mocks))
#     if False in results:
#         print('One or more Touchstone tests failed.')
#         return False
#     else:
#         print('All Touchstone tests passed successfully!')
#         return True
#
# def __accept_user_command(self):
#     print('\nIn dev mode - keeping alive\n'
#           'run - Runs all Touchstone tests. Changed tests take affect until re-running Touchstone.\n'
#           'exit - Exit Touchstone dev mode.')
#     while True:
#         command = input('Touchstone Command: ')
#         if command == 'run':
#             self.__run_all_service_tests()
#             self.mocks.load_defaults()
#         elif command == 'exit':
#             self.__exit(True)
#         else:
#             print(f'Unknown command "{command}"')
#
# def __exit(self, did_pass: bool):
#     print('Exiting...')
#     if did_pass:
#         code = 0
#     else:
#         code = 1
#     DockerManager.instance().cleanup()
#     sys.exit(code)
