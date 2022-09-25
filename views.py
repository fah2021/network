from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import Posts, User, Follow
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


class PostsList(LoginRequiredMixin,generic.ListView):
    paginate_by = 10
   # context_object_name = 'posts'
    model = Posts
    template_name = 'network/index.html'
    login_url = '/login' 
    
    #ordering = ['-timestamp']
    
    def get_queryset(self):
        return Posts.objects.all()

class Owners_views(LoginRequiredMixin,generic.ListView):
    paginate_by = 10
   # context_object_name = 'posts'
    model = Posts
    template_name = 'network/owner.html'
    login_url = '/login' 
    
    #ordering = ['-timestamp']
    
    def get_queryset(self):
        return Posts.objects.filter(user_id=self.request.user.id)

class Following(LoginRequiredMixin,generic.ListView):
    paginate_by = 10
   # context_object_name = 'posts'
    model = Posts #Follow
    template_name = 'network/following.html'
    login_url = '/login' 
    
    def get_queryset(self):
        following = Follow.objects.filter(user_id=self.request.user.id).values('follower_id')

        return Posts.objects.filter(user__in=following).order_by('-timestamp')
   
    
def index(request):
    request=request
    return render(request, "network/index.html")

@csrf_exempt
def edit(request, post_id):
    post = Posts.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.message = data["post"]
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def profile(request, post_owner):
    current_user = post_owner
    print(current_user)
    logged_in_user = request.user.id
    print(logged_in_user)
    owner=User.objects.get(id=post_owner)

    posts = Posts.objects.filter(user=owner).order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    record = Follow.objects.filter(user=logged_in_user,follower=post_owner)
    user_followers = len(Follow.objects.filter(user_id=current_user))
    user_following = len(Follow.objects.filter(follower_id=current_user))
    if(record):
        return render(request, "network/profile.html", {
        'post_owner':owner.username,
        'current_user':current_user,
        'follows': True,
        'user_followers':user_followers,
        'user_following':user_following,
        'owner': owner,
        "page_obj": page_obj, 
        
        
    }) 

    else:
        return render(request, "network/profile.html", {
        'post_owner':owner.username,
        'current_user':current_user,

        'user_followers':user_followers,
        'user_following':user_following,
        'owner': owner,
        "page_obj": page_obj, 

        'follows': False
        
    }) 
  
@csrf_exempt
def followers_count(request,post_owner):
    if request.method == 'POST':
        #value = request.POST.get('value', False)
        #user = request.POST.get('user',False)
        #follower = request.POST.get('follower',False)
        user = request.user
        #post_owner=User.objects.get(id=post_owner)
        record = Follow.objects.filter(user_id=user.id,follower_id=post_owner)
        record_count = Follow.objects.filter(user_id=user.id,follower_id=post_owner).count()
        
        if record_count <1:
            f = Follow.objects.create(user_id=user.id,follower_id=post_owner)
            f.save()
            count = Follow.objects.all().count()
            resp = {
                'follows': 't',
                'total_follows': count
            }
        else:
            f = Follow.objects.filter(user_id=user.id,follower_id=post_owner).delete()
            count = Follow.objects.all().count()
            resp = {
                'follows': 'f',
                'total_follows': count

            }

        response = json.dumps(resp)
        return HttpResponse(response, content_type = "application/json") 
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

@csrf_exempt
def like(request, post_id):
   
    if request.method == "POST":
        user = request.user
        p=Posts.objects.get(id=post_id)
        
        if user in p.likes.all():
            p.likes.remove(user)
            p.save()
            resp = {
                'liked':"f"
            }
        else:
            p.likes.add(user)
            p.save()
            resp = {
                'liked':"t"
            }

        response = json.dumps(resp)
        return HttpResponse(response, content_type = "application/json")
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


@csrf_exempt
def add_post(request):
    print(request)

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Please be logged in to post to the server"}, status=400)

    data = json.loads(request.body)
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")

    Posts(user=request.user, message=message, timestamp=timestamp).save()

    return JsonResponse({"success": "message posted successfully!"}, status=201)


def get_message(request):
    try:
        queryset = Posts.objects.filter(user=request.user)
        list = []  # create list
        for row in queryset:  # populate list
            list.append({'message': row.message, 'user': row.user.username, 'user_id': row.user.id,
                         'timestamp': str(row.timestamp)})
        json_data = json.dumps(list)  # dump list as JSON
        return HttpResponse(json_data, 'application/javascript')
        
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Posts not found."}, status=404)


def get_all_messages(request):
    try:
        queryset = Posts.objects.all()
        list = []  # create list
        for row in queryset:  # populate list
            list.append({'message': row.message, 'user': row.user.username, 'user_id': row.user.id,
                         'timestamp': str(row.timestamp)})
        json_data = json.dumps(list)  # dump list as JSON
        return HttpResponse(json_data, 'application/javascript')

    except Posts.DoesNotExist:
        return JsonResponse({"error": "Posts not found."}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
