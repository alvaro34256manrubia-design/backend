# external_api/test_api.py
import requests

def test_external_api():
    # URL de ejemplo (JSONPlaceholder)
    URL = "https://jsonplaceholder.typicode.com/posts/1"
    
    # 1. Hacer la petición GET
    response = requests.get(URL)
    
    # 2. Verificar que la respuesta fue exitosa (código 200)
    print(f"Status Code: {response.status_code}")
    
    # 3. Convertir la respuesta a JSON (que en Python es un diccionario)
    response_json = response.json()
    
    # 4. Mostrar los datos
    print(f"Datos recibidos: {response_json}")
    
    # 5. Acceder a datos específicos
    print(f"\nTítulo: {response_json.get('title')}")
    print(f"Cuerpo: {response_json.get('body')}")

if __name__ == "__main__":
    test_external_api()