from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

def get_external_data(request):
    URL = "https://jsonplaceholder.typicode.com/posts/1"
    
    try:
        response = requests.get(URL)
        response.raise_for_status()  
        data = response.json()
        context = {
            'api_data': data,
            'title': data.get('title', 'Sin título'),
            'body': data.get('body', 'Sin contenido'),
            'status_code': response.status_code,
        }
        
        return render(request, './data.html', context)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_multiple_posts(request):
    URL = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        all_posts = response.json()[:10]
        
        context = {
            'posts': all_posts,
            'total_posts': len(all_posts)
        }
        
        return render(request, './posts.html', context)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)