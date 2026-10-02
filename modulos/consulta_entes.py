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
from conexion import ejecutar_consulta

def render():
    st.header("📇 Directorio de Entes, Autoridades y Contactos")
    st.caption("Consulta la información institucional y los datos del personal directivo y operativo.")

    # --- 1. BUSCADOR Y FILTROS ---
    c1, c2 = st.columns(2)
    with c1:
        busqueda = st.text_input("🔍 Buscar por nombre de institución:", placeholder="Ej: Hospital, Alcaldía, Escuela...")
    with c2:
        # Cargar lista de cargos para filtrar
        cargos_db = ejecutar_consulta("SELECT nombre_cargo FROM cargos ORDER BY nombre_cargo;")
        lista_cargos = ["-- Todos los Cargos --"] + [c['nombre_cargo'] for c in cargos_db] if cargos_db else ["-- Todos los Cargos --"]
        cargo_filtro = st.selectbox("Filtrar por Cargo de Autoridad:", lista_cargos)

    # --- 2. CONSULTA A LA BASE DE DATOS ---
    sql = """
        SELECT 
            e.id_ente,
            e.nombre_ente AS "Institución",
            e.comuna AS "Comuna",
            e.direccion AS "Dirección",
            
            -- Datos de la Autoridad Activa
            ha.nombre_auto AS "Nombre Autoridad",
            ha.cargo_auto AS "Cargo Autoridad",
            ha.celular_auto AS "Celular Autoridad",
            COALESCE(ha.telef_auto, 'N/A') AS "Teléfono Autoridad",
            COALESCE(ha.email_auto, 'N/A') AS "Correo Autoridad",
            
            -- Datos del Contacto Operativo Activo
            COALESCE(hc.nombre_cont, 'Sin registrar') AS "Nombre Contacto",
            COALESCE(hc.cargo_cont, 'N/A') AS "Cargo Contacto",
            COALESCE(hc.celular_cont, 'N/A') AS "Celular Contacto",
            COALESCE(hc.telef_cont, 'N/A') AS "Teléfono Contacto",
            COALESCE(hc.email_cont, 'N/A') AS "Correo Contacto"
            
        FROM entes e
        LEFT JOIN historial_autoridades ha ON e.id_ente = ha.id_ente AND ha.activo_auto = TRUE
        LEFT JOIN historial_contactos hc ON e.id_ente = hc.id_ente AND hc.activo_cont = TRUE
        WHERE 1=1
    """
    parametros = []

    if busqueda.strip():
        sql += " AND e.nombre_ente ILIKE %s"
        parametros.append(f"%{busqueda.strip()}%")

    if cargo_filtro != "-- Todos los Cargos --":
        sql += " AND ha.cargo_auto = %s"
        parametros.append(cargo_filtro)

    sql += " ORDER BY e.nombre_ente ASC;"

    datos = ejecutar_consulta(sql, tuple(parametros))

    # --- 3. PRESENTACIÓN DE RESULTADOS ---
    if datos:
        df = pd.DataFrame([dict(row) for row in datos])
        
        st.write(f"📋 **{len(df)}** instituciones encontradas.")
        
        # Selector para ver la ficha detallada de una institución
        lista_entes = df["Institución"].tolist()
        ente_seleccionado = st.selectbox("Seleccione una institución para ver la ficha completa:", lista_entes)

        if ente_seleccionado:
            row = df[df["Institución"] == ente_seleccionado].iloc[0]
            
            st.divider()
            st.subheader(f"🏛️ {row['Institución']}")
            st.caption(f"📍 **Dirección:** {row['Dirección']} | **Comuna:** {row['Comuna']}")

            col_aut, col_con = st.columns(2)

            # --- TARJETA AUTORIDAD ---
            with col_aut:
                st.markdown("### 👔 Autoridad Principal")
                st.info(
                    f"**Nombre:** {row['Nombre Autoridad']}\n\n"
                    f"**Cargo:** {row['Cargo Autoridad']}\n\n"
                    f"📱 **Celular:** {row['Celular Autoridad']}\n\n"
                    f"☎️ **Teléfono Fijo:** {row['Teléfono Autoridad']}\n\n"
                    f"✉️ **Correo:** {row['Correo Autoridad']}"
                )

            # --- TARJETA CONTACTO ---
            with col_con:
                st.markdown("### 📞 Contacto Operativo")
                if row['Nombre Contacto'] != 'Sin registrar':
                    st.success(
                        f"**Nombre:** {row['Nombre Contacto']}\n\n"
                        f"**Cargo:** {row['Cargo Contacto']}\n\n"
                        f"📱 **Celular:** {row['Celular Contacto']}\n\n"
                        f"☎️ **Teléfono Fijo:** {row['Teléfono Contacto']}\n\n"
                        f"✉️ **Correo:** {row['Correo Contacto']}"
                    )
                else:
                    st.warning("Esta institución no tiene un contacto operativo registrado.")

            # --- HISTORIAL DE CAMBIOS DE PERSONAL ---
            with st.expander("📜 Ver Historial de Autoridades y Contactos Anteriores"):
                id_e = int(row['id_ente'])
                
                hist_aut = ejecutar_consulta(
                    "SELECT nombre_auto, cargo_auto, celular_auto, email_auto, activo_auto FROM historial_autoridades WHERE id_ente = %s ORDER BY id_auto DESC;", 
                    (id_e,)
                )
                if hist_aut:
                    st.caption("Historial de Autoridades:")
                    st.dataframe(pd.DataFrame([dict(r) for r in hist_aut]), use_container_width=True)

                # Se utiliza 'id_cont' que es la columna primaria real
                hist_cont = ejecutar_consulta(
                    "SELECT nombre_cont, cargo_cont, celular_cont, email_cont, activo_cont FROM historial_contactos WHERE id_ente = %s ORDER BY id_cont DESC;", 
                    (id_e,)
                )
                if hist_cont:
                    st.caption("Historial de Contactos Operativos:")
                    st.dataframe(pd.DataFrame([dict(r) for r in hist_cont]), use_container_width=True)

    else:
        st.warning("No se encontraron instituciones que coincidan con la búsqueda.")
