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
import pandas as pd
import datetime
import io
from conexion import ejecutar_consulta

def generar_ods(df):
    """Convierte un DataFrame de pandas a un archivo .ods en memoria."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='odf') as writer:
        df.to_excel(writer, index=False, sheet_name='Reportes_Tecnicos')
    buffer.seek(0)
    return buffer

def render():
    st.header("📊 Exportación Personalizada de Datos (.ods)")
    st.caption("Selecciona los criterios de búsqueda para filtrar la información antes de descargar.")

    # --- 1. CARGAR DATOS PARA LOS FILTROS ---
    entes = ejecutar_consulta("SELECT id_ente, nombre_ente FROM entes ORDER BY nombre_ente;")
    tecnicos = ejecutar_consulta("SELECT id_tecnico, nombre_tecnico FROM tecnicos ORDER BY nombre_tecnico;")
    tipos = ejecutar_consulta("SELECT id_tipo, nombre_tipo FROM tipos_equipo ORDER BY nombre_tipo;")

    dict_entes = {e['nombre_ente']: e['id_ente'] for e in entes} if entes else {}
    dict_tecnicos = {t['nombre_tecnico']: t['id_tecnico'] for t in tecnicos} if tecnicos else {}
    dict_tipos = {t['nombre_tipo']: t['id_tipo'] for t in tipos} if tipos else {}

    opcion_todos = "-- Todos --"

    # --- 2. PANEL DE FILTROS EN LA INTERFAZ ---
    with st.expander("🔍 Opciones de Filtro", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            fecha_inicio = st.date_input("Fecha Inicial", datetime.date(2026, 1, 1))
            ente_sel = st.selectbox("Institución / Ente", [opcion_todos] + list(dict_entes.keys()))
            tecnico_sel = st.selectbox("Técnico Responsable", [opcion_todos] + list(dict_tecnicos.keys()))
        
        with f2:
            fecha_fin = st.date_input("Fecha Final", datetime.date.today())
            tipo_sel = st.selectbox("Tipo de Equipo", [opcion_todos] + list(dict_tipos.keys()))
            estatus_sel = st.selectbox("Estatus Final", [opcion_todos, "Reparado", "Reparado – Parcial", "Inoperativo"])

    # --- 3. CONSTRUCCIÓN DINÁMICA DE LA CONSULTA SQL ---
    query = """
        SELECT 
            r.codigo_equipo AS "Código",
            r.fecha_servicio AS "Fecha",
            e.nombre_ente AS "Institución",
            r.departamento AS "Departamento",
            r.piso AS "Piso",
            teq.nombre_tipo AS "Tipo Equipo",
            r.marca AS "Marca",
            r.modelo AS "Modelo",
            r.serial AS "Serial",
            r.nro_bien_nacional AS "Bien Nacional",
            r.estatus_inicial AS "Estatus Inicial",
            r.descripcion_falla AS "Falla Detectada",
            r.estatus_final AS "Estatus Final",
            r.observaciones_accion AS "Informe Posterior",
            t.nombre_tecnico AS "Técnico Responsable"
        FROM reporte r
        JOIN entes e ON r.id_ente = e.id_ente
        JOIN tipos_equipo teq ON r.id_tipo = teq.id_tipo
        JOIN tecnicos t ON r.id_tecnico = t.id_tecnico
        WHERE r.fecha_servicio BETWEEN %s AND %s
    """
    parametros = [fecha_inicio, fecha_fin]

    # Agregar condiciones dinámicas según los filtros seleccionados
    if ente_sel != opcion_todos:
        query += " AND r.id_ente = %s"
        parametros.append(dict_entes[ente_sel])

    if técnico_sel if (tecnico_sel := tecnico_sel) != opcion_todos else False:
        query += " AND r.id_tecnico = %s"
        parametros.append(dict_tecnicos[tecnico_sel])

    if tipo_sel != opcion_todos:
        query += " AND r.id_tipo = %s"
        parametros.append(dict_tipos[tipo_sel])

    if estatus_sel != opcion_todos:
        query += " AND r.estatus_final = %s"
        parametros.append(estatus_sel)

    query += " ORDER BY r.fecha_servicio DESC;"

    # --- 4. EJECUCIÓN Y VISTA PREVIA ---
    datos = ejecutar_consulta(query, tuple(parametros))

    st.divider()

    if datos:
        df = pd.DataFrame([dict(row) for row in datos])
        
        st.success(f"Se encontraron **{len(df)}** registros que coinciden con los filtros.")
        
        # Mostrar vista previa de los datos a descargar
        st.subheader("📋 Vista previa de datos a exportar")
        st.dataframe(df, use_container_width=True)

        # Generación del archivo ODS en memoria
        fecha_actual_str = datetime.datetime.now().strftime("%d_%m_%Y")
        nombre_archivo_ods = f"reporte_{fecha_actual_str}.ods"
        archivo_ods = generar_ods(df)

        st.divider()

        # Botón de Descarga
        st.download_button(
            label="📥 Descargar Reporte Filtrado (.ods)",
            data=archivo_ods,
            file_name=nombre_archivo_ods,
            mime="application/vnd.oasis.opendocument.spreadsheet",
            type="primary"
        )
    else:
        st.warning("⚠️ No se encontraron registros con los criterios de filtro seleccionados.")
