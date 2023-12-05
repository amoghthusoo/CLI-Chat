from multiprocessing import Process, Queue, Event
from time import sleep
from sys import getsizeof


class Task1:


    def terminate(self):
        raise Exception

    def task1(self, event):
        
        while True:

            if(event.is_set()):
                event.clear()
                break
            
            print("hello world")
            sleep(1)
            
def task2():

    event = Event()
    obj2 = Task1()

    process2 = Process(target=obj2.task1, args=(event,))
    process2.start()
    sleep(3)    
    event.set()
    

    sleep(1)

    print(event.is_set())
    
    

    

if __name__ == "__main__":
    
    process1 = Process(target = task2)
    process1.start()

   