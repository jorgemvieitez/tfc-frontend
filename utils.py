import tkinter
def popup(text, command):
    popup = tkinter.Toplevel()
    label = tkinter.Label(popup, text = text)
    label.grid()
    btn = tkinter.Button(popup, text ="OK", command= command)
    btn.grid(row =1)


def popup_no_main_window(text):
    popup = tkinter.Tk()
    label = tkinter.Label(popup, text = text)
    label.grid()
    btn = tkinter.Button(popup, text ="OK", command= popup.destroy)
    btn.grid(row =1)
    popup.mainloop()
