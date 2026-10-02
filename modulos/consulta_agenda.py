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
import pandas as pd
from conexion import ejecutar_consulta

def render():
    st.header("📅 Consulta de Agenda Semanal")
    st.caption("Visualiza la planificación de actividades programadas para la semana de interés.")

    fecha_ref = st.date_input("Selecciona un día de la semana de interés", datetime.date.today())
    
    inicio_semana = fecha_ref - datetime.timedelta(days=fecha_ref.weekday())
    fin_semana = inicio_semana + datetime.timedelta(days=6)

    st.info(f"Mostrando actividades del **{inicio_semana.strftime('%d/%m/%Y')}** al **{fin_semana.strftime('%d/%m/%Y')}**")

    sql_agenda = """
        SELECT 
            a.fecha_programada AS "Fecha",
            e.nombre_ente AS "Institución",
            a.actividad AS "Actividad",
            a.objetivo AS "Objetivo",
            a.descripcion AS "Descripción"
        FROM agenda a
        JOIN entes e ON a.id_ente = e.id_ente
        WHERE a.fecha_programada BETWEEN %s AND %s
        ORDER BY a.fecha_programada ASC;
    """
    datos_agenda = ejecutar_consulta(sql_agenda, (inicio_semana, fin_semana))
    
    if datos_agenda:
        df_agenda = pd.DataFrame([dict(row) for row in datos_agenda])
        st.dataframe(df_agenda, use_container_width=True)
    else:
        st.warning("No hay actividades programadas para esta semana.")
