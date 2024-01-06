from django import forms
from orders.models import Article, Delivery


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class deliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'