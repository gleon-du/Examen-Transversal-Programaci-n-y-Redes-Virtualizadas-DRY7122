import requests
import math

# Clave de API de Graphhopper
api_key = "2506e1dc-2670-40be-b8d4-a753aefdb2e7"

def obtener_coordenadas(ciudad):
    """Obtiene latitud y longitud usando la API de Geocoding de Graphhopper"""
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&key={api_key}&limit=1"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos.get('hits'):
                lat = datos['hits'][0]['point']['lat']
                lng = datos['hits'][0]['point']['lng']
                return lat, lng
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al buscar la ciudad: {e}")
        return None

def calcular_distancia_avion(lat1, lon1, lat2, lon2):
    """Calcula la distancia en línea recta (Haversine) para vuelos"""
    R = 6371.0 # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def main():
    print("======================================================")
    print(" Calculadora de Rutas Avanzada (Graphhopper)")
    print(" (Presione 's' o 'salir' para finalizar)")
    print("======================================================\n")

    while True:
        origen = input("Ingrese Ciudad de Origen: ").strip()
        if origen.lower() in ['s', 'salir']:
            break
            
        destino = input("Ingrese Ciudad de Destino: ").strip()
        if destino.lower() in ['s', 'salir']:
            break

        print("\nSeleccione el medio de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. A pie")
        print("4. Avión")
        opcion_vehiculo = input("Opción (1/2/3/4): ").strip()

        # Mapeo de perfiles de Graphhopper
        perfiles = {"1": "car", "2": "bike", "3": "foot"}
        
        if opcion_vehiculo not in ['1', '2', '3', '4']:
            print("[!] Opción no válida. Intente nuevamente.\n")
            continue

        print("\nCalculando ruta y obteniendo coordenadas...")
        coords_origen = obtener_coordenadas(origen)
        coords_destino = obtener_coordenadas(destino)

        if not coords_origen or not coords_destino:
            print("[!] Error: No se encontraron las coordenadas de una de las ciudades.\n")
            continue

        lat1, lng1 = coords_origen
        lat2, lng2 = coords_destino

        print("\n" + "="*50)
        print("                 RESUMEN DEL VIAJE")
        print("=" * 50)
        print(f"Ruta           : {origen.capitalize()} -> {destino.capitalize()}")

        # LÓGICA PARA AVIÓN (Cálculo matemático directo)
        if opcion_vehiculo == '4':
            distancia_km = calcular_distancia_avion(lat1, lng1, lat2, lng2)
            # Velocidad promedio avión comercial: 800 km/h
            tiempo_horas = distancia_km / 800.0
            horas = int(tiempo_horas)
            minutos = int((tiempo_horas - horas) * 60)
            
            # Consumo estimado comercial (aprox 4 litros por km en total del avión)
            combustible_litros = distancia_km * 4.0 
            
            print(f"Medio          : Avión (Vuelo en línea recta)")
            print(f"Distancia      : {distancia_km:.2f} kilómetros")
            print(f"Duración est.  : {horas} horas, {minutos} minutos")
            print(f"Combustible    : {combustible_litros:.2f} litros de Jet Fuel (Total aeronave)")
            print("-" * 50)
            print("--- NARRATIVA DE LA RUTA ---")
            print(f"- Despegue desde aeropuerto cercano a {origen.capitalize()}")
            print(f"- Vuelo directo manteniendo rumbo hacia las coordenadas {lat2:.4f}, {lng2:.4f}")
            print(f"- Aterrizaje en aeropuerto cercano a {destino.capitalize()}")
            print("======================================================\n")

        # LÓGICA PARA RUTAS TERRESTRES (API Graphhopper)
        else:
            perfil = perfiles[opcion_vehiculo]
            url_ruta = f"https://graphhopper.com/api/1/route?point={lat1},{lng1}&point={lat2},{lng2}&vehicle={perfil}&locale=es&key={api_key}"
            
            try:
                respuesta = requests.get(url_ruta)
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    ruta = datos['paths'][0]
                    
                    distancia_km = ruta['distance'] / 1000
                    tiempo_seg_total = ruta['time'] / 1000
                    
                    horas = int(tiempo_seg_total // 3600)
                    minutos = int((tiempo_seg_total % 3600) // 60)
                    segundos = int(tiempo_seg_total % 60)
                    
                    print(f"Medio          : {perfil.capitalize()}")
                    print(f"Distancia      : {distancia_km:.2f} kilómetros")
                    print(f"Duración       : {horas} horas, {minutos} minutos, {segundos} segundos")
                    
                    if perfil == "car":
                        combustible_litros = distancia_km / 12.0
                        print(f"Combustible    : {combustible_litros:.2f} litros requeridos")
                    else:
                        print("Combustible    : 0 litros (Energía humana)")
                        
                    print("-" * 50)
                    print("--- NARRATIVA DE LA RUTA ---")
                    
                    instrucciones = ruta['instructions']
                    for paso in instrucciones:
                        # Extraemos el texto de la instrucción y la distancia de ese tramo
                        distancia_tramo = paso['distance'] / 1000
                        texto = paso['text']
                        if distancia_tramo > 0:
                            print(f"- {texto} ({distancia_tramo:.2f} km)")
                        else:
                            print(f"- {texto}")
                    print("======================================================\n")
                    
                else:
                    print(f"\n[!] Error en el cálculo. Código HTTP: {respuesta.status_code}")
                    print(f"Detalle: {respuesta.text}\n")
                    
            except Exception as e:
                print(f"\n[!] Error de conexión con la API de rutas: {e}\n")

if __name__ == "__main__":
    main()