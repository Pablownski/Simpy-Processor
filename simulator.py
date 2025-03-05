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
        tiempos.append(self.env.now - self.tiempo_inicio)
        print("RAM actual: ", self.ram.level)

def correr_simulacion(num_procesos, intervalo, ram_size, cpu_speed, num_cpus):
    global tiempos
    tiempos = []
    
    env = simpy.Environment()
    ram = simpy.Container(env, init=ram_size, capacity=ram_size)
    cpu = simpy.Resource(env, capacity=num_cpus)
    
    def generar_procesos(env):
        for i in range(num_procesos):
            yield env.timeout(random.expovariate(1.0 / intervalo))
            Proceso(env, f"Proceso-{i}", ram, cpu, random.randint(1, 10), cpu_speed)
    print("RAM inicial: ", ram.capacity)
    env.process(generar_procesos(env))
    env.run()
    
    return np.mean(tiempos), np.std(tiempos)


