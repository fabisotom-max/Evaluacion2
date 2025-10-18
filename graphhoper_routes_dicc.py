import requests
import urllib.parse
from googletrans import Translator
translator = Translator()

route_url = "https://graphhopper.com/api/1/route?"
key = "a4e0fa61-126f-4249-bc8a-9a177475a304"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        value1 = translator.translate(value, src='en', dest='es').text

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value1 + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status, round(lat,2), round(lng,2), new_loc

while True:
    print("\n++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, pie")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("Si desea salir escriba 'salir' ó 's'")
    profile = ["auto", "bicicleta", "pie"]
    vehicle = input("Ingresa un perfil de vehículo de la lista anterior: ")
    
    if vehicle == "s" or vehicle == "salir":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "auto"
        print("No se ingresó un perfil de vehículo válido. Se usará el perfil de auto.")

    loc1 = input("Ubicación de inicio: ")
    if loc1 == "s" or loc1 == "salir":
        break
    orig = geocoding(loc1, key)
    print(orig)
    loc2 = input("Destino: ")
    if loc2 == "s" or loc2 == "salir":
        break
    dest = geocoding(loc2, key)
    print("=====================================================")
    if vehicle == "auto":
        vehicle1 = "car"
    elif vehicle == "bicicleta":
        vehicle1 = "bike"
    elif vehicle == "pie":
        vehicle1 = "foot"


    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle1}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nURL de la API de enrutamiento:\n" + paths_url)
        print("Dirección desde " + orig[3] + " hacia " + dest[3] + " en " + vehicle)
        print("=====================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración de viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=====================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                instr = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]

                instr_es = translator.translate(instr, src='en', dest='es').text
                print(f"{instr_es} ({distance/1000:.1f} km / {distance/1000/1.61:.1f} millas)")
            print("=====================================================")
        else:
            print("Mensaje de error " + paths_data["message"])
            print("*****************************************************")