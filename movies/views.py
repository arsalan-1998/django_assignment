from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from movies.models import movieCollections, getCollections, movies, favorite_genres
import json
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import requests
import base64

def home(request):
    return HttpResponse("hello world")

def signup(request):
    if request.method == 'GET':
        return HttpResponse( "hello" )
    else:
        data = {
            "username": request.POST['username'],
            "password": make_password(request.POST['password']),
            "status": ""
        }
        print(data)
        user = User.objects.create(username=data['username'], password=data['password'])
        user.save()
        data['status'] = "User Created"
        return HttpResponse( json.dumps(data) )

def create_movies(request):
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded_credentials = auth_header.split(' ')  # Removes "Basic " to isolate credentials
    decoded_credentials = base64.b64decode(encoded_credentials[1]).decode("utf-8").split(':')
    username = decoded_credentials[0]
    password = decoded_credentials[1]
    data = {
        "username": username,
        "password": password
    }
    if encoded_credentials[0] != 'Basic':
        return HttpResponse(status=401)
    else:
        page = request.GET.get('page', '')
        if page != '' :
            collection = requests.get('https://demo.credy.in/api/v1/maya/movies/?page={}'.format(int(page)), auth=(data['username'], data['password'])).json()
            return JsonResponse(collection, safe=False)   
        else:
            collection = requests.get('https://demo.credy.in/api/v1/maya/movies/', auth=(data['username'], data['password'])).json()
            return JsonResponse(collection, safe=False)   

def collections(request):
    if request.method == 'POST':
        data = {
            "title": request.POST['title_collection'],
            "description": request.POST['description'],
            "movies": [
                {
                    "title": request.POST['title'],
                    "description": request.POST['description'],
                    "genres": request.POST['genres'],
                    "uuid": request.POST['uuid'],
                }
            ],
            "status": ""
        }
        movie = movies.objects.create(title=data['movies'][0]['title'], description=data['movies'][0]['description'], genres=data['movies'][0]['genres'], uuid=data['movies'][0]['uuid'])
        movie.save()
        mov_obj = movies.objects.latest('id')
        print(mov_obj.id)
        m_collection = movieCollections.objects.create(title=data['title'], description=data['description'], collections_id=mov_obj.id)
        m_collection.save()
        data['status'] = "Created Collection"

        return HttpResponse(json.dumps(data['movies'][0]['uuid']))
    elif request.method == 'PUT':
        collection_id = request.GET.get('col_id', '')
        data = {
            "movies": [
                {
                    "title": "Spiderman Home Coming",
                    "description": "This is an action movie",
                    "genres": "Action"
                }
            ],
            "status": ""
        }

        if collection_id != '':
            m_col = movies.objects.get(uuid=collection_id)
            print(m_col.title)
            m_col.title=data['movies'][0]['title'] 
            m_col.description=data['movies'][0]['description']
            m_col.genres=data['movies'][0]['genres']
            m_col.save()
            data['status'] = 'update done'
            return JsonResponse(data, safe=False)
        data['status'] = 'update failed'
        return JsonResponse(data, safe=False)
    elif request.method == 'DELETE':
        collection_id = request.GET.get('col_id', '')
        if collection_id != '':
            m_col = movies.objects.get(uuid=collection_id)
            movieCollections.objects.get(id=m_col.id).delete()
            m_col = movies.objects.get(uuid=collection_id).delete()
            data = 'delete done'
            return JsonResponse(data, safe=False)
        data = 'delete failed'
        return JsonResponse(data, safe=False)
    else:
        collection_id = request.GET.get('col_id', '')
        m_collections = {
            "is_success": True, 
            "data": {
                "collection": []
            }
        }
        if collection_id != '':
            d = movies.objects.get(uuid=collection_id)
            if d == '':
                data = 'Invalid id'
            else:
                data = {
                "title": d.title,
                "uuid": d.uuid, 
                "description": d.description
                }
                m_collections['data']['collection'].append(data)
            return JsonResponse(m_collections, safe=False)
        for d in movies.objects.all():
            data = {
                "title": d.title,
                "uuid": d.uuid, 
                "description": d.description
            }
            m_collections['data']['collection'].append(data)
        
        return JsonResponse(m_collections, safe=False)
