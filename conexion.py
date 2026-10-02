#  Sistema CAYAPA COJEDES - Unidad de Gestión Técnica
#  Copyright (C) 2026 Víctor Meléndez
#
#  Este programa es software libre; puedes redistribuirlo y/o modificarlo
#  bajo los términos de la Licencia Pública General GNU tal como fue publicada
#  por la Free Software Foundation, ya sea la versión 3 de la Licencia, o
#  (a tu elección) cualquier versión posterior.
#
#  Este programa se distribuye con la esperanza de que sea útil, pero
#  SIN NINGUNA GARANTÍA. Vea la Licencia Pública General GNU para más detalles.

import psycopg2
from psycopg2.extras import DictCursor

def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="cayapa",
        user="usuario",
        password="C44rd3n1d4r"
    )

def ejecutar_consulta(query, params=None):
    with obtener_conexion() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params or ())
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return None
