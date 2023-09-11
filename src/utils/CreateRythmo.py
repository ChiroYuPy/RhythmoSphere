import os
import zipfile
import json


def load_map_config(name):
    zip_file_path = f'maps/{name}.rythmo'
    if not os.path.exists(zip_file_path):
        raise FileNotFoundError(f"Map '{name}' not found.")
    with zipfile.ZipFile(zip_file_path, 'r') as myzip:
        with myzip.open('config.json') as json_file:
            donnees_json = json.load(json_file)
    return donnees_json


def load_map_data(name):
    zip_file_path = f'maps/{name}.rythmo'
    if not os.path.exists(zip_file_path):
        raise FileNotFoundError(f"Map '{name}' not found.")
    with zipfile.ZipFile(zip_file_path, 'r') as myzip:
        with myzip.open('map.csv') as csv_file:
            donnees_csv = csv_file.read()
    return donnees_csv


def play_map_music(name, pygame):
    zip_file_path = f'maps/{name}.rythmo'
    mp3_file_path = f'song.mp3'
    with zipfile.ZipFile(zip_file_path, 'r') as myzip:
        myzip.extract(mp3_file_path, 'temp')
    pygame.mixer.init()
    pygame.mixer.music.load(f'temp/song.mp3')
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
