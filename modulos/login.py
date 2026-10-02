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

import streamlit as st
from PIL import Image
import bcrypt
from conexion import ejecutar_consulta

# Ruta exacta del archivo del logo
LOGO_PATH = "logo.jpg"
try:
    logo_img = Image.open(LOGO_PATH)
except Exception:
    logo_img = None


def verificar_password(password_plana: str, password_hash: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return bcrypt.checkpw(password_plana.encode('utf-8'), password_hash.encode('utf-8'))


def login_form():
    # 1. CENTRAR Y MOSTRAR EL LOGO ARRIBA
    if logo_img:
        # Usamos 3 columnas para centrar el logo proporcionalmente
        col_img1, col_img2, col_img3 = st.columns([1.5, 1, 1.5])
        with col_img2:
            st.image(logo_img, use_container_width=True)

    # 2. TEXTO DE BIENVENIDA (Debajo del logo)
    st.markdown("<h2 style='text-align: center;'>Sistema CAYAPA COJEDES</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Unidad de Gestión Técnica - Inicio de Sesión</h4>", unsafe_allow_html=True)
    st.write("")

    # 3. FORMULARIO DE INICIO DE SESIÓN
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("form_login"):
            usuario = st.text_input("Usuario", placeholder="Ej: rtorrealba").strip()
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar al Sistema", use_container_width=True)

            if submitted:
                if not usuario or not password:
                    st.error("⚠️ Ingrese su usuario y contraseña.")
                else:
                    # Buscar el usuario en la tabla tecnicos
                    sql = """
                        SELECT id_tecnico, nombre_tecnico, usuario, password_hash, rol, activo 
                        FROM tecnicos 
                        WHERE usuario = %s AND activo = TRUE;
                    """
                    res = ejecutar_consulta(sql, (usuario,))

                    if res:
                        user_data = res[0]
                        hash_guardado = user_data['password_hash']

                        if hash_guardado and verificar_password(password, hash_guardado):
                            # Guardar estado de la sesión
                            st.session_state["autenticado"] = True
                            st.session_state["usuario_id"] = user_data['id_tecnico']
                            st.session_state["usuario_nombre"] = user_data['nombre_tecnico']
                            st.session_state["usuario_rol"] = user_data['rol']
                            st.success(f"¡Bienvenido(a), {user_data['nombre_tecnico']}!")
                            st.rerun()
                        else:
                            st.error("❌ Contraseña incorrecta.")
                    else:
                        st.error("❌ Usuario no encontrado o inactivo.")
