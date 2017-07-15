import os
import sys
from importlib.machinery import SourceFileLoader

class Scanless:
    services = {}
    def __init_(self):
        pass


    def get_services(self):
        return self.services


    def get_helpers(self):
        for name,value in self.services.items():
            self.get_helper(name)


    def get_helper(self, service_name):
            self.services[service_name].help()

    #def execute_service(self, service_name,target):
    #    self.services[service_name].execute(target)

    def execute_service(self, worker_command):
        return self.services[worker_command.getService()].execute(worker_command.getTarget())


    def load_services(self,services_path):
        '''
        loadModules
        '''
        try:
            services = {}
            services_file = []
            for root, dirs, files in os.walk(os.path.abspath(services_path)):
                for file in files:
                    if file.endswith('.py'):
                        services_file.append(os.path.join(root, file))
            for s in services_file:
                service_name = os.path.splitext(os.path.basename(s))[0]
                self.services[service_name] = SourceFileLoader(service_name,s).load_module()
            return services
        except:
            print(sys.exc_info())
            pass
