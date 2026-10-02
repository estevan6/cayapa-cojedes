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
import os
import pandas as pd
from conexion import ejecutar_consulta

def render():
    st.header("🖥️ Consulta de Equipos e Intervenciones")

    c1, c2 = st.columns(2)
    with c1:
        f_inicio = st.date_input("Fecha Inicial", datetime.date(2026, 1, 1))
    with c2:
        f_fin = st.date_input("Fecha Final", datetime.date.today())

    sql_reportes = """
        SELECT 
            r.codigo_equipo AS "Código Equipo",
            r.fecha_servicio AS "Fecha",
            e.nombre_ente AS "Institución",
            r.departamento AS "Departamento",
            r.piso AS "Piso",
            teq.nombre_tipo AS "Equipo",
            r.marca AS "Marca",
            r.serial AS "Serial",
            r.estatus_inicial AS "Estatus Inicial",
            r.descripcion_falla AS "Falla Detectada",
            r.estatus_final AS "Estatus Final",
            r.observaciones_accion AS "Informe / Acciones",
            r.foto_chapa, r.foto_falla, r.foto_trabajo
        FROM reporte r
        JOIN entes e ON r.id_ente = e.id_ente
        JOIN tipos_equipo teq ON r.id_tipo = teq.id_tipo
        WHERE r.fecha_servicio BETWEEN %s AND %s
        ORDER BY r.fecha_servicio DESC;
    """
    datos = ejecutar_consulta(sql_reportes, (f_inicio, f_fin))

    if datos:
        df = pd.DataFrame([dict(row) for row in datos])
        
        # Ocultar rutas absolutas de la tabla principal de vista general
        df_display = df.drop(columns=["foto_chapa", "foto_falla", "foto_trabajo"])
        st.dataframe(df_display, use_container_width=True)

        st.divider()
        st.subheader("🔍 Ver Evidencias Fotográficas de un Equipo")
        
        # Selector para ver fotos de un reporte específico
        codigos = df["Código Equipo"].tolist()
        equipo_sel = st.selectbox("Seleccione el Código de Equipo para ver fotografías:", codigos)

        if equipo_sel:
            fila = df[df["Código Equipo"] == equipo_sel].iloc[0]
            
            p1, p2, p3 = st.columns(3)
            
            with p1:
                st.caption("📷 1. Chapa / Serial")
                if fila["foto_chapa"] and os.path.exists(fila["foto_chapa"]):
                    st.image(fila["foto_chapa"], use_container_width=True)
                else:
                    st.info("Sin foto de chapa")

            with p2:
                st.caption("📷 2. Falla Principal")
                if fila["foto_falla"] and os.path.exists(fila["foto_falla"]):
                    st.image(fila["foto_falla"], use_container_width=True)
                else:
                    st.info("Sin foto de falla")

            with p3:
                st.caption("📷 3. Trabajo Concluido")
                if fila["foto_trabajo"] and os.path.exists(fila["foto_trabajo"]):
                    st.image(fila["foto_trabajo"], use_container_width=True)
                else:
                    st.info("Sin foto de conclusión")
    else:
        st.warning("No se encontraron intervenciones en las fechas seleccionadas.")
