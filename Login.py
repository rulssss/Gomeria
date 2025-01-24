import tkinter as tk
from tkinter import ttk, messagebox
from funciones import *
from funciones import *
from validacion import check_activation, validate_code
import uuid
from validacion import * 
## VENTANA DE LOGINS 


class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x300")
        self.master.resizable(False, False)  # Deshabilitar redimensionamiento

        # Centrar la ventana
        self.center_window()

        # Cargar o inicializar la configuración
        config = load_activation_data()
        if 'start_date' not in config or 'business_id' not in config:
            config['start_date'] = datetime.now().strftime("%Y-%m-%d")
            config['business_id'] = generate_business_id()  # Generar un business_id más corto
            save_activation_data(config)

        # Verificar la activación
        activated, validation_code = check_activation()
        if not activated:
            self.request_validation_code(validation_code)
        elif hay_admin():
            self.open_login_window()
        else:
            self.create_register_window()

    def center_window(self):
        window_width = 400
        window_height = 420
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.master.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        # Cargar la imagen del icono
        icon_path = resource_path("resources/r.ico")  # Ruta relativa a la imagen del icono
        self.master.iconbitmap(icon_path)

    def request_validation_code(self, validation_code):
        for widget in self.master.winfo_children():
            widget.destroy()

        config = load_activation_data()
        start_date, business_id = config.get('start_date', 'Fecha no disponible'), config.get('business_id', 'ID no disponible')
        
        tk.Label(self.master, text=f"ID del negocio: {business_id}", font=("Segoe UI", 12)).pack(pady=10)
        tk.Label(self.master, text=f"Fecha de inicio del negocio: {start_date}", font=("Segoe UI", 12)).pack(pady=10)
        tk.Label(self.master, text="Ingrese el código de validación", font=("Segoe UI", 14)).pack(pady=20)
        
        self.validation_entry = tk.Entry(self.master, font=("Segoe UI", 12))
        self.validation_entry.pack(pady=10)

        def copy_business_id():
            self.master.clipboard_clear()
            self.master.clipboard_append(business_id)
            messagebox.showinfo("Copiado", "ID del negocio copiado al portapapeles")

        tk.Button(self.master, text="Copiar ID del negocio", command=copy_business_id, font=("Segoe UI", 12)).pack(pady=10)

        def validate():
            input_code = self.validation_entry.get().strip()
            result = validate_code(input_code, business_id)
            if result == True:
                messagebox.showinfo("Validación", "Código de validación correcto. El programa se ha activado por otros 30 días.")
                self.__init__(self.master)
            elif result == -1:
                messagebox.showinfo("Validación", "Código de validación correcto. La validación mensual ha sido desactivada.")
                self.__init__(self.master)
            else:
                messagebox.showerror("Error", "Código de validación incorrecto. El programa se cerrará.")
                self.master.destroy()

        tk.Button(self.master, text="Validar", command=validate, font=("Segoe UI", 12)).pack(pady=10)
        self.master.bind("<Return>", lambda event: validate())

    

    def create_register_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Registrar Cuenta", font=("Segoe UI", 14)).pack(pady=20)
        tk.Label(self.master, text="Tipo de cuenta:", font=("Segoe UI", 12)).pack(pady=10)
        self.account_type = ttk.Combobox(self.master, values=["Usuario", "Administrador"], font=("Segoe UI", 12), state="readonly")
        self.account_type.set("Administrador")  # Establecer "Administrador" como valor predeterminado
        self.account_type.pack(pady=10)

        tk.Label(self.master, text="Usuario:", font=("Segoe UI", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.master, font=("Segoe UI", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Contraseña:", font=("Segoe UI", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(pady=5)

        # Crear el botón "Registrar"
        register_button = tk.Button(self.master, text="Registrar", command=self.register_user, font=("Segoe UI", 12))
        register_button.pack(pady=10)
        # Vincular la tecla Enter al comando del botón "Registrar"
        self.master.bind("<Return>", lambda event: register_button.invoke())

        tk.Button(self.master, text="< Volver", command=self.open_login_window, font=("Segoe UI", 10)).pack(side="left", anchor="sw", padx=10, pady=10)

    def id_para_registrar(self):
        if hay_admin():
            id_window = tk.Toplevel(self.master)
            id_window.title("Ingresar ID para Registrar")
            id_window.geometry("400x200")
            id_window.resizable(False, False)  # Deshabilitar redimensionamiento
            id_window.grab_set()  # Bloquear la ventana principal
            
            # Centrar la ventana
            window_width = 400
            window_height = 200
            screen_width = id_window.winfo_screenwidth()
            screen_height = id_window.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            id_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

            tk.Label(id_window, text="Ingrese el ID para registrar:", font=("Segoe UI", 14)).pack(pady=20)
            self.id_entry = tk.Entry(id_window, font=("Segoe UI", 12))
            self.id_entry.pack(pady=10)

            def validar_id():
                id_value = self.id_entry.get().strip()
                if id_value == "-1":
                    id_window.destroy()
                    self.id_entry = None  # Limpiar la entrada de ID
                    return True
                else:
                    messagebox.showerror("Error", "ID incorrecto")
                    return False

            # Crear el botón "Aceptar"
            aceptar_button = tk.Button(id_window, text="Aceptar", command=lambda: self.master.after(0, lambda: validar_id() and id_window.destroy()), font=("Segoe UI", 12))
            aceptar_button.pack(pady=10)
            # Vincular la tecla Enter al comando del botón "Aceptar"
            id_window.bind("<Return>", lambda event: aceptar_button.invoke())

            id_window.wait_window()  # Esperar a que la ventana se cierre
            return self.id_entry is None  # Retornar True si la entrada de ID fue limpiada (ID correcto)
            
            
        else:
            return False


    def register_user(self):
        account = self.account_type.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password or not account:
            messagebox.showerror("Error", "Debe ingresar un tipo de usuario, nombre de usuario y contraseña")
        elif existe_usuario(username):
            messagebox.showerror("Error", "Usuario ya registrado.")
            
            
        else:
            # Función para enviar el usuario y contraseña a la base de datos
            if hay_admin() and account == "Administrador":
                id_window = tk.Toplevel(self.master)
                id_window.title("Ingresar ID para Registrar")
                id_window.geometry("400x200")
                id_window.resizable(False, False)  # Deshabilitar redimensionamiento
                id_window.grab_set()  # Bloquear la ventana principal
                
                # Centrar la ventana
                window_width = 400
                window_height = 200
                screen_width = id_window.winfo_screenwidth()
                screen_height = id_window.winfo_screenheight()
                position_top = int(screen_height / 2 - window_height / 2)
                position_right = int(screen_width / 2 - window_width / 2)
                id_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

                tk.Label(id_window, text="Ingrese el ID para registrar:", font=("Segoe UI", 14)).pack(pady=20)
                self.id_entry = tk.Entry(id_window, font=("Segoe UI", 12))
                self.id_entry.pack(pady=10)


                def validar_id():
                    id_value = self.id_entry.get().strip()
                    if id_value == "-1":
                        registrar_usuario(username, password, account)
                        messagebox.showinfo("Registro", f"{account} {username} registrado correctamente")
                        id_window.destroy()
                        self.open_login_window()
                        self.id_entry = None  # Limpiar la entrada de ID
                        
                    else:
                        messagebox.showerror("Error", "ID incorrecto")
                        


                # Crear el botón "Aceptar"
                aceptar_button = tk.Button(id_window, text="Aceptar", command=lambda: self.master.after(0, lambda: validar_id() and id_window.destroy()), font=("Segoe UI", 12))
                aceptar_button.pack(pady=10)
                # Vincular la tecla Enter al comando del botón "Aceptar"
                id_window.bind("<Return>", lambda event: aceptar_button.invoke())
            
            else:
                registrar_usuario(username, password, account)
                messagebox.showinfo("Registro", f"{account} {username} registrado correctamente")
                self.open_login_window()

                
        

    def open_login_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Seleccione tipo de cuenta:", font=("Segoe UI", 14)).pack(pady=20)
        self.account_type = ttk.Combobox(self.master, values=["Usuario", "Administrador"], font=("Segoe UI", 12), state="readonly")
        self.account_type.set("Administrador")  # Establecer "Administrador" como valor predeterminado
        self.account_type.pack(pady=10)

        tk.Label(self.master, text="Usuario:", font=("Segoe UI", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.master, font=("Segoe UI", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Contraseña:", font=("Segoe UI", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(pady=5)

        # Crear el botón "Aceptar"
        aceptar_button = tk.Button(self.master, text="Aceptar", command=self.login, font=("Segoe UI", 12))
        aceptar_button.pack(pady=10)
        # Vincular la tecla Enter al comando del botón "Aceptar"
        self.master.bind("<Return>", lambda event: aceptar_button.invoke())

        tk.Button(self.master, text="Registrar cuenta", command=self.create_register_window, font=("Segoe UI", 10)).pack(pady=5)
        tk.Button(self.master, text="Recuperar cuenta", command=self.open_recover_window, font=("Segoe UI", 10)).pack(pady=5)

    def open_recover_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Recuperar Cuenta", font=("Segoe UI", 14)).pack(pady=20)
        tk.Label(self.master, text="ID de recuperación:", font=("Segoe UI", 12)).pack(pady=5)
        self.recover_id_entry = tk.Entry(self.master, font=("Segoe UI", 12))
        validate_id = self.master.register(self.validate_numeric_input)
        self.recover_id_entry.config(validate="key", validatecommand=(validate_id, "%P"))
        self.recover_id_entry.pack(pady=10)

        # Crear el botón "Aceptar"
        aceptar_button = tk.Button(self.master, text="Aceptar", command=self.recover_account, font=("Segoe UI", 12))
        aceptar_button.pack(pady=10)
        # Vincular la tecla Enter al comando del botón "Aceptar"
        self.master.bind("<Return>", lambda event: aceptar_button.invoke())

        tk.Button(self.master, text="< Volver", command=self.open_login_window, font=("Segoe UI", 10)).pack(side="left", anchor="sw", padx=10, pady=10)

    def validate_numeric_input(self, input_value):
        return input_value.isdigit() or input_value == ""

    def recover_account(self):
        global recover_id
        recover_id = self.recover_id_entry.get()

        if not recover_id:
            messagebox.showerror("Error", "Debe ingresar el ID de recuperación")
        elif not existencia_de_id(recover_id):
            messagebox.showerror("Error", "ID Incorrecto")
        else:
            self.open_reset_password_window()

    def open_reset_password_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Reestablecer Contraseña", font=("Segoe UI", 14)).pack(pady=20)
        tk.Label(self.master, text="Contraseña nueva:", font=("Segoe UI", 12)).pack(pady=5)
        self.new_password_entry = tk.Entry(self.master, show="*", font=("Segoe UI", 12))
        self.new_password_entry.pack(pady=5)

        tk.Label(self.master, text="Repetir contraseña:", font=("Segoe UI", 12)).pack(pady=5)
        self.repeat_password_entry = tk.Entry(self.master, show="*", font=("Segoe UI", 12))
        self.repeat_password_entry.pack(pady=5)

        # Crear el botón "Aceptar"
        aceptar_button = tk.Button(self.master, text="Aceptar", command=self.confirm_password, font=("Segoe UI", 12))
        aceptar_button.pack(pady=10)
        # Vincular la tecla Enter al comando del botón "Aceptar"
        self.master.bind("<Return>", lambda event: aceptar_button.invoke())

        tk.Button(self.master, text="<< Volver", command=self.open_login_window, font=("Segoe UI", 10)).pack(side="left", anchor="sw", padx=10, pady=10)

    def confirm_password(self):
        new_password = self.new_password_entry.get()
        repeat_password = self.repeat_password_entry.get()

        if not new_password or not repeat_password:
            messagebox.showerror("Error", "Las contraseñas no pueden estar vacías")
        elif new_password != repeat_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
        else:
            actualizar_contrasena(new_password, recover_id)
            messagebox.showinfo("Recuperación", "Contraseña reestablecida correctamente")
            self.open_login_window()

    def login(self):
        account = self.account_type.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Debe ingresar un nombre de usuario y una contraseña")
        elif not existe_usuario(username):
            messagebox.showerror("Error", "Usuario no encontrado.")
        elif verificar_contrasenia(password, username, account):
            messagebox.showerror("Error", "Contraseña incorrecta o tipo de usuario mal seleccionado.")
        else:
            messagebox.showinfo("Acceso", f"Accediendo como {account} con usuario {username}")
            self.master.destroy()
            #minimarket_root = tk.Tk()
            if account == "Usuario":
                account = False
            else:
                account = True
                
            # DAR INICIO A LA VENTANA PRINCIPAL



            
# Crear la ventana principal
root = tk.Tk()
app = Login(root)
root.mainloop()