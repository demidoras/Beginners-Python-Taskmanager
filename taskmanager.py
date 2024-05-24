#Bienvenido a mi taskmanager hecho con Python
#Author: Áster de Rivas

#Importamos el módulo nativo 'time' para poder usar funciones sleep
import time

#Importamos el módulo pickle para poder almacenar los datos que introduzcamos como tarea y recuperarlos
import pickle

#Importamos colorama para poder inicializarlo. Ya debe estar instalado en el sistema
from colorama import init
# Inicializamos Colorama
init()
#Importamos los diversos ajustes de colorama para el fondo, la letra, etc
from colorama import Fore, Back, Style

class Task:
#Clase que contiene lo necesario para mostrar una tarea con título, id y estado
    def __init__(self, id, title):
        self.title = title
        self.id = id
        #Dejamos self.done en "false" porque inicialmente todas las tareas estarán pendientes. Porque, si está completada, ¿para qué la añades a la lista?
        self.done = False

    def is_done(self):
        #Marca la tarea como completada.
        self.done = True

    #Devolvemos el estado de la tarea como una string u otra dependiendo de cuál sea, a partir del resultado booleano de is_done()
    def status(self):
       return Fore.GREEN + "Completada" + Fore.RESET if self.done else "Pendiente"

    #Permite devolver el estado de la tarea de un color concreto dependiendo del valor de este
    def status_color(self):
        if self.status == "Completada":
            return Fore.GREEN
        else:
            return Fore.RED

    def __str__(self):
        #Es lo que nos devolverá el contenido de la lista de tareas al llamarlo.
        return f"{self.id} - {self.title} - {self.status_color()}{self.status()}{Style.RESET_ALL}"

class TaskList:
#Clase que gestiona la lista de tareas como tal.
    def __init__(self):
        #Inicializamos una lista vacía de tareas.
        self.tasks = []
        #Con esto asignamos un id, que después se irá incrementando mediante lógica.
        self.next_id = 1
        self.load_task() #Necesitamos llamar a este método para cargar el archivo donde almacenamos las tareas cada vez que iniciamos el script

    #De esta forma localizamos los IDs de cada tarea
    def find_task_by_id(self, id):
        for task in self.tasks:
            if task.id == id:
                return task
        return None

    def add_task(self, title):
        #Agrega una nueva tarea a la lista.
        new_task = Task(self.next_id, title)
        self.tasks.append(new_task)
        #Esto nos permitirá que cada tarea tenga un id de x(número anterior)+1 y que no se repitan.
        '''También nos permite colocarle un id único a cada tarea y que, a diferencia del funcionamiento estándar de Python,
            que cambia todos los IDs si borramos una de las tareas, cada tarea mantenga su ID único por mucho que
            la lista se modifique.'''
        self.next_id += 1
        self.save_task()
        print(Fore.GREEN + f"La tarea '{title}' se ha agregado exitosamente" + Fore.RESET)


    def mark_task_done(self, id):
        #Marca una tarea como completada dada su posición en la lista, y si el índice no es válido maneja la excepción
        task = self.find_task_by_id(id)
        try:
            if task:
                task.is_done()
                self.save_task()
                print(Fore.GREEN + f"La tarea '{task.title}' se ha marcado como completada." + Fore.RESET)
            else:
                raise IndexError
        except IndexError:
            print("Error: El número de tarea no es válido")

    def show_all_tasks(self):
        #Muestra todas las tareas pendientes y completadas.
        if not self.tasks:
            print(Style.BRIGHT + Fore.RED + Back.WHITE + "La lista de tareas está vacía" + Style.RESET_ALL)
        else:
            for task in self.tasks:
                print(task)
                print()


    def delete_task(self, id):
        #Elimina una tarea de la lista dada su posición y maneja la excepción por índice no válido si la hay
        task = self.find_task_by_id(id)
        try:
            if task:
                self.tasks.remove(task)
                self.save_task()
                print()
                print(Fore.RED + f"Se ha borrado la tarea '{task.title}' con identificador '{id}'" + Fore.RESET)
                print(Fore.YELLOW + "Ten en cuenta que la lista ha cambiado")
                print("Aquí puedes ver la lista actualizada y los nuevos id de las tareas:" + Fore.RESET)
                print()
                time.sleep(1)
                task_list = TaskList()
                task_list.show_all_tasks()
                return
            else:
                raise IndexError
        except IndexError:
            print(Fore.RED + "Error: El número de tarea no es válido" + Fore.RESET)
            return

    def save_task(self):
        #Así guardamos todas las tareas que creemos en el archivo especificado
        with open("tasks.pickle", "wb") as file:
            task_data = [(task.id, task.title, task.done) for task in self.tasks]
            pickle.dump(task_data, file)

    def load_task(self):
        #Con esta función podremos cargar nuestro archivo de tareas al iniciar el código
        try:
            with open("tasks.pickle", "rb") as file:
                if file.seek(0, 2) == 0: #Esto comprueba la longitud del fichero y si es 0 es que está vacío
                    print(Style.BRIGHT + Fore.RED + Back.WHITE + "El archivo de tareas está vacío" + Style.RESET_ALL)
                    print()
                    return  #Si el archivo está vacío salimos del método
                else:
                    file.seek(0)
                    task_data = pickle.load(file)
                    self.tasks = []
                    for id, title, done in task_data:
                        task = Task(id, title)
                        task.done = done
                        self.tasks.append(task)
                        '''Se comprueban los IDs para asegurarnos de que no nos saltamos ningún número
                            y que tampoco hemos asignado un ID de uso futuro a una de nuestras tareas actuales'''
                        if id >= self.next_id:
                            self.next_id = id +1
        except FileNotFoundError:
            print(Fore.RED + "No se ha encontrado el archivo de tareas" + Fore.RESET)
            print()


def show_menu():
    #Muestra el menú de opciones
    print(Style.BRIGHT + Fore.BLUE + "\n--- Menú de gestión de tareas ---" + Style.RESET_ALL)
    print("-------------------------------------")
    time.sleep(0.5)
    print("1. Agregar una nueva tarea")
    time.sleep(0.5)
    print("2. Marcar una tarea como completada")
    time.sleep(0.5)
    print("3. Mostrar todas las tareas")
    time.sleep(0.5)
    print("4. Eliminar una tarea")
    time.sleep(0.5)
    print(Fore.RED + "5. Salir"+ Style.RESET_ALL)


def main():
    #El funcionamiento del menú principal del programa, que permite la interacción
    task_list = TaskList()
   
    #Preparo una condición para dar un mensaje de bienvenida solo si es la primera vez que se inicia el script
    message_displayed = False

    while True:
        if not message_displayed:
            print(Fore.WHITE + Back.MAGENTA + "¡Bienvenido al gestor de tareas!" + Style.RESET_ALL)
            message_displayed = True

    #Ahora empieza el loop que contiene el grueso del script
        time.sleep(2)
        show_menu()
        try:
            #
            print()
            option = int(input("Selecciona una opción: "))
            print()
            if option == 1:
                time.sleep(2)
                print(Fore.YELLOW + "Has escogido la opción:" + Fore.RESET, option)
                time.sleep(1)
                title = input(Fore.YELLOW + "Introduce el nombre de la nueva tarea: " + Fore.RESET)
                task_list.add_task(title)
                time.sleep(1)
                print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)
                time.sleep(1)

            elif option == 2:
                print(Fore.YELLOW + "¿Quieres marcar una tarea como completada? Estas son las tareas que tienes actualmente:" + Fore.RESET)
                task_list.show_all_tasks()
                id = int(input(Fore.YELLOW + "Introduce el número de la tarea que has terminado: " + Fore.RESET))
                time.sleep(1)
                task_list.mark_task_done(id)
                time.sleep(1)
                print()
                print(Back.BLACK + Fore.CYAN + "Esta es la lista actualizada de tareas:" + Fore.RESET)
                task_list.show_all_tasks()

            elif option == 3:
                time.sleep(1)
                print("Has escogido la opción:", option)
                print(Fore.YELLOW + "Se va a mostrar la lista completa de tareas" + Fore.RESET)
                print()
                time.sleep(2)
                task_list.show_all_tasks()
                time.sleep(1)
                print()
                print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)
                time.sleep(1)

            elif option == 4:
                if not task_list.tasks:
                    print(Fore.RED + "¡No se puede borrar nada! No hay ninguna tarea en la lista" + Fore.RESET)
                    print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)
                    time.sleep(2)
                else:
                    print("¿Quieres borrar una tarea? Se te va a mostrar la lista de tareas de nuevo")
                    task_list.show_all_tasks()
                    id = int(input(Fore.YELLOW + "Introduce el número de la tarea que quieres borrar: " + Fore.RESET))
                    task_list.delete_task(id)
                    time.sleep(0.5)
                    print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)

            elif option == 5:
                print()
                print(Fore.RED + "Saliendo del programa..." + Fore.RESET)
                break
            else:
                time.sleep(2)
                print(Fore.RED + "La opción introducida no es válida. Por favor, inténtalo de nuevo.")
                time.sleep(1)
                print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)
                time.sleep(1)

        except ValueError:
            print(Fore.RED + "Error: El valor introducido no es válido. Debes introducir un número.")
            print(Fore.MAGENTA + "Volviendo al menú..." + Fore.RESET)
            time.sleep(1)

if __name__ == "__main__":
    main()