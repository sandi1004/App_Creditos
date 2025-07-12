# 💼 Registro de Créditos

Este proyecto es una aplicación web sencilla hecha con Flask y SQLite, pensada para registrar, consultar y administrar créditos otorgados a diferentes clientes. Incluye formularios con validaciones, mensajes dinámicos, paginación y una gráfica para visualizar los datos de forma clara.

---

## ✅ Requisitos

- Python 3.13.5
- Flask

---

## ⚙️ Instalación

1. **Clonar el proyecto**

2. **Crear y activar un entorno virtual:**

```bash
python -m venv venv
# Activar en Windows
venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install flask
```

---

## 🚀 Ejecución

Inicia la aplicación con el siguiente comando:

```bash
python app.py
```

Luego abre tu navegador y accede a:

```
http://localhost:5000
```

---

## 📌 Funcionalidades

- Registro de nuevos créditos mediante formularios con validación.
- Edición y eliminación de créditos desde una tabla interactiva.
- Alertas informativas con Bootstrap.
- Gráfico de distribución de créditos por cliente o por rango de monto.
- Paginación simple con JavaScript.
- Interfaz clara, profesional y responsiva.

---

## 🗂️ Estructura del Proyecto

```
/registro-creditos/
│
├── app.py                 # Lógica principal de la app Flask
├── db.py                  # Base de datos SQLite
│
├── /templates/
│   └── index.html         # Vista principal
│ 
├── /venv/
│ 
│ 
├── /static/
│   ├── styles.css         # Estilos personalizados
│   └── chart.js           # Lógica de gráfica con Chart.js
```

---

## 📊 Tecnologías Usadas

- Flask
- SQLite
- Bootstrap 5
- Chart.js
- HTML5 / CSS3 / JavaScript

---
