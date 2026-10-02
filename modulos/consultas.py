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
    st.header("📊 Módulo de Consultas y Exportación")
    
    tab1, tab2 = st.tabs(["📅 Agenda Semanal", "📋 Reporte por Intervalo de Tiempo"])

    # --- PESTAÑA 1: AGENDA SEMANAL ---
    with tab1:
        st.subheader("Generar Agenda Semanal")
        fecha_ref = st.date_input("Selecciona un día de la semana de interés", datetime.date.today())
        
        inicio_semana = fecha_ref - datetime.timedelta(days=fecha_ref.weekday())
        fin_semana = inicio_semana + datetime.timedelta(days=6)

        st.info(f"Mostrando agenda desde el **{inicio_semana.strftime('%d/%m/%Y')}** hasta el **{fin_semana.strftime('%d/%m/%Y')}**")

        sql_agenda = """
            SELECT a.fecha_programada, e.nombre_ente, a.actividad, a.objetivo
            FROM agenda a
            JOIN entes e ON a.id_ente = e.id_ente
            WHERE a.fecha_programada BETWEEN %s AND %s
            ORDER BY a.fecha_programada ASC;
        """
        datos_agenda = ejecutar_consulta(sql_agenda, (inicio_semana, fin_semana))
        if datos_agenda:
            filas_agenda = [dict(row) for row in datos_agenda]
            df_agenda = pd.DataFrame(filas_agenda)
            st.dataframe(df_agenda, use_container_width=True)
        else:
            st.warning("No hay actividades agendadas para esta semana.")

    # --- PESTAÑA 2: REPORTE POR INTERVALO ---
    with tab2:
        st.subheader("Filtrar Reportes por Rango de Fechas")
        c1, c2 = st.columns(2)
        with c1:
            f_inicio = st.date_input("Fecha Inicial", datetime.date(2026, 1, 1))
        with c2:
            f_fin = st.date_input("Fecha Final", datetime.date.today())

        if f_inicio > f_fin:
            st.error("La fecha inicial no puede ser mayor a la fecha final.")
        else:
            sql_reportes = """
                SELECT 
                    r.codigo_equipo AS "Código Equipo",
                    r.fecha_servicio AS "Fecha",
                    t.nombre_tecnico AS "Técnico",
                    e.nombre_ente AS "Institución",
                    r.departamento AS "Departamento/Unidad",
                    r.piso AS "Piso",
                    cat.nombre_categoria AS "Área",
                    teq.nombre_tipo AS "Equipo",
                    r.marca AS "Marca",
                    r.modelo AS "Modelo",
                    r.nro_bien_nacional AS "Bien Nac.",
                    r.estatus_inicial AS antes,
                    r.estatus_final AS despues,
                    r.tipo_mantenimiento AS "Mantenimiento"
                FROM reporte r
                JOIN tecnicos t ON r.id_tecnico = t.id_tecnico
                JOIN entes e ON r.id_ente = e.id_ente
                JOIN tipos_equipo teq ON r.id_tipo = teq.id_tipo
                JOIN categorias cat ON teq.id_categoria = cat.id_categoria
                WHERE r.fecha_servicio BETWEEN %s AND %s
                ORDER BY r.fecha_servicio DESC;
            """
            datos_rep = ejecutar_consulta(sql_reportes, (f_inicio, f_fin))
            
            if datos_rep:
                filas = [dict(row) for row in datos_rep]
                df_rep = pd.DataFrame(filas)
                
                col_antes = 'antes' if 'antes' in df_rep.columns else 'estatus_inicial'
                col_despues = 'despues' if 'despues' in df_rep.columns else 'estatus_final'

                st.dataframe(df_rep, use_container_width=True)
                
                col_m1, col_m2 = st.columns(2)
                col_m1.metric("Total Intervenciones", len(df_rep))
                
                reparados = len(df_rep[(df_rep[col_antes] == 'Inoperativo') & (df_rep[col_despues] == 'Operativo')])
                col_m2.metric("Equipos Recuperados", reparados)
            else:
                st.warning("No se encontraron registros en el rango seleccionado.")
