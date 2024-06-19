import matplotlib.pyplot as plt
import numpy as np

listint1 = []
listint2 = []

with open("lab-1-SethBrand-sys/lab2/reactions.csv", "r") as reactions:
    ctrllist1 = reactions.readlines()
    reactions.close()

for i in range(len(ctrllist1)):
    ctrllist1[i] = ctrllist1[i].replace("\n","")
    ctrllist1[i] = ctrllist1[i].split(",")

for i in range(len(ctrllist1)):
    listint1.append(int(ctrllist1[i][0]))
    listint2.append(int(ctrllist1[i][1]))

x = [1,2,3,4,5,6,7,8,9,10]
y = listint2
colorslist = []
avglist = []
for i in range(len(x)):
    b = listint2[i] - listint1[i]
    if b > 0:
        colorslist.append("b")
        avglist.append(b)
    else:
        colorslist.append("r")
        
avg = 0
for i in range(len(avglist)):
    avg = avg + avglist[i]
avg = avg / len(avglist)

ar = np.array((x,y))
fig,ax = plt.subplots()
ax.bar(x,y, width = 0.9, color = colorslist, )
ax.set_xticks(x)
ax.set_xlabel("Trial")
ax.set_ylabel("Time (ms)")
ax.set_title(f"Average Reaction Time for Valid Trials: {avg} (ms)")
plt.savefig("lab-1-SethBrand-sys/lab2/reactions.png")
plt.show()