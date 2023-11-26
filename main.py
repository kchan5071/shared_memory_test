import time
from multiprocessing import Process, Value
import random

class Counter:
    def __init__(self, start, end, increment, rand, done):
        self.increment = increment
        self.rand = rand
        self.start = start
        self.end = end
        self.num = start
        self.sqnum = start
        self.done = done

    def count(self):
        while self.num < self.end:
            self.num += 1
            self.increment.value = self.num
        
        self.done.value = True

    def rand_count(self):
        while not self.done.value:
            self.sqnum = random.randint(1, 100000000)
            self.rand.value = self.sqnum

class Reader:
    def __init__(self, increment, rand, done):
        self.increment = increment
        self.rand = rand
        self.done = done
        self.max_iterations = 100

    def read(self):
        while not self.done.value and self.max_iterations > 0:
            inc = self.increment.value
            rd = self.rand.value
            print(f"increment = {inc}, rand = {rd}")
            time.sleep(.5)
            self.max_iterations -= 1

def main():
    start = time.perf_counter()
    
    #create process to count to 100000
    max = 100000

    inc = Value('i', 0)
    rand = Value('i', 0)
    done = Value('b', False)
    counter = Counter(0, max, inc, rand, done)
    p1 = Process(target=counter.count)
    p2 = Process(target=counter.rand_count) 

    #create process to read current count every 1 second
    p3 = Process(target=Reader(inc, rand, done).read)

    #start processes
    p1.start()
    p2.start()
    p3.start()

    #join processes
    p1.join()
    p2.join()
    p3.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")

if __name__ == '__main__':
    main()