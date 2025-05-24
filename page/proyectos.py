import tkinter
from tkinter import ttk
from tkinter import font

import api
from utils import *
from page import canales

def window(user):
    (status, datos) = api.rq("get", "project", user)
    if status == False:
        popup_no_main_window(datos)
        return

    root = tkinter.Tk()
    frm = tkinter.Frame(root)
    frm.grid()
    ttk.Label(frm, text="Proyectos disponibles").grid(column=0, row=0, columnspan=2)
    
    def boton_abrir(id):
        def inner():
            root.destroy()
            canales.window(user, id)
        return inner

    def boton_crear(): pass

    row = 1

    for d in datos:
        clr_frm = tkinter.Frame(frm,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=d["nombre"]).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(dat_frm, command=boton_abrir(d["id"]), text="Abrir").grid(column=1, row=0, pady=5, padx=(0, 5))

        row += 1
    
    tkinter.Button(frm, text="+", font = font.BOLD, command=boton_crear).grid(column=0, row=row)

    root.mainloop()
