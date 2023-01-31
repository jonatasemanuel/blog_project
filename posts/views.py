from django.shortcuts import redirect

from .models import Post
from comments.models import Comment

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(published_post=True)
        qs = qs.annotate(
            num_comments=Count(
                Case(
                    When(comment__published_comment=True,  then=1)
                )
            )
        )

        return qs

class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.resquest.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(title_post__icontains=termo) |
            Q(author_post__username__iexact=termo) |
            Q(content_post__icontains=termo) |
            Q(excerpt_post__icontains=termo) |
            Q(categorie_post__name_categorie__iexact=termo)
        )

        return qs




class PostCategories(PostIndex):
    template_name = 'posts/post_categories.html'

    def get_queryset(self):
        qs = super().get_queryset()
        
        categorie = self.kwargs.get('categorie', None)

        if not categorie:
            return qs
        
        qs = qs.filter(categorie_post__name_categorie_iexact=categorie)

        return qs


class PostDetails(UpdateView):
    template_name = 'posts/post_details.html'
    model = Post
    form_class = FormComment
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(published_comment=True,
                                          post_comment=post.id)
        context['comments'] = comments
        return context
    
    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.post_comment = post
        
        if self.request.user.is_authenticated:
            comment.user_comment = self.request.user
        
        comment.save()
        messages.success(self.request, 'Good')
        return redirect('details', pk=post.id)