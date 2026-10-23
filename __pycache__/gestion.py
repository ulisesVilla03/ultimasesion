import json
from datetime import datetime
#clase tarea
class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False #hasta que nosotros no le demos una indicacion de que ya esta completado debe mantenerse
        #en false (sin completar)
    def marcar_completado(self):
        self.completado = True
    def editar_tarea(self, nuevo_titulo, nueva_descripcion, nueva_fecha):
        self.titulo = nuevo_titulo
        self.descripcion = nueva_descripcion
        self.fecha_vencimiento = nueva_fecha

class Usuario:
    def __init__(self, nombre_usuario, contraseña):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.tareas = []
    def agregar_tarea(self,tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, titulo_tarea):
        self.tareas = [tarea for tarea in self.tareas if tarea.titulo != titulo_tarea]
#recorre toda la lista de tareas hasta llegar a que tenga el titulo al igual que al ingresado
    def obtener_tareas(self):
        return self.tareas

#gestion de tareas
class sistema_gestion_tareas:
    #inicializacion del sistema de un archivo
    def __init__(self, archivo_datos = "datos_usuario.json"):
        self.usuarios = {}
        self.archivo_datos = archivo_datos
        self.cargar_datos()

    def cargar_datos(self):
        #cargar datos de los usuarios en json
        try:
            with open (self.archivo_datos, "r") as archivo:
                datos = json.load(archivo)
                for nombre_usuario, info in datos.items():
                    #crea un objeto usuario para cada usuario en los datos
                    usuario_obj = Usuario(nombre_usuario, info["contraseña"])
                for tarea_info in info ["tareas"]:
                    #crea un objeto tarea para cada usuario
                    tarea = Tarea(tarea_info["titulo"], tarea_info ["descripcion"], tarea_info["fecha_vencimiento"]) 
                    tarea.completado = tarea_info ["completado"]
                    usuario_obj.agregar_tarea(tarea)
                self.usuarios[nombre_usuario] = usuario_obj
        except FileNotFoundError: #manejo de escepciones 
            print ("Archivo de datos no encontrado, se creara uno nuevo al guardar")

    def guardar_datos(self):
        #guardar datos del usuario en archivo
        datos = {}
        for nombre_usuarios, usuario in self.usuarios.items():
            #organiza las tareas y la informacion del usuario en el diccionario
            datos[nombre_usuarios] = { 
                "contraseña": usuario.contraseña,
                "tareas": [
                    {"titulo": tarea.titulo, "descripcion": tarea.descripcion, "fecha_vencimiento": tarea.fecha_vencimiento,"completado": tarea.completado}
                    for tarea in usuario.tareas
                ]
            }
        with open(self.archivo_datos, "w") as archivo:
            json.dump(datos, archivo)

    def registrar_usuario(self,nombre_usuario, contraseña):
        #registrar un nuevo usuario
        if nombre_usuario in self.usuarios:
            print("El nombre de usuario ya existe")
            return False
        else:
            self.usuarios[nombre_usuario] = Usuario(nombre_usuario,contraseña)
            self.guardar_datos()
            print("Usuario registrado con exito")
            return True
    def iniciar_sesion(self, nombre_usuario, contraseña):
        usuario = self.usuarios.get(nombre_usuario)
        if usuario and usuario.contraseña == contraseña:
            print("Inicio de sesion exitoso")
            return usuario
        else:
            print("Nombre de usuario o contraseña incorrectos")
            return None

    def menu_usuario(self, usuario):
        while True:
            print("\n1. crear tarea")
            print("2. ver tarea")
            print("3. editar tarea")
            print("4. completar tarea")
            print("5. elimianr tarea")
            print("6. Cerrar sesion")

            opcion= input("Selecciona una opcion: ")
            if opcion == "1":
                titulo = input("Titulo de la tarea: ")
                descripcion = input("Ingresa la descripcion: ")
                fecha_vencimiento = input("Fecha de vencimiento(YYYY-MM-DD): ")
                nueva_tarea = Tarea(titulo, descripcion,fecha_vencimiento)
                usuario.agregar_tarea(nueva_tarea)
                self.guardar_datos()
                print("Tarea entregada con exito")
            elif opcion == "2":
                tareas = usuario.obtener_tareas()
                if not tareas:
                    print("No tienes tareas") 
                for idx, tarea in enumerate(tareas, start=1):
                    estado = "Completado" if tarea.completado else "Pendiente"
                    print(f"{idx}.{tarea.titulo} - {estado} (vence: {tarea.fecha_vencimiento})") 
            elif opcion == "3":
                titulo_tarea = input("Titulo de la tarea a editar: ")
                tarea = next((t for t in usuario.tareas if t.titulo == titulo_tarea), None )
                if tarea:
                    nuevo_titulo = input("Nuevo titulo: ")
                    nueva_descripcion = input("Nueva descripcion: ")
                    nueva_fecha = input("Nueva fecha de vencimiento (YYYY-MM-DD): ")
                    tarea.editar_tarea(nuevo_titulo, nueva_descripcion, nueva_fecha)
                    self.guardar_datos()
                    print("Trea actualizada con exito")
                else:
                    print("Tarea no encontrada")

            elif opcion == "4":
                titulo_tarea = input("Titulo de la tarea a completar: ")
                tarea = next ((t for t in usuario.tareas if titulo == titulo_tarea), None)
                if tarea:
                    tarea.marcar_completada()
                    self.guardar_datos()
                    print("Tarea marcada como completada")
                else:
                    print("Tarea no encontrada")

            elif opcion == "5":
                titulo_tarea = input("Titulo de la tarea a eliminar: ")
                usuario.eliminar_tarea (titulo_tarea)
                self.guardar_datos()
                print("Tarea eliminada con exito")

            elif opcion == "6":
                print("Cerrando sesion...")
                break
            else:
                print("Opcion no valida. Intentalo de nuevo.")
if __name__ == "__main__":
    sistema = sistema_gestion_tareas()
    while True:
        print("\n----- Sistema de Gestion de Tareas------")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            nombre_usuario = input("Ingrese nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            sistema.registrar_usuario(nombre_usuario, contraseña)

        elif opcion == "2":
            nombre_usuario = input ("Nombre de usuario: ")
            contraseña = input ("Ingrese la contraseña: ")
            usuario = sistema.iniciar_sesion(nombre_usuario, contraseña)
            if usuario:
                sistema.menu_usuario(usuario)

        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion no valida. Intentalo de nuevo")
    