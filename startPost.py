import time, sched
import os
def event_func(msg):  
    print("Current Time:", time.strftime("%y-%m-%d %H:%M:%S"), 'msg:', msg)  
    os.system("python3 sendData.py")
    print("post data")
  
def run_function():  
    s = sched.scheduler(time.time, time.sleep)  
    s.enter(0, 2, event_func, ("Timer event.",))  
    s.run()  
  
def timer1():  
    while True:  
        time.sleep(500)  
        run_function()  
  
if __name__ == "__main__":  
    timer1()  
