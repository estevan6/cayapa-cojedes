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

import bcrypt
from conexion import ejecutar_consulta

def hashear_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Definir credenciales iniciales (¡Cambia estas claves por unas de tu preferencia!)
clave_admin = "AdminCayapa2026*"
clave_tecnico = "TecnicoCayapa2026*"

hash_admin = hashear_password(clave_admin)
hash_tecnico = hashear_password(clave_tecnico)

# 1. Asignar clave al administrador Richard Torrealba
ejecutar_consulta(
    "UPDATE tecnicos SET password_hash = %s WHERE rol = 'admin';", 
    (hash_admin,)
)

# 2. Asignar clave general al resto de los técnicos
ejecutar_consulta(
    "UPDATE tecnicos SET password_hash = %s WHERE rol = 'tecnico' OR rol IS NULL;", 
    (hash_tecnico,)
)

print("✅ Contraseñas encriptadas correctamente en la base de datos.")
print(f"🔑 Admin (rtorrealba) -> Contraseña: {clave_admin}")
print(f"🔑 Técnicos generales -> Contraseña: {clave_tecnico}")
