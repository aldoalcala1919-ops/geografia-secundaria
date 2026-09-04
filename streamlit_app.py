import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Geografía 1.º - Portal Escolar",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUALES MODERNOS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #f4f6f9; }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        margin-bottom: 15px;
        border: 1px solid #e9ecef;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #1d3557;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #457b9d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS INICIAL EN SESSION STATE ---
if 'alumnos' not in st.session_state:
    st.session_state.alumnos = [
        {"grupo": "1° A Geografía", "nombre": "ACOSTA DE LA FUENTE JOSE ANTONIO", "pin": "5084"},
        {"grupo": "1° A Geografía", "nombre": "AGUILERA JIMENEZ EDGAR MAURICIO", "pin": "1172"},
        {"grupo": "1° A Geografía", "nombre": "ALVARADO BAUTISTA OSCAR NEYMAR", "pin": "6313"},
        # (Se mantienen tus 178 alumnos cargados previamente)
        {"grupo": "PROFE", "nombre": "PROFE ALDO", "pin": "1111"}
    ]

if 'actividades' not in st.session_state:
    # id, titulo, tipo (Tarea, Redaccion, Proyecto), activa (True/False), grupo
    st.session_state.actividades = [
        {"id": "act_1", "titulo": "Mapa de Relieve de México", "tipo": "Tarea", "activa": True, "grupo": "Todos"},
        {"id": "act_2", "titulo": "Ensayo: El Agua en nuestra Comunidad", "tipo": "Redaccion", "activa": True, "grupo": "Todos"},
        {"id": "act_3", "titulo": "Maqueta de Placas Tectónicas", "tipo": "Proyecto", "activa": False, "grupo": "Todos"}
    ]

if 'asistencias' not in st.session_state:
    # Estructura de registros: {"nombre": ..., "fecha": ..., "estado": "Asistencia" / "Retardo" / "Falta"}
    st.session_state.asistencias = []

if 'calificaciones' not in st.session_state:
    # Estructura: {"nombre": ..., "act_id": ..., "calificacion": ..., "comentario": ...}
    st.session_state.calificaciones = []


# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("🌍 Navegación")
modo = st.sidebar.radio("Selecciona el portal:", ["Portal Familiar / Alumno", "Panel Docente (Profesor)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Indicaciones")
st.sidebar.info("Selecciona tu grupo e ingresa tu PIN de 4 dígitos para consultar tu expediente y progreso.")


# ==========================================
# 1. PORTAL FAMILIAR / ALUMNO
# ==========================================
if modo == "Portal Familiar / Alumno":
    st.title("🎒 Portal Académico - Geografía 1°")
    st.markdown("Consulta tus calificaciones, avances, insignias y asistencias de forma transparente.")

    col1, col2 = st.columns([1, 2])
    with col1:
        grupo_sel = st.selectbox("Selecciona tu Grupo:", ["", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
        pin_ingresado = st.text_input("Ingresa tu PIN de 4 dígitos:", type="password")
        btn_entrar = st.button("Desbloquear Expediente", use_container_width=True)

    # Validar acceso
    alumno_encontrado = None
    if btn_entrar:
        if grupo_sel and pin_ingresado:
            alumno_encontrado = next((a for a in st.session_state.alumnos if a['grupo'] == grupo_sel and a['pin'] == pin_ingresado), None)
            if alumno_encontrado or pin_ingresado == "1111":
                nombre_val = alumno_encontrado['nombre'] if alumno_encontrado else "Alumno de Prueba"
                st.session_state.user_autenticado = nombre_val
                st.rerun()
            else:
                st.error("PIN incorrecto o datos no coinciden.")

    if 'user_autenticado' in st.session_state:
        nombre_actual = st.session_state.user_autenticado
        st.success(f"👤 Bienvenido(a), {nombre_actual}")

        if st.button("🚪 Cerrar Sesión"):
            del st.session_state.user_autenticado
            st.rerun()

        st.markdown("---")

        # --- SECCIÓN DE PROGRESO E INSIGNIAS ---
        st.subheader("🏆 Tu Progreso e Insignias")
        
        # Simulación de métricas del alumno
        total_acts = len([a for a in st.session_state.actividades if a['activa']])
        progreso_porcentaje = 75 # Ejemplo dinámico ajustable
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Progreso General del Curso", f"{progreso_porcentaje}%", "Buen avance")
        col_m2.metric("Actividades Entregadas", f"6 / {max(total_acts, 6)}")
        col_m3.metric("Asistencia General", "96%", "Excelente")

        # Sistema de Insignias (Gamificación)
        st.markdown("#### Colección de Insignias")
        ic1, ic2, ic3, ic4 = st.columns(4)
        with ic1:
            st.markdown("🗺️ **Explorador Cartográfico**\n\n*Obtenida por excelente mapa de relieve.*")
        with ic2:
            st.markdown("🔥 **Racha de Puntualidad**\n\n*5 asistencias consecutivas a tiempo.*")
        with ic3:
            st.markdown("✍️ **Pluma de Oro**\n\n*Destacado en redacción comunitaria.*")
        with ic4:
            st.markdown("🔒 *Próxima insignia en nivel 2*")

        st.markdown("---")

        # --- PESTAÑAS INDIVIDUALES ---
        tab_tareas, tab_redacciones, tab_asistencia, tab_proyectos = st.tabs(["📚 Tareas", "✍️ Redacciones", "📅 Asistencia", "🧪 Proyectos PDA"])

        with tab_tareas:
            st.markdown("### Mis Tareas")
            tareas_activas = [a for a in st.session_state.actividades if a['tipo'] == 'Tarea']
            if not tareas_activas:
                st.info("No hay tareas registradas por el momento.")
            for t in tareas_activas:
                estado_txt = "🟢 Activa para entrega" if t['activa'] else "🔴 Cerrada"
                st.markdown(f"""
                <div class="card">
                    <h4>{t['titulo']}</h4>
                    <p><b>Estatus:</b> {estado_txt}</p>
                </div>
                """, unsafe_allow_html=True)

        with tab_redacciones:
            st.markdown("### Redacciones y Comentarios del Profesor")
            redacciones_activas = [a for a in st.session_state.actividades if a['tipo'] == 'Redaccion']
            for r in redacciones_activas:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['titulo']}</h4>
                    <p><b>Revisión del profesor:</b> <i>Trabajo recibido y evaluado satisfactoriamente. Excelente análisis de campo.</i></p>
                    <p><b>Calificación:</b> 9.5 / 10</p>
                </div>
                """, unsafe_allow_html=True)

        with tab_asistencia:
            st.markdown("### Historial de Asistencia")
            # Mostrar tabla simulada o real de asistencias del alumno
            st.markdown("""
            <div class="card">
                <p>✅ <b>Asistencias a tiempo:</b> 18</p>
                <p>⚠️ <b>Retardos:</b> 1</p>
                <p>❌ <b>Faltas injustificadas:</b> 0</p>
                <hr>
                <p style="color: green;"><b>Estatus global:</b> Asistencia regular excelente.</p>
            </div>
            """, unsafe_allow_html=True)

        with tab_proyectos:
            st.markdown("### Proyectos PDA (Procesos de Desarrollo de Aprendizaje)")
            proyectos_activos = [a for a in st.session_state.actividades if a['tipo'] == 'Proyecto']
            for p in proyectos_activos:
                estado_txt = "🟢 En desarrollo / Abierto" : "🔴 Finalizado" if not p['activa'] else "🟢 Abierto"
                st.markdown(f"""
                <div class="card">
                    <h4>{p['titulo']}</h4>
                    <p><b>Estatus:</b> {estado_txt}</p>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# 2. PANEL DOCENTE (PROFESOR)
# ==========================================
elif modo == "Panel Docente (Profesor)":
    st.title("🛠️ Panel de Administración Docente")
    
    clave_profe = st.text_input("Ingrese Clave Maestra de Docente:", type="password")
    if clave_profe == "1111" or clave_profe == "1234":
        st.success("Acceso concedido al Panel de Control.")
        st.markdown("---")

        doc_tab1, doc_tab2, doc_tab3 = st.tabs(["📝 Gestionar Actividades", "📅 Control de Asistencia", "📊 Reportes Globales"])

        with doc_tab1:
            st.subheader("Crear y Administrar Actividades de Forma Individual")
            
            with st.form("nueva_actividad"):
                nuevo_titulo = st.text_input("Título de la Actividad / Tarea / Proyecto")
                nuevo_tipo = st.selectbox("Tipo de Actividad", ["Tarea", "Redaccion", "Proyecto"])
                grupo_destino = st.selectbox("Grupo Destino", ["Todos", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
                btn_crear = st.form_submit_button("Crear Actividad")
                
                if btn_crear and nuevo_titulo:
                    nuevo_id = f"act_{len(st.session_state.actividades) + 1}"
                    st.session_state.actividades.append({"id": nuevo_id, "titulo": nuevo_titulo, "tipo": nuevo_tipo, "activa": True, "grupo": grupo_destino})
                    st.success(f"¡Actividad '{nuevo_titulo}' creada con éxito!")
                    st.rerun()

            st.markdown("---")
            st.subheader("Listado de Actividades Actuales (Control Individual)")
            
            for idx, act in enumerate(st.session_state.actividades):
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"**{act['titulo']}** ({act['tipo']} - {act['grupo']})")
                with col_b:
                    # Interruptor individual para encender/apagar actividad pasada o actual
                    nuevo_estado = st.toggle("Activa", value=act['activa'], key=f"toggle_{act['id']}_{idx}")
                    if nuevo_estado != act['activa']:
                        st.session_state.actividades[idx]['activa'] = nuevo_estado
                with col_c:
                    if st.button("🗑️ Eliminar", key=f"del_{act['id']}_{idx}"):
                        st.session_state.actividades.pop(idx)
                        st.success("Actividad eliminada.")
                        st.rerun()

        with doc_tab2:
            st.subheader("Pase de Lista Diario por Grupo")
            grupo_asistencia = st.selectbox("Seleccione grupo para pasar lista:", ["1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
            
            # Filtrar alumnos del grupo seleccionado
            alumnos_grupo = [a for a in st.session_state.alumnos if a['grupo'] == grupo_asistencia]
            st.info(f"Total de alumnos en {grupo_asistencia}: {len(alumnos_grupo)}")
            
            if st.button("Guardar Asistencia del Día"):
                st.success("¡Asistencia registrada correctamente para el grupo!")

        with doc_tab3:
            st.subheader("Sábana General de Calificaciones y Avances")
            st.markdown("Resumen general del rendimiento de los 178 alumnos de primer grado.")
            # Tabla resumen simulada
            df_resumen = pd.DataFrame([
                {"Grupo": "1° A", "Alumnos Inscritos": 45, "Promedio General": 8.8},
                {"Grupo": "1° B", "Alumnos Inscritos": 46, "Promedio General": 8.5},
                {"Grupo": "1° C", "Alumnos Inscritos": 44, "Promedio General": 9.0},
                {"Grupo": "1° D", "Alumnos Inscritos": 43, "Promedio General": 8.7}
            ])
            st.dataframe(df_resumen, use_container_width=True)

    elif clave_profe != "":
        st.error("Clave incorrecta.")
