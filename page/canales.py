import tkinter
from tkinter import font
from tkinter import ttk

import api
from utils import *
from page import proyectos, datos_canal

def main_data(root, frm, user, project, info_proj, canales, miembros):
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
        def inner():
            (status, datos) = api.rq("delete", f"project/{project}/member/{id}", user)
            if status == False:
                if datos == "401 Unauthorized":
                    popup("¡No tienes permiso para hacer eso!")
                else:
                    popup(datos)
                    root.destroy()
                    return
            (status, miembros) = api.rq("get", f"project/{project}/member", user)
            if status == False:
                popup(miembros)
                root.destroy()
                return
            
            frm.destroy()
            frm.__init__(root)
            main_data(root, frm, user, project, info_proj, canales, miembros)
            
        return inner
    
    def boton_crear_canal():
        (status, permisos_self) = api.rq("get", f"project/{project}/self", user)
        if status == False:
            popup(permisos_self)
            root.destroy()
            return
        
        if permisos_self["permisos"] == "Lectura":
            popup("¡No tienes permiso para hacer esto!")
            return

        (nombre, tipo) = datos_canal.crear_canal(info_proj['nombre'])

        if nombre == "": return

        (status, datos) = api.rq("post", f"project/{project}/channel", user , {"nombre": nombre, "type": tipo})
        if status == False:
            popup(datos)
            root.destroy()
            return

        (status, canales) = api.rq("get", f"project/{project}/channel", user)
        if status == False:
            popup(canales)
            root.destroy()
            return
        
        frm.destroy()
        frm.__init__(root)
        main_data(root, frm, user, project, info_proj, canales, miembros)

    def boton_borrar_canal(id):
        def inner():
            (status, datos) = api.rq("delete", f"project/{project}/channel/{id}", user)
            if status == False:
                if datos == "401 Unauthorized":
                    popup("¡No tienes permiso para hacer eso!")
                else:
                    popup(datos)
                    root.destroy()
                    return
            (status, canales) = api.rq("get", f"project/{project}/channel", user)
            if status == False:
                popup(canales)
                root.destroy()
                return
            
            frm.destroy()
            frm.__init__(root)
            main_data(root, frm, user, project, info_proj, canales, miembros)

        return inner
    
    def boton_añadir_miembro():
        (status, permisos_self) = api.rq("get", f"project/{project}/self", user)
        if status == False:
            popup(permisos_self)
            root.destroy()
            return
        
        if permisos_self["permisos"] != "Admin":
            popup("¡No tienes permiso para hacer esto!")
            return

        (id, permisos) = datos_canal.añadir_miembro(info_proj["nombre"])

        if id == "": return

        (status, datos) = api.rq("post", f"project/{project}/member", user , {"usuario": int(id), "permisos": permisos})
        if status == False:
            if datos == "404 Not Found":
                popup("El usuario no existe")
                return
            elif datos == "409 Conflict":
                popup("El usuario ya está en este proyecto")
                return
            else:
                popup(datos)
                root.destroy()
                return

        (status, miembros) = api.rq("get", f"project/{project}/member", user)
        if status == False:
            popup(miembros)
            root.destroy()
            return
        
        frm.destroy()
        frm.__init__(root)
        main_data(root, frm, user, project, info_proj, canales, miembros)

    frm.grid()
    ttk.Label(frm, text=f"Proyecto: {info_proj['nombre']}").grid(column=0, row=0, columnspan=4)
    
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
        brn_borrar = tkinter.Button(dat_frm, text="X", command=boton_borrar_canal(c["id"]))
        btn_abrir.grid(column=1, row=0, pady=5, rowspan=2)
        brn_borrar.grid(column=2, row=0, rowspan=2, padx=(0, 5))

        btn_abrir["state"] = "disabled"

    tkinter.Button(frm_main, text="+", font = font.BOLD, command=boton_crear_canal).grid(column=0, columnspan=2)

    row = 1

    for m in miembros:
        (status, m_usr) = api.rq("get", f"user/{m['usuario']}", user)
        if status == False:
            popup(m_usr)
            root.destroy()
            return

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
        btn_echar = tkinter.Button(dat_frm_usr, text="X", command=boton_borrar_miembro(m_usr["id"]))
        btn_echar.grid(column=1, row=0)

        if user == m_usr["id"]:
            btn_echar["state"] = "disabled"

        row += 1

    ttk.Button(frm, text="Atrás", command=boton_atras).grid(column=0, row=3)
    ttk.Button(frm, text="Nombre").grid(column=1, row=3)
    ttk.Button(frm, text="+ Gente", command=boton_añadir_miembro).grid(column=2, row=3)
    ttk.Button(frm, text="Eliminar", style="Red.TButton", command=boton_borrar).grid(column=3, row=3)
    
    root.mainloop()

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
    main_data(root, frm, user, project, info_proj, canales, miembros)