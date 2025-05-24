import tkinter
from tkinter import ttk

def popup(text):
    popup = tkinter.Toplevel()
    tkinter.Label(popup, text = text).grid()
    tkinter.Button(popup, text ="OK", command= popup.destroy).grid(row =1)
    popup.wait_window()

def popup_no_main_window(text):
    popup = tkinter.Tk()
    tkinter.Label(popup, text = text).grid()
    tkinter.Button(popup, text ="OK", command= popup.destroy).grid(row =1)
    popup.mainloop()

def popup_ask_name(text):
    popup = tkinter.Toplevel()
    tkinter.Label(popup, text = text).grid(row=0, columnspan=2)
    name_var = tkinter.StringVar()
    tkinter.Entry(popup, textvariable=name_var).grid(row=1, columnspan=2)

    def boton_ok():
        if name_var.get() != "":
            popup.destroy()

    def boton_cancelar():
        popup.destroy()
        name_var.set("")

    ttk.Button(popup, text ="OK", command=boton_ok).grid(row =2, column=0)
    ttk.Button(popup, text ="Cancelar", command=boton_cancelar).grid(row =2, column=1)

    popup.wait_window()

    return name_var.get()