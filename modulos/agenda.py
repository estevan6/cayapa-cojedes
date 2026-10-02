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
import datetime
from conexion import ejecutar_consulta

def render():
    # --- ENCABEZADO COSMÉTICO CENTRADO ---
    st.markdown("<h2 style='text-align: center;'>📅 Carga de Agenda de Actividades</h2>", unsafe_allow_html=True)
    
    # Obtener y formatear la fecha del día en dd/mm/aaaa
    fecha_hoy = datetime.date.today().strftime('%d/%m/%Y')
    st.markdown(f"<h4 style='text-align: center; color: #6c757d;'>Fecha de hoy: {fecha_hoy}</h4>", unsafe_allow_html=True)
    
    st.divider()

    # Cargar entes desde la base de datos
    entes = ejecutar_consulta("SELECT id_ente, nombre_ente FROM entes ORDER BY nombre_ente;")
    dict_entes = {e['nombre_ente']: e['id_ente'] for e in entes} if entes else {}

    # --- FORMULARIO DE CARGA ---
    with st.form("form_agenda", clear_on_submit=True):
        fecha = st.date_input("Fecha Programada para la Actividad", datetime.date.today())
        ente_sel = st.selectbox("Institución / Ente", list(dict_entes.keys()) if dict_entes else ["No hay entes registrados"])
        actividad = st.text_area("Actividad a realizar")
        objetivo = st.text_area("Objetivo de la actividad")

        enviar = st.form_submit_button("Guardar en Agenda")

        if enviar:
            if not actividad:
                st.warning("Por favor describe la actividad.")
            elif not dict_entes:
                st.error("No se puede guardar sin un Ente válido.")
            else:
                try:
                    # 1. Obtener ID del técnico autenticado en la sesión
                    usuario_id = st.session_state.get('usuario_id')

                    # 2. SQL actualizado para incluir creado_por_id
                    sql = """
                        INSERT INTO agenda (fecha_programada, id_ente, actividad, objetivo, creado_por_id)
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    ejecutar_consulta(sql, (fecha, dict_entes[ente_sel], actividad, objetivo, usuario_id))

                    # 3. Registrar el evento en la bitácora de auditoría (logs_sistema)
                    sql_log = """
                        INSERT INTO logs_sistema (id_tecnico, accion, detalles)
                        VALUES (%s, %s, %s);
                    """
                    detalles_log = f"Agendó actividad para '{ente_sel}' programada el {fecha.strftime('%d/%m/%Y')}."
                    ejecutar_consulta(sql_log, (usuario_id, "CREAR_AGENDA", detalles_log))

                    st.success("¡Actividad agendada con éxito!")
                except Exception as e:
                    st.error(f"Error al agendar: {e}")
