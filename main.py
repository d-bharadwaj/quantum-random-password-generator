import numpy as np

# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from ibm_quantum_widgets import *
from qiskit.providers.aer import QasmSimulator
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumRegister, ClassicalRegister, execute
from qiskit import QuantumCircuit, execute, Aer, IBMQ
import operator as op

# Loading your IBM Quantum account(s)
provider = IBMQ.load_account()

backend = Aer.get_backend('qasm_simulator')

q = QuantumRegister(5, 'q')
c = ClassicalRegister(5, 'c')

circuit = QuantumCircuit(q, c)
circuit.h(q[0])
circuit.h(q[1])
circuit.h(q[2])
circuit.h(q[3])
circuit.h(q[4])

circuit.measure(q, c)
#circuit.draw() will draw out our circuit 


alphabet_code = {
    "00000" : 'A',
    "00001" : 'B',
    "00010" : 'C',
    "00011" : 'D',
    "00100" : 'E',
    "00101" : 'F',
    "00110" : 'G',
    "00111" : 'H',
    "01000" : 'I',
    "01001" : 'J',
    "01010" : 'K',
    "01011" : 'L',
    "01100" : 'M',
    "01101" : 'N',
    "01110" : 'O',
    "01111" : 'P',
    "10000" : 'Q',
    "10001" : 'R',
    "10010" : 'S',
    "10011" : 'T',
    "10100" : 'U',
    "10101" : 'V',
    "10110" : 'W',
    "10111" : 'X',
    "11000" : 'Y',
    "11001" : 'Z',
    "11010" : '!',
    "11011" : '?',
    "11100" : '*',
    "11101" : '$',
    "11110" : '#',
    "11111" : '-',
}


def password_generator():
    job = execute(circuit, backend)
    result = job.result()
    count = result.get_counts(circuit)

    #choose a password length between 10 and 13 (inclusive)
    maximum = max(count.items(), key=op.itemgetter(1))[0]
    count.pop(maximum)
    password_length = int(maximum, 2)%4 # converting a binary to integer with int using 2 as parameter
    password_length += 10

    #we chose a random number through this way ^ for the number of letters to maximize randomness

    #assigns 10-13 characters to a temporary password builder 
    passwordBuilder = ""
    for x in range(password_length):
        maximum = max(count.items(), key=op.itemgetter(1))[0]
        count.pop(maximum)
        passwordBuilder += alphabet_code.get(maximum)


    #chooses up to 3 random indexes
    indexes = []
    for x in range(3):
        maximum = max(count.items(), key=op.itemgetter(1))[0]
        count.pop(maximum)
        next_index = int(maximum, 2)%password_length
        indexes.append(next_index)


    #changes characters at chosen indexes to numbers
    password = ""
    num = 0 
    for x in range(password_length):
        if (x in indexes and num == 0):
            password += passwordBuilder[x].lower()
            num += 1
        elif x in indexes:
            password += str(x)
            
        else:
            password += passwordBuilder[x]
    
    #adds a number (between 0 and 31) to the end of the password
    maximum = max(count.items(), key=op.itemgetter(1))[0]
    count.pop(maximum)
    number = str(int(maximum, 2))
    password += number

    return password


def main():
    result = password_generator()
    print(result)

if __name__ == '__main__':
    main()