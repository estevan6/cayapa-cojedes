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

# Ruta exacta del archivo del logo
LOGO_PATH = "logo.jpg"

try:
    logo_img = Image.open(LOGO_PATH)
except Exception:
    logo_img = None

# --- 1. CONFIGURACIÓN DE PÁGINA (FAVICON EN LA PESTAÑA) ---
st.set_page_config(
    page_title="Sistema CAYAPA HEROICA COJEDES",
    page_icon=logo_img if logo_img else "🏢",
    layout="wide"
)

# --- 2. CONTROL DE SESIÓN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

from modulos import login

if not st.session_state["autenticado"]:
    login.login_form()
else:
    # --- 3. APLICACIÓN PRINCIPAL ---
    from modulos import (
        entes, 
        consulta_entes, 
        agenda, 
        consulta_agenda, 
        reportes, 
        consulta_reportes, 
        exportacion, 
        usuarios, 
        auditoria
    )

    # Reemplazo en la Barra Lateral: Imagen en lugar de emoji 🛠️
    if logo_img:
        st.sidebar.image(logo_img, use_container_width=True)
    
    st.sidebar.markdown("### **Sistema CAYAPA COJEDES**")
    st.sidebar.write(f"👤 **{st.session_state['usuario_nombre']}**")
    st.sidebar.caption(f"Rol: `{st.session_state['usuario_rol'].upper()}`")

    # Opciones de navegación
    opciones_menu = [
        "🏫 Gestión de Entes",        
        "📅 Carga de Agenda",
        "📝 Carga de Reporte",
        "🔍 Consulta de Entes",
        "🔍 Consulta de Agenda",
        "🖥️ Consulta de Reportes",
        "👤 Mi Perfil / Usuarios"
    ]

    # Opciones exclusivas del Administrador
    if st.session_state["usuario_rol"] == "admin":
        opciones_menu.append("📥 Exportación de Datos")
        opciones_menu.append("🛡️ Auditoría")

    opcion = st.sidebar.radio("Navegación", opciones_menu)

    st.sidebar.divider()
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- 4. RUTEO DE MÓDULOS ---
    if opcion == "🏫 Gestión de Entes":
        entes.render()
    elif opcion == "🔍 Consulta de Entes":
        consulta_entes.render()
    elif opcion == "📅 Carga de Agenda":
        agenda.render()
    elif opcion == "🔍 Consulta de Agenda":
        consulta_agenda.render()
    elif opcion == "📝 Carga de Reporte":
        reportes.render()
    elif opcion == "🖥️ Consulta de Reportes":
        consulta_reportes.render()
    elif opcion == "👤 Mi Perfil / Usuarios":
        usuarios.render()
    elif opcion == "📥 Exportación de Datos" and st.session_state["usuario_rol"] == "admin":
        exportacion.render()
    elif opcion == "🛡️ Auditoría" and st.session_state["usuario_rol"] == "admin":
        auditoria.render()
