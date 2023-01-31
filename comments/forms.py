from django.forms import ModelForm
from .models import Comment


class FormComment(ModelForm):
    def clean(self):
        data = self.cleaned_data
        name = data.get('name_comment')
        email = data.get('email_comment')
        comment = data.get('comment_comment')
         
    
    class Meta:
        model = Comment
        fields = ('name_comment', 'email_comment', 'comment_comment')