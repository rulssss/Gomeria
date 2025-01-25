from funciones import *
import tkinter as tk
from tkinter import ttk, messagebox




class Gomeria:
    def __init__(self, master, username, account_type):
        self.master = master
        self.master.title("rls")

        

        # Configurar la ventana para que tome el tamaño de la pantalla sin ser pantalla completa
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")
        self.master.update_idletasks()  # Asegura que la geometría se actualice
        #self.master.state('zoomed')  # Maximiza la ventana
        self.master.geometry("1000x600")
        self.master.minsize(800, 600)  # Tamaño mínimo de la ventana

        # Cargar la imagen del icono
        icon_path = resource_path("resources/goma.ico")  # Ruta relativa a la imagen del icono
        self.master.iconbitmap(icon_path)


        # Crear la barra de navegación
        self.create_navbar()

        # Mostrar ID del usuario de forma transparente y bienvenida
        self.mostrar_id_inicio(username)
        


        # Mostrar pestañas según el tipo de cuenta
        if account_type:  # Si es True, mostrar todas las pestañas

            pass

        else:  # Si es False, mostrar solo Buscar Datos y Administración

            pass

        # Configurar estilo para eliminar bordes del Notebook
        # Configurar estilo para aumentar tamaño de fuente y cambiar colores de las pestañas
        style = ttk.Style()
        style.configure("CustomNotebook.TNotebook", borderwidth=0, background="white")
        style.configure("CustomNotebook.TNotebook.Tab", font=("Segoe UI", 11), padding=[10, 5])
        style.map("CustomNotebook.TNotebook.Tab", background=[("selected", "#d1e0e0")], foreground=[("selected", "#000000")])

    
    def create_navbar(self):
        self.navbar = tk.Frame(self.master, bg="gray")
        self.navbar.place(x=0, y=0, relwidth=1, height=50)

        # Agregar botones a la barra de navegación
        buttons = ["Home", "About", "Services", "Products", "Clients", "Contact", "Help", "Settings"]
        self.navbar_buttons = []
        for i, btn_text in enumerate(buttons):
            btn = tk.Button(self.navbar, text=btn_text, command=lambda text=btn_text: self.navbar_action(text), font=("Segoe UI", 14))
            btn.place(relx=i/len(buttons), rely=0, relwidth=1/len(buttons), relheight=1)
            self.navbar_buttons.append(btn)

    def navbar_action(self, text):
        print(f"Button {text} clicked")

    def on_resize(self, event):
        self.navbar.place(x=0, y=0, relwidth=1, height=50)
        for i, btn in enumerate(self.navbar_buttons):
            btn.place(relx=i/len(self.navbar_buttons), rely=0, relwidth=1/len(self.navbar_buttons), relheight=1)




    def mostrar_id_inicio(self, username):
        # Simular la obtención del ID del usuario
        id_usuario = obtener_id_usuario(username)  # Método que debes implementar

         # Mostrar mensaje de bienvenida como un título en la parte superior
        self.bienvenida = tk.Label(self.master, text="Bienvenido!", font=("Segoe UI", 50))
        self.bienvenida.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Etiqueta transparente para mostrar el ID
        self.id_label = tk.Label(
            self.master,
            text=f"ID usuario: {id_usuario}",
            font=("Segoe UI", 30, "bold"),
            bg="black",
            fg="white",
            relief="flat", bd=3, padx=15
        )
        self.id_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Configurar opacidad simulada y desaparecer después de 3 segundos
        self.bienvenida.after(10000, self.bienvenida.destroy)
        self.id_label.after(5000, self.id_label.destroy)



#Crear la ventana principal
root = tk.Tk()
app = Gomeria(root, "mariano", True)
root.mainloop()