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
import bcrypt
import pandas as pd
from conexion import ejecutar_consulta

def hashear_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def registrar_log(id_tecnico: int, accion: str, detalles: str):
    sql = "INSERT INTO logs_sistema (id_tecnico, accion, detalles) VALUES (%s, %s, %s);"
    ejecutar_consulta(sql, (id_tecnico, accion, detalles))

def render():
    st.header("⚙️ Gestión de Usuarios y Perfiles")

    es_admin = st.session_state.get("usuario_rol") == "admin"

    tab_perfil, tab_admin = st.tabs(["👤 Mi Perfil", "👑 Administración de Usuarios y Claves (Solo Admin)"])

    # -------------------------------------------------------------
    # TAB 1: MI PERFIL (LECTURA)
    # -------------------------------------------------------------
    with tab_perfil:
        st.subheader("Datos de la Sesión Actual")
        st.info(
            f"**Nombre:** {st.session_state['usuario_nombre']}\n\n"
            f"**ID de Técnico:** {st.session_state['usuario_id']}\n\n"
            f"**Rol Asignado:** `{st.session_state['usuario_rol'].upper()}`"
        )
        if not es_admin:
            st.caption("ℹ️ *Nota: Por políticas de seguridad, la gestión y cambio de contraseñas es realizada únicamente por el usuario Administrador.*")

    # -------------------------------------------------------------
    # TAB 2: PANEL EXCLUSIVO ADMINISTRADOR
    # -------------------------------------------------------------
    with tab_admin:
        if not es_admin:
            st.error("🔒 Acceso Restringido. Esta pestaña está reservada exclusivamente para el Administrador del Sistema.")
        else:
            st.subheader("➕ Crear Nuevo Técnico / Usuario")
            with st.form("form_nuevo_usuario", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    nombre = st.text_input("Nombre Completo *")
                    usuario = st.text_input("Nombre de Usuario (Login) *").strip().lower()
                    telefono = st.text_input("Teléfono de Contacto")
                with col2:
                    rol = st.selectbox("Rol de Acceso", ["tecnico", "admin"])
                    clave_inicial = st.text_input("Contraseña Inicial *", type="password")
                
                btn_crear = st.form_submit_button("Crear Usuario")
                
                if btn_crear:
                    if not nombre or not usuario or not clave_inicial:
                        st.error("⚠️ Los campos Nombre, Usuario y Contraseña son obligatorios.")
                    else:
                        try:
                            hash_c = hashear_password(clave_inicial)
                            sql = """
                                INSERT INTO tecnicos (nombre_tecnico, usuario, password_hash, rol, activo)
                                VALUES (%s, %s, %s, %s, %s, TRUE);
                            """
                            ejecutar_consulta(sql, (nombre, usuario, hash_c, rol, telefono))
                            registrar_log(
                                st.session_state['usuario_id'], 
                                "CREAR_USUARIO", 
                                f"El administrador creó el usuario '{usuario}' con rol '{rol}'."
                            )
                            st.success(f"¡Usuario '{usuario}' registrado correctamente con su contraseña inicial!")
                        except Exception as e:
                            st.error(f"❌ Error al crear usuario (es posible que el usuario ya exista): {e}")

            st.divider()
            st.subheader("📋 Usuarios Registrados")
            
            tecnicos_db = ejecutar_consulta("SELECT id_tecnico, nombre_tecnico, usuario, rol, activo FROM tecnicos ORDER BY id_tecnico ASC;")
            if tecnicos_db:
                df_tec = pd.DataFrame([dict(r) for r in tecnicos_db])
                st.dataframe(df_tec, use_container_width=True)

                st.divider()
                st.subheader("🔑 Gestión de Claves y Estado de Accesos")
                
                dict_tecnicos = {f"{r['nombre_tecnico']} (@{r['usuario']})": r for r in tecnicos_db}
                user_sel_key = st.selectbox("Seleccione un usuario para administrar:", list(dict_tecnicos.keys()))
                u_data = dict_tecnicos[user_sel_key]

                col_act1, col_act2 = st.columns(2)
                
                # Modificar Estado de Acceso
                with col_act1:
                    st.markdown("#### Estado de Cuenta")
                    nuevo_estado = st.checkbox("Usuario Activo (Permitir Acceso)", value=u_data['activo'])
                    if st.button("Actualizar Estado de Acceso"):
                        ejecutar_consulta("UPDATE tecnicos SET activo = %s WHERE id_tecnico = %s;", (nuevo_estado, u_data['id_tecnico']))
                        registrar_log(st.session_state['usuario_id'], "MODIFICAR_ESTADO", f"Cambió estado de {u_data['usuario']} a activo={nuevo_estado}")
                        st.success("Estado actualizado con éxito.")
                        st.rerun()

                # Asignar / Resetear Contraseña
                with col_act2:
                    st.markdown("#### Cambiar / Resetear Contraseña")
                    nueva_clave_res = st.text_input("Nueva Contraseña", type="password", key="res_p")
                    if st.button("Establecer Nueva Contraseña"):
                        if nueva_clave_res:
                            h_res = hashear_password(nueva_clave_res)
                            ejecutar_consulta("UPDATE tecnicos SET password_hash = %s WHERE id_tecnico = %s;", (h_res, u_data['id_tecnico']))
                            registrar_log(st.session_state['usuario_id'], "RESETEAR_CLAVE", f"Administrador cambió la clave del usuario {u_data['usuario']}")
                            st.success(f"¡Contraseña de {u_data['usuario']} actualizada exitosamente!")
                        else:
                            st.error("Ingrese una nueva contraseña válida.")
