from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# creacion de la ventana
from sklearn import tree

root = Tk()
root.title("Administracion del Personal")
root.geometry("600x350")
root.resizable(False, False)

miId = StringVar()
miNombre = StringVar()
miCargo = StringVar()
miSalario = StringVar()


# conexion a la base de datos
def conexionBBDD():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()

    try:
        miCursor.execute("CREATE TABLE IF NO EXISTS empleado(ID INTEGER PRYMARY KEY AUTOINCREMENT,NOMBRE TEXT,CARGO TEXT,SALARIO INT)")
        miConexion.commit()
        miCursor.close()
        miConexion.close()
        messagebox.showinfo("CONEXION", "Base de datos creada exitosamente")
    except:
        messagebox.showinfo("CONEXION", "Conexion exitosa con la base de datos")

def eliminarBBDD():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()
    if messagebox.askyesno(message="Lo datsos se borran totalmente, desea continuar?", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE empleado")
    else:
        pass
    limpiarCampos()
    mostrar()




def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")

def mensaje():
    acerca = '''
    Aplicacion: Administracion del Personal.
    Version: 1.0
    Lenguaje de Programacion: Python 3.8.5
    Creador: Ing. Jose Alberto Vasquez Lorenzo.
    Fecha: 10/01/2021.
    '''
    messagebox.showinfo(title= "Informacion", message= acerca)

# ###################### Metodos para el CRUD ################################

def crear():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()

    try:
        datos = miNombre.get(), miCargo.get(), miSalario.get()
        miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", datos)
        miConexion.commit()

    except:
        messagebox.showwarning("ADVERTENCIA:", "Ocurrio un error al crear el registro, verifique la conexion con la base de datos")
        pass
    limpiarCampos()
    mostrar()

def mostrar():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)

    try:
        miCursor.execute("SELECT * FROM empleado")
        miConexion.commit()
        for row in miCursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))

    except:
        pass

# ################################ Tabla ##########################################
tree = ttk.Treeview(height = 10, columns = ('#0', '#1', '#2'))
tree.place(x =0, y = 130)
tree.column('#0', width = 100)
tree.heading('#0', text = "ID", anchor = CENTER)
tree.heading('#1', text = "Nombre del empleado", anchor = CENTER)
tree.heading('#2', text = "Cargo", anchor = CENTER)
tree.column('#3', width = 100)
tree.heading('#3', text = "Salario", anchor = CENTER)


def seleccionar(event):
    item = tree.identify('item', event.x,event.y)
    miId.set(tree.item(item, "text"))
    miNombre.set(tree.item(item, "values")[0])
    miCargo.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])

tree.bind("<Double-1>", seleccionar)


def actualizar():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()

    try:
        datos = miNombre.get(), miCargo.get(), miSalario.get()
        miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=? WHERE ID=" + miId.get(), datos)
        miConexion.commit()

    except:
        messagebox.showwarning("ADVERTENCIA:", "Ocurrio un error al actualizar el registro")
        pass
    limpiarCampos()
    mostrar()

def borrar():
    miConexion = sqlite3.connect('base.db')
    miCursor = miConexion.cursor()


    try:
        if messagebox.askyesno(message="Desea eliminar el registro?", title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM empleado WHERE ID=" + miId.get())
            miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al tratar de eliminar el registro")
        pass
    limpiarCampos()
    mostrar()



# ################# Colocar los elementos en la ventana #######################################

# Creando la barra de menu de la aplicacion
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff = 0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command = conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command = eliminarBBDD)
menubasedat.add_command(label="Salir ", command = root.quit)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff = 0)
ayudamenu.add_command(label="Limpiar Campos", command = limpiarCampos)
ayudamenu.add_command(label="Acerca de", command = mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

root.config(menu=menubar)

# Creando las entrada de los datos en la ventana
e1= Entry(root, textvariable = miId)
l2= Label(root, text = "Nombre")
l2.place(x = 50, y = 10)
e2 = Entry(root, textvariable = miNombre, width = 50)
e2.place(x = 100, y = 10)

l3= Label(root, text = "Cargo")
l3.place(x = 50, y = 40)
e3 = Entry(root, textvariable = miCargo)
e3.place(x = 100, y = 40)

l4= Label(root, text = "Salario")
l4.place(x =280 , y = 40)
e4 = Entry(root, textvariable = miSalario, width = 10)
e4.place(x = 320, y = 40)

l4= Label(root, text = "RD$")
l4.place(x =385, y = 40)

# Creando los botones

b1 = Button(root, text = "Agregar Registro", command = crear)
b1.place(x = 50, y = 90)

b2 = Button(root, text = "Actualizar Registro", command = actualizar)
b2.place(x = 180, y = 90)

b3 = Button(root, text = "Listar Registro", command = mostrar)
b3.place(x = 320, y = 90)

b4 = Button(root, text = "Eliminar Registro", bg = "red", command = borrar)
b4.place(x = 450, y = 90)


root.mainloop()