import numpy as np

arr1 = np.array([[i*j for i in range(10)] for j in range(10)])

def MAP_printer(MAP):
    for row in MAP:
        print(row)
    print()

cropedarr1 = arr1[4:6,0:4]

MAP_printer(arr1)
MAP_printer(cropedarr1)