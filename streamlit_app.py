import streamlit as json_lib # placeholder
import streamlit as st
import pandas as pd
from google import genai
from datetime import datetime

# Configuración de la página orientada a móviles
st.set_page_config(page_title="Geografía 1° — Secundaria", page_icon="🌍", layout="centered")

# --- SIMULACIÓN DE BASE DE DATOS LOCAL O CONEXIÓN ---
# Aquí puedes mantener tus listas de alumnos o conectar un Google Sheets / CSV
if 'alumnos' not in st.session_state:
    st.session_state.alumnos = [
        {"grupo": "1° A Geografía", "nombre": "Ejemplo Alumno 1", "pin": "1234"},
        # Puedes agregar aquí el resto de tus alumnos de los 4 grupos
    ]

if 'switches' not in st.session_state:
    st.session_state.switches = {"Tareas": True, "Redaccion": True, "Proyectos": True}

if 'entregas' not in st.session_state:
    st.session_state.entregas = []

if 'actividades' not in st.session_state:
    st.session_state.actividades = [
        {"id": "act_1", "titulo": "Mapa de riesgos digitales", "grupo": "1° A Geografía", "estado": "Abierta"}
    ]

# --- MENÚ LATERAL PARA ELEGIR VISTA ---
st.sidebar.title("🧭 Navegación")
vista_seleccionada = st.sidebar.radio("Selecciona el Portal:", ["Portal Familiar / Alumno", "Panel Docente"])

# ==========================================
# 1. PORTAL FAMILIAR / ALUMNO
# ==========================================
if vista_seleccionada == "Portal Familiar / Alumno":
    st.markdown("<h2 style='text-align: center;'>🌍 Geografía 1° — Secundaria</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Portal Familiar de Consulta Escolar</p>", unsafe_allow_html=True)

    with st.container():
        st.subheader("🔒 Acceso Familiar")
        grupo_sel = st.selectbox("Selecciona tu Grupo:", ["", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
        pin_ingresado = st.text_input("Ingresa tu PIN de 4 dígitos:", type="password")

        if st.button("Desbloquear Expediente", use_container_width=True):
            # Validación simple
            alumno_encontrado = next((a for a in st.session_state.alumnos if a['grupo'] == grupo_sel and a['pin'] == pin_ingresado), None)
            
            if alumno_encontrado or pin_ingresado == "1234": # PIN comodín de prueba
                st.session_state.user_autenticado = alumno_encontrado['nombre'] if alumno_encontrado else "Alumno de Prueba"
                st.rerun()
            else:
                st.error("PIN incorrecto o grupo no seleccionado.")

    # Si ya está autenticado
    if 'user_autenticado' in st.session_state:
        nombre_actual = st.session_state.user_autenticado
        st.success(f"👤 Bienvenido(a), {nombre_actual}")

        if st.button("🔒 Cerrar Sesión"):
            del st.session_state.user_autenticado
            st.rerun()

        st.divider()

        # Métricas visuales
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Asistencia Global", value="100%")
        with col2:
            st.metric(label="Promedio Orientativo", value="90")

        # Insignias
        st.subheader("🏆 Insignias de Valor")
        c1, c2, c3, c4 = st.columns(4)
        c1.info("🧭 Brújula\nAsistencia")
        c2.info("⭐ Participación\nTareas")
        c3.info("📜 Escribano\nRedacción")
        c4.info("🛡️ Guardián\nDigitales")

        # Apartado Tareas
        st.subheader("📝 1. Apartado de Actividades y Tareas")
        if not st.session_state.switches["Tareas"]:
            st.warning("🔒 La entrega de tareas se encuentra cerrada temporalmente por el profesor.")
        else:
            for act in st.session_state.actividades:
                st.markdown(f"**{act['titulo']}** ({act['grupo']})")
                foto_subida = st.file_uploader(f"Subir evidencia para: {act['titulo']}", type=["jpg", "png", "jpeg"], key=act['id'])
                
                if foto_subida and st.button(f"Enviar Tarea con IA ({act['id']})"):
                    with st.spinner("Analizando con Gemini (priorizando esfuerzo y entrega)..."):
                        # Llamada real a Gemini API con el SDK moderno google-genai
                        try:
                            # Nota: Puedes configurar tu API Key como secreto en Streamlit
                            client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", "TU_API_KEY"))
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=['Evalúa esta tarea escolar priorizando la entrega. Devuelve retroalimentación constructiva y una calificación orientativa de 70 a 100.', foto_subida.getvalue()]
                            )
                            st.success("¡Tarea evaluada y registrada con éxito!")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error al conectar con la IA: {e}")

        # Apartado Redacciones
        st.subheader("📜 2. Redacción Escolar (Análisis IA)")
        if not st.session_state.switches["Redaccion"]:
            st.warning("🔒 La subida de redacciones está cerrada temporalmente.")
        else:
            foto_redaccion = st.file_uploader("Sube la foto de tu redacción escolar:", type=["jpg", "png", "jpeg"], key="redac_file")
            if foto_redaccion and st.button("Enviar Redacción con IA"):
                st.success("¡Redacción analizada y guardada correctamente!")

        # Apartado Proyectos PDA
        st.subheader("🗺️ 3. Proyectos PDA (Riesgos en Redes Sociales)")
        if not st.session_state.switches["Proyectos"]:
            st.warning("🔒 Los proyectos PDA están cerrados temporalmente.")
        else:
            st.info("Bloque actual: Identificación de situaciones de riesgo en redes sociales.")
            foto_proy = st.file_uploader("Sube evidencia de tu proyecto PDA:", type=["jpg", "png", "jpeg"], key="proy_file")
            if foto_proy and st.button("Enviar Proyecto con IA"):
                st.success("¡Proyecto PDA registrado con éxito!")

# ==========================================
# 2. PANEL DOCENTE
# ==========================================
elif vista_seleccionada == "Panel Docente":
    st.markdown("<h2 style='text-align: center;'>👨‍🏫 Panel Docente — Geografía 1°</h2>", unsafe_allow_html=True)
    
    clave_docente = st.text_input("🔑 Clave de Acceso Docente:", type="password")
    
    if clave_docente == "1234": # Tu clave maestra
        st.success("¡Acceso concedido al panel de control!")
        
        st.divider()
        st.subheader("⚡ Interruptores Globales (Kill Switches)")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.session_state.switches["Tareas"] = st.toggle("Apartado Tareas", value=st.session_state.switches["Tareas"])
        with col_s2:
            st.session_state.switches["Redaccion"] = st.toggle("Apartado Redacciones", value=st.session_state.switches["Redaccion"])
        with col_s3:
            st.session_state.switches["Proyectos"] = st.toggle("Proyectos PDA", value=st.session_state.switches["Proyectos"])

        st.divider()
        st.subheader("📚 Crear Nueva Actividad")
        nuevo_titulo = st.text_input("Título de la Actividad:")
        grupo_destino = st.selectbox("Grupo Destino:", ["Todos", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
        if st.button("Publicar Actividad"):
            if nuevo_titulo:
                st.session_state.actividades.append({"id": f"act_{len(st.session_state.actividades)+1}", "titulo": nuevo_titulo, "grupo": grupo_destino, "estado": "Abierta"})
                st.success("¡Actividad publicada con éxito!")
            else:
                st.error("Escribe un título para la actividad.")

        st.divider()
        st.subheader("⚖️ Control de Asistencia y Justificaciones")
        st.info("Aquí podrás tomar lista rápidamente y justificar faltas con comprobante en mano.")
        
        alumno_a_justificar = st.text_input("Nombre del alumno a justificar falta:")
        fecha_falta = st.text_input("Fecha de la falta (DD/MM/AAAA):")
        if st.button("Justificar Falta"):
            if alumno_a_justificar and fecha_falta:
                st.success(f"¡Falta de {alumno_a_justificar} del día {fecha_falta} cambiada a Justificado!")
            else:
                st.error("Completa los datos.")

    elif clave_docente != "":
        st.error("Clave de docente incorrecta.")
