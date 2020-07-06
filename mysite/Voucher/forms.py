from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
import datetime
from django.forms import ModelForm, formset_factory, inlineformset_factory, BaseFormSet
from .models import Account,Subject, SubjectDetail
from django.forms.utils import ErrorList
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit




class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])

class AccountForm(ModelForm):

    class Meta:
        model = Account
        fields = ['account_date', 'producer', 'audit']



class SubjectModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'

  


    class Meta:
        model = Subject
        fields = ['name', 'category', 'code']
        #widgets = {'name': forms.TextInput(attrs=({'class':'form-control'})),'code': forms.TextInput(attrs=({'class':'form-control'})),'category':forms.Select(attrs=({'class':'form-control custom-select-sm custom-select'}))}
        



class AccountModelForm(ModelForm):
    class Meta:
        model = Account
        exclude = ['account_date']
        




class BaseSubjectDetailFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two subjects have the same
        name or the same code."""


        if any(self.errors):
            # Don't bother validating the formset unless
            # ehch form is valid on its own
            return
        names = []
        codes = []
        for form in self.forms:
            name = form.cleaned_data.get('name')
            code = form.cleaned_data.get('code')
            if name in names or code in codes:
                raise forms.ValidationError('科目名称、编码不能重复.')
            if SubjectDetail.objects.filter(Q(name__exact=name) | Q(code__exact=code)).exists():
                raise forms.ValidationError('子科目已存在相同科目名称或编码')


            names.append(name)
            codes.append(code)

        



class SubjectDetialForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control'})),max_length=50, label='科目名称')
    code = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control'})),max_length=50, label='科目编码')
    error_class = DivErrorList





class SubjectForm(forms.Form):
    SUBJECT_CATEGORY_CHOICES = [(None,'请选择'),('debit','借'),('credit','贷'),]
    name = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control'})),max_length=50, label='科目名称')
    category = forms.ChoiceField(widget=forms.Select(attrs=({'class':'form-control custom-select-sm custom-select'})),choices=SUBJECT_CATEGORY_CHOICES, label='科目类型')
    code = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control'})),max_length=50, label='科目编码')


    def clean(self):
        super().clean()
        name = self.cleaned_data.get('name')
        code = self.cleaned_data.get('code')
        if Subject.objects.filter(Q(name__exact= name) | Q(code__exact= code)).exists():
            raise forms.ValidationError('已存在相同的科目名称或科目编码') 




class SubjectFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.label_class = 'col-lg-2'
        self.field_class = 'col-lg-6'
        self.disable_csrf = True 
        #self.template = 'bootstrap/table_inline_formset.html' 

