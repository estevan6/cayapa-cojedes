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
import psycopg2
from PIL import Image, ImageOps
from conexion import ejecutar_consulta

UPLOADS_DIR = "static/uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def guardar_imagen(file, codigo_equipo, tipo_foto, max_ancho=1280, calidad=75):
    """Procesa, redimensiona y comprime una imagen con Pillow antes de guardarla."""
    if file is None:
        return None
    
    nombre_archivo = f"{codigo_equipo}_{tipo_foto}.jpg"
    ruta_completa = os.path.join(UPLOADS_DIR, nombre_archivo)
    
    try:
        img = Image.open(file)
        img = ImageOps.exif_transpose(img)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        ancho_orig, alto_orig = img.size
        if ancho_orig > max_ancho:
            proporcion = max_ancho / float(ancho_orig)
            nuevo_alto = int((float(alto_orig) * float(proporcion)))
            img = img.resize((max_ancho, nuevo_alto), Image.Resampling.LANCZOS)
            
        img.save(ruta_completa, "JPEG", optimize=True, quality=calidad)
        return ruta_completa
        
    except Exception as e:
        st.error(f"Error al procesar la imagen {tipo_foto}: {e}")
        return None

def render():
    st.header("📝 Registro de Reporte Técnico")

    # 1. Cargar datos maestros principales
    entes = ejecutar_consulta("SELECT id_ente, nombre_ente FROM entes ORDER BY nombre_ente;")
    tecnicos = ejecutar_consulta("SELECT id_tecnico, nombre_tecnico FROM tecnicos ORDER BY nombre_tecnico;")
    categorias = ejecutar_consulta("SELECT id_categoria, nombre_categoria FROM categorias ORDER BY nombre_categoria;")

    dict_entes = {e['nombre_ente']: e['id_ente'] for e in entes} if entes else {}
    dict_tecnicos = {t['nombre_tecnico']: t['id_tecnico'] for t in tecnicos} if tecnicos else {}
    dict_categorias = {c['nombre_categoria']: c['id_categoria'] for c in categorias} if categorias else {}

    st.subheader("1. Categoría General")
    
    if not dict_categorias:
        st.error("No hay categorías registradas en la base de datos.")
        return

    categoria_sel = st.selectbox(
        "Categoría General (Área Técnica)", 
        list(dict_categorias.keys())
    )

    id_cat = dict_categorias.get(categoria_sel)
    tipos = ejecutar_consulta(
        "SELECT id_tipo, nombre_tipo FROM tipos_equipo WHERE id_categoria = %s ORDER BY nombre_tipo;", 
        (id_cat,)
    ) if id_cat else []
    
    dict_tipos = {t['nombre_tipo']: t['id_tipo'] for t in tipos} if tipos else {}

    st.divider()
    
    with st.form("form_reporte", clear_on_submit=True):
        st.subheader("2. Datos Principales del Servicio y Ubicación")
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha de Servicio", datetime.date.today())
            ente_sel = st.selectbox("Ente / Institución", list(dict_entes.keys()) if dict_entes else ["Sin entes"])
        with col2:
            tecnico_sel = st.selectbox("Técnico Responsable", list(dict_tecnicos.keys()) if dict_tecnicos else ["Sin técnicos"])
            tipo_sel = st.selectbox("Tipo de Equipo Específico", list(dict_tipos.keys()) if dict_tipos else ["Sin tipos registrados"])

        st.caption("📍 Ubicación Interna en la Institución")
        u1, u2 = st.columns(2)
        with u1:
            # max_chars previene que el usuario escriba más del límite de la BD
            departamento = st.text_input("Unidad / Departamento / Servicio", max_chars=150, placeholder="Ej: Recursos Humanos, Emergencia")
        with u2:
            piso = st.text_input("Piso / Nivel", max_chars=50, placeholder="Ej: Planta Baja, Piso 1")

        c3, c4 = st.columns(2)
        with c3:
            marca = st.text_input("Marca", max_chars=100)
            serial = st.text_input("Serial", max_chars=100)
        with c4:
            modelo = st.text_input("Modelo", max_chars=100)
            bien_nac = st.text_input("Nro. Bien Nacional", max_chars=100)

        st.divider()

        # --- SECCIÓN 3: AUDITORÍA PREVIA Y DIAGNÓSTICO ---
        st.subheader("3. Auditoría de Estado Previo a Revisión")
        aud_prev1, aud_prev2 = st.columns(2)
        with aud_prev1:
            est_init = st.selectbox(
                "Estatus Inicial", 
                ["Revisado – Inoperativa", "Revisado – Operativo Parcial", "Por Revisar"]
            )
            tipo_mant = st.selectbox("Tipo de Mantenimiento / Acción Prevista", ["Correctivo", "Preventivo", "Diagnóstico"])
        
        with aud_prev2:
            descripcion_falla = st.text_area(
                "Descripción de Problemas / Fallas Detectadas *",
                placeholder="Indique las razones o fallas que implicaron la necesidad de intervención..."
            )

        st.divider()

        # --- SECCIÓN 4: AUDITORÍA POSTERIOR ---
        st.subheader("4. Auditoría de Estado Posterior")
        est_fin = st.selectbox("Estatus Final", ["Reparado", "Reparado – Parcial", "Inoperativo"])

        observaciones_accion = st.text_area(
            "Descripción de Acciones, Diagnóstico y/o Informe Posterior *",
            placeholder="Describa los problemas corregidos, acciones tomadas o justificación de inoperatividad..."
        )

        st.divider()

        # --- SECCIÓN 5: EVIDENCIAS FOTOGRÁFICAS ---
        st.subheader("📷 Evidencias Fotográficas (Opcional)")
        st.caption("Si lo deseas, puedes adjuntar hasta 3 fotos. Formatos: JPG, JPEG, PNG.")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            file_chapa = st.file_uploader("1. Foto Chapa / Serial (Opcional)", type=["jpg", "jpeg", "png"])
        with col_f2:
            file_falla = st.file_uploader("2. Foto Falla Principal (Opcional)", type=["jpg", "jpeg", "png"])
        with col_f3:
            file_trabajo = st.file_uploader("3. Foto Trabajo Concluido (Opcional)", type=["jpg", "jpeg", "png"])

        guardar = st.form_submit_button("Guardar Reporte Técnico")

        if guardar:
            if not dict_tipos or tipo_sel not in dict_tipos:
                st.error("⚠️ Debes seleccionar un tipo de equipo válido.")
            elif not dict_entes or ente_sel not in dict_entes:
                st.error("⚠️ Debes seleccionar un Ente válido.")
            elif not descripcion_falla.strip():
                st.error("⚠️ El campo 'Descripción de Problemas / Fallas Detectadas' es obligatorio.")
            elif not observaciones_accion.strip():
                st.error("⚠️ El campo 'Descripción de Acciones / Informe Posterior' es obligatorio.")
            else:
                try:
                    res_cod = ejecutar_consulta("SELECT 'CH-COJ-' || LPAD(nextval('seq_codigo_equipo')::text, 6, '0') AS nuevo_codigo;")
                    nuevo_codigo = res_cod[0]['nuevo_codigo']

                    path_chapa = guardar_imagen(file_chapa, nuevo_codigo, "chapa")
                    path_falla = guardar_imagen(file_falla, nuevo_codigo, "falla")
                    path_trabajo = guardar_imagen(file_trabajo, nuevo_codigo, "trabajo")

                    sql = """
                        INSERT INTO reporte (
                            codigo_equipo, fecha_servicio, id_ente, id_tecnico, id_tipo,
                            piso, departamento, marca, modelo, serial, nro_bien_nacional,
                            estatus_inicial, descripcion_falla, estatus_final, tipo_mantenimiento, 
                            observaciones_accion, foto_chapa, foto_falla, foto_trabajo
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    ejecutar_consulta(sql, (
                        nuevo_codigo, fecha, dict_entes[ente_sel], dict_tecnicos[tecnico_sel], dict_tipos[tipo_sel],
                        piso, departamento, marca, modelo, serial, bien_nac, 
                        est_init, descripcion_falla, est_fin, tipo_mant, observaciones_accion,
                        path_chapa, path_falla, path_trabajo
                    ))
                    
                    st.success("¡Reporte guardado exitosamente!")
                    st.info(f"🏷️ **Código asignado al equipo:** `{nuevo_codigo}`")
                
                # Interceptor de errores detallado
                except Exception as e:
                    msg_error = str(e)
                    if "value too long for type character varying" in msg_error or "StringDataRightTruncation" in msg_error:
                        st.error("⚠️ **Error al guardar:** Uno de los textos ingresados excede el límite permitido por la base de datos.")
                        st.warning("👉 Por favor verifica que los campos como **Serial**, **Bien Nacional**, **Marca**, **Modelo**, **Piso** o **Departamento** no tengan textos excesivamente largos.")
                    elif "unique constraint" in msg_error or "UniqueViolation" in msg_error:
                        st.error("⚠️ **Error de duplicado:** Ya existe un registro guardado con ese mismo Serial o Código de Equipo.")
                    else:
                        st.error(f"❌ Error inesperado al guardar el reporte: {msg_error}")
