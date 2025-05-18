import tkinter
from tkinter import ttk

import api

def window(user):
    (status, datos) = api.rq("get", "project", user)
    if status == False:
        raise Exception("Error " + datos)

    root = tkinter.Tk()
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0, columnspan=2)
    
    i = 1
    for d in datos:
        ttk.Label(frm, text=d["nombre"]).grid(column=0, row=i)
        i += 1

    root.mainloop()
