
from ncclient import manager
import sys

# Parámetros de aprovisionamiento para el dispositivo CSR1000v
router_device = {
    "host": "192.168.56.117",     # Dirección IP asignada al router en el lab
    "port": 830,                   # Puerto de escucha del servicio NETCONF
    "username": "cisco",           # Credencial de acceso de administrador
    "password": "cisco123!",       # Clave secreta del laboratorio
    "hostkey_verify": False
}

# Payload XML estructurado bajo el modelo YANG Cisco-IOS-XE-native
config_payload = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>Leon_Leon</hostname>
        <interface>
            <Loopback>
                <name>111</name>
                <description>Interfaz Loopback provista mediante NETCONF - Examen Transversal</description>
                <ip>
                    <address>
                        <primary>
                            <address>111.111.111.111</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

def ejecutar_automatizacion():
    print("[*] Estableciendo conexión segura SSH con el subsistema NETCONF...")
    try:
        # Inicialización del gestor de conexiones cifradas de ncclient
        with manager.connect(**router_device) as sesion:
            print("[+] Conexión establecida de forma exitosa.")
            print("[*] Despachando configuración estructurada al running-config...")
            
            # Ejecución del comando de edición de configuración remota
            respuesta_rpc = sesion.edit_config(target='running', config=config_payload)
            
            # El protocolo NETCONF responde con una etiqueta <ok/> si la sintaxis es válida
            if "<ok/>" in str(respuesta_rpc):
                print("\n=======================================================")
                print("[+] ¡PROCEDIMIENTO COMPLETADO EXITOSAMENTE!")
                print(" - El Hostname ha mutado a los apellidos corporativos.")
                print(" - Se ha desplegado la interfaz Loopback 111 (111.111.111.111/32).")
                print("=======================================================")
            else:
                print("[-] Respuesta inesperada del dispositivo de red:")
                print(respuesta_rpc)
                
    except Exception as error:
        print(f"\n[!] Fallo crítico en la sesión NETCONF: {error}")
        print("[!] Compruebe el direccionamiento IP y valide que 'netconf-yang' esté corriendo.")

if __name__ == "__main__":
    ejecutar_automatizacion()