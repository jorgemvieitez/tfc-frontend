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
    do_style()
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text=f"Proyecto: {info_proj['nombre']}").grid(column=0, row=0, columnspan=4)
    
    def boton_atras():
        root.destroy()
        proyectos.window(user)

    def boton_borrar():
        (status, datos) = api.rq("delete", f"project/{project}", user)
        if status == False:
            if datos == "401 Unauthorized":
                popup("¡No tienes permisos para hacer esto!")
            else:
                popup(datos)
                root.destroy()
            return
        (status, datos) = api.rq("get", "project", user)
        if status == False:
            popup(datos)
            root.destroy()
            return

        root.destroy()
        proyectos.window(user)
    
    def boton_borrar_miembro(id):
        def inner(): pass
            
        return inner

    frm_main = tkinter.Frame(frm)
    frm_main.grid(columnspan=4)
    ttk.Label(frm_main, text=f"Canales").grid(column=0, row=0, columnspan=2)
    ttk.Label(frm_main, text=f"Miembros").grid(column=2, row=0, columnspan=2)

    if len(canales) == 0:
        ttk.Label(frm_main, text="<Ningún canal>").grid()

    for c in canales:
        clr_frm = tkinter.Frame(frm_main,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5, columnspan=2)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=c["nombre"]).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(dat_frm, text=c["type"]).grid(column=0, row=1, padx=5, pady=(0, 5))
        btn_abrir = ttk.Button(dat_frm, text="Abrir")
        btn_abrir.grid(column=1, row=0, rowspan=2, pady=5, padx=(0, 5))

        btn_abrir["state"] = "disabled"

    row = 1

    for m in miembros:
        (status, m_usr) = api.rq("get", f"user/{m['usuario']}", user)

        clr_frm = tkinter.Frame(frm_main,borderwidth=1, bg="grey")
        clr_frm.grid(pady=5, padx=5, columnspan=2, column=2, row=row)
        dat_frm = tkinter.Frame(clr_frm)
        dat_frm.grid()
        ttk.Label(dat_frm, text=m_usr["nombre"]).grid(column=2, row=0, padx=5, pady=5)
        ttk.Label(dat_frm, text=m["permisos"]).grid(column=2, row=1, padx=5, pady=(0, 5))

        clr_frm_usr = tkinter.Frame(dat_frm, borderwidth=1, bg="grey")
        clr_frm_usr.grid(pady=5, padx=5, column=3, row=0, rowspan=2)
        dat_frm_usr = tkinter.Frame(clr_frm_usr)
        dat_frm_usr.grid()
        tkinter.Button(dat_frm_usr, text="...").grid(column=0, row=0)
        tkinter.Button(dat_frm_usr, text="X", command=boton_borrar_miembro(m_usr["id"])).grid(column=1, row=0)

        row += 1

    ttk.Button(frm, text="Atrás", command=boton_atras).grid(column=0, row=3)
    ttk.Button(frm, text="Nombre").grid(column=1, row=3)
    ttk.Button(frm, text="+ Gente").grid(column=2, row=3)
    ttk.Button(frm, text="Eliminar", style="Red.TButton", command=boton_borrar).grid(column=3, row=3)
    
    root.mainloop()
