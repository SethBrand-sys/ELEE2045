
import numpy as np
import matplotlib.pyplot as plt

#Voltage and Resistor values
v1 = 10
r1 = 10
r2 = 20
r3 = 40
r4 = 20


serr2r4 = r2 + r4 #R2 and R4 in series
res234 = ((r3*(serr2r4))/(r3+(serr2r4)))
req = res234 + r1 #Got equivalent resistance
totalcurrent = v1 / req #Got current
#print(f"Total Current: {'%.2f' % totalcurrent}")

v2 = totalcurrent * r1 #Got voltage from first resistor


voltdrop = v1 - v2 #Voltage left after first resistor
#print(f"Voltdrop: {'%.2f' % voltdrop}")

i3 = voltdrop / r3 #Current from R3 with voltdrop

r24 = r2 + r4 
i24 = voltdrop / r24 #Current in R2 and R4

if ("%.2f" % (i3 + i24)) == ("%.2f" % totalcurrent):
    print(f"The current in R1 is about {'%.2f' % totalcurrent} Amps\nThe current in R2 and in R4 is about {'%.2f' % i24} Amps\nThe current in R3 is about {'%.2f' % i3} Amps")

P1 = r1 * (totalcurrent**2)
P2 = r2 * (i24**2)
P3 = r3 * (i3**2)
P4 = r4 * (i24**2)

print(f"The power dissipated from R1 is {'%.2f' % P1} Watts")
print(f"The power dissipated from R2 is {'%.2f' % P2} Watts")
print(f"The power dissipated from R3 is {'%.2f' % P3} Watts")
print(f"The power dissipated from R4 is {'%.2f' % P4} Watts")

x = np.array(["R1", "R2", "R3", "R4"])
y = np.array([P1, P2, P3, P4])
fig,ax = plt.subplots()
plot = ax.bar(x,y)
plt.ylim(bottom = 0)
plt.xticks(["R1","R2","R3","R4"])
plt.xlabel("Resistor")
plt.ylabel("Power (Watts)")
plt.grid(True)
plt.title(label = "Power of Each Resistor in the Circuit")
plt.show()

# P = RI^2


