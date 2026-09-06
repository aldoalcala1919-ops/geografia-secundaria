import streamlit as st
import pandas as pd
import json
import os
import re
from datetime import date
from google import genai
from google.genai import types

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Geografía 1.º - Portal Escolar",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURACIÓN DE GEMINI API ---
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=gemini_key) if gemini_key else None

# --- PERSISTENCIA ROBUSTA EN JSON ---
DB_FILE = "school_database.json"

def cargar_datos_persistidos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"actividades": [], "entregas": {}, "asistencias": {}}

def guardar_datos_persistidos(actividades, entregas, asistencias=None):
    if asistencias is None:
        asistencias = {}
    data = {"actividades": actividades, "entregas": entregas, "asistencias": asistencias}
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error al guardar datos: {e}")

stored_data = cargar_datos_persistidos()
if 'actividades' not in st.session_state:
    st.session_state.actividades = stored_data.get("actividades", [])

if 'entregas_alumnos' not in st.session_state:
    st.session_state.entregas_alumnos = stored_data.get("entregas", {})

if 'asistencias_alumnos' not in st.session_state:
    # Estructura: {"Nombre Alumno": {"YYYY-MM-DD": "Justificante"}}
    st.session_state.asistencias_alumnos = stored_data.get("asistencias", {})

# --- ESTILOS VISUALES ADAPTADOS A MÓVIL ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #f8f9fa; }
    .card-modern {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        border: 1px solid #eaeaea;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        background-color: #1d3557;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #457b9d;
        color: white;
        box-shadow: 0 4px 12px rgba(29, 53, 87, 0.2);
    }
    h1, h2, h3 {
        color: #1d3557;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE ALUMNOS ---
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
        {"grupo": "PROFE", "nombre": "PROFE ALDO", "pin": "1111"}
    ]

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("🌍 Navegación")
modo = st.sidebar.radio("Selecciona el portal:", ["Portal Familiar / Alumno", "Panel Docente (Profesor)"])


# ==========================================
# 1. PORTAL FAMILIAR / ALUMNO
# ==========================================
if modo == "Portal Familiar / Alumno":
    st.title("🎒 Portal Académico - Geografía 1°")
    st.markdown("Consulta tus calificaciones, avances, insignias y sube tus actividades de forma individual.")

    st.markdown('<div class="card-modern">', unsafe_allow_html=True)
    col1, _ = st.columns([2, 1])
    with col1:
        st.subheader("🔑 Acceso al Expediente")
        grupo_sel = st.selectbox("Selecciona tu Grupo:", ["", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
        pin_ingresado = st.text_input("Ingresa tu PIN de 4 dígitos:", type="password")
        btn_entrar = st.button("Desbloquear Expediente", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

        current_data = cargar_datos_persistidos()
        st.session_state.actividades = current_data.get("actividades", [])
        st.session_state.entregas_alumnos = current_data.get("entregas", {})
        st.session_state.asistencias_alumnos = current_data.get("asistencias", {})

        if nombre_actual not in st.session_state.entregas_alumnos:
            st.session_state.entregas_alumnos[nombre_actual] = {}

        # --- SECCIÓN DE PROGRESO E INSIGNIAS ---
        st.subheader("🏆 Tu Progreso e Insignias")
        
        acts_totales = len([a for a in st.session_state.actividades if a['activa']])
        entregadas_count = len(st.session_state.entregas_alumnos[nombre_actual])
        progreso_porcentaje = int((entregadas_count / acts_totales * 100)) if acts_totales > 0 else 0
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Progreso del Curso", f"{progreso_porcentaje}%")
        col_m2.metric("Entregadas", f"{entregadas_count} / {acts_totales}")

        st.markdown("#### Colección de Insignias")
        st.markdown("""
        <div class="card-modern">
            <p>🗺️ <b>Explorador Inicial:</b> <span style="color: green;">Activo en plataforma</span></p>
            <p>🔥 <b>Racha de Puntualidad:</b> <span>En progreso</span></p>
            <p>✍️ <b>Pluma Escolar:</b> <span style="color: gray;">Sin asignar</span></p>
            <p>🔒 <b>Nivel 2:</b> <span style="color: gray;">Bloqueado</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        tab_tareas, tab_redacciones, tab_asistencia, tab_proyectos = st.tabs(["📚 Tareas", "✍️ Redacciones", "📅 Asistencia", "🧪 Proyectos"])

        def mostrar_seccion_actividades(tipo_filtro):
            acts = [a for a in st.session_state.actividades if a['tipo'] == tipo_filtro]
            
            if not acts:
                st.info(f"No hay {tipo_filtro.lower()}s registradas o activas por el momento.")
                return

            for t in acts:
                st.markdown('<div class="card-modern">', unsafe_allow_html=True)
                st.markdown(f"### 📌 {t['titulo']}")
                estado_txt = "🟢 Abierta para entrega" if t['activa'] else "🔴 Cerrada"
                st.write(f"**Estatus:** {estado_txt}")

                entrega_actual = st.session_state.entregas_alumnos[nombre_actual].get(t['id'], {})
                
                if entrega_actual.get('calificacion') is not None:
                    st.markdown("---")
                    st.markdown("#### 📋 Reporte de Evaluación IA")
                    df_eval = pd.DataFrame([{
                        "Actividad": t['titulo'],
                        "Calificación": f"{entrega_actual['calificacion']} / 10",
                        "Retroalimentación": entrega_actual.get('revision', 'Sin comentarios')
                    }])
                    st.dataframe(df_eval, use_container_width=True, hide_index=True)
                elif entrega_actual.get('revision'):
                    st.info(f"**Estatus de revisión:** {entrega_actual['revision']}")
                
                if entrega_actual.get('archivo'):
                    st.write(f"📄 **Archivo entregado:** `{entrega_actual['archivo']}`")

                if t['activa']:
                    st.markdown("---")
                    st.markdown("#### 📂 Subir archivo para esta actividad")
                    
                    archivo_subido = st.file_uploader(
                        f"Selecciona tu archivo para: {t['titulo']}", 
                        type=["pdf", "png", "jpg", "jpeg", "txt", "docx"], 
                        key=f"upload_independiente_{t['id']}"
                    )
                    
                    if archivo_subido is not None:
                        if st.button(f"🚀 Enviar tarea: {t['titulo']}", key=f"btn_enviar_indiv_{t['id']}"):
                            st.session_state.entregas_alumnos[nombre_actual][t['id']] = {
                                "archivo": archivo_subido.name,
                                "contenido_bytes": list(archivo_subido.getvalue()),
                                "tipo_archivo": archivo_subido.type,
                                "revision": "Entregado correctamente, pendiente de revisión.",
                                "calificacion": None
                            }
                            guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                            st.success(f"¡Actividad '{t['titulo']}' enviada con éxito!")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        with tab_tareas:
            mostrar_seccion_actividades("Tarea")

        with tab_redacciones:
            mostrar_seccion_actividades("Redaccion")

        with tab_asistencia:
            st.markdown("### Historial de Asistencia y Justificantes")
            st.markdown("""
            <div class="card-modern">
                <p>✅ <b>Asistencias a tiempo:</b> Registradas</p>
                <p>⚠️ <b>Retardos:</b> Registrados</p>
                <p>📝 <b>Justificantes:</b> Válidos (Aplicados por docente)</p>
                <p>❌ <b>Faltas:</b> Registradas</p>
                <hr>
                <p style="color: #1d3557;"><b>Estatus:</b> Tu récord se actualiza conforme el profesor registra asistencia o justificantes históricos.</p>
            </div>
            """, unsafe_allow_html=True)

        with tab_proyectos:
            mostrar_seccion_actividades("Proyecto")


# ==========================================
# 2. PANEL DOCENTE (PROFESOR)
# ==========================================
elif modo == "Panel Docente (Profesor)":
    st.title("🛠️ Panel de Administración Docente")
    
    st.markdown('<div class="card-modern">', unsafe_allow_html=True)
    clave_profe = st.text_input("Ingrese Clave Maestra de Docente:", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    if clave_profe == "1111" or clave_profe == "1234":
        st.success("Acceso concedido al Panel de Control.")
        st.markdown("---")

        current_data = cargar_datos_persistidos()
        st.session_state.actividades = current_data.get("actividades", [])
        st.session_state.entregas_alumnos = current_data.get("entregas", {})
        st.session_state.asistencias_alumnos = current_data.get("asistencias", {})

        doc_tab1, doc_tab2, doc_tab3, doc_tab4 = st.tabs(["📝 Actividades", "🤖 Revisión IA", "📅 Asistencia / Justificantes", "📊 Reportes"])

        with doc_tab1:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("Crear y Administrar Actividades")
            with st.form("nueva_actividad"):
                nuevo_titulo = st.text_input("Título de la Actividad / Tarea / Proyecto")
                nuevo_tipo = st.selectbox("Tipo de Actividad", ["Tarea", "Redaccion", "Proyecto"])
                grupo_destino = st.selectbox("Grupo Destino", ["Todos", "1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"])
                btn_crear = st.form_submit_button("Crear Actividad")
                
                if btn_crear and nuevo_titulo:
                    nuevo_id = f"act_{len(st.session_state.actividades) + 1}"
                    st.session_state.actividades.append({"id": nuevo_id, "titulo": nuevo_titulo, "tipo": nuevo_tipo, "activa": True, "grupo": grupo_destino})
                    
                    guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                    st.success(f"¡Actividad '{nuevo_titulo}' creada y sincronizada con éxito!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("Listado de Actividades Actuales")
            
            for idx, act in enumerate(list(st.session_state.actividades)):
                st.markdown('<div class="card-modern">', unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"**{act['titulo']}** ({act['tipo']} - {act['grupo']})")
                with col_b:
                    nuevo_estado = st.toggle("Activa", value=act['activa'], key=f"toggle_{act['id']}_{idx}")
                    if nuevo_estado != act['activa']:
                        st.session_state.actividades[idx]['activa'] = nuevo_estado
                        guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                with col_c:
                    if st.button("🗑️", key=f"del_{act['id']}_{idx}"):
                        st.session_state.actividades.pop(idx)
                        guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                        st.success("Actividad eliminada.")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        with doc_tab2:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("🤖 Asistente de Revisión Inteligente")
            st.markdown("Revisión directa, concisa y general de las actividades mediante IA.")
            
            if not client:
                st.warning("⚠️ La API de Gemini no está configurada. Añade tu `GEMINI_API_KEY` en los secrets.")
            else:
                 alumnos_con_entregas = [a['nombre'] for a in st.session_state.alumnos if a['nombre'] in st.session_state.entregas_alumnos and st.session_state.entregas_alumnos[a['nombre']]]
                 if alumnos_con_entregas:
                     alumno_sel_rev = st.selectbox("Selecciona Alumno a Revisar:", alumnos_con_entregas)
                     acts_alumno = list(st.session_state.entregas_alumnos[alumno_sel_rev].keys())
                     act_sel_id = st.selectbox("Selecciona Actividad Entregada:", acts_alumno)
                     
                     entrega_data = st.session_state.entregas_alumnos[alumno_sel_rev][act_sel_id]
                     st.write(f"**Archivo entregado:** {entrega_data['archivo']}")
                     
                     if st.button("✨ Generar Revisión Directa con IA"):
                         with st.spinner("Analizando entrega..."):
                             try:
                                 prompt_ia = (
                                     "Actúa como profesor de geografía de secundaria. "
                                     "Revisa la entrega de forma directa, general y breve (máximo dos oraciones de comentario). "
                                     "Obligatoriamente debes incluir al final una calificación numérica exacta del 0 al 10 con este formato exacto: "
                                     "Calificación: X.X"
                                 )
                                 
                                 contents = [prompt_ia]
                                 if entrega_data.get('contenido_bytes'):
                                     byte_data = bytes(entrega_data['contenido_bytes'])
                                     contents.append(
                                         types.Part.from_bytes(
                                             data=byte_data,
                                             mime_type=entrega_data['tipo_archivo'],
                                         )
                                     )
                                 
                                 response = client.models.generate_content(
                                     model='gemini-3.6-flash',
                                     contents=contents,
                                 )
                                 
                                 texto_respuesta = response.text
                                 match_cal = re.search(r"Calificaci[oó]n:\s*([0-9]+(?:\.[0-9]+)?)", texto_respuesta, re.IGNORECASE)
                                 calif_extraida = float(match_cal.group(1)) if match_cal else 8.0
                                 
                                 st.success("¡Análisis completado!")
                                 st.write(texto_respuesta)
                                 
                                 st.session_state.entregas_alumnos[alumno_sel_rev][act_sel_id]['revision'] = texto_respuesta
                                 st.session_state.entregas_alumnos[alumno_sel_rev][act_sel_id]['calificacion'] = calif_extraida
                                 guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                             except Exception as e:
                                 st.error(f"Error al procesar con IA: {e}")
                 else:
                     st.info("Aún no hay alumnos con entregas de archivos registradas.")
            st.markdown('</div>', unsafe_allow_html=True)

        with doc_tab3:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("📅 Control de Asistencia y Justificantes Históricos")
            st.markdown("Aquí puedes pasar lista del día o **justificar faltas de semanas anteriores** seleccionando la fecha correspondiente.")
            
            # Selector de fecha para pase o justificación retroactiva
            fecha_asistencia = st.date_input("Fecha a registrar / justificar:", value=date.today())
            fecha_str = fecha_asistencia.strftime("%Y-%m-%d")
            
            grupo_asistencia = st.selectbox("Seleccione grupo:", ["1° A Geografía", "1° B Geografía", "1° C Geografía", "1° D Geografía"], key="sel_asist_grupo_hist")
            
            alumnos_grupo = [a for a in st.session_state.alumnos if a['grupo'] == grupo_asistencia]
            st.markdown(f"**Registrando para la fecha:** `{fecha_str}` ({len(alumnos_grupo)} alumnos)")
            st.markdown("---")
            
            with st.form("form_pase_lista_historica"):
                for idx, alu in enumerate(alumnos_grupo):
                    col_n, col_s = st.columns([3, 2])
                    with col_n:
                        st.write(f"**{alu['nombre']}**")
                    with col_s:
                        # Recuperar estatus previo si ya existe para esa fecha
                        alu_asist_dict = st.session_state.asistencias_alumnos.get(alu['nombre'], {})
                        estatus_previo = alu_asist_dict.get(fecha_str, "Asistencia")
                        opciones_estatus = ["Asistencia", "Retardo", "Justificante", "Falta"]
                        idx_def = opciones_estatus.index(estatus_previo) if estatus_previo in opciones_estatus else 0
                        
                        st.selectbox(
                            "Estatus", 
                            opciones_estatus, 
                            index=idx_def,
                            key=f"asis_hist_{grupo_asistencia}_{idx}", 
                            label_visibility="collapsed"
                        )
                
                if st.form_submit_button("💾 Guardar Récord de Asistencia y Justificantes"):
                    # Guardar en el estado de sesión y persistir en JSON
                    for idx, alu in enumerate(alumnos_grupo):
                        estatus_elegido = st.session_state[f"asis_hist_{grupo_asistencia}_{idx}"]
                        if alu['nombre'] not in st.session_state.asistencias_alumnos:
                            st.session_state.asistencias_alumnos[alu['nombre']] = {}
                        st.session_state.asistencias_alumnos[alu['nombre']][fecha_str] = estatus_elegido
                    
                    guardar_datos_persistidos(st.session_state.actividades, st.session_state.entregas_alumnos, st.session_state.asistencias_alumnos)
                    st.success(f"¡Récord de asistencia actualizado correctamente para el {fecha_str}!")
            st.markdown('</div>', unsafe_allow_html=True)

        with doc_tab4:
            st.markdown('<div class="card-modern">', unsafe_allow_html=True)
            st.subheader("Sábana General de Calificaciones y Avances")
            df_resumen = pd.DataFrame([
                {"Grupo": "1° A", "Alumnos Inscritos": 45, "Promedio General": 0.0},
                {"Grupo": "1° B", "Alumnos Inscritos": 46, "Promedio General": 0.0},
                {"Grupo": "1° C", "Alumnos Inscritos": 44, "Promedio General": 0.0},
                {"Grupo": "1° D", "Alumnos Inscritos": 43, "Promedio General": 0.0}
            ])
            st.dataframe(df_resumen, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif clave_profe != "":
        st.error("Clave incorrecta.")
