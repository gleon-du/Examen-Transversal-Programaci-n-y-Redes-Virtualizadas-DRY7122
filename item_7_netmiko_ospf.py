from netmiko import ConnectHandler

def main():
    # Diccionario con los parámetros de conexión
    csr1000v = {
        'device_type': 'cisco_ios',
        'host': '192.168.56.117', 
        'username': 'cisco',
        'password': 'cisco123!',
        
    }

    print("[*] Conectando al router CSR1000v vía SSH con Netmiko...")
    try:
        net_connect = ConnectHandler(**csr1000v)
        
        print("[+] Conexión exitosa.\n")

        # 1. Lista de comandos de configuración para OSPF (IPv4 e IPv6)
        ospf_config = [
            'ipv6 unicast-routing',
            # Configuración OSPF para IPv4
            'router ospf 1',
            'router-id 1.1.1.1',
            'passive-interface default',
            'no passive-interface GigabitEthernet1',
            'network 0.0.0.0 255.255.255.255 area 0',
            'exit',
            # Configuración OSPF para IPv6 (OSPFv3)
            'ipv6 router ospf 1',
            'router-id 1.1.1.1',
            'passive-interface default',
            'no passive-interface GigabitEthernet1',
            'exit',
            # Aplicar OSPF IPv6 en la interfaz
            'interface GigabitEthernet1',
            'ipv6 ospf 1 area 0',
            'exit'
        ]

        print("[*] Enviando configuración OSPF al router...")
        output_conf = net_connect.send_config_set(ospf_config)
        print("--- Salida de Configuración ---")
        print(output_conf)
        print("-------------------------------\n")

        # 2. Lista de comandos SHOW 
        comandos_show = [
            'show running-config | section ospf',
            'show ip interface brief',
            'show ipv6 interface brief',
            'show version',
            'show running-config'
        ]

        # 3. Ejecutar y mostrar cada comando
        for cmd in comandos_show:
            print(f"\n{'='*60}")
            print(f" Ejecutando: {cmd}")
            print(f"{'='*60}")
            
            # send_command obtiene la salida del comando y la guarda en formato string
            salida = net_connect.send_command(cmd)
            
            # Para el running-config, que es muy largo, se guarda un respaldo en txt
            if cmd == 'show running-config':
                print("[*] Guardando salida de running-config en 'netmiko_run_config.txt'...")
                with open("netmiko_run_config.txt", "w") as f:
                    f.write(salida)
                # Solo las primeras 15 líneas en consola para no saturar
                print('\n'.join(salida.split('\n')[:15]))
                print("... [Salida resumida en pantalla, revisa el archivo .txt] ...")
            else:
                print(salida)

        # Cerrar la conexión
        net_connect.disconnect()
        print("\n[+] Tareas de Netmiko finalizadas. Conexión cerrada.")

    except Exception as e:
        print(f"\n[!] Ocurrió un error en la conexión o ejecución: {e}")

if __name__ == "__main__":
    main()
