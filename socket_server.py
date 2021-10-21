#!/usr/bin/env python3
import socket
import numpy as np
import json
import time
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

      
HOST = '172.20.10.3'   # Standard loopback interface address
PORT = 6531            # Port to listen on (use ports > 1023)

plt_array = {}
source = ["Gyro", "Acce"]
ax = ["x", "y", "z"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("listen!")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            # print(len(data)) ## 201
            try:
                json_data = json.loads(data)
                print('Received data from socket client:', json_data)
                if not plt_array:
                    plt_array = json_data
                for ss in source:
                    for aa in ax:
                        if not isinstance(plt_array[ss][aa], list):
                            plt_array[ss][aa] = [plt_array[ss][aa], json_data[ss][aa]]
                        else:
                            plt_array[ss][aa].append(json_data[ss][aa])

            except:
                break

# plt_array = {'Gyro': {'x': [280.0, 290.0], 'y': [-1890.0, -1789.0], 'z': [770.0, 800.0]}, 'Acce': {'x': [18.0,20.0], 'y': [-27.0, -25.0], 'z': [1001.0, 1011.0]}}
print(plt_array)
fig = plt.figure(figsize = plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot(plt_array["Gyro"]["x"], plt_array["Gyro"]["y"], plt_array["Gyro"]["z"], label = "Gyro", color="blue")
ax.legend()
ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.plot(plt_array["Acce"]["x"], plt_array["Acce"]["y"], plt_array["Acce"]["z"], label = "Acce", color="red")
ax.legend()
plt.show()



                
