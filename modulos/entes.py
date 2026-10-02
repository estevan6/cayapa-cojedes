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
import re
import pandas as pd
from conexion import ejecutar_consulta

# --- FUNCIÓN CONVERSORA DE COORDENADAS (DMS -> DECIMAL) ---
def convertir_a_decimal(coordenada_str) -> float:
    if not coordenada_str:
        return 0.0

    texto = str(coordenada_str).strip().upper()

    # 1. Si ya viene en formato decimal
    try:
        return float(texto.replace(',', '.'))
    except ValueError:
        pass

    # 2. Si viene en formato Grados, Minutos, Segundos (DMS)
    patron = r"(\d+)[\°\s]+(\d+)[\'\s]+(\d+(?:\.\d+)?)[\"\s]*([NSEWO]?)"
    match = re.search(patron, texto)

    if match:
        grados = float(match.group(1))
        minutos = float(match.group(2))
        segundos = float(match.group(3))
        orientacion = match.group(4)

        decimal = grados + (minutos / 60.0) + (segundos / 3600.0)

        if orientacion in ['S', 'W', 'O']:
            decimal = -decimal
        elif not orientacion and grados > 50:  # Asumir Oeste para Venezuela
            decimal = -decimal

        return round(decimal, 6)

    return 0.0


def render():
    st.markdown("<h2 style='text-align: center;'>🏫 Gestión de Entes e Historiales</h2>", unsafe_allow_html=True)
    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "➕ Registrar Ente", 
        "🏛️ Historial Autoridades", 
        "📞 Historial Contactos"
    ])

    # =========================================================================
    # TAB 1: REGISTRO DE ENTE
    # =========================================================================
    with tab1:
        with st.form("form_ente", clear_on_submit=True):
            st.subheader("Ubicación e Identificación de la Institución")
            
            nombre_ente = st.text_input("Nombre de la Institución / Ente *")
            direccion = st.text_area("Dirección Completa")
            comuna = st.text_input("Comuna / Circuito Comunal")

            col_lat, col_lon = st.columns(2)
            with col_lat:
                lat_txt = st.text_input("Latitud *", placeholder="Ej: 9.6200 o 9°37'12.0\"N")
            with col_lon:
                lon_txt = st.text_input("Longitud *", placeholder="Ej: -68.5800 o 68°34'48.0\"W")

            btn_guardar = st.form_submit_button("Guardar Ente", use_container_width=True)

            if btn_guardar:
                if not nombre_ente:
                    st.warning("⚠️ Debe ingresar el nombre de la institución.")
                elif not lat_txt or not lon_txt:
                    st.warning("⚠️ Ingrese ambas coordenadas.")
                else:
                    try:
                        lat_decimal = convertir_a_decimal(lat_txt)
                        lon_decimal = convertir_a_decimal(lon_txt)

                        if lat_decimal == 0.0 or lon_decimal == 0.0:
                            st.error("❌ El formato de las coordenadas no fue reconocido.")
                        else:
                            sql = """
                                INSERT INTO entes (nombre_ente, direccion, comuna, latitud, longitud)
                                VALUES (%s, %s, %s, %s, %s) RETURNING id_ente;
                            """
                            res = ejecutar_consulta(sql, (nombre_ente, direccion, comuna, lat_decimal, lon_decimal))

                            if res and st.session_state.get('usuario_id'):
                                sql_log = "INSERT INTO logs_sistema (id_tecnico, accion, detalles) VALUES (%s, %s, %s);"
                                ejecutar_consulta(
                                    sql_log, 
                                    (st.session_state['usuario_id'], "CREAR_ENTE", f"Registró el ente '{nombre_ente}'")
                                )

                            st.success(f"¡Ente '{nombre_ente}' registrado con éxito!")
                            st.info(f"📍 **Coordenadas guardadas:** Latitud: `{lat_decimal}` | Longitud: `{lon_decimal}`")
                    except Exception as e:
                        st.error(f"❌ Error al registrar en la base de datos: {e}")

    # Cargar entes registrados para las pestañas de historial
    entes_db = ejecutar_consulta("SELECT id_ente, nombre_ente FROM entes ORDER BY nombre_ente;")
    dict_entes = {e['nombre_ente']: e['id_ente'] for e in entes_db} if entes_db else {}

    # =========================================================================
    # TAB 2: HISTORIAL DE AUTORIDADES (historial_autoridades)
    # =========================================================================
    with tab2:
        st.subheader("Gestión de Autoridades del Ente")
        if not dict_entes:
            st.info("Debe registrar al menos un Ente para gestionar sus autoridades.")
        else:
            ente_sel_auto = st.selectbox("Seleccione el Ente:", list(dict_entes.keys()), key="sb_auto")
            id_ente_auto = dict_entes[ente_sel_auto]

            with st.form("form_autoridad", clear_on_submit=True):
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    nombre_auto = st.text_input("Nombre de la Autoridad *")
                    cargo_auto = st.text_input("Cargo de la Autoridad")
                    celular_auto = st.text_input("Celular")
                with col_a2:
                    telef_auto = st.text_input("Teléfono de Oficina")
                    email_auto = st.text_input("Correo Electrónico")

                btn_add_auto = st.form_submit_button("Registrar / Actualizar Autoridad")

                if btn_add_auto:
                    if not nombre_auto:
                        st.warning("⚠️ El nombre de la autoridad es obligatorio.")
                    else:
                        try:
                            # 1. Marcar autoridades anteriores del ente como inactivas (opcional)
                            ejecutar_consulta(
                                "UPDATE historial_autoridades SET activo_auto = FALSE WHERE id_ente = %s;", 
                                (id_ente_auto,)
                            )

                            # 2. Insertar nueva autoridad activa
                            sql_ins = """
                                INSERT INTO historial_autoridades 
                                (id_ente, nombre_auto, cargo_auto, celular_auto, telef_auto, email_auto, activo_auto)
                                VALUES (%s, %s, %s, %s, %s, %s, TRUE);
                            """
                            ejecutar_consulta(
                                sql_ins, 
                                (id_ente_auto, nombre_auto, cargo_auto, celular_auto, telef_auto, email_auto)
                            )

                            if st.session_state.get('usuario_id'):
                                ejecutar_consulta(
                                    "INSERT INTO logs_sistema (id_tecnico, accion, detalles) VALUES (%s, %s, %s);",
                                    (st.session_state['usuario_id'], "REGISTRAR_AUTORIDAD", f"Registró a '{nombre_auto}' en '{ente_sel_auto}'")
                                )

                            st.success(f"¡Autoridad '{nombre_auto}' asignada a {ente_sel_auto}!")
                        except Exception as e:
                            st.error(f"Error al registrar autoridad: {e}")

            st.divider()
            st.markdown(f"#### 📜 Historial de Autoridades: *{ente_sel_auto}*")
            autos = ejecutar_consulta("""
                SELECT 
                    nombre_auto AS "Nombre", 
                    cargo_auto AS "Cargo", 
                    celular_auto AS "Celular", 
                    telef_auto AS "Teléfono", 
                    email_auto AS "Correo", 
                    CASE WHEN activo_auto THEN 'Vigente' ELSE 'Histórico' END AS "Estatus"
                FROM historial_autoridades 
                WHERE id_ente = %s 
                ORDER BY id_auto DESC;
            """, (id_ente_auto,))

            if autos:
                st.dataframe(pd.DataFrame([dict(r) for r in autos]), use_container_width=True)
            else:
                st.caption("No hay registro de autoridades para este ente.")

    # =========================================================================
    # TAB 3: HISTORIAL DE CONTACTOS (historial_contactos)
    # =========================================================================
    with tab3:
        st.subheader("Gestión de Personas de Contacto")
        if not dict_entes:
            st.info("Debe registrar al menos un Ente para gestionar sus contactos.")
        else:
            ente_sel_cont = st.selectbox("Seleccione el Ente:", list(dict_entes.keys()), key="sb_cont")
            id_ente_cont = dict_entes[ente_sel_cont]

            with st.form("form_contacto", clear_on_submit=True):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    nombre_cont = st.text_input("Nombre del Contacto *")
                    cargo_cont = st.text_input("Cargo / Función")
                    celular_cont = st.text_input("Celular")
                with col_c2:
                    telef_cont = st.text_input("Teléfono Secundario")
                    email_cont = st.text_input("Correo Electrónico")

                btn_add_cont = st.form_submit_button("Registrar / Actualizar Contacto")

                if btn_add_cont:
                    if not nombre_cont:
                        st.warning("⚠️ El nombre del contacto es obligatorio.")
                    else:
                        try:
                            # 1. Marcar contactos anteriores como históricos
                            ejecutar_consulta(
                                "UPDATE historial_contactos SET activo_cont = FALSE WHERE id_ente = %s;", 
                                (id_ente_cont,)
                            )

                            # 2. Insertar nuevo contacto activo
                            sql_ins_c = """
                                INSERT INTO historial_contactos 
                                (id_ente, nombre_cont, cargo_cont, celular_cont, telef_cont, email_cont, activo_cont)
                                VALUES (%s, %s, %s, %s, %s, %s, TRUE);
                            """
                            ejecutar_consulta(
                                sql_ins_c, 
                                (id_ente_cont, nombre_cont, cargo_cont, celular_cont, telef_cont, email_cont)
                            )

                            if st.session_state.get('usuario_id'):
                                ejecutar_consulta(
                                    "INSERT INTO logs_sistema (id_tecnico, accion, detalles) VALUES (%s, %s, %s);",
                                    (st.session_state['usuario_id'], "REGISTRAR_CONTACTO", f"Registró contacto '{nombre_cont}' en '{ente_sel_cont}'")
                                )

                            st.success(f"¡Contacto '{nombre_cont}' asignado a {ente_sel_cont}!")
                        except Exception as e:
                            st.error(f"Error al registrar contacto: {e}")

            st.divider()
            st.markdown(f"#### 📜 Historial de Contactos: *{ente_sel_cont}*")
            conts = ejecutar_consulta("""
                SELECT 
                    nombre_cont AS "Nombre", 
                    cargo_cont AS "Cargo", 
                    celular_cont AS "Celular", 
                    telef_cont AS "Teléfono", 
                    email_cont AS "Correo", 
                    CASE WHEN activo_cont THEN 'Vigente' ELSE 'Histórico' END AS "Estatus"
                FROM historial_contactos 
                WHERE id_ente = %s 
                ORDER BY id_cont DESC;
            """, (id_ente_cont,))

            if conts:
                st.dataframe(pd.DataFrame([dict(r) for r in conts]), use_container_width=True)
            else:
                st.caption("No hay registro de contactos para este ente.")
