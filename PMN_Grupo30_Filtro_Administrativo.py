import streamlit as st
import json
import os

DB_FILE = 'db_practicas.json'

# INICIALIZACIÓN DE LA BASE DE DATOS
def init_db():
    if not os.path.exists(DB_FILE):
        data = {
            "usuarios": {
                "coordinador.practicas@uct.cl": "password123"
            },
            "solicitudes": {
                "1": {
                    "estudiante": "Vicente Budini",
                    "empresa": "Sistemas Temuco SpA",
                    "estado": "En Revisión Administrativa"
                }
            }
        }
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)

# FUNCIONES DE LECTURA Y ESCRITURA
def load_data():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Ejecutamos la inicialización
init_db()

# Configuración de Identidad Visual
st.set_page_config(page_title="PMV - Grupo 30", layout="centered", initial_sidebar_state="collapsed")

# Control de navegación
if 'page' not in st.session_state:
    st.session_state.page = "login"
    
if st.session_state.page != "login":
    with st.sidebar:
        st.subheader("Panel de Administración")
        st.caption("Usuario Activo: Coordinador")
        st.divider()
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


# ACCESO AL SISTEMA (LOGIN REAL) 
if st.session_state.page == "login":
    st.markdown("<h2 style='text-align: center;'>Sistema de Gestión de Prácticas</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Portal de Autenticación Institucional</p>", unsafe_allow_html=True)
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


# DASHBOARD DEL COORDINADOR
elif st.session_state.page == "dashboard":
    st.title("Panel de Control General")
    st.markdown("### Solicitudes Pendientes de Filtro Administrativo")
    st.write("")
    
    data = load_data()
    solicitud = data["solicitudes"]["1"]
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
            if estado_actual == "En Revisión Administrativa":
                st.warning(estado_actual)
            elif estado_actual == "Activa (En Curso)":
                st.success(estado_actual)
            else:
                st.error(estado_actual)
                
        st.divider()
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            if estado_actual == "En Revisión Administrativa":
                if st.button("Revisar Expediente Completo", type="primary"):
                    st.session_state.page = "detalle"
                    st.rerun()
            else:
                st.info("El expediente ya ha sido procesado por administración.")
                
        with col_btn2:
            if st.button("Reiniciar Prueba", use_container_width=True):
                data["solicitudes"]["1"]["estado"] = "En Revisión Administrativa"
                save_data(data)
                st.rerun()


# EXPEDIENTE DIGITAL Y DECISIÓN
elif st.session_state.page == "detalle":
    st.title("Auditoría de Expediente Digital")
    
    data = load_data()
    solicitud = data["solicitudes"]["1"]
    
    st.subheader(f"Ficha del Postulante: {solicitud['estudiante']}")
    st.caption(f"Organización Destino: {solicitud['empresa']}")
    st.divider()
    
    st.markdown("### Documentación Legal Adjunta")
    with st.container(border=True):
        st.write("Por favor, verifique la validez e integridad de los archivos PDF:")
        seguro_ok = st.checkbox("Seguro_Escolar_Vigente_Vicente.pdf")
        convenio_ok = st.checkbox("Convenio_UCT_Firmado_SistemasTemuco.pdf")
    
    st.markdown("---")
    st.markdown("#### Resolución Administrativa")
    st.write("¿El expediente cumple a cabalidad con los requisitos institucionales y legales?")
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("APROBAR SOLICITUD", use_container_width=True, type="primary"):
            if seguro_ok and convenio_ok:
                data["solicitudes"]["1"]["estado"] = "Activa (En Curso)"
                save_data(data)
                st.session_state.page = "exito"
                st.rerun()
            else:
                st.error("Error Operacional: Debe auditar y marcar ambos documentos como válidos antes de aprobar.")
                
    with btn_col2:
        if st.button("RECHAZAR SOLICITUD", use_container_width=True):
            data["solicitudes"]["1"]["estado"] = "Rechazada (Documentación Inválida)"
            save_data(data)
            st.session_state.page = "error"
            st.rerun()

    with btn_col3:
        if st.button("Volver al Panel", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "exito":
    st.success("Filtro Administrativo Completado Exitosamente")
    
    data = load_data()
    with st.container(border=True):
        st.markdown(f"Nuevo Estado Técnico de la Entidad: **{data['solicitudes']['1']['estado']}**")
        st.markdown("### Efectos Automatizados en el Sistema:")
        st.write("1. Notificación de activación despachada al correo institucional del alumno.")
        st.write("2. Creación formal del registro de seguimiento semanal y habilitación de bitácoras.")
        
    st.write("")
    if st.button("Volver al Dashboard Administrativo", type="primary"):
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "error":
    st.error("Excepción Activada: Documentación Incompleta o Inválida")
    
    with st.container(border=True):
        st.write("El expediente ha sido devuelto automáticamente al buzón del alumno.")
        st.write("Se ha generado un requerimiento para corregir los documentos observados.")
        
    st.write("")
    if st.button("Volver al Dashboard Administrativo", type="primary"):
        st.session_state.page = "dashboard"
        st.rerun()