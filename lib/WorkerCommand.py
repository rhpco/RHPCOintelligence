import os
import sys

class WorkerCommand(object):

    _service=False
    _target=False
    _parameters={}

    def __init__(self, service, target, parameters):
        self.setService(service)
        self.setTarget(target)
        self.setParameters(parameters)


    def setService(self,service):
        self._service = service
        return

    def getService(self):
        return self._service

    def setTarget(self,target):
        self._target = target
        return

    def getTarget(self):
        return self._target

    def addParameter(self,key,value):
        self._parameters[key]=value
        return

    def setParameters(self,parameters):
        self._parameters = parameters
        return

    def getParameters(self):
        return self._parameters

