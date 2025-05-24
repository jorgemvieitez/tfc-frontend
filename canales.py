import tkinter
from tkinter import ttk

import api
from utils import *
import proyectos

def window(user, project):
    (status1, info_proj) = api.rq("get", f"project/{project}", user)
    (status2, datos) = api.rq("get", f"project/{project}/channel", user)
    if status1 == False or status2 == False:
        popup_no_main_window(datos)
        return

    root = tkinter.Tk()
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text=f"Proyecto: {info_proj['nombre']}").grid(column=0, row=0, columnspan=2)
    
    def boton_atras():
        root.destroy()
        proyectos.window(user)

    def boton_abrir(id):
        def inner(): pass
        return inner

    row = 1

    for d in datos:
        clr_frm = tkinter.Frame(frm,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5, columnspan=2)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=d["nombre"]).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(dat_frm, text=d["type"]).grid(column=0, row=1, padx=5, pady=(0, 5))
        ttk.Button(dat_frm, command=boton_abrir(d["id"]), text="Abrir").grid(column=1, row=0, rowspan=2, pady=5, padx=(0, 5))

        row += 1
    
    ttk.Button(frm, text= "Atrás", command=boton_atras).grid(column=0, row=row)
    ttk.Button(frm, text= "Ajustes").grid(column=1, row=row)
    
    root.mainloop()
