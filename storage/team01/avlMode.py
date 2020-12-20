#Funciones que deben estar disponibles para que el componente SQL Parser pueda hacer uso de estas

import avl
from typing import Any

mBBDD = avl.AVL()

#Crea una base de datos. (CREATE)
def createDatabase(database: str) -> int:
    res = mBBDD.agregar(database)
    return res #0 operación exitosa, 1 error en la operación, 2 base de datos existente

#Renombra la base de datos databaseOld por databaseNew. (UPDATE)
def alterDatabase(databaseOld: str, databaseNew) -> int:
    if databaseOld in mBBDD:
        if databaseNew not in mBBDD:
            res = mBBDD.quitar(databaseOld)
            if res == 0:
                res = mBBDD.agregar(databaseNew)
                return res #0 si operación es exitosa
            else:
                return 1 #Error en la operación
        else:
            return 3 #databaseNew existente            
    else:
        return 2 #databaseOld no existente
		

#Elimina por completo la base de datos indicada en database. (DELETE)
def dropDatabase(database: str) -> int:
    res = mBBDD.quitar(database)
    return res #0 operación exitosa, 1 error en la operación, 2 base de datos no existente

# show databases by constructing a list
def showDatabases() -> list:
    if mBBDD.tamano == 0:
        return []
    else:
        return list(mBBDD.raiz)

#Crea una tabla en una base de datos especificada
def createTable(database: str, table: str, numberColumns: int) -> int:
    if database in mBBDD:
        nodoBD = mBBDD.obtener(database)
        if nodoBD:
            if table not in nodoBD.datos:
                res = nodoBD.datos.agregar(table, [list(range(0, numberColumns+1)), [0], 1])
                return res #0=Operación exitosa, 1=Error en la operación
            else:
                return 3 #Tabla existente
        else:
            return 1 #Error en la operación
    else:
        return 2 #Base de datos inexistente

#Devuelve una lista de los nombres de las tablas de una bases de datos
def showTables(database: str) -> list:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        if nodoBD.datos.tamano == 0:
            return []
        else:
            return list(nodoBD.datos.raiz)
    else:
        return None

#Extrae y devuelve una lista con elementos que corresponden a cada registro de la tabla
def extractTable(database: str, table: str) -> list:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        nodoTBL = nodoBD.datos.obtener(table)
        if nodoTBL:
            if nodoTBL.datos.tamano == 0:
                return [] #No hay registros
            else:
                return list(nodoTBL.datos.raiz) #Lista de registros
        else:
            return None #Tabla inexistente en la Base de Datos
    else:
        return None #Base de Datos inexistente
    

#Extrae y devuelve una lista con los elementos que corresponden a un rango de registros de la tabla
def extractRangeTable(database: str, table: str, lower: any, upper: any) -> list:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        nodoTBL = nodoBD.datos.obtener(table)
        if nodoTBL:
            if nodoTBL.datos.tamano == 0:
                return [] #No hay registros
            else:
                #Filtrar lo datos entre lower y upper
                return list(nodoTBL.datos.raiz) #Lista de registros
        else:
            return None #Tabla inexistente en la Base de Datos
    else:
        return None #Base de Datos inexistente

#Asocia a la tabla una llave primaria simple o compuesta mediante la lista de número de columnas
def alterAddPK(database: str, table: str, columns: list) -> int:
    return -1

#Elimina la llave primaria actual en la información de la tabla,
#manteniendo el índice actual de la estructura del árbol hasta que se invoque de nuevo el alterAddPK(). (UPDATE)
def alterDropPK(database: str, table: str) -> int:
    try:
        nodoBD = mBBDD.obtener(database)
        if nodoBD:
            nodoTBL = nodoBD.datos.obtener(table)
            if nodoTBL:
                if nodoTBL.valor[1][0] > 0:
                    nodoTBL.valor[1][0] *= -1
                    return 0 #Operacion exitosa
                else:
                    return 4 #Llave primaria inexistente
            else:
                return 3 #Tabla inexistente en la Base de Datos
        else:
            return 2 #Base de Datos inexistente
    except:
        return 1 #Error en la operación

#Asocia la integridad referencial entre llaves foráneas y llaves primarias, para efectos de la fase 1 se ignora esta petición
def alterAddFK(database: str, table: str, references: dict) -> int:
    return -1

#Asocia un índice, para efectos de la fase 1 se ignora esta petición
def alterAddIndex(database: str, table: str, references: dict) -> int:
    return -1

#Renombra el nombre de la tabla de una base de datos especificada. (UPDATE)
def alterTable(database: str, tableOld: str, tableNew: str) -> int:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        nodoTBL = nodoBD.datos.obtener(tableOld)
        if nodoTBL:
            if tableNew not in nodoBD.datos:
                v = nodoTBL.valor
                d = nodoTBL.datos 
                res = nodoBD.datos.quitar(tableOld)
                if res == 0:
                    res = nodoBD.datos.agregar(tableNew, v, d)
                    return res #0 si operación es exitosa
                else:
                    return 1 #Error en la operación
            else:
                return 4 #Tabla ya existe en la Base de Datos
        else:
            return 3 #Tabla inexistente en la Base de Datos
    else:
        return 2 #Base de Datos inexistente

#Agrega una columna al final de cada registro de la tabla y base de datos especificada
def alterAddColumn(database: str, table: str, default: any) -> int:
    return -1

#Eliminar una n-ésima columna de cada registro de la tabla excepto si son llaves primarias
def alterDropColumn(database: str, table: str, columnNumber: int) -> int:
    return -1

#Elimina por completo una tabla de una base de datos especificada. (DELETE)
def dropTable(database: str, table: str) -> int:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        res = nodoBD.datos.quitar(table)
        if res == 2: res = 3
        return res #0 operación exitosa, 1 error en la operación, 3 tabla no existe en la BD
    else:
        return 2 # Base de datos inexistente

#Inserta un registro en la estructura de datos asociada a la tabla y la base de datos. (CREATE)
def insert(database: str, table: str, register: list) -> int:
    return -1

#Carga un archivo CSV de una ruta especificada indicando la base de datos y tabla donde será almacenado
def loadCSV(file: str, database: str, table: str) -> list:
    try:
        import csv
        res = []
        with open(file, 'r') as Archivo:
            reader = csv.reader(Archivo, delimiter = ',')
            for row in reader:
                res.append(insert(database,table,row))
        return res
    except:
        return [] #Error en la operación

#Extrae y devuelve un registro especificado por su llave primaria. (READ)
def extractRow(database: str, table: str, columns: list) -> list:
    try:
        nodoBD = mBBDD.obtener(database)
        if nodoBD:
            nodoTBL = nodoBD.datos.obtener(table)
            if nodoTBL:
                if nodoTBL.valor[1] == [-999]:
                    #Tiene llave primaria oculta
                    if len(columns) == 1:
                        nodoRow = nodoTBL.datos.obtener(columns[0])
                        if nodoRow:
                            return nodoRow.valor
                        else:
                            return []
                    else:
                        return [] #Numero de columnas no coincide con columnas de indice
                elif len(nodoTBL.valor[1]) == 1:
                    #Tiene llave primaria simple
                    if len(columns) == 1:
                        nodoRow = nodoTBL.datos.obtener(columns[0])
                        if nodoRow:
                            return nodoRow.valor
                        else:
                            return []
                    else:
                        return [] #Numero de columnas no coincide con columnas de indice
                else:
                    #Tiene llave primaria compuesta
                    if len(columns) == len(nodoTBL.valor[1]):
                        nodoRow = nodoTBL.datos.obtener(columns)
                        if nodoRow:
                            return nodoRow.valor
                        else:
                            return []
                    else:
                        return [] #Numero de columnas no coincide con columnas de indice
            else:
                return [] #Tabla no existe en la base de datos
        else:
            return [] #Base de datos inexistente
    except:
        return [] #Error en la operación

#auxiliar para la función 'update'
def update_aux(nodoTBL, nodoRow, register) -> int:
    valorActual = nodoRow.valor
    claveActual = nodoRow.clave
    valorNuevo = valorActual
    for c, v in register.items():
        print(valorNuevo)
        print(valorNuevo[c], " = ", v)
        valorNuevo[c] = v
    if nodoTBL.valor[1] == [-999]:
        #Tiene llave oculta
        if 0 in register:
            ##nodoRow.valor = valorActual
            return 1 #La llave oculta no puede actualizarse
        else:
            nodoRow.valor = valorNuevo
            return 0 #Operacion exitosa
    elif len(nodoTBL.valor[1]) == 1:
        #Tiene llave primaria sencilla
        idx = nodoTBL.valor[1][0]
        pos = nodoTBL.valor[0].index(idx)
        nuevaClave = valorNuevo[pos]
        if nuevaClave != claveActual:
            #La clave ha cambiado
            nodoBuscar = nodoTBL.datos.obtener(nuevaClave)
            if nodoBuscar:
                return 1 #Hay conflicto porque ya existe una llave primaria con ese valor
            else:
                #ELIMINAR CLAVE ACTUAL
                res = nodoTBL.datos.quitar(claveActual)
                if res == 0:
                    #AGREGAR CLAVE NUEVAS
                    res = nodoTBL.datos.agregar(nuevaClave, valorNuevo)
                    return res #0 operación exitosa, 1 error en la operación
                else:
                    return 1 #Error en la operación
        else:
            #Clave primaria no ha cambiado
            nodoRow.valor = valorNuevo
            return 0 #Operación exitosa
    else:
        #Tiene llave primaria compuesta
        nuevaClave = []
        for i in nodoTBL.valor[1]:
            pos = nodoTBL.valor[0].index(i)
            nuevaClave.append(valorNuevo[pos])
        if nuevaClave != claveActual:
            #La clave ha cambiado
            nodoBuscar = nodoTBL.datos.obtener(nuevaClave)
            if nodoBuscar:
                return 1 #Hay conflicto porque ya existe una llave primaria con ese valor
            else:
                #ELIMINAR CLAVE ACTUAL
                res = nodoTBL.datos.quitar(claveActual)
                if res == 0:
                    #AGREGAR CLAVE NUEVAS
                    res = nodoTBL.datos.agregar(nuevaClave, valorNuevo)
                    return res #0 operación exitosa, 1 error en la operación
                else:
                    return 1 #Error en la operación
        else:
            #Clave primaria no ha cambiado
            nodoRow.valor = valorNuevo
            return 0 #Operación exitosa
        
#Inserta un registro     en la estructura de datos asociada a la tabla y la base de datos. (UPDATE)
def update(database: str, table: str, register: dict, columns: list) -> int:
    try:
        nodoBD = mBBDD.obtener(database)
        if nodoBD:
            nodoTBL = nodoBD.datos.obtener(table)
            if nodoTBL:
                if nodoTBL.valor[1] == [-999]:
                    #Tiene llave primaria oculta
                    if len(columns) == 1:
                        nodoRow = nodoTBL.datos.obtener(columns[0])
                        if nodoRow:
                            return update_aux(nodoTBL, nodoRow, register)
                        else:
                            return 1
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
                elif len(nodoTBL.valor[1]) == 1:
                    #Tiene llave primaria simple
                    if len(columns) == 1:
                        nodoRow = nodoTBL.datos.obtener(columns[0])
                        if nodoRow:
                            return update_aux(nodoTBL, nodoRow, register)
                        else:
                            return 1
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
                else:
                    #Tiene llave primaria compuesta
                    if len(columns) == len(nodoTBL.valor[1]):
                        nodoRow = nodoTBL.datos.obtener(columns)
                        if nodoRow:
                            return update_aux(nodoTBL, nodoRow, register)
                        else:
                            return 1
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
            else:
                return 3 #Tabla no existe en la base de datos
        else:
            return 2 #Base de datos inexistente
    except:
        return 1 #Error en la operación
    
#Elimina un registro de una tabla y base de datos especificados por la llave primaria. (DELETE)
def delete(database: str, table: str, columns: list) -> int:
    try:
        nodoBD = mBBDD.obtener(database)
        if nodoBD:
            nodoTBL = nodoBD.datos.obtener(table)
            if nodoTBL:
                if nodoTBL.valor[1] == [-999]:
                    #Tiene llave primaria oculta
                    if len(columns) == 1:
                        res = nodoTBL.datos.quitar(columns[0])
                        if res == 2: res = 4
                        return res #0 operación exitosa, 1 error en la operación, 4 llave primaria no existe
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
                elif len(nodoTBL.valor[1]) == 1:
                    #Tiene llave primaria simple
                    if len(columns) == 1:
                        res = nodoTBL.datos.quitar(columns[0])
                        if res == 2: res = 4
                        return res #0 operación exitosa, 1 error en la operación, 4 llave primaria no existe
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
                else:
                    #Tiene llave primaria compuesta
                    if len(columns) == len(nodoTBL.valor[1]):
                        res = nodoTBL.datos.quitar(columns)
                        if res == 2: res = 4
                        return res #0 operación exitosa, 1 error en la operación, 4 llave primaria no existe
                    else:
                        return 1 #Numero de columnas no coincide con columnas de indice
            else:
                return 3 #Tabla no existe en la base de datos
        else:
            return 2 #Base de datos inexistente
    except:
        return 1 #Error en la operación

#Elimina todos los registros de una tabla y base de datos. (DELETE)
def truncate(database: str, table: str) -> int:
    nodoBD = mBBDD.obtener(database)
    if nodoBD:
        nodoTBL = nodoBD.datos.obtener(table)
        if nodoTBL:
            nodoTBL.datos.raiz = None
            nodoTBL.datos.tamano = 0
            return 0 #Operacion exitosa
        else:
            return 3 #Tabla no existe en la base de datos
    else:
        return 2 #Base de datos inexistente

#Graba las Bases de Datos y sus resectivas Tablas a Disco
def grabaBD():
    serializar("BBDD.pickle", "wb", "")
    colaBD = []
    if mBBDD.raiz: colaBD.append(mBBDD.raiz)
    while len(colaBD) > 0:
        data = []
        nodoBD = colaBD.pop(0)
        data.append(nodoBD.clave)
        colaTBL = []
        if nodoBD.datos.raiz: colaTBL.append(nodoBD.datos.raiz)
        while len(colaTBL) > 0:
            nodoTBL = colaTBL.pop(0)
            data.append([nodoTBL.clave, nodoTBL.valor])
            if nodoTBL.Izq: colaTBL.append(nodoTBL.Izq)
            if nodoTBL.Der: colaTBL.append(nodoTBL.Der)
        serializar("BBDD.pickle", "ab", data)
        print(data)
        if nodoBD.Izq: colaBD.append(nodoBD.Izq)
        if nodoBD.Der: colaBD.append(nodoBD.Der)

#Graba los Registros de las Tablas de las Bases de Datos a Disco
def grabaREG():
    serializar("REGS.pickle", "wb", "")
    colaBD = []
    data = []
    if mBBDD.raiz: colaBD.append(mBBDD.raiz)
    while len(colaBD) > 0:
        nodoBD = colaBD.pop(0)
        colaTBL = []
        data = []
        if nodoBD.datos.raiz: colaTBL.append(nodoBD.datos.raiz)
        while len(colaTBL) > 0:
            nodoTBL = colaTBL.pop(0)
            data = []
            data.append(nodoBD.clave)
            data.append(nodoTBL.clave)
            colaREG = []
            if nodoTBL.datos.raiz: colaREG.append(nodoTBL.datos.raiz)
            while len(colaREG) > 0:
                nodoREG = colaREG.pop(0)
                data.append([nodoREG.clave, nodoREG.valor])
                if nodoREG.Izq: colaREG.append(nodoREG.Izq)
                if nodoREG.Der: colaREG.append(nodoREG.Der)
            if nodoTBL.Izq: colaTBL.append(nodoTBL.Izq)
            if nodoTBL.Der: colaTBL.append(nodoTBL.Der)
        if data != []:
            serializar("REGS.pickle", "ab", data)
            print(data)
        if nodoBD.Izq: colaBD.append(nodoBD.Izq)
        if nodoBD.Der: colaBD.append(nodoBD.Der)

#Lee las Bases de Datos y sus respectivas Tablas desde Disco
def leerBD():
    try:
        dataBD = deserializar("BBDD.pickle")
        dataBD.pop(0)
        bd = ""
        for item in dataBD:
            if item != None:
                #print(item[0], len(item), item[1:])
                bd = item[0]
                createDatabase(bd)
                nodoBD = mBBDD.obtener(bd)
                for i in range(1, len(item)):
                    nodoBD.datos.agregar(item[i][0], [item[i][1][0], item[i][1][1], item[i][1][2]])
    except:
        return

#Lee los Registros de las Tablas de las Bases de Datos desde disco
def leerREG():
    try:
        dataREG = deserializar("REGS.pickle")
        dataREG.pop(0)
        for item in dataREG:
            if item != None:
                bd = item[0]
                tbl = item[1]
                nodoBD = mBBDD.obtener(bd)
                nodoTBL = nodoBD.datos.obtener(tbl)
                for i in range(2, len(item)):
                    print(item[i])
                    print(item[i][0])
                    print(item[i][1])
                    insert(bd, tbl, item[i][1])
    except:
        return

#Guarda pickles a disco
def serializar(archivo, modo, data):
    with open(archivo, modo) as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

#Lee pickles desde disco
def deserializar(archivo) -> list:
    data = []
    with open(archivo, 'rb') as f:
        try:
            while True:
                data.append(pickle.load(f))
        except EOFError:
           pass
        return data
