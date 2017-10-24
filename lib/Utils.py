import os
import sys

class Utils:
    @staticmethod
    def createServiceList(scanners):
        serviceList = []
        if not isinstance(scanners,list):
            serviceList.append(scanners)
            return serviceList
        else:
            serviceList = scanners

        return serviceList
