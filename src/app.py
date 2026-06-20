import streamlit as st
import json
import os
from datetime import date, datetime

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'db_practicas.json')

ESTADOS_COLOR = {
    "En Revisión Administrativa": "warning",
    "Activa (En Curso)": "success",
    "Aprobación Condicional": "info",
    "Rechazada": "error",
    "Vencida": "error",
}


# ============================================================
# PERSISTENCIA
# ============================================================
def init_db():
    if not os.path.exists(DB_FILE):
        data = {
            "usuarios": {"coordinador.practicas@uct.cl": "password123"},
            "solicitudes": {}
        }
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)


def load_data():
    with open(DB_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


init_db()


# ============================================================
# REGLAS DE NEGOCIO
# ============================================================
def seguro_vencido(solicitud):
    """Regla: el seguro escolar no puede estar vencido a la fecha actual."""
    try:
        fecha_venc = datetime.strptime(solicitud["fecha_vencimiento_seguro"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return False
    return fecha_venc < date.today()


def documentos_completos(solicitud):
    """Regla: todos los documentos deben estar presentes."""
    return all(doc["presente"] for doc in solicitud["documentos"].values())


def documentos_validados(solicitud):
    """Regla: todos los documentos presentes deben haber sido marcados como válidos
    por el coordinador durante la auditoría."""
    return all(
        doc["valido"] is True
        for doc in solicitud["documentos"].values()
        if doc["presente"]
    )


def puede_aprobar_total(solicitud):
    return documentos_completos(solicitud) and documentos_validados(solicitud) and not seguro_vencido(solicitud)


# ============================================================
# CONFIGURACIÓN DE PÁGINA Y NAVEGACIÓN
# ============================================================
st.set_page_config(page_title="PMV - Grupo 30", layout="centered", initial_sidebar_state="collapsed")

# ------------------------------------------------------------
# ESTILOS PERSONALIZADOS
# ------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(180deg, #0f1226 0%, #161a35 100%);
    }

    /* Barra superior con marca */
    .topbar {
        background: linear-gradient(90deg, #6C63FF 0%, #4834D4 100%);
        padding: 1.1rem 1.6rem;
        border-radius: 14px;
        margin-bottom: 1.6rem;
        box-shadow: 0 8px 24px rgba(108, 99, 255, 0.35);
        text-align: center;
    }
    .topbar h1 {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .topbar p {
        color: rgba(255,255,255,0.85);
        margin: 0.2rem 0 0 0;
        font-size: 0.85rem;
    }

    /* Tarjetas (containers con borde) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #1d2142;
        border: 1px solid #2c3163 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 26px rgba(108, 99, 255, 0.25);
    }

    /* Texto general más claro sobre fondo oscuro */
    .stMarkdown, .stCaption, p, span, label {
        color: #E6E6F0;
    }

    /* Botones */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.15s ease;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6C63FF, #4834D4) !important;
        box-shadow: 0 4px 14px rgba(108, 99, 255, 0.4);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(108, 99, 255, 0.55);
    }
    .stButton > button:not([kind="primary"]) {
        background: #262b52 !important;
        color: #E6E6F0 !important;
        border: 1px solid #3a3f72 !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: #313773 !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background-color: #161a35 !important;
        color: #E6E6F0 !important;
        border-radius: 10px !important;
        border: 1px solid #2c3163 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #14172e;
        border-right: 1px solid #2c3163;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #F2F2FA !important;
        font-weight: 700 !important;
    }

    /* Divider */
    hr {
        border-color: #2c3163 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <h1>Sistema de Gestión de Prácticas</h1>
    <p>Grupo 30 · Filtro Administrativo · Desarrollo de Aplicaciones Empresariales</p>
</div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'solicitud_id' not in st.session_state:
    st.session_state.solicitud_id = None

if st.session_state.page != "login":
    with st.sidebar:
        st.subheader("Panel de Administración")
        st.caption("Usuario Activo: Coordinador")
        st.divider()
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.solicitud_id = None
            st.rerun()


# ============================================================
# LOGIN
# ============================================================
if st.session_state.page == "login":
    st.markdown("<p style='text-align: center; color: #B8B8D6; margin-top: -0.5rem;'>Portal de Autenticación Institucional</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            usuario = st.text_input("Nombre de Usuario (Coordinador)")
            password = st.text_input("Contraseña de Seguridad", type="password")

            st.write("")
            if st.button("Ingresar al Panel", use_container_width=True, type="primary"):
                data = load_data()
                if usuario in data["usuarios"] and data["usuarios"][usuario] == password:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Error: Credenciales incorrectas o usuario no registrado.")


# ============================================================
# DASHBOARD — LISTADO DE TODAS LAS SOLICITUDES
# ============================================================
elif st.session_state.page == "dashboard":
    st.title("Panel de Control General")
    st.markdown("### Solicitudes Registradas")
    st.write("")

    data = load_data()
    solicitudes = data["solicitudes"]

    if not solicitudes:
        st.info("No hay solicitudes registradas en el sistema.")
    else:
        for sol_id, solicitud in solicitudes.items():
            estado_actual = solicitud["estado"]
            with st.container(border=True):
                col_est, col_emp, col_estdo = st.columns([2, 2, 2])

                with col_est:
                    st.markdown("**Estudiante Postulante**")
                    st.write(solicitud["estudiante"])

                with col_emp:
                    st.markdown("**Centro de Práctica**")
                    st.write(solicitud["empresa"])

                with col_estdo:
                    st.markdown("**Estado del Proceso**")
                    tipo = ESTADOS_COLOR.get(estado_actual, "info")
                    getattr(st, tipo)(estado_actual)

                if seguro_vencido(solicitud) and estado_actual == "En Revisión Administrativa":
                    st.caption("Seguro escolar vencido — requiere atención antes de aprobar.")

                col_btn1, col_btn2 = st.columns([3, 1])
                with col_btn1:
                    if estado_actual in ("En Revisión Administrativa",):
                        if st.button("Revisar Expediente Completo", key=f"rev_{sol_id}", type="primary"):
                            st.session_state.solicitud_id = sol_id
                            st.session_state.page = "detalle"
                            st.rerun()
                    else:
                        if st.button("Ver Expediente", key=f"ver_{sol_id}"):
                            st.session_state.solicitud_id = sol_id
                            st.session_state.page = "detalle"
                            st.rerun()
                with col_btn2:
                    if st.button("Reiniciar", key=f"reset_{sol_id}", use_container_width=True):
                        for doc in data["solicitudes"][sol_id]["documentos"].values():
                            doc["valido"] = None
                        data["solicitudes"][sol_id]["estado"] = "En Revisión Administrativa"
                        save_data(data)
                        st.rerun()


# ============================================================
# EXPEDIENTE DIGITAL Y DECISIÓN
# ============================================================
elif st.session_state.page == "detalle":
    data = load_data()
    sol_id = st.session_state.solicitud_id
    solicitud = data["solicitudes"][sol_id]

    st.title("Auditoría de Expediente Digital")
    st.subheader(f"Ficha del Postulante: {solicitud['estudiante']}")
    st.caption(f"Organización Destino: {solicitud['empresa']}")
    st.caption(f"Ingreso de solicitud: {solicitud.get('fecha_ingreso', '—')}")
    st.divider()

    # --- Cambio de empresa ---
    with st.expander("Cambiar empresa / centro de práctica"):
        nueva_empresa = st.text_input("Nueva empresa", value=solicitud["empresa"], key=f"emp_{sol_id}")
        if st.button("Actualizar empresa", key=f"upd_emp_{sol_id}"):
            data["solicitudes"][sol_id]["empresa"] = nueva_empresa
            save_data(data)
            st.success("Empresa actualizada correctamente.")
            st.rerun()

    # --- Documentación legal (simulación de documentos reales) ---
    st.markdown("### Documentación Legal Adjunta")
    with st.container(border=True):
        for doc_nombre, doc_info in solicitud["documentos"].items():
            col_doc, col_estado, col_valid = st.columns([3, 2, 2])
            with col_doc:
                st.write(doc_nombre)
            with col_estado:
                if doc_info["presente"]:
                    st.caption("Adjuntado por el estudiante")
                else:
                    st.caption("No adjuntado")
            with col_valid:
                if doc_info["presente"]:
                    valido = st.checkbox(
                        "Validar documento",
                        value=bool(doc_info["valido"]),
                        key=f"valid_{sol_id}_{doc_nombre}"
                    )
                    if valido != doc_info["valido"]:
                        data["solicitudes"][sol_id]["documentos"][doc_nombre]["valido"] = valido
                        save_data(data)
                else:
                    st.write("—")

    # --- Vencimiento del seguro ---
    venc = solicitud.get("fecha_vencimiento_seguro", "—")
    if seguro_vencido(solicitud):
        st.error(f"El seguro escolar venció el {venc}. No se puede aprobar totalmente sin renovación.")
    else:
        st.caption(f"Vigencia del seguro escolar: hasta {venc}")

    # --- Observaciones ---
    st.markdown("### Observaciones del Coordinador")
    for obs in solicitud.get("observaciones", []):
        st.write(f"- {obs}")
    nueva_obs = st.text_area("Agregar observación", key=f"obs_{sol_id}", placeholder="Ej: Falta firma del representante legal de la empresa.")

    st.markdown("---")
    st.markdown("#### Resolución Administrativa")

    estado_actual = solicitud["estado"]
    if estado_actual != "En Revisión Administrativa":
        st.info(f"Este expediente ya fue resuelto. Estado actual: **{estado_actual}**")
        if st.button("Volver al Panel"):
            st.session_state.page = "dashboard"
            st.rerun()
    else:
        st.write("¿El expediente cumple a cabalidad con los requisitos institucionales y legales?")
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

        with btn_col1:
            if st.button("APROBAR", use_container_width=True, type="primary"):
                if puede_aprobar_total(solicitud):
                    data["solicitudes"][sol_id]["estado"] = "Activa (En Curso)"
                    if nueva_obs:
                        data["solicitudes"][sol_id]["observaciones"].append(nueva_obs)
                    save_data(data)
                    st.session_state.page = "exito"
                    st.rerun()
                else:
                    motivos = []
                    if not documentos_completos(solicitud):
                        motivos.append("faltan documentos por adjuntar")
                    if not documentos_validados(solicitud):
                        motivos.append("hay documentos sin validar")
                    if seguro_vencido(solicitud):
                        motivos.append("el seguro escolar está vencido")
                    st.error("No se puede aprobar de forma total: " + "; ".join(motivos) + ".")

        with btn_col2:
            if st.button("APROBACIÓN CONDICIONAL", use_container_width=True):
                if not nueva_obs:
                    st.error("Debe registrar una observación indicando la condición para la aprobación condicional.")
                else:
                    data["solicitudes"][sol_id]["estado"] = "Aprobación Condicional"
                    data["solicitudes"][sol_id]["observaciones"].append(nueva_obs)
                    save_data(data)
                    st.session_state.page = "exito"
                    st.rerun()

        with btn_col3:
            if st.button("RECHAZAR", use_container_width=True):
                data["solicitudes"][sol_id]["estado"] = "Rechazada"
                if nueva_obs:
                    data["solicitudes"][sol_id]["observaciones"].append(nueva_obs)
                save_data(data)
                st.session_state.page = "error"
                st.rerun()

        with btn_col4:
            if st.button("Volver al Panel", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()


# ============================================================
# RESULTADOS
# ============================================================
elif st.session_state.page == "exito":
    data = load_data()
    solicitud = data["solicitudes"][st.session_state.solicitud_id]

    st.success("Filtro Administrativo Completado Exitosamente")
    with st.container(border=True):
        st.markdown(f"Nuevo Estado Técnico de la Entidad: **{solicitud['estado']}**")
        if solicitud["observaciones"]:
            st.markdown("**Última observación registrada:**")
            st.write(solicitud["observaciones"][-1])
        st.markdown("### Efectos Automatizados en el Sistema:")
        st.write("1. Notificación de activación despachada al correo institucional del alumno.")
        st.write("2. Creación formal del registro de seguimiento semanal y habilitación de bitácoras.")

    st.write("")
    if st.button("Volver al Dashboard Administrativo", type="primary"):
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "error":
    st.error("Excepción Activada: Solicitud Rechazada")
    with st.container(border=True):
        st.write("El expediente ha sido devuelto automáticamente al buzón del alumno.")
        st.write("Se ha generado un requerimiento para corregir los documentos observados.")

    st.write("")
    if st.button("Volver al Dashboard Administrativo", type="primary"):
        st.session_state.page = "dashboard"
        st.rerun()