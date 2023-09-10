import zipfile
import json

# Ouvrez le fichier ZIP (astronomia.rythmo)
with zipfile.ZipFile('maps/astronomi.rythmo', 'r') as myzip:
    # Lisez le contenu du fichier JSON (config.json)
    with myzip.open('config.json') as json_file:
        # Chargez les données JSON
        donnees_json = json.load(json_file)

# Imprimez les données dans la console
print("BPM:", donnees_json.get("BPM"))
print("Vitesse d'apparition des cercles:", donnees_json.get("VitesseApparitionCercles"))
print("Taille des cercles:", donnees_json.get("TailleCercles"))
print("Nom de la carte:", donnees_json.get("NomMap"))
print("Description de la carte:", donnees_json.get("DescriptionMap"))
print("Nombre d'objets:", donnees_json.get("NombreObjets"))


# Mettez à jour les données existantes (ou ajoutez de nouvelles données)
donnees_json["BPM"] = 140
donnees_json["VitesseApparitionCercles"] = 2.5

# Réécrivez les données dans le fichier astronomia.rythmo
donnees_json_str = json.dumps(donnees_json)
with zipfile.ZipFile('maps/astronomia.rythmo', 'w', zipfile.ZIP_DEFLATED) as myzip:
    myzip.write('sound/astronomia.mp3', 'song.mp3')
    myzip.write('map.csv', 'map.csv')
    myzip.writestr('config.json', donnees_json_str)
