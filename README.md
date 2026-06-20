# Sistema de Gestión de Prácticas Empresariales

**Grupo 30 · Filtro Administrativo · Desarrollo de Aplicaciones Empresariales**

Sistema interactivo para gestionar y auditar solicitudes de prácticas empresariales de estudiantes. Permite validar documentación, verificar vigencia de seguros y ejecutar el filtro administrativo requerido antes de activar una práctica.

---

## Inicio Rápido

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el repositorio**
   ```bash
   cd D.APLICACIONES.EMPRESARIALES
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run src/app.py
   ```

4. **Acceder a la aplicación**
   ```
   Local URL: http://localhost:8501
   ```

---

## Descripción General

La aplicación implementa un **filtro administrativo digital** para validar que las solicitudes de práctica cumplan con los requisitos institucionales antes de activarlas. El coordinador de prácticas puede:

- Revisar expedientes digitales completos
- Validar documentación requerida (seguro escolar, convenios, etc.)
- Verificar vigencia del seguro escolar
- Tomar decisiones administrativas (aprobar, rechazar, aprobación condicional)
- Registrar observaciones y motivos de las decisiones

---

## Autenticación

**Usuario de prueba:**
- **Email/Usuario:** `coordinador.practicas@uct.cl`
- **Contraseña:** `password123`

---

## Funcionalidades Principales

### 1. **Panel de Autenticación**
- Login seguro con credenciales de coordinador
- Gestión de sesiones

### 2. **Dashboard General**
- Listado de todas las solicitudes registradas
- Visualización rápida del estado de cada expediente
- Indicadores de alertas (seguro vencido, documentos faltantes)
- Acceso rápido a expedientes en revisión

### 3. **Auditoría de Expedientes**
- **Información del postulante:** Nombre del estudiante, empresa destino, fecha de ingreso
- **Validación de documentos:** 
  - Seguro Escolar Vigente
  - Convenio Firmado
  - Estado de presencia y validez de cada documento
- **Vigencia del seguro:** Visualización de fecha de vencimiento con alertas automáticas
- **Cambio de empresa:** Permite actualizar el centro de práctica si es necesario
- **Observaciones:** El coordinador puede registrar comentarios y motivos

### 4. **Resolución Administrativa**
Cuatro opciones de decisión:

| Decisión | Descripción | Requisitos |
|----------|-------------|-----------|
| **APROBAR** | Activa la práctica en el sistema | Documentos completos, validados y seguro vigente |
| **APROBACIÓN CONDICIONAL** | Activación con condiciones pendientes | Requiere observación explicando la condición |
| **RECHAZAR** | Devuelve la solicitud para correcciones | Genera requerimiento automático |
| **Volver** | Regresa al panel sin cambios | Sin requisitos |

### 5. **Reglas de Negocio Automáticas**

El sistema valida automáticamente:

- ✅ **Seguro escolar no vencido** → Fecha de vencimiento mayor a hoy
- ✅ **Documentos completos** → Todos los documentos deben estar adjuntados
- ✅ **Documentos validados** → Todos los presentes deben estar marcados como válidos por el coordinador

---

## Estructura del Proyecto

```
D.APLICACIONES.EMPRESARIALES/
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias del proyecto
├── data/
│   └── db_practicas.json         # Base de datos JSON (persistencia)
└── src/
    └── app.py                    # Aplicación principal (Streamlit)
```

### Descripción de archivos

- **`app.py`**: Código principal con toda la lógica de la aplicación
- **`db_practicas.json`**: Base de datos que almacena usuarios y solicitudes
- **`requirements.txt`**: Lista de librerías necesarias para ejecutar el proyecto

---

## 🛠️ Tecnologías Utilizadas

- **Streamlit** (≥1.30.0) - Framework para aplicaciones web interactivas
- **Python 3** - Lenguaje de programación
- **JSON** - Formato de almacenamiento de datos

---

## Estados de una Solicitud

```
En Revisión Administrativa
         ↓
    [AUDITORÍA]
    ↙        ↓        ↘
Activa  Condicional  Rechazada
(En Curso)
```

| Estado | Color | Significado |
|--------|-------|------------|
| En Revisión Administrativa | 🟡 Amarillo | Pendiente de auditoría |
| Activa (En Curso) | 🟢 Verde | Práctica activada |
| Aprobación Condicional | 🔵 Azul | Activada con condiciones |
| Rechazada | 🔴 Rojo | Requiere correcciones |

---

## Persistencia de Datos

La aplicación utiliza un archivo JSON como base de datos:

```json
{
  "usuarios": {
    "coordinador.practicas@uct.cl": "password123"
  },
  "solicitudes": {
    "1": {
      "estudiante": "Nombre del Estudiante",
      "empresa": "Nombre de la Empresa",
      "estado": "En Revisión Administrativa",
      "fecha_ingreso": "2026-06-10",
      "fecha_vencimiento_seguro": "2026-12-31",
      "documentos": {
        "Seguro_Escolar_Vigente.pdf": {"presente": true, "valido": null},
        "Convenio_Firmado.pdf": {"presente": false, "valido": null}
      },
      "observaciones": []
    }
  }
}
```

---

## Interfaz de Usuario

La aplicación cuenta con:
- **Diseño oscuro moderno** con gradientes en púrpura y azul
- **Responsive design** optimizado para navegadores web
- **Tipografía elegante** con fuente Poppins
- **Componentes interactivos** intuitivos y accesibles

---

## Flujo de Uso Típico

1. **Login** → Ingresa credenciales del coordinador
2. **Dashboard** → Visualiza lista de solicitudes
3. **Selecciona** → Click en "Revisar Expediente Completo"
4. **Audita** → Valida documentos y revisa información
5. **Decide** → Elige una opción de resolución
6. **Confirma** → El sistema registra la decisión y notifica

---

## Notas Técnicas

- La aplicación reinicia automáticamente cuando hay cambios en los datos
- Las validaciones de documentos se guardan en tiempo real
- El estado se sincroniza entre sesiones mediante el archivo JSON
- Cada solicitud puede ser reiniciada desde el dashboard

---

## Autor

**Grupo 30 - Asignatura: Desarrollo de Aplicaciones Empresariales**

---

## Licencia

Proyecto educativo - Universidad Católica de Temuco


