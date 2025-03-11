# from django.shortcuts import render, get_object_or_404
# from django.views.generic.list import ListView
# from .models import Post, Tag, Author
# # from django.views.generic.detail import DetailView
# from .forms import CommentForm
# from django.views import View
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# # Create your views here.

# class StartingPageView(ListView):
#     model = Post
#     template_name = "blog/index.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         return Post.objects.all().order_by("-date")[:3]

# class AllPostsView(ListView):
#     model = Post
#     template_name = "blog/all-posts.html"
#     ordering=["-date"]
#     context_object_name = "all_posts"
    
# class PostDetailView(View):
#     model = Post
#     template_name = "blog/post-detail.html"
#     context_object_name = "post"
    
#     def get(self,request,slug):
#         post=Post.objects.get(slug=slug)
#         context={
#             "post":post,
#             "post_tags":post.tags.all(),
#             "comment_form":CommentForm(),
#         }
#         return render(request,"blog/post-details.html",context)
        
        
        
#     def post(self,request,slug):
#         comment_form=CommentForm(request.POST)
#         post=Post.objects.get(slug=slug)

#         if comment_form.is_valid():
#             comment=comment_form.save(commit=False)
#             comment.post=post
#             comment.save()
            
#             return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        
#         context={
#             "post":post,
#             "post_tags":post.tags.all(),
#             "comment_form":CommentForm(),
#         }
#         return render(request,"blog/post-details.html",context)
        
        
        
          
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Tag, Author
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-date")[:3]

class AllPostsView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "all_posts"
    ordering = ["-date"]

class PostDetailView(View):
    
    def is_stored_post(self,request,post_id):
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later=post_id in stored_posts
        else:
            is_saved_for_later=False
        return is_saved_for_later        
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)            
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request,post.id)
        }
        return render(request, "blog/post-detail.html", context)
    
    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post=post
            comment.save()
            
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request,post.id)

        }
        return render(request,"blog/post-detail.html",context)
    
    
class ReadLaterView(View):
    
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=stored_posts)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
          stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
          stored_posts.append(post_id)
        else:
          stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")
        
    
    # model = Post
    # template_name = "blog/post-detail.html"
    # context_object_name = "post"
    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         comment = comment_form.save(commit=False)
    #         comment.post = self.object
    #         comment.save()
    #         return HttpResponseRedirect(reverse("post-detail-page", args=[self.object.slug]))
    #     context = self.get_context_data()
    #     context["comment_form"] = comment_form
    #     return self.render_to_response(context)        