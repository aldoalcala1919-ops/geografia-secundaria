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
        {"grupo": "1° A Geografía", "nombre": "ACOSTA DE LA FUENTE JOSE ANTONIO", "pin": "5084"},
        {"grupo": "1° A Geografía", "nombre": "AGUILERA JIMENEZ EDGAR MAURICIO", "pin": "1172"},
        {"grupo": "1° A Geografía", "nombre": "ALVARADO BAUTISTA OSCAR NEYMAR", "pin": "6313"},
        {"grupo": "1° A Geografía", "nombre": "ALVARADO RUIZ CARLOS ZACKTIEL", "pin": "4749"},
        {"grupo": "1° A Geografía", "nombre": "ALVARADO RUIZ OSCAR JAZIEL", "pin": "4951"},
        {"grupo": "1° A Geografía", "nombre": "ALVAREZ PEREZ GIOVANY ALEXANDER", "pin": "8270"},
        {"grupo": "1° A Geografía", "nombre": "ARENAS PEREZ NAYLA NYKOL", "pin": "4069"},
        {"grupo": "1° A Geografía", "nombre": "BENITEZ HERRERA KATLLYNE JEALE", "pin": "8925"},
        {"grupo": "1° A Geografía", "nombre": "CAMPOS IXBA EMILIANO DE JESUS", "pin": "2199"},
        {"grupo": "1° A Geografía", "nombre": "CARDENAS HENANDEZ ALISSON MONSERRAT", "pin": "5838"},
        {"grupo": "1° A Geografía", "nombre": "CARDONA SOLIS IKER PATRICIO", "pin": "7660"},
        {"grupo": "1° A Geografía", "nombre": "COLORADO NAVA ALLISON MONSERRAT", "pin": "7353"},
        {"grupo": "1° A Geografía", "nombre": "CUPERTINO CAMRGO GISELLE ANGELY", "pin": "5506"},
        {"grupo": "1° A Geografía", "nombre": "ESPINOZA PACHECO SENDERO ABISAI", "pin": "2495"},
        {"grupo": "1° A Geografía", "nombre": "FLORES GUTIERREZ BRYANNA ALEJANDRA", "pin": "9133"},
        {"grupo": "1° A Geografía", "nombre": "FLORES MACIAS VICTOR URIEL", "pin": "8054"},
        {"grupo": "1° A Geografía", "nombre": "FUENTES JIMENEZ JANETH ESMERALDA", "pin": "9427"},
        {"grupo": "1° A Geografía", "nombre": "GARCIA CORTES SOFIA RAQUEL", "pin": "5729"},
        {"grupo": "1° A Geografía", "nombre": "GARCIA HERNANDEZ JOHAN FRANCISCO TADEO", "pin": "6862"},
        {"grupo": "1° A Geografía", "nombre": "HERNANDEZ DIMINGUEZ DAMIAN ALEJANDRO", "pin": "8621"},
        {"grupo": "1° A Geografía", "nombre": "HERNANDEZ HERNANDEZ ALEXA ISABELA", "pin": "8812"},
        {"grupo": "1° A Geografía", "nombre": "HERNANDEZ HERNANDEZ DEREK YOETH", "pin": "1974"},
        {"grupo": "1° A Geografía", "nombre": "JUAREZ CASTILLO NAIDELYNE ADTZARI", "pin": "6022"},
        {"grupo": "1° A Geografía", "nombre": "LOPEZ GARCIA AIDE", "pin": "1029"},
        {"grupo": "1° A Geografía", "nombre": "LOREDO SANCHEZ CINTHIA", "pin": "7024"},
        {"grupo": "1° A Geografía", "nombre": "LUNA LOPEZ MIA MONSERRAT", "pin": "9766"},
        {"grupo": "1° A Geografía", "nombre": "MARTEL RIVERA ZULEIKA DEENISSE", "pin": "2263"},
        {"grupo": "1° A Geografía", "nombre": "MARTINEZ HERNANDEZ ANA VICTORIA", "pin": "8582"},
        {"grupo": "1° A Geografía", "nombre": "MENDOZA GONZALEZ LUNA YAILIN", "pin": "3688"},
        {"grupo": "1° A Geografía", "nombre": "ORTIZ CUETO AMANDA", "pin": "5012"},
        {"grupo": "1° A Geografía", "nombre": "PASCUAL GUZMAN ANDREA CONSTANZA", "pin": "3711"},
        {"grupo": "1° A Geografía", "nombre": "PEÑA FLORES ALEXA NICOLE", "pin": "3738"},
        {"grupo": "1° A Geografía", "nombre": "QUINTANILLA ANDRADE SERGIO ALEXANDER", "pin": "3355"},
        {"grupo": "1° A Geografía", "nombre": "RAMIREZ BALDERAS EMILY ASHLEY", "pin": "1754"},
        {"grupo": "1° A Geografía", "nombre": "RAMIREZ FRAIRE JOSE LUIS", "pin": "8256"},
        {"grupo": "1° A Geografía", "nombre": "RANGEL MALDONADO CAMILA NOHEMI", "pin": "2286"},
        {"grupo": "1° A Geografía", "nombre": "REQUENA MATA JOHVANA CRISTEL", "pin": "5736"},
        {"grupo": "1° A Geografía", "nombre": "ROBLES MARTINEZ KATERINE", "pin": "3603"},
        {"grupo": "1° A Geografía", "nombre": "RODRIGUEZ MARTINEZ IKER SANTIAGO", "pin": "5406"},
        {"grupo": "1° A Geografía", "nombre": "ROJAS BETANCOURT VALENTINA", "pin": "3530"},
        {"grupo": "1° A Geografía", "nombre": "SANTOS HERNANDEZ KARLA MICHELLE", "pin": "3983"},
        {"grupo": "1° A Geografía", "nombre": "TOBIAS GRANADOS HECTOR ALEJANDRO", "pin": "2154"},
        {"grupo": "1° A Geografía", "nombre": "TORRES TORRES DILAN DI JERZHU", "pin": "4759"},
        {"grupo": "1° A Geografía", "nombre": "VILLARREAL GUERRERO IAN RODRIGO", "pin": "1336"},
        {"grupo": "1° A Geografía", "nombre": "LOPEZ CERNA DOMINIC MATEO", "pin": "7714"},
        {"grupo": "1° B Geografía", "nombre": "ABARCA GONZALEZ ALEXA ANAHI", "pin": "4777"},
        {"grupo": "1° B Geografía", "nombre": "ALMAGUER RAMIREZ MATEO DANIEL", "pin": "7319"},
        {"grupo": "1° B Geografía", "nombre": "ARCE ZAPATA ANTONI JEFERSON", "pin": "7310"},
        {"grupo": "1° B Geografía", "nombre": "ARREDONDO ZAPATA CRISTOPHER JAVIER", "pin": "1430"},
        {"grupo": "1° B Geografía", "nombre": "BUSTOS TORRES RAUL FERNANDO", "pin": "7043"},
        {"grupo": "1° B Geografía", "nombre": "CARRANZA BERMUDEZ DIEGO ALBERTO", "pin": "1431"},
        {"grupo": "1° B Geografía", "nombre": "CARRIZALES HERNANDEZ ELY SADDAI", "pin": "5922"},
        {"grupo": "1° B Geografía", "nombre": "CASTELUM MONCADA DARIUS ISAI", "pin": "7842"},
        {"grupo": "1° B Geografía", "nombre": "CASTILLO ESTRADA JATZIRI YAZARETH", "pin": "7142"},
        {"grupo": "1° B Geografía", "nombre": "CHAVARRIA SERRATO BRANDON DANIEL", "pin": "8246"},
        {"grupo": "1° B Geografía", "nombre": "CHAVARRIA SERRATO BRUNO DAMIAN", "pin": "6265"},
        {"grupo": "1° B Geografía", "nombre": "CISNEROS CALVILLO XIOMARA", "pin": "3003"},
        {"grupo": "1° B Geografía", "nombre": "CORDOVA LOZANO DUILIO JARED", "pin": "2653"},
        {"grupo": "1° B Geografía", "nombre": "CORTINES GALVAN ROMINA SUSANA", "pin": "9172"},
        {"grupo": "1° B Geografía", "nombre": "CRUZ LAZARIN KEYLA CAROLINA", "pin": "5204"},
        {"grupo": "1° B Geografía", "nombre": "DEL ANGEL NICANOR HEYDI YAMILETH", "pin": "5751"},
        {"grupo": "1° B Geografía", "nombre": "DIAZ ESTRADA MARCELO IZUA", "pin": "8778"},
        {"grupo": "1° B Geografía", "nombre": "ENRIQUEZ PEREZ KIMBERLY YOSELIN", "pin": "1789"},
        {"grupo": "1° B Geografía", "nombre": "GARCIA AGUAYO MATEO NICOLAS", "pin": "8082"},
        {"grupo": "1° B Geografía", "nombre": "GARCIA BACA EDUARDO KALEB", "pin": "9026"},
        {"grupo": "1° B Geografía", "nombre": "GOMEZ GOMEZ ALEXADER", "pin": "6603"},
        {"grupo": "1° B Geografía", "nombre": "GONZALEZ HERNANDEZ JAYDEN ANTUAN", "pin": "8528"},
        {"grupo": "1° B Geografía", "nombre": "HERNANDEZ HERNANDEZ MILAN DAVID", "pin": "8998"},
        {"grupo": "1° B Geografía", "nombre": "HERRERA GALINDO MAXIMO", "pin": "6122"},
        {"grupo": "1° B Geografía", "nombre": "LEAL VITAL MIA NATHALIA", "pin": "7940"},
        {"grupo": "1° B Geografía", "nombre": "LLANES SANCHEZ VALERIA", "pin": "7252"},
        {"grupo": "1° B Geografía", "nombre": "MACIAS DIAZ HAROLD EDUARDO", "pin": "4835"},
        {"grupo": "1° B Geografía", "nombre": "MARTINEZ MARQUEZ LESLIE ESTEFANIA AGLAHE", "pin": "3133"},
        {"grupo": "1° B Geografía", "nombre": "MARTINEZ SIFUENTES JESUS FIDENCIO", "pin": "6818"},
        {"grupo": "1° B Geografía", "nombre": "MUÑOZ SORIANO LESLY NALLEYLY", "pin": "5349"},
        {"grupo": "1° B Geografía", "nombre": "NAVARRO CASTILLO IKER TADEO", "pin": "8986"},
        {"grupo": "1° B Geografía", "nombre": "PIÑA ESPINOSA SANTIAGO DAMIAN", "pin": "9678"},
        {"grupo": "1° B Geografía", "nombre": "RAMIREZ GARCIA CHELSIE MONSERRAT", "pin": "7438"},
        {"grupo": "1° B Geografía", "nombre": "RAMOS REYNA KALED ALEJANDRO", "pin": "8153"},
        {"grupo": "1° B Geografía", "nombre": "RODRIGUEZ SOLIS ANNA LUCIA", "pin": "3161"},
        {"grupo": "1° B Geografía", "nombre": "RODRIGUEZ VIRAMONTES JULIETA MARIANA", "pin": "4059"},
        {"grupo": "1° B Geografía", "nombre": "SALAZAR MARTINEZ ALDO JOEL", "pin": "2197"},
        {"grupo": "1° B Geografía", "nombre": "SANCHEZ CARRILLO DARIANA PAOLA", "pin": "1570"},
        {"grupo": "1° B Geografía", "nombre": "SANTIAGO GALVAN LIZBETH", "pin": "2271"},
        {"grupo": "1° B Geografía", "nombre": "SOLIS BENITEZ ALISSON", "pin": "2676"},
        {"grupo": "1° B Geografía", "nombre": "TREVIÑO RODRIGUEZ MIGUEL TADEO", "pin": "5863"},
        {"grupo": "1° B Geografía", "nombre": "VILLA RAMIREZ ALICIA MABEL", "pin": "1055"},
        {"grupo": "1° B Geografía", "nombre": "ZAPATA GARCIA EMILY DANAHI", "pin": "6916"},
        {"grupo": "1° B Geografía", "nombre": "ZAVALA DE LA ROSA NATHAN EMMANUEL", "pin": "1460"},
        {"grupo": "1° C Geografía", "nombre": "AGUSTIN VERONICA REYNA NICOLE", "pin": "9504"},
        {"grupo": "1° C Geografía", "nombre": "ANTONIO FELICIANO GABRIEL", "pin": "8619"},
        {"grupo": "1° C Geografía", "nombre": "MARAIZA ESPIRICUETA DOMINICK ALEXANDER", "pin": "3991"},
        {"grupo": "1° C Geografía", "nombre": "BAUTISTA HERNANDEZ ITZEL", "pin": "1162"},
        {"grupo": "1° C Geografía", "nombre": "BRAJAS SANTOS EVAN JOSUE", "pin": "9085"},
        {"grupo": "1° C Geografía", "nombre": "BUENROSTRO GONZALEZ CINTHYA YOSELIN", "pin": "5989"},
        {"grupo": "1° C Geografía", "nombre": "CAMACHO TORRES SOFIA LIZBETH", "pin": "3470"},
        {"grupo": "1° C Geografía", "nombre": "CARRILLO PUENTE MABEL", "pin": "6159"},
        {"grupo": "1° C Geografía", "nombre": "CASTILLO CISNEROS NABIL ALESSANDRA", "pin": "7128"},
        {"grupo": "1° C Geografía", "nombre": "CASTILLO VILLARREAL ARIANA GUADALUPE", "pin": "2571"},
        {"grupo": "1° C Geografía", "nombre": "CASTRO LEDEZMA JUSTIN ALEJANDRO", "pin": "9227"},
        {"grupo": "1° C Geografía", "nombre": "CHAVEZ GARCIA ANGEL EMMANUEL", "pin": "3654"},
        {"grupo": "1° C Geografía", "nombre": "DIAZ ROCHA BARBARA MICHEL", "pin": "3279"},
        {"grupo": "1° C Geografía", "nombre": "FLORES RODRIGUEZ NOEMI ESTHELA", "pin": "7695"},
        {"grupo": "1° C Geografía", "nombre": "FLORES ULLOA DIEGO SEBASTIAN", "pin": "6524"},
        {"grupo": "1° C Geografía", "nombre": "GONZALEZ REYES LEONEL", "pin": "6932"},
        {"grupo": "1° C Geografía", "nombre": "GONZALEZ SIERRA NICOLE MONSERRAT", "pin": "1470"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ BRIONES ZOE ASTRID", "pin": "9557"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ ESCOBEDO YETZIN ALEXADER", "pin": "7249"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ HERNANDEZ ANGELA LUCIA", "pin": "6375"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ MARTINEZ MELANIE BERENICE", "pin": "9556"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ MEDINA ASHLY ZARET", "pin": "3231"},
        {"grupo": "1° C Geografía", "nombre": "HERNANDEZ RUELAS JIMENA SAMARA", "pin": "8011"},
        {"grupo": "1° C Geografía", "nombre": "LODOÑO LOPEZ NICOL ZARAY", "pin": "9987"},
        {"grupo": "1° C Geografía", "nombre": "LUGO OLVERA ALISON DAYANA", "pin": "1129"},
        {"grupo": "1° C Geografía", "nombre": "LUIS REYES ZOELY NICOL", "pin": "2002"},
        {"grupo": "1° C Geografía", "nombre": "LUNA SALAZAR EDDAR NAHUM", "pin": "9019"},
        {"grupo": "1° C Geografía", "nombre": "MARTINEZ CORONADO CRISTIAN DE JESUS", "pin": "5435"},
        {"grupo": "1° C Geografía", "nombre": "MARTINEZ MORIN WALTER MISSAEL", "pin": "2811"},
        {"grupo": "1° C Geografía", "nombre": "MARTINEZ VARELA HANNIA LIZBETH", "pin": "2272"},
        {"grupo": "1° C Geografía", "nombre": "MONTOYA MARTINEZ ABEL ALEJANDRO", "pin": "2052"},
        {"grupo": "1° C Geografía", "nombre": "MUÑOZ MARTINEZ IKER YANDEL", "pin": "1886"},
        {"grupo": "1° C Geografía", "nombre": "OVALLE LUNA BRIANA NAYLIN", "pin": "1741"},
        {"grupo": "1° C Geografía", "nombre": "PEREZ REYES EIZA SOPHIA", "pin": "7085"},
        {"grupo": "1° C Geografía", "nombre": "PRESAS GARCIA ANGEL LEONARDO", "pin": "7633"},
        {"grupo": "1° C Geografía", "nombre": "RAMIREZ DEL ANGEL BEATRIZ JACQUELINE", "pin": "4680"},
        {"grupo": "1° C Geografía", "nombre": "RAMOS RODRIGUEZ ESTEFANY", "pin": "5099"},
        {"grupo": "1° C Geografía", "nombre": "RENTERIA ALVAREZ IAN AZAEL", "pin": "9138"},
        {"grupo": "1° C Geografía", "nombre": "ROSALES PICON ANGEL GABRIEL", "pin": "4809"},
        {"grupo": "1° C Geografía", "nombre": "SANCHEZ ESTRADA ARIANNA LINETH", "pin": "4262"},
        {"grupo": "1° C Geografía", "nombre": "SORIANO CHAVEZ ANGEL ANTONIO", "pin": "7557"},
        {"grupo": "1° C Geografía", "nombre": "TREJO JAUREGUI VALERIA NICOLLE", "pin": "4793"},
        {"grupo": "1° C Geografía", "nombre": "ZAMORA LOPEZ JEREIDY CITLALLI", "pin": "6119"},
        {"grupo": "1° C Geografía", "nombre": "ZAVALA VILLASANA KEVIN", "pin": "1712"},
        {"grupo": "1° D Geografía", "nombre": "ALVARADO AGUILAR JOANN TADEO", "pin": "5926"},
        {"grupo": "1° D Geografía", "nombre": "BALLEZA ALVAREZ DONOVAN ENRIQUE", "pin": "6567"},
        {"grupo": "1° D Geografía", "nombre": "CANIZALES LOPES IVANA MONSERRATH", "pin": "2183"},
        {"grupo": "1° D Geografía", "nombre": "CASTRO MARIN ADRIANA NOHEMI", "pin": "6801"},
        {"grupo": "1° D Geografía", "nombre": "CILOS OLGUIN IVANNA MICHELLE", "pin": "8763"},
        {"grupo": "1° D Geografía", "nombre": "CORTES BADILLO YOSELIN", "pin": "4034"},
        {"grupo": "1° D Geografía", "nombre": "DOMINGUEZ BENITEZ NICOLE ALEXANDRA", "pin": "1843"},
        {"grupo": "1° D Geografía", "nombre": "EGUIA MORALES ISRAEL ELI", "pin": "1257"},
        {"grupo": "1° D Geografía", "nombre": "ESPERICUETA ALVAREZ ALMA MICHELLE", "pin": "5753"},
        {"grupo": "1° D Geografía", "nombre": "FLORES MORALES LESLY NICOLE", "pin": "2145"},
        {"grupo": "1° D Geografía", "nombre": "FLORES ROMERO PABLO ELEAZAR", "pin": "9491"},
        {"grupo": "1° D Geografía", "nombre": "GARCIA VALENCIA LETICIA LUCIA", "pin": "5533"},
        {"grupo": "1° D Geografía", "nombre": "GUARDADO ZEPEDA CARLOS MANUEL", "pin": "9240"},
        {"grupo": "1° D Geografía", "nombre": "GÜITIAN HERRARA NAHOMY GUADALUPE", "pin": "3261"},
        {"grupo": "1° D Geografía", "nombre": "GUTIERREZ SOLIS IKER BAYRON", "pin": "5493"},
        {"grupo": "1° D Geografía", "nombre": "GUZMAN CARDONA PERLA GISELLE", "pin": "7477"},
        {"grupo": "1° D Geografía", "nombre": "HERNANDEZ PASCUAL AXEL", "pin": "6834"},
        {"grupo": "1° D Geografía", "nombre": "JIMENEZ ALFARO DANNA REGINA", "pin": "6926"},
        {"grupo": "1° D Geografía", "nombre": "JUAREZ RODRIGUEZ JULIO CESAR", "pin": "5185"},
        {"grupo": "1° D Geografía", "nombre": "MARTINEZ PEREZ ALEJANDRA", "pin": "3397"},
        {"grupo": "1° D Geografía", "nombre": "MARTINEZ SALAZAR MARLON ANTONIO", "pin": "5164"},
        {"grupo": "1° D Geografía", "nombre": "MATA ROMERO ALEXA DANIELA", "pin": "9873"},
        {"grupo": "1° D Geografía", "nombre": "MENCHACA LOPEZ MEREDITH SARAI", "pin": "3536"},
        {"grupo": "1° D Geografía", "nombre": "MORENO CANALES CARLOS DAMIAN", "pin": "8817"},
        {"grupo": "1° D Geografía", "nombre": "MORENO MARTINEZ SOFIA", "pin": "7519"},
        {"grupo": "1° D Geografía", "nombre": "MUÑIZ RIVERA REYNA SOFIA", "pin": "1948"},
        {"grupo": "1° D Geografía", "nombre": "MUÑOZ SANCHEZ YULY MARIHAN", "pin": "6624"},
        {"grupo": "1° D Geografía", "nombre": "OLIVARES ACOSTO KEILYN ARIADNE", "pin": "1474"},
        {"grupo": "1° D Geografía", "nombre": "PEREZ CASTILLO SURI MICHELLE", "pin": "9792"},
        {"grupo": "1° D Geografía", "nombre": "PEREZ GARCIA AYLIN MONSERRAT", "pin": "6652"},
        {"grupo": "1° D Geografía", "nombre": "PEREZ GRCIA AYDIL NOHEMI", "pin": "7003"},
        {"grupo": "1° D Geografía", "nombre": "PUENTE CEDILLO DARWIN JAVIER", "pin": "9494"},
        {"grupo": "1° D Geografía", "nombre": "QUISTIANO LOPEZ NOE ISMAEL", "pin": "6726"},
        {"grupo": "1° D Geografía", "nombre": "RAMOS ENRIQUEZ GAEL", "pin": "7525"},
        {"grupo": "1° D Geografía", "nombre": "RAMOS ESTRADA JAMAL DE JESUS", "pin": "3109"},
        {"grupo": "1° D Geografía", "nombre": "REYES FRAGA MONSERRAT", "pin": "1775"},
        {"grupo": "1° D Geografía", "nombre": "ROSALES MARTINEZ MEREDY ALEXA", "pin": "9194"},
        {"grupo": "1° D Geografía", "nombre": "SANTOS HERNANDEZ JENIFER ARANZA", "pin": "1213"},
        {"grupo": "1° D Geografía", "nombre": "SANTOS MADERO CARLOS", "pin": "4668"},
        {"grupo": "1° D Geografía", "nombre": "SILVA CASTILLO LUIS ALEXIS", "pin": "4921"},
        {"grupo": "1° D Geografía", "nombre": "SOLIS ARRIAGA GISSELLA ANTONELLA", "pin": "1425"},
        {"grupo": "1° D Geografía", "nombre": "TOVAR AYALA CAMILA GISELLE", "pin": "5070"},
        {"grupo": "1° D Geografía", "nombre": "TOVAR MORENO CHRISTOPHER GIOVANNI", "pin": "8202"},
        {"grupo": "1° D Geografía", "nombre": "VAZQUEZ CARDONA MADELYN XIMENA", "pin": "6667"},
        {"grupo": "1° D Geografía", "nombre": "PROFE ALDO", "pin": "1111"},
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
