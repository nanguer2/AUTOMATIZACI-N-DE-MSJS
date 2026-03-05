import json
import os
import time
from datetime import datetime
import pytz
import pywhatkit

# --- CONFIGURACIÓN ---
ARCHIVO_JSON = 'mensajes.json'
ARCHIVO_PROGRESO = 'progreso.txt'
ZONA_HORARIA = pytz.timezone('America/Argentina/Buenos_Aires')
HORA_ENVIO = 16
MINUTO_ENVIO = 44

# --- FUNCIONES DE PERSISTENCIA Y CARGA ---

def cargar_mensajes():
    """Lee el archivo JSON. Si no existe, lo crea vacío."""
    if not os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[ERROR] No se pudo leer el JSON: {e}")
        return []

def guardar_mensajes(lista):
    """Guarda la lista de mensajes en el JSON con formato legible."""
    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def obtener_progreso():
    """Lee el índice del último mensaje enviado."""
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, 'r') as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def guardar_progreso(indice):
    """Guarda el índice actual para persistencia."""
    with open(ARCHIVO_PROGRESO, 'w') as f:
        f.write(str(indice))

# --- FUNCIONES DE GESTIÓN (ABM) ---

def gestionar_mensajes():
    """Menú para insertar y eliminar mensajes."""
    while True:
        mensajes = cargar_mensajes()
        progreso = obtener_progreso()
        
        print(f"\n--- GESTOR DE MENSAJES (Total: {len(mensajes)} | Enviados: {progreso}) ---")
        print("1. Ver lista de mensajes")
        print("2. Agregar nuevo mensaje (al final)")
        print("3. Eliminar un mensaje")
        print("4. Volver al menú principal")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            if not mensajes: print("La lista está vacía.")
            for i, msg in enumerate(mensajes):
                estado = "[ENVIADO]" if i < progreso else "[PENDIENTE]"
                print(f"{i}. {estado}: {msg}")
        
        elif opcion == "2":
            nuevo = input("Escribe el contenido del mensaje: ")
            mensajes.append(nuevo)
            guardar_mensajes(mensajes)
            print("¡Mensaje añadido con éxito!")
            
        elif opcion == "3":
            idx = int(input("Introduce el número del mensaje a eliminar: "))
            if 0 <= idx < len(mensajes):
                if idx < progreso:
                    confirmar = input("⚠️ Este mensaje ya fue enviado. ¿Eliminar de todos modos? (s/n): ")
                    if confirmar.lower() != 's': continue
                
                eliminado = mensajes.pop(idx)
                guardar_mensajes(mensajes)
                print(f"Eliminado correctamente: {eliminado}")
            else:
                print("Número no válido.")
        
        elif opcion == "4":
            break

# --- LÓGICA PRINCIPAL DEL BOT ---

def ejecutar_bot():
    mensajes = cargar_mensajes()
    if not mensajes:
        print("[ERROR] No hay mensajes para enviar. Agrega algunos primero.")
        return

    indice_actual = obtener_progreso()
    total_mensajes = len(mensajes)

    if indice_actual >= total_mensajes:
        print("\n[INFO] ¡Todos los mensajes de la lista ya han sido enviados!")
        return

    print(f"\n--- CONFIGURACIÓN DE ENVÍO ---")
    numero_destino = input("Introduce el número de teléfono (+549...): ").strip()

    print(f"\n[INFO] Bot en marcha. Faltan {total_mensajes - indice_actual} días.")
    print(f"[*] Próximo envío: Hoy a las {HORA_ENVIO}:{MINUTO_ENVIO} (Hora Argentina)")

    while indice_actual < total_mensajes:
        ahora = datetime.now(ZONA_HORARIA)
        
        if ahora.hour == HORA_ENVIO and ahora.minute == MINUTO_ENVIO:
            mensaje_a_enviar = mensajes[indice_actual]
            print(f"\n[{ahora.strftime('%H:%M:%S')}] Enviando Mensaje Día {indice_actual + 1}...")
            
            try:
                pywhatkit.sendwhatmsg_instantly(
                    phone_no=numero_destino, 
                    message=mensaje_a_enviar, 
                    wait_time=15, 
                    tab_close=True, 
                    close_time=5
                )
                
                print(f"[{datetime.now(ZONA_HORARIA).strftime('%H:%M:%S')}] ¡Éxito!")
                indice_actual += 1
                guardar_progreso(indice_actual)
                
                print(f"Esperando 24hs para el siguiente...")
                time.sleep(65) # Evita repetir en el mismo minuto

            except Exception as e:
                print(f"\n[ERROR] Fallo en el envío: {e}")
                time.sleep(60)
        else:
            # Latido del sistema cada hora para verificar que sigue vivo
            if ahora.second == 0 and ahora.minute == 0:
                print(f"[{ahora.strftime('%H:%M:%S')}] Script activo. Esperando hora de envío...")
            
            time.sleep(10)

# --- MENÚ DE ENTRADA ---

def main():
    while True:
        print("\n==========================================")
        print("      WHATSAPP AUTO-BOT 100 DÍAS")
        print("==========================================")
        print("1. Iniciar/Continuar ciclo de envíos")
        print("2. Gestionar mensajes (Ver/Agregar/Borrar)")
        print("3. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            ejecutar_bot()
        elif opcion == "2":
            gestionar_mensajes()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    main()