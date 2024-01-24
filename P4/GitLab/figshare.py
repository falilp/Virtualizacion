import hashlib
import json
import os
import requests
from requests.exceptions import HTTPError

BASE_URL = 'https://api.figshare.com/v2/account/articles'
TOKEN = os.getenv('FIGSHARE_API_TOKEN') # Utiliza la variable de entorno que configuraste en GitLab
CHUNK_SIZE = 1048576

FILE_PATH = './grafico.png' # Ruta relativa de la imagen en tu repositorio
TITLE = 'Mi Imagen' # Título del artículo de Figshare

def list_articles():
    endpoint = 'account/articles'
    response = requests.get(BASE_URL.format(endpoint=endpoint), headers={'Authorization': f'token {TOKEN}'})
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    else:
        articles = response.json()
        for article in articles:
            print(f'ID: {article["id"]}, Title: {article["title"]}')

def create_article(title):
    endpoint = 'account/articles'
    headers = {'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    data = json.dumps({'title': title})
    response = requests.post(BASE_URL.format(endpoint=endpoint), headers=headers, data=data)
    if response.status_code != 201:
        raise Exception(f'Failed to create article: {response.content}')
    return response.json()['location'].split('/')[-1]

def list_files_of_article(article_id):
    endpoint = f'account/articles/{article_id}/files'
    response = requests.get(BASE_URL.format(endpoint=endpoint), headers={'Authorization': f'token {TOKEN}'})
    if response.status_code != 200:
        raise Exception(f'Failed to list files of article: {response.content}')
    return response.json()

def initiate_new_upload(article_id, file_path):
    endpoint = f'account/articles/{article_id}/files'
    headers = {'Authorization': f'token {TOKEN}'}
    with open(file_path, 'rb') as file:
        data = {'name': os.path.basename(file_path)}
        response = requests.post(BASE_URL.format(endpoint=endpoint), headers=headers, data=json.dumps(data), files={'filedata': file})
    if response.status_code != 201:
        raise Exception(f'Failed to initiate upload: {response.content}')
    return response.json()

def upload_parts(file_info):
    endpoint = f'account/articles/{file_info["article_id"]}/files/{file_info["id"]}/parts'
    headers = {'Authorization': f'token {TOKEN}'}
    with open(file_info['file_path'], 'rb') as file:
        data = {'partNumber': 1, 'totalParts': 1}
        response = requests.put(BASE_URL.format(endpoint=endpoint), headers=headers, data=data, files={'filedata': file})
    if response.status_code != 200:
        raise Exception(f'Failed to upload parts: {response.content}')

def complete_upload(article_id, file_id):
    endpoint = f'account/articles/{article_id}/files/{file_id}/complete'
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.post(BASE_URL.format(endpoint=endpoint), headers=headers)
    if response.status_code != 200:
        raise Exception(f'Failed to complete upload: {response.content}')

def main():
    # Primero creamos el artículo
    list_articles()
    article_id = create_article(TITLE)
    list_articles()
    list_files_of_article(article_id)

    # Luego subimos el archivo.
    file_info = initiate_new_upload(article_id, FILE_PATH)
    # Hasta aquí usamos la API de Figshare; las siguientes líneas usan la API de carga de Figshare.
    upload_parts(file_info)
    # Volvemos a la API de Figshare para completar el proceso de carga del archivo.
    complete_upload(article_id, file_info['id'])
    list_files_of_article(article_id)


if __name__ == '__main__':
    main()
