# 🚀 WhatsApp 100-Day Scheduler (Argentina Time)

Un script de automatización robusto en **Python** diseñado para enviar una secuencia de 100 mensajes personalizados a través de **WhatsApp Web**. Optimizado para ejecuciones prolongadas, garantizando precisión horaria y continuidad tras reinicios del sistema.

---

## 📝 Descripción

Este bot permite programar el envío de un mensaje diario (extraído de una lista de 100) a un número específico. Está diseñado pensando en la **resiliencia**: si la computadora se apaga o el script se detiene, el sistema guarda el progreso en un archivo local para retomar exactamente donde quedó, evitando repetir mensajes.

---

## ✨ Características Principales

* **📅 Ciclo de 100 Días:** Envía un mensaje diferente cada día de forma secuencial.
* **⏰ Horario Fijo (ART):** Programado para las **16:44 (4:44 PM)** en la zona horaria de **Argentina**, sin importar la configuración de hora de tu sistema local.
* **💾 Persistencia de Datos:** Utiliza un archivo `progreso.txt` para registrar el índice del último mensaje enviado.
* **🌐 Gestión de Recursos:** Cierra automáticamente la pestaña del navegador tras el envío para ahorrar memoria RAM.
* **🛡️ Manejo de Errores:** Control de excepciones para archivos JSON corruptos o fallos de conexión.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener:

1.  **Python 3.8+** instalado.
2.  **Google Chrome** (o tu navegador predeterminado) con la sesión de **WhatsApp Web** ya iniciada.
3.  Instalar las dependencias necesarias:

```bash
pip install pywhatkit pytz