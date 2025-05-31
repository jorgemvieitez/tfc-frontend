import tkinter
from tkinter import ttk

def crear_canal(project_name):
    popup = tkinter.Toplevel()
    tkinter.Label(popup, text = f"Creando un nuevo canal en {project_name}").grid(row=0, columnspan=3)
    name_var = tkinter.StringVar()
    type_var = tkinter.StringVar()
    ttk.Label(popup, text = "Nombre").grid()
    tkinter.Entry(popup, textvariable=name_var).grid(row=1, column=1, columnspan=2)
    ttk.Label(popup, text = "Tipo").grid()
    combo = ttk.Combobox(popup, textvariable=type_var, values=["Texto", "Documento", "Kanban"], state="readonly")
    combo.grid(row=2, column=1, columnspan=2)
    combo.current(0)

    def boton_ok():
        if name_var.get() != "":
            popup.destroy()

    def boton_cancelar():
        name_var.set("")
        type_var.set("")
        popup.destroy()

    frm_buttons = ttk.Frame(popup)
    frm_buttons.grid(columnspan=3)
    ttk.Button(frm_buttons, text ="OK", command=boton_ok).grid(column=0)
    ttk.Button(frm_buttons, text ="Cancelar", command=boton_cancelar).grid(column=1, row= 0)

    popup.wait_window()

    return (name_var.get(), type_var.get())

def modificar_canal():
    pass

def añadir_miembro(project_name):
    popup = tkinter.Toplevel()
    tkinter.Label(popup, text = f"Añadiendo un nuevo miembro a {project_name}").grid(row=0, columnspan=3)
    id_var = tkinter.StringVar()
    type_var = tkinter.StringVar()
    ttk.Label(popup, text = "ID").grid()
    tkinter.Entry(popup, textvariable=id_var).grid(row=1, column=1, columnspan=2)
    ttk.Label(popup, text = "Permisos").grid()
    combo = ttk.Combobox(popup, textvariable=type_var, values=["Lectura", "Moderación", "Admin"], state="readonly")
    combo.grid(row=2, column=1, columnspan=2)
    combo.current(0)

    def boton_ok():
        if id_var.get() != "" and id_var.get().isnumeric():
            popup.destroy()

    def boton_cancelar():
        id_var.set("")
        type_var.set("")
        popup.destroy()

    frm_buttons = ttk.Frame(popup)
    frm_buttons.grid(columnspan=3)
    ttk.Button(frm_buttons, text ="OK", command=boton_ok).grid(column=0)
    ttk.Button(frm_buttons, text ="Cancelar", command=boton_cancelar).grid(column=1, row= 0)

    popup.wait_window()

    return (id_var.get(), type_var.get().replace("ó", "o"))

def modificar_permisos_miembro():
    pass