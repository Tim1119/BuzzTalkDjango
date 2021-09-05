from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import UserPostModel
from profiles.models import Profile
from django.http import JsonResponse
from .forms import UserPostEditForm,UserPostForm
from django.contrib.auth.models import User
from itertools import chain
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def HomeView(request):
    object_list= UserPostModel.objects.all().exclude()

    all_posts=[]
    combine_queryset=[]
    q = UserPostModel.objects.none()
    form=UserPostForm()
    # get profiles of everyone that the llogged in user is following
    all_profiles = Profile.objects.get(user=request.user).following.all() 
    all_profiles =list(all_profiles)
    # logged in user posts
    request_user_posts = UserPostModel.objects.filter(user=request.user)
    request_user_posts= list(request_user_posts)
    
    for i in all_profiles:
       combine_queryset+=q|UserPostModel.objects.filter(user=i.id)
    request_user_posts+= combine_queryset   
    all_posts.extend(request_user_posts)
    all_posts.reverse()
    
    #sort list
    for j in range(len(all_posts)):
        swapped=False
        i=0
        while i<len(all_posts)-1:
            if all_posts[i].created>all_posts[i+1].created:
                all_posts[i],all_posts[i+1]=all_posts[i+1],all_posts[i]
                swapped=True 
            i=i+1
        if swapped==False:
            break
    all_posts.reverse()
    return render(request,'posts/index.html',{'object_list':all_posts,'form':form})

@login_required
def PostView(request):
    form = UserPostForm()
    if request.method == 'POST':
            form = UserPostForm(request.POST or None,request.FILES or None)
            if form.is_valid():
                form.save()
                return redirect('posts:home')
    return render(request,'posts/post-content.html',{'form':form})


@login_required
def edit_view(request,pk):
    post = UserPostModel.objects.get(pk=pk)
    form = UserPostEditForm(instance=post)
    if request.method == 'POST':
        form = UserPostEditForm(request.POST or None,request.FILES or None,instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('/edit'+'/'+'{}'.format(pk))

    return render(request,'posts/edit-posts.html',{'form':form,'post':post})

@login_required
def delete_view(request):
    if request.method == 'POST':
        pk = request.POST.get('post_id')
        post = get_object_or_404(UserPostModel,pk=pk)
        post.delete()
        return redirect('/')

@login_required
def like_view(request):
    if request.method=='POST':
        pk = request.POST.get('post_id')
        post = get_object_or_404(UserPostModel,pk=pk)
        liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return redirect('/')
        else:
            post.likes.add(request.user)
        return redirect('/')
    else:
        return redirect('/')

    


    



