import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 69
random.seed(RANDOM_SEED)

class Proceso:
    def __init__(self, env, name, ram, cpu, num_instrucciones, cpu_speed):
        self.env = env
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.instrucciones_restantes = num_instrucciones
        self.cpu_speed = cpu_speed
        self.tiempo_inicio = env.now
        env.process(self.run()) # ejecuta el environment del proceso

    def run(self):
        memoria_requerida = random.randint(1,10)
        
        print(f"{self.name} iniciando con {memoria_requerida} memoria requerida y {self.instrucciones_restantes} instrucciones restantes")

        while self.ram.level < memoria_requerida:
            yield self.env.timeout(1)
            print(f"{self.name} espera por memoria")
        
        self.ram.get(memoria_requerida)
        print("RAM actual: ", self.ram.level)
        while self.instrucciones_restantes > 0:
            with self.cpu.request() as req:
                yield req
                yield self.env.timeout(1)
                
                self.instrucciones_restantes -= min(self.cpu_speed, self.instrucciones_restantes) # Para evitar instrucciones negativas
                print(f"{self.name} ejecuta {self.cpu_speed} instrucciones, {self.instrucciones_restantes} restantes")

                if self.instrucciones_restantes <= 0:
                    print(f"{self.name} termina")
                    break

                decision = random.randint(1, 2) # 1 -> waiting, 2 -> ready
                if decision == 1:
                    yield self.env.timeout(random.randint(1, 5))
                    print(f"{self.name} espera en I/O")
        self.ram.put(memoria_requerida)
        print("RAM actual: ", self.ram.level)

# Simulación básica
env = simpy.Environment()
cpu = simpy.Resource(env, 1)
ram = simpy.Container(env, 100, 100)

print("RAM inicial: ", ram.capacity)
proceso1 = Proceso(env, "Proceso 1", ram, cpu, random.randint(1,10), 3)
proceso2 = Proceso(env, "Proceso 2", ram, cpu, random.randint(1,10), 3)
proceso3 = Proceso(env, "Proceso 3", ram, cpu, random.randint(1,10), 3)

env.run(until=env.now + 11) # 10 ticks de prueba
