from Tkinter import *
import Adafruit_DHT


def getSensorData():
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
    # return dict
    return (str(RH), str(T))


root = Tk()

var = StringVar()
label = Label(root, textvariable=var, relief=RAISED)

RH, T = getSensorData()
var.set("Humidity: %s, Temperature: %s" % (RH, T))
label.pack()
root.mainloop()
