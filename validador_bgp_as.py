def validar_as_bgp():
    try:
        x = int(input("Ingrese el número de AS de BGP a consultar: "))

        # Rangos de AS Privados
        if (64512 <= x <= 65534) or (4200000000 <= x <= 4294967294):
            print(f"El AS {x} corresponde a un AS Privado.")
        # Rangos de AS Públicos
        elif (1 <= x <= 64495) or (131072 <= x <= 4199999999):
            print(f"El AS {x} corresponde a un AS Público.")
        else:
            print(f"El AS {x} es un número reservado o no válido para asignación general.")

    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

validar_as_bgp()