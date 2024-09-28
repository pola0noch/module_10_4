# Домашнее задание по теме "Очереди для обмена данными между потоками."

import queue
from threading import Thread
import threading
import random
import time
from queue import Queue


class Table:
    def __init__(self, number, guest = None):
        self.number = number
        self.guest = guest

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        delay = random.randint(3, 10)
        time.sleep(delay)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            found_table = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    threading.Thread(target=guest.run).start()
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    found_table = True
                    break
            if not found_table:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        threading.Thread(target=new_guest.run).start()


tables = [Table(number) for number in range(1, 6)]

guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)

cafe.guest_arrival(*guests)
cafe.discuss_guests()







