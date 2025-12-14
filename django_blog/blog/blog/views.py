from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import RegisterForm, ProfileForm, PostForm
from .models import Post, Comment
from taggit.models import Tag   # <-- import Tag from taggit, not blog.models


# -------------------------
# Homepage
# -------------------------
def index(request):
    """Homepage view."""
    return render(request, 'blog/index.html', {'title': 'Home'})


# -------------------------
# Authentication
# -------------------------
@method_decorator(csrf_protect, name='dispatch')
class BlogLoginView(LoginView):
    """Login view using Django’s built-in LoginView."""
    template_name = 'blog/auth/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class BlogLogoutView(LogoutView):
    """Logout view using Django’s built-in LogoutView."""
    next_page = 'blog:index'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


@csrf_protect
def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('blog:index')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'blog/auth/register.html', {'form': form, 'title': 'Register'})


@login_required
@csrf_protect
def profile(request):
    """Profile management view for authenticated users."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('blog:profile')
        else:
            messages.error(request, "Update failed. Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/auth/profile.html', {'form': form, 'title': 'Profile'})


# -------------------------
# Post Views (CRUD)
# -------------------------
class PostListView(ListView):
    """List all posts."""
    model = Post
    template_name = 'blog/posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    """Show a single post with its comments."""
    model = Post
    template_name = 'blog/posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.all()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/posts/post_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post."""
    model = Post
    template_name = 'blog/posts/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.request.user == self.get_object().author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)


# -------------------------
# Comment Views (CRUD)
# -------------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Add a new comment to a post."""
    model = Comment
    fields = ['content']
    template_name = 'blog/comments/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        messages.success(self.request, "Comment added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit an existing comment."""
    model = Comment
    fields = ['content']
    template_name = 'blog/comments/comment_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = 'blog/comments/comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


# -------------------------
# Tag & Search Views
# -------------------------
class TagPostListView(ListView):
    """List posts filtered by a tag."""
    model = Post
    template_name = 'blog/tags/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = self.tag
        return ctx


class SearchResultsView(ListView):
    """Search posts by title, content, or tags."""
    model = Post
    template_name = 'blog/search/results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '').strip()
        return ctx
