from page import login, proyectos

creds = login.window()
if hasattr(login, "user"):
    proyectos.window(login.user)