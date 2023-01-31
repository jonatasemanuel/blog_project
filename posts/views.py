from django.shortcuts import redirect, get_object_or_404, render
from django.views import View

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
        termo = self.request.GET.get('termo')

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


class PostDetails(View):
    template_name = 'posts/post_details.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, published_post=True)
        self.context = {
            'post': post,
            'comments': Comment.objects.filter(post_comment=post,
                                               published_comment=True),
            'form': FormComment(request.POST or None),
        }
    
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = self.context['form']
        if not form.is_valid():
            return render(request, self.template_name, self.context)

        comment = form.save(commit=False)
        
        if request.user.is_authenticated:
            comment.user_comment = request.user
        
        comment.post_comment = self.context['post']
        comment.save()
        messages.success(request, 'Your comments stages to review')
        return redirect('details', pk=self.kwargs.get('pk'))
            
        

"""class PostDetails(UpdateView):
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
        return redirect('details', pk=post.id)"""