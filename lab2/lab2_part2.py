import serial
import csv
s = serial.Serial("COM3",115200)#note, replace serial_port with your serial port string


trials = []
for i in range(10):
    one_line = s.readline().decode().strip()
    trials.append(one_line)
print(trials)
with open("lab-1-SethBrand-sys/lab2/reactions.csv", "w") as reactions:
    for line in range(len(trials)):
        reactions.write(trials[line])
        reactions.write("\n")
    reactions.close()

s.close()

