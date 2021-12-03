from random import randint
from time import sleep
from threading import Thread, Lock

pratos = [0, 0, 0, 0, 0] 

class Filosofo(Thread):
    alive = True

    def __init__(self, name, fork_left, fork_right, time_to_eat, time_to_wait):
        Thread.__init__(self)
        self.name = name
        self.time_to_eat = time_to_eat
        self.time_to_wait = time_to_wait
        self.fork_left = fork_left
        self.fork_right = fork_right

    def run(self):
        while self.alive:
            waitingTime = 0
            rand = randint(5, 15)

            print(f"\n{self.name} está pensando")
            sleep(rand) 
            alreadyEat = self.eat()

            if alreadyEat == 1: #verificação se ele conseguiu comer ou nao
                waitingTime = 0
            else:
                waitingTime += rand

            if (waitingTime + 5) > self.time_to_wait:  #resolução do starvation
                self.fork_left.acquire(True)
                self.fork_right.acquire(True)
                print(f"\n{self.name} começou a comer")
                sleep(self.time_to_eat)
                print(f"\n{self.name} parou de comer")
                pratos[names.index(self.name)] += 1
                print("Quantidade que cada filósofo comeu: ", pratos)
                self.fork_left.release()  # libera o garfo 1
                self.fork_right.release()  # libera o garfo 2

    def eat(self):
        fork1, fork2, name = self.fork_left, self.fork_right, self.name

        print(f"\n{self.name} quer comer e tenta pegar um garfo")

        fork1.acquire(True)
        noLocked = fork2.acquire(False)  # verifica se o segundo não está sendo usado

        if noLocked:
            print(f"\n{self.name} começou a comer")
            sleep(self.time_to_eat)
            print(f"\n{self.name} parou de comer")
            pratos[names.index(self.name)] += 1  # quantas vezes cada filosofo comeu
            print("Quantidade que cada filósofo comeu: ", pratos)
            fork1.release()  # libera o garfo 1
            fork2.release()  # libera o garfo 2
            return 1
        else:
            fork1.release()  # libera o primeiro garfo pra não gerar deadlock
            print(f"\n{self.name} não conseguiu comer")
            return 0


names = ['Filósofo 1', 'Filósofo 2', 'Filósofo 3', 'Filósofo 4', 'Filósofo 5']
forks = [Lock() for _ in range(5)]
timeToEat = [randint(1, 5) for _ in range(5)] #tempo que cada um demora para comer
timeToWait = [randint(25, 50) for _ in range(5)] #tempo que cada um pode ficar sem comer
table = [Filosofo(names[i], forks[i % 5], forks[(i + 1) % 5], timeToEat[i], timeToWait[i]) for i in range(5)]

for filosofo in table:
    filosofo.start()  
    sleep(1)