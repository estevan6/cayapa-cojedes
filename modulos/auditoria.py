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
    st.header("🛡️ Historial de Auditoría y Trazabilidad")
    st.caption("Registro de bitácora sobre acciones realizadas en el sistema CAYAPA.")

    if st.session_state.get("usuario_rol") != "admin":
        st.error("🔒 Acceso denegado. Solo el usuario Administrador puede consultar la auditoría del sistema.")
        return

    logs = ejecutar_consulta("""
        SELECT 
            l.id_log AS "ID",
            l.fecha AS "Fecha/Hora",
            COALESCE(t.nombre_tecnico, 'Sistema') AS "Usuario",
            l.accion AS "Acción",
            l.detalles AS "Detalles"
        FROM logs_sistema l
        LEFT JOIN tecnicos t ON l.id_tecnico = t.id_tecnico
        ORDER BY l.fecha DESC
        LIMIT 200;
    """)

    if logs:
        st.subheader("📋 Trazabilidad de Eventos Recientes")
        df_logs = pd.DataFrame([dict(r) for r in logs])
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("No existen registros en la bitácora de auditoría aún.")
