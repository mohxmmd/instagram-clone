from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,View,CreateView,DetailView
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Post,Stories,Message,DirectMessage,Comment
# Create your views here.



class Home(TemplateView):

    template_name = 'home2.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        stories = reversed(Stories.objects.all())
        posts = reversed(Post.objects.all())
        messages = reversed(Message.objects.all())
        user = self.request.user.id
        
        # context['stories'] = stories
        # context['posts']=posts
        # context['messages'] = messages

        context = {
            'stories': stories,
            'posts': posts,
            'messages': messages
        }
        return context
    





class SigninView(View):

    def get(self,request,*args,**kw):
        form = SigninForm()
        return render (request,"signin.html",{"form":form}) 
    
    def post(self,request,*args,**kw):
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                return redirect('signin')



class SignupView(CreateView):
    model=User
    form_class=SignupForm
    template_name='signup.html'
    success_url=reverse_lazy('signin')

class AddPostView(View):
    def get(self, request, *args, **kwargs):
        form = AddPostForm()
        return render(request, "addpost.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AddPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = request.user
                caption = form.cleaned_data.get('caption')
                form.save()
                return redirect('home')
        else:
            form = AddPostForm()
        return render(request, 'addpost.html', {'form': form})

class AddStoryView(View):
    def get(self,request,*args,**kw):
        form = AddStoryForm()
        return render (request,"addstory.html",{"form":form})
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AddStoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('home')
        else:
            form = AddStoryForm()
        return render(request, 'addstory.html', {'form': form})



def chat_view(request):
    messages = Message.objects.all()
    return render(request, 'chat.html', {'messages': messages})



def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        Message.objects.create(user=user, content=content)
    return redirect('home')



def send_dm(request,*args,**kwargs):
    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        id = kwargs.get('id')
        reciever =  User.objects.get(id=id)
        print(reciever)
        DirectMessage.objects.create(sender=sender,reciever = reciever, content=content)
    return redirect('dm', id=id)



class DirectMessageView(TemplateView):
    template_name = 'dm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender = self.request.user
        id = kwargs.get('id')
        reciever =  User.objects.get(id=id)
        context['sender']=sender
        context['reciever'] =reciever
        sentmessages = DirectMessage.objects.filter(sender=sender.id, reciever = reciever.id) 
        recievedmessages = DirectMessage.objects.filter(sender=reciever.id,reciever = sender.id) 
        messages = sentmessages.union(recievedmessages)
        context['messages']=messages
        context['sentmessages']=sentmessages
        context['recievedmessages']  = recievedmessages
        print('-----------------------------------------------')
        print (sentmessages)
        print(messages)

        
        return context


class Chat(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        id = user.id
        users = reversed(User.objects.exclude(id=id))
        context['users']=users
        return context



        

class ExploreView(View):
   def get(self,request,*args,**kw):
        user = request.user
        id = user.id
        users = reversed(User.objects.exclude(id=id))
        return render(request,'explore.html',{'users':users})
    

class StoryView(DetailView):
    model = Stories
    template_name = 'story.html'
    pk_url_kwarg = 'id'
    context_object_name = 'story'

    
class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    pk_url_kwarg = 'id'
    context_object_name = 'user'

# class LikeView(View):
#     def post(self,request,*args,**kw):
#         user = request.user
#         post_id = kw.get('id')
#         post = Post.objects.get(id=post_id)
#         return render(request,'home.html')
#     def post(self,request,*args,**kw):
#         user = request.user
#         post_id = kw.get('id')
#         post = Post.objects.get(id=post_id)
#         if Like.like == False:
#             Like.like = True
#             Like.save()
#             print('11111111111111111111111111111111111111111111111111111111111111111')
            
#         else:
#             Like.like = False
#             Like.save()
#             print('0000000000000000000000000000000000000000000000000000000')

#         print('333333333333333333333333333333333333333333333')
#         return render(request,'home.html')
    
# def like_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)

#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return redirect(request,'home.html', post_id=post_id)

# def like_post(request, id):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return render(request,'home.html')
        
       

class CommentView(View):
    def get(self,request,*args,**kw):
        form = CommentForm()
        post_id = kw.get('id')
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        length = len(comments)
        print('==============================================================================')
        print(length)
        return render (request,"comments.html",{"form":form,'comments':comments,'length':length})
    
    def post(self,request,*args,**kw):
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            form.instance.user = request.user
            post_id = kw.get('id')
            post = Post.objects.get(id=post_id)
            form.instance.post = post
            form.save()
            return redirect('comment' ,id=post.id)
        
class ComingSoon(TemplateView):
    template_name = 'comingsoon.html'