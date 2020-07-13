# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import MyCommentForm
#from django.views.generic.detail import DetailView
from django.views import generic
from django.template.loader import render_to_string
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.db.models import Q
from Socialize.models import FollowUser, MyPost, MyProfile, MyComment, PostLike
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin



# Create your views here.
#Home Page
@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "xyz/home.html"
    #paginate_by= 5

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followed_list = FollowUser.objects.filter( followed_by=self.request.user.myprofile)
        followedlist2 = []
        for e in followed_list:
            followedlist2.append(e.profile)
        #f = len(followed_list)

        #followedlist2 = FollowUser.objects.filter(followed_by = e)
        #followcount = f
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        Allposts = MyPost.objects.filter(Q(uploaded_by__in = followedlist2)).filter(Q(subject__icontains = si) | Q(msg__icontains = si))
        for p1 in Allposts:
            p1.liked = False
            y = PostLike.objects.filter(post = p1, liked_by=self.request.user.myprofile)
            if y :
                p1.liked = True
            y = PostLike.objects.filter(post = p1)
            p1.likecount = y.count()
        context["mypost_list"] = Allposts
        return context



class AboutView(TemplateView):
    template_name = "xyz/about.html"

class ContactView(TemplateView):
    template_name = "xyz/contact.html"


@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address1", "status", "gender", "phone_no", "description", "pic"]
    template_name = "auth/user_form.html"





    def get_object(self):
         return get_object_or_404(MyProfile, pk = self.request.user.id)
@method_decorator(login_required, name="dispatch")
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject", "msg", "pic"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):

    model = MyPost
    paginate_by = 9
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)| Q(cr_date__icontains = si))

@method_decorator(login_required, name="dispatch")
class MyPostDetailView(FormMixin,DetailView):
    model = MyPost
    template_name = "Socialize/mypost_detail.html"
    form_class = MyCommentForm
    def get_success_url(self):
        return reverse("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = MyComment.objects.all()

        context['comments'] =comments
        context['form'] = MyCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


        #if self.method == "POST":
            #form = MyCommentForm(self.POST)
            #if form.is_valid():
                #comments = form.save(commit=False)
                #comments.post = post
                #comments.save()
                #return redirect('home', context)
        #else:
            #form = MyCommentForm()
        #return {'form': form}
        #if request.method == 'POST':
        #form = MyCommentForm(data=request.POST)
        #if form.is_valid():
            #msg = request.POST.get('msg')
        #else:
            #form = MyCommentForm()











            # Create Comment object but don't save to database y








    #context_object_name = 'mypost'

    #def get_object(self):
         #return get_object_or_404(MyPost, pk=self.request.x.id)





    #template_name = "Socialize/mypost_detail.html"
    #def get_queryset( self,request, pk=None,*args, **kwargs):
        #return get_object_or_404(MyPost, pk=self.request.mypost.id)

        #return get_object_or_404(MyPost, pk=kwargs['pk'])
    #

@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required, name="dispatch")
class MyProfileListView(ListView):
    model = MyProfile
    paginate_by = 2
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profileList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address1__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id");
        for p1 in profileList:
            p1.followed = False
            y = FollowUser.objects.filter(profile = p1, followed_by=self.request.user.myprofile)
            if y :
                p1.followed = True
        return profileList














@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView, MultipleObjectMixin):
    model = MyProfile
    paginate_by=5
    #


    #}

    template_name = "Socialize/myprofile_detail.html"
    def get_context_data(self,**kwargs):
        pk = self.kwargs.get('pk')
        Allposts = MyPost.objects.filter(uploaded_by_id=pk).all()
        context = super(MyProfileDetailView, self).get_context_data(object_list=Allposts,**kwargs)

        #followed_list = FollowUser.objects.filter( followed_by=self.request.user.myprofile)
        #followedlist2 = []
        #for e in followed_list:
            #followedlist2.append(e.profile)
        si = self.request.GET.get("si")
        if si == None:
            si = ""

        #followers = FollowUser.objects.filter()
        #context['followers'] = followers

        #context = super(MyProfileDetailView, self).get_context_data(object_list=Allposts,**kwargs)

        #paginator = Paginator(Allposts, 5)
        #page_number = self.request.GET.get('page_number')

        #try:
            #page = int(paginator.get('page',1))

        #except:
            #page = 1
            #result = paginator.page(1)
        #except EmptyPage:
            #result = paginator.page(paginator.num_pages)


                # If page is not an integer, deliver first page.


                # If page is out of range (e.g. 9999), deliver last page of results.

        #try:
            #matches = paginator.page(page_number)

        #except (PageNotAnInteger,ValueError):
            #matches = paginator.page(1)


        #page_obj = paginator.get_page(page_number)




        for p1 in Allposts:
            p1.liked = False
            y = PostLike.objects.filter(post = p1, liked_by=self.request.user.myprofile)
            if y :
                p1.liked = True
            y = PostLike.objects.filter(post = p1)
            p1.likecount = y.count()
        context["mypost_list"] = Allposts
        #context["page_obj"] = page_obj
        followcount = FollowUser.objects.filter(profile_id=pk).count()
        following = FollowUser.objects.filter(followed_by_id=pk).count()
        context["following"]= following

        context["followcount"]= followcount
        return context




def follow(req, pk):
    id = req.GET.get("id")
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/myprofile/")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/myprofile/")

def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.myprofile)
    #return HttpResponseRedirect(redirect_to="/home/")
    #if req.is_ajax():
        #html = render_to_string('Socialize/like_1.html',req=req,pk=pk)
        #return JsonResponse({'form':html})
    return HttpResponseRedirect(redirect_to="/home/")

def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/home/")


@method_decorator(login_required, name="dispatch")
class MyPostUpdateView(UpdateView):
    model = MyPost
    fields = ["msg", "subject", "pic",]
    #def get_object(self):
         #return get_object_or_404(MyPost, pk = self.request.user.id)
