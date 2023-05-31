from fastapi import FastAPI
from typing import Dict
import sqlite3
 
app = FastAPI()
conn = sqlite3.connect('inventario.sqlite', check_same_thread=False)
cur = conn.cursor()

my_inventary = '''
    CREATE TABLE IF NOT EXISTS inventary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        cantidad INTEGER,
        valor INTEGER
    );
'''
cur.execute(my_inventary)
conn.commit()

@app.post("/api/invent")
def guardar_inventario(dic: Dict):
    Insert = f"""INSERT INTO inventary 
    (id,nombre,cantidad,valor) VALUES (
        '{dic['id']}',
        '{dic['nombre']}',
        '{dic['cantidad']}',
        '{dic['valor']}'
    )"""
    try:
        cur.execute(Insert)
        conn.commit()
        return {"status":True}
    except Exception as error:
        return {"status":False, "msg":str(error)}
    
@app.get("/api/invent/all")
def todo_el_inventario():
    lista_inventario=[]
    selects = """
    SELECT id,nombre,cantidad,valor  FROM inventary
    """
    cur.execute(selects)
    all = cur.fetchall()

    for inventarys in all:
        lista_inventario.append({
            "id": inventarys[0],
            "nombre": inventarys[1],
            "cantidad": inventarys[2],
            "valor": inventarys[3],
           
        })
 
    return {"status":True, "data":lista_inventario}

@app.get("/api/invent/{id}")
def oneinventary(id:int):
    
    queryGetinventary = f"""
    SELECT id,nombre,cantidad,valor FROM inventary
    WHERE id = {id}
    """
    cur.execute(queryGetinventary)
    ones = cur.fetchone()

    return {
            "id": ones[0],
            "nombre": ones[1],
            "cantidad": ones[2],
            "valor": ones[3],
           
        }
@app.delete("/api/invent/{id}")
def eliminar_registro(id:int):
    queryDelete = f"""
    DELETE FROM inventary WHERE id= {id}
    """
 
    try:
        cur.execute(queryDelete)
        conn.commit()
        return {"status":True}
    except Exception as error:
        return {"status":False, "msg":str(error)}
    


@app.put("/api/invent/{id}")
def updateinvent(id:int, dic: Dict):
 
    queryUpdate = f"""
    UPDATE inventary SET nombre='{dic["nombre"]}',
    cantidad='{dic["cantidad"]}',
    valor='{dic["valor"]}' WHERE id = {id}
    """
 
    try:
        cur.execute(queryUpdate)
        conn.commit()
        return {"status":True}
    except Exception as error:
        return {"status":False, "msg":str(error)}