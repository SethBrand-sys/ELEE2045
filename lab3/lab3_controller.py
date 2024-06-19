import paho.mqtt.client as mqtt
import time
import tkinter as tk




root = tk.Tk()
root.title("WiFi Color Changer")
light_status_var = tk.StringVar()
if light_status_var.get() == "":
    light_status_var.set("ON")
light_time_var = tk.StringVar()
if light_time_var.get() == "":
    light_time_var.set("Unkown")
light_color_var = tk.StringVar()
if light_color_var.get() == "":
    light_color_var.set("#000000")

def myButtonCallback():
    r = red.get()
    g = green.get()
    b = blue.get()
    client.publish(light_control_color, f"{r}{g}{b}")
    
    
#light_control_color
#light_control_status






def toggleLight():
    status = 1 if light_status_var.get() == "ON" else 1
    client.publish(light_control_status, bytearray([status]))
    
def setHex(re,gr,bl):
    print(hex(re))
    re = hex(re)[2:]
    gr = hex(gr)[2:]
    bl = hex(bl)[2:]
    rgb = [str(re),str(gr),str(bl)]
    print(rgb)
    rgb = ''.join(rgb)
    print(rgb)
    light_color_var.set(rgb)
    return


def myRepeatedCallback():
    print(light_time_var.get()) 
    root.after(2000, myRepeatedCallback)

def pumpMQTT():
    client.loop(0)
    root.after(10,pumpMQTT)




frame1 = tk.LabelFrame(root, labelanchor = "n", text = "Light Status", height = 200, width = 200)

frame1.grid(row = 1, column = 2)

frame2 = tk.LabelFrame(root, labelanchor = "n", text = "Light Color", height = 200, width = 160)
frame2.grid(row = 3, column = 2)

canvas = tk.Canvas(frame1, height = 200, width = 200)
canvas.grid(row = 2, column = 1)
canvas2 = tk.Canvas(frame2, height = 200, width = 150)
canvas2.grid(row=4,column = 1)
status = canvas.create_text(100,175, text = light_status_var.get(), fill = 'red')
clock = canvas.create_text(100,25, text = light_time_var.get(),fill ='red')
color = canvas.create_rectangle(50,50,150,150, fill = light_color_var.get())


lbl = tk.Label(root, text = "Color Changer")
lbl.grid(row = 0, column = 2)
btn = tk.Button(root, text = "Set Color", command = myButtonCallback)
btn.grid(row = 2,column = 1)
btn2 = tk.Button(root, text = "Toggle Light", command = toggleLight)
btn2.grid(row = 2, column = 3)




red = tk.Scale(frame2, from_ = 0, to = 255, orient='horizontal', troughcolor = 'red')
red.grid(row = 3, column = 2)
red.place(x = 25, y = 0)
blue = tk.Scale(frame2, from_ = 0, to = 255, orient='horizontal', troughcolor= 'blue')
blue.grid(row = 3, column = 2)
blue.place(x = 25, y = 100)
green = tk.Scale(frame2, from_ = 0, to = 255, orient='horizontal', troughcolor= 'green')
green.grid(row = 3, column = 2)
green.place(x = 25, y = 50)









myRepeatedCallback()


client_id = 'client1'
broker = 'test.mosquitto.org'
light_control_color = 'elee2045sp23/811899823/light_control_color'
light_control_status = 'elee2045sp23/811899823/light_control_status'
topic_status = 'elee2045sp23/811899823/light_status'




def onMessageFromLight(client_obj,userdata, message:mqtt.MQTTMessage):

    print(f"Message received: {message.payload.decode('utf8')}")
    if message.topic == topic_status:
        status =int(message.payload[0])
        print(status)
        r = int(message.payload[0])
        g = int(message.payload[1])
        b = int(message.payload[2])
        setHex(r,g,b)

        
        if status:
            light_status_var.set("ON")
        else:
            light_status_var.set("OFF")
        light_time_var.set(time.ctime())


client = mqtt.Client(client_id)
client.on_message = onMessageFromLight
client.connect(broker)
client.subscribe(light_control_color)
client.subscribe(light_control_status)
client.subscribe(topic_status)  
pumpMQTT()
root.mainloop()







while True:
    client.loop_forever()
    time.sleep(1)

