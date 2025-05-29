import tkinter
from tkinter import ttk

import api
from utils import *
from page import proyectos

def window(user, project):
    (status, info_proj) = api.rq("get", f"project/{project}", user)
    if status == False:
        popup_no_main_window(info_proj)
        return

    (status, canales) = api.rq("get", f"project/{project}/channel", user)
    if status == False:
        popup_no_main_window(canales)
        return

    (status, miembros) = api.rq("get", f"project/{project}/member", user)
    if status == False:
        popup_no_main_window(miembros)
        return

    root = tkinter.Tk()
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text=f"Proyecto: {info_proj['nombre']}").grid(column=0, row=0, columnspan=4)
    ttk.Label(frm, text=f"Canales").grid(column=0, row=1, columnspan=2)
    ttk.Label(frm, text=f"Miembros").grid(column=2, row=1, columnspan=2)
    
    def boton_atras():
        root.destroy()
        proyectos.window(user)

    def boton_abrir(id):
        def inner(): pass
        return inner

    row_c = 1
    row_m = 2

    for c in canales:
        clr_frm = tkinter.Frame(frm,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5, columnspan=2)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=c["nombre"]).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(dat_frm, text=c["type"]).grid(column=0, row=1, padx=5, pady=(0, 5))
        ttk.Button(dat_frm, command=boton_abrir(c["id"]), text="Abrir").grid(column=1, row=0, rowspan=2, pady=5, padx=(0, 5))

        row_c += 1

    for m in miembros:
        (status, m_usr) = api.rq("get", f"user/{m['usuario']}", user)

        clr_frm = tkinter.Frame(frm,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5, columnspan=2, column=2, row=row_m)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=m_usr["nombre"]).grid(column=2, row=0, padx=5, pady=5)
        ttk.Label(dat_frm, text=m["permisos"]).grid(column=2, row=1, padx=5, pady=(0, 5))

        row_m += 1
    
    row = max(row_c, row_m)

    ttk.Button(frm, text="Atrás", command=boton_atras).grid(column=0, row=row)
    ttk.Button(frm, text="Ajustes").grid(column=1, row=row)
    ttk.Button(frm, text="Salir").grid(column=2, row=row)
    
    root.mainloop()
