# Sistema de Gestión para Clínica Veterinaria

Este proyecto es un sistema web desarrollado en Python (Flask) para la gestión integral de una clínica veterinaria. Permite organizar citas, registrar clientes y mascotas, gestionar servicios médicos y de estética, llevar el historial clínico y controlar los roles del personal.

---

## Características Principales

- **Gestión de clientes y mascotas:** Registro, consulta y edición de datos.
- **Agenda de citas:** Agendamiento, modificación y cancelación de citas médicas y servicios directos.
- **Historial clínico:** Registro y consulta de observaciones clínicas por mascota.
- **Gestión de servicios:** Registro de servicios médicos y de estética (baño, corte, etc.).
- **Gestión de usuarios y roles:** Administrador, recepcionista, veterinario y personal auxiliar.
- **Reportes básicos y facturación manual.**

---

## Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- SQLite (por defecto) o MySQL (opcional)
- Navegador web moderno

---

## Instalación y Ejecución

1. **Descarga o clona este repositorio.**

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos:**
   - Por defecto, el sistema usa SQLite. Si deseas usar MySQL, ajusta la cadena de conexión en `app/__init__.py`.

4. **Realiza las migraciones de la base de datos:**
   ```bash
   flask db upgrade
   ```

5. **Ejecuta la aplicación:**
   ```bash
   flask run
   ```

6. **Accede al sistema:**
   - Abre tu navegador y ve a [http://localhost:5000](http://localhost:5000)

---

## Estructura del Proyecto

- `app/` - Código principal de la aplicación (modelos, rutas, plantillas, etc.)
- `migrations/` - Archivos de migración de la base de datos
- `requirements.txt` - Lista de dependencias de Python
- `README.md` - Este archivo

---

## Notas

- El sistema está pensado para uso en red local, pero puede adaptarse para despliegue en la nube.
- Para soporte o dudas, consulta la documentación interna o contacta al desarrollador original.
- Puedes ampliar el sistema agregando módulos de inventario, facturación electrónica o portal para clientes en el futuro.

---

**¡Gracias por usar este sistema!**