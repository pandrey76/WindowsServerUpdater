'''
Created on Aug 27, 2016
@author: Burkhard
'''

# Scheduling imports
import schedule

# Windows Service imports
import win32service
import win32serviceutil  
import win32event                              

import os
import os.path
from ActivateEngine import Engine


class PythonTaskSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonWindowsServerUpdater"
    _svc_display_name_ = "Python Windows Service Updater"
    _svc_description_ = "This Python schedules tasks service updating windows system services"
      
    def __init__(self, args):
        """

        :param args:
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
        
    def SvcDoRun(self):  
        def job():
            try:
                engine = Engine(600)
                engine.run()
            except Exception as er:
                with open("c:\\13.txt", 'a') as g:
                    g.write(str(er))
                    g.write(os.linesep)

        schedule.every(1).minutes.do(job)
        
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            schedule.run_pending()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)  
            
    def SvcStop(self):  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        win32event.SetEvent(self.hWaitStop)  


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PythonTaskSvc)
    
#===============================================================================
# python Task_Scheduler_Svc.py install
# python Task_Scheduler_Svc.py remove

# Usage: 'Task_Scheduler_Svc.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]'
# Options for 'install' and 'update' commands only:
#  --username domain\username : The Username the service is to run under
#  --password password : The password for the username
#  --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
#  --interactive : Allow the service to interact with the desktop.
#  --perfmonini file: .ini file to use for registering performance monitor data
#  --perfmondll file: .dll file to use when querying the service for
#    performance data, default = perfmondata.dll
# Options for 'start' and 'stop' commands only:
#  --wait seconds: Wait for the service to actually start or stop.
#                  If you specify --wait with the 'stop' option, the service
#                  and all dependent services will be stopped, each waiting
#                  the specified period.
#===============================================================================
