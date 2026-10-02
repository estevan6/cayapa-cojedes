import streamlit as st
from conexion import ejecutar_consulta

def render():
    st.header("🏫 Registro de Entes e Historial de Personal")

    # Cargar lista de cargos desde la base de datos
    cargos_db = ejecutar_consulta("SELECT nombre_cargo FROM cargos ORDER BY nombre_cargo;")
    lista_cargos = [c['nombre_cargo'] for c in cargos_db] if cargos_db else ["Sin cargos registrados"]

    with st.form("form_ente", clear_on_submit=True):
        st.subheader("1. Identificación y Ubicación")
        nombre_ente = st.text_input("Nombre de la Institución / Ente *", max_chars=255)
        direccion = st.text_area("Dirección Completa")
        comuna = st.text_input("Comuna / Circuito Comunal", max_chars=150)
        
        c_lat, c_lng = st.columns(2)
        with c_lat:
            latitud = st.number_input("Latitud (Ej: 9.6200)", format="%.8f", value=0.0)
        with c_lng:
            longitud = st.number_input("Longitud (Ej: -68.5800)", format="%.8f", value=0.0)

        st.divider()
        
        # --- SECCIÓN 2: AUTORIDAD PRINCIPAL ---
        st.subheader("2. Autoridad Principal (Obligatorio)")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            nombre_auto = st.text_input("Nombre de la Autoridad *", max_chars=150)
            cargo_auto = st.selectbox("Cargo Autoridad *", lista_cargos, key="cargo_auto_select")
            celular_auto = st.text_input("Celular Autoridad", max_chars=20)
        with col_a2:
            telef_auto = st.text_input("Teléfono Fijo Autoridad (Opcional)", max_chars=20)
            email_auto = st.text_input("Correo Autoridad (Opcional)", max_chars=100)

        st.divider()
        
        # --- SECCIÓN 3: CONTACTO OPERATIVO (OPCIONAL) ---
        st.subheader("3. Persona de Contacto Operativo (Opcional)")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nombre_cont = st.text_input("Nombre del Contacto (Opcional)", max_chars=150)
            cargo_cont = st.selectbox("Cargo Contacto (Opcional)", ["-- Sin seleccionar --"] + lista_cargos, key="cargo_cont_select")
            celular_cont = st.text_input("Celular Contacto (Opcional)", max_chars=20)
        with col_c2:
            telef_cont = st.text_input("Teléfono Fijo Contacto (Opcional)", max_chars=20)
            email_cont = st.text_input("Correo Contacto (Opcional)", max_chars=100)

        st.divider()
        
        # --- SECCIÓN 4: POBLACIÓN ATENDIDA ---
        st.subheader("4. Población Atendida (Impacto Social)")
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            kids_fem = st.number_input("Niñas (0-10)", min_value=0, step=1)
            kids_mas = st.number_input("Niños (0-10)", min_value=0, step=1)
        with p2:
            joven_fem = st.number_input("Jóvenes Fem. (11-25)", min_value=0, step=1)
            joven_mas = st.number_input("Jóvenes Masc. (11-24)", min_value=0, step=1)
        with p3:
            mujer = st.number_input("Mujeres (25-59)", min_value=0, step=1)
            hombre = st.number_input("Hombres (25-59)", min_value=0, step=1)
        with p4:
            am_fem = st.number_input("Adultas Mayores (>59)", min_value=0, step=1)
            am_mas = st.number_input("Adultos Mayores (>59)", min_value=0, step=1)

        guardar = st.form_submit_button("Guardar Institución")

        if guardar:
            if not nombre_ente.strip():
                st.error("⚠️ El Nombre de la Institución es obligatorio.")
            elif not nombre_auto.strip():
                st.error("⚠️ El Nombre de la Autoridad es obligatorio.")
            else:
                try:
                    # 1. Insertar el Ente
                    sql_ente = """
                        INSERT INTO entes (
                            nombre_ente, direccion, comuna, latitud, longitud,
                            kids_fem, kids_mas, joven_fem, joven_mas, mujer, hombre, am_fem, am_mas
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id_ente;
                    """
                    res = ejecutar_consulta(sql_ente, (
                        nombre_ente, direccion, comuna, latitud, longitud,
                        kids_fem, kids_mas, joven_fem, joven_mas, mujer, hombre, am_fem, am_mas
                    ))
                    id_nuevo_ente = res[0]['id_ente']

                    # 2. Insertar Autoridad (Obligatoria)
                    sql_auto = """
                        INSERT INTO historial_autoridades (
                            id_ente, nombre_auto, cargo_auto, celular_auto, telef_auto, email_auto, activo_auto
                        ) VALUES (%s, %s, %s, %s, %s, %s, TRUE);
                    """
                    ejecutar_consulta(sql_auto, (
                        id_nuevo_ente, nombre_auto, cargo_auto, 
                        celular_auto if celular_auto.strip() else None, 
                        telef_auto if telef_auto.strip() else None, 
                        email_auto if email_auto.strip() else None
                    ))

                    # 3. Insertar Contacto solo si el usuario ingresó al menos el nombre o un cargo
                    if nombre_cont.strip() or cargo_cont != "-- Sin seleccionar --":
                        cargo_cont_valor = cargo_cont if cargo_cont != "-- Sin seleccionar --" else None
                        
                        sql_cont = """
                            INSERT INTO historial_contactos (
                                id_ente, nombre_cont, cargo_cont, celular_cont, telef_cont, email_cont, activo_cont
                            ) VALUES (%s, %s, %s, %s, %s, %s, TRUE);
                        """
                        ejecutar_consulta(sql_cont, (
                            id_nuevo_ente, 
                            nombre_cont.strip() if nombre_cont.strip() else "Contacto no registrado", 
                            cargo_cont_valor, 
                            celular_cont if celular_cont.strip() else None, 
                            telef_cont if telef_cont.strip() else None, 
                            email_cont if email_cont.strip() else None
                        ))

                    st.success(f"¡Institución '{nombre_ente}' registrada exitosamente!")
                except Exception as e:
                    msg_error = str(e)
                    if "unique constraint" in msg_error or "UniqueViolation" in msg_error:
                        st.error("⚠️ Ya existe una institución registrada con ese nombre.")
                    else:
                        st.error(f"❌ Error al guardar en la base de datos: {msg_error}")
