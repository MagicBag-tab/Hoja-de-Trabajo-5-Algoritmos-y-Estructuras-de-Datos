import simpy
import random
import numpy as np
import pandas as pd

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
