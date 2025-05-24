import tkinter
from tkinter import ttk
from tkinter import font

import api
from utils import *
from page import canales

def main_data(root, frm, user, datos):
    def boton_abrir(id):
        def inner():
            root.destroy()
            canales.window(user, id)
        return inner

    def boton_crear():
        nombre = popup_ask_name("Nombre del proyecto")
        if nombre == "": return
        (status, datos) = api.rq("post", "project", user, {"nombre": nombre})
        if status == False:
            popup(datos)
            root.destroy()
        (status, datos) = api.rq("get", "project", user)
        if status == False:
            popup(datos)
            root.destroy()

        frm.destroy()
        frm.__init__(root)
        main_data(root, frm, user, datos)
    
    def boton_borrar(id):
        def inner():
            (status, datos) = api.rq("delete", f"project/{id}", user)
            if status == False:
                if datos == "401 Unauthorized":
                    popup("¡No tienes permiso para hacer eso!")
                else:
                    popup(datos)
                    root.destroy()
            (status, datos) = api.rq("get", "project", user)
            if status == False:
                popup(datos)
                root.destroy()

            frm.destroy()
            frm.__init__(root)
            main_data(root, frm, user, datos)
        return inner

    frm.grid()
    ttk.Label(frm, text="Proyectos disponibles").grid(column=0, row=0, columnspan=2)

    row = 1

    for d in datos:
        clr_frm = tkinter.Frame(frm,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=d["nombre"]).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(dat_frm, command=boton_abrir(d["id"]), text="Abrir").grid(column=1, row=0, pady=5, padx=(0, 5))
        tkinter.Button(dat_frm, text="X", command=boton_borrar(d["id"])).grid(column=2, row=0)

        row += 1
    
    tkinter.Button(frm, text="+", font = font.BOLD, command=boton_crear).grid(column=0, row=row)

def window(user):
    (status, datos) = api.rq("get", "project", user)
    if status == False:
        popup_no_main_window(datos)
        return

    root = tkinter.Tk()
    frm = tkinter.Frame(root)

    main_data(root, frm, user, datos)

    root.mainloop()
