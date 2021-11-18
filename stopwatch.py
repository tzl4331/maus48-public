import time
import threading

StopwatchActivateStatus = True

def Start():
    
    def Stopwatch():
        hours = 0
        minutes = 0
        seconds = 0

        global StopwatchActivateStatus
        
        while StopwatchActivateStatus:
            time.sleep(1)
            seconds+=1

            if seconds == 60:
                minutes += 1
                seconds -= 60

            if minutes == 60:
                hours += 1
                minutes -= 60    
            
            print ("{0} : {1} : {2}".format(str(hours).zfill(1), str(minutes).zfill(2), str(seconds).zfill(2)))

    T2 = threading.Thread(target=Stopwatch)
    T2.start()

Start()