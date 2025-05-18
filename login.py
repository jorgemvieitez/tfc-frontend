import tkinter
from tkinter import ttk

global user

def window():
    root = tkinter.Tk()
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0, columnspan=2)
    ttk.Label(root, text="Usuario").grid(column=0, row=1)
    user_var = tkinter.StringVar()
    ttk.Entry(root, textvariable=user_var).grid(column=1, row=1)

    def boton_empezar():
        if user_var.get().isnumeric():
            global user
            user = int(user_var.get())
            root.destroy()

    ttk.Button(root, text="Empezar", command=boton_empezar).grid(column=0, row=2, columnspan=2)
    root.mainloop()
