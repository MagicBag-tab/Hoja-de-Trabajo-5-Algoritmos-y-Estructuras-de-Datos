
import simpy
import random
import numpy as np
import pandas as pd

random.seed(7)
np.random.seed(7)

def proceso(env, name, RAM, CPU, data):
    ## Asignación de espacio de memoria, de 1 a 10 unidades:
    memory = random.randint(1, 10)
    # Asignación de números de instrucciones por proceso:
    instruction = random.randint(1, 10)
    arrivalTime = env.now

    print(f"{env.now}: El Proceso {name} se encuentra solicitando {memory} unidades de memoria RAM.")

    # Verifica si hay suficiente memoria RAM para asignarle al proceso las unidades que necesita 
    with RAM.get(memory) as request:
        # Momento de espera para recibir RAM
        yield request
        print(f"{env.now}: El Proceso {name} ahora contiene {memory} unidades de memoria RAM")

        while instruction > 0:  # Verifica que haya más de una instrucción en el proceso para que la CPU pueda avanzar con la simulación.
            with CPU.request() as CPURequest:
                yield CPURequest
                realized = min(3, instruction)  # Definir los 3 ciclos que la CPU puede procesar.
                yield env.timeout(1)
                instruction -= realized
                print(f"{env.now}: En el proceso {name} se han logrado ejecutar {realized} instrucciones. Por lo tanto, quedan {instruction} instrucciones.")

                # Momento de espera:
                if instruction > 0 and random.choice([1, 2]) == 1:
                    print(f"{env.now}: El proceso {name} ha entrado en espera.")
                    yield env.timeout(3)
                else:
                    print(f"{env.now}: El proceso {name} ha regresado para ser evaluado de nuevo.")

    yield RAM.put(memory)
    print(f"{env.now}: El proceso {name} ha sido completado. Se han liberado {memory} unidades de RAM.")
    complete = env.now
    data.append([name, arrivalTime, complete, complete - arrivalTime])

    """
    Función donde se le asigan a la RAM y al CPU sus valores y ver como
    es que se desencuelven los procesos según sus capacidades.
    """
def RAM_simulation(env, process, data):
    # Asignarle a la RAM 100 unidades libres:
    RAM = simpy.Container(env, init=100, capacity=100) 
    # Asignarle al CPU como evaluador de un solo proceso:
    CPU = simpy.Resource(env, capacity=1)

    for i in range(process):
        env.process(proceso(env, f"No.{i + 1}", RAM, CPU, data))
        # Asignación de intervalos de inicio o llegada:
        yield env.timeout(random.expovariate(1.0 / 5))
        
def calculator():
    env = simpy.Environment()
    # Definir el número de procesos:
    process = 200
    data = []  # Lista para Excel

    env.process(RAM_simulation(env, process, data))
    env.run()

    # PANDAS:
    df = pd.DataFrame(data, columns=["Proceso", "Tiempo de Llegada en segundos", "Tiempo Finalizado en segundos", "Tiempo Ejecutado en segundos"])

    # Desviación estándar:
    dev = np.std(df["Tiempo Ejecutado en segundos"])
    print(f"Desviación estándar: {dev}")

    df.to_csv("SimulaciónG2P200.csv", index=False)
    df.to_excel("Resultados.xlsx", index=False)
    print("Los datos se han guardado.")

calculator()