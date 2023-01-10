from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from ProgrammingCategory.forms import *
from ProgrammingCategory.models import *
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView
from ProgrammingCategory.utils import *

class DeveloperHome(DataMixin, ListView):
  model = Developer
  template_name = 'ProgrammingCategory/index.html'
  context_object_name = 'posts'

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c_def = self.get_user_context(title="Main page")
    return dict(list(context.items()) + list(c_def.items()))
  
  def get_queryset(self):
    return Developer.objects.filter(is_published=True).select_related('cat')
  
  
# def index(request):
#   posts = Developer.objects.all()
  
#   context = {
#     'posts': posts,
#     'menu': menu, 
#     'title': 'Main page',
#     'cat_selected': 0,
#   }
#   return render(request, 'ProgrammingCategory/index.html', context=context)

def about(request):
  contact_list = Developer.objects.all()
  paginator = Paginator(contact_list, 3)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'ProgrammingCategory/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'About site'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
  form_class = AddPostForm
  template_name = 'ProgrammingCategory/addpage.html'
  success_url = reverse_lazy('home')
  login_url = reverse_lazy('home')
  raise_exceptin = True
  
  def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c_def = self.get_user_context(title="Add page")
    return dict(list(context.items()) + list(c_def.items()))



# def addpage(request):
#   if request.method == 'POST':
#     form = AddPostForm(request.POST, request.FILES)
#     if form.is_valid():
#       # print(form.cleaned_data)
#       form.save()
#       return redirect('home')
#   else:
#     form = AddPostForm()
  
#   return render(request, 'ProgrammingCategory/addpage.html', {'form': form, 'menu': menu, 'title': 'Adding of page'})

# def contact(request):
#   return HttpResponse("Call back")

class ContactFormView(DataMixin, FormView):
  form_class = ContactForm
  template_name = 'ProgrammingCategory/contact.html'
  success_url = reverse_lazy('home')

  def get_context_data(self, *, object_list=None, **kwargs):
      context = super().get_context_data(**kwargs)
      c_def = self.get_user_context(title="Call back")
      return dict(list(context.items()) + list(c_def.items()))
  
  def form_valid(seld, form):
    print(form.cleaned_data)
    return redirect('home')


# def login(request):
#   return HttpResponse("To Avtorize")

def pageNotFound(request, exception):
  return HttpResponseNotFound('<h1>Site not found</h1>')
  
# def show_post(request, post_slug):
#   post = get_object_or_404(Developer, slug=post_slug)
  
#   context = {
#     'post': post,
#     'menu': menu,
#     'title': post.title,
#     'cat_selected': post.cat_id,
#   }
  
#   return render(request, 'ProgrammingCategory/post.html', context=context)

class ShowPost(DataMixin, DetailView):
  model = Developer
  template_name = 'ProgrammingCategory/post.html'
  slug_url_kwarg = 'post_slug'
  context_object_name = 'post'
  
  def get_context_data(self, *, object_list=None, **kwargs):
      context = super().get_context_data(**kwargs)
      c_def = self.get_user_context(title=context['post'])
      return dict(list(context.items()) + list(c_def.items()))
  

def show_category(request, cat_id):
  return HttpResponse(f"Showes of category with id = {cat_id}")

class DeveloperCategory(DataMixin, ListView):
  model = Developer
  template_name = 'ProgrammingCategory/index.html'
  context_object_name = 'posts'
  allow_empty = False
  
  def get_queryset(self):
    return Developer.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
  
  def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c = Category.objects.get(slug=self.kwargs['cat_slug'])
    c_def = self.get_user_context(title='Category - ' + str(c.name),
      cat_selected=c.pk)
    return dict(list(context.items()) + list(c_def.items()))
  
# def show_category(request, cat_id):
#   posts = Developer.objects.filter(cat_id=cat_id)
  
#   if len(posts) == 0:
#     raise Http404()
  
#   context = {
#     'posts': posts,
#     'menu': menu,
#     'title': 'Shows by rubrics',
#     'cat_selected': cat_id,
#   }
  
#   return render(request, 'ProgrammingCategory/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
  form_class = RegisterUserForm
  template_name = 'ProgrammingCategory/register.html'
  success_url = reverse_lazy('login')

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c_def = self.get_user_context(title="Registration")
    return dict(list(context.items()) + list(c_def.items()))

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return redirect('home')


class LoginUser(DataMixin, LoginView):
  form_class = LoginUserForm
  template_name = 'ProgrammingCategory/login.html'

  def get_user_context(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c_def = self.get_user_context(title="Avtorisetion")
    return dict(list(context.items()) + list(c_def.items()))
  
  def get_success_url(self):
    return reverse_lazy('home')


def logout_user(request):
  logout(request)
  return redirect('login')
