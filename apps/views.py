from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView

from apps.forms import RegisterForm, EmailForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category, Email
from django.shortcuts import render, redirect




class BlogListView(ListView):
    paginate_by = 5
    template_name = 'apps/blogs/blog-list.html'
    queryset = Blog.objects.order_by('-id')
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get('search'):
            return queryset.filter(name__icontains=search)
        return queryset


class BlogDetailView(DetailView):
    queryset = Blog.objects.order_by('-created_at')
    template_name = 'apps/blogs/blog-detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = self.get_queryset()[:3]
        return context


class IndexView(TemplateView):
    template_name = 'apps/index.html'


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login.html'
    next_page = 'index_page'


class RegisterFormView(FormView):
    template_name = 'apps/login.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProcessEmailView(View):
    template_name = 'apps/base.html'
    form_class = EmailForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email already exists in the database
            if not Email.objects.filter(email=email).exists():
                # If not, save the email to the database
                Email.objects.create(email=email)

            # You can add further logic or redirect the user as needed
            return redirect('index_page')

        return render(request, self.template_name, {'form': form})


