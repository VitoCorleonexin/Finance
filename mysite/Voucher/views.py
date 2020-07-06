from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import AccountDetail,Account,Subject as subject_parent,SubjectDetail as subject_child
from .forms import SubjectForm, BaseSubjectDetailFormSet, SubjectDetialForm,DivErrorList,SubjectModelForm,SubjectFormSetHelper, AccountModelForm
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
import pdb
import datetime

# Create your views here.

def manage_subject(request,pk):
    success = ''
    entity = subject_parent.objects.get(pk=pk)
    form = SubjectModelForm(instance=entity)
    detailInlineFormSet = inlineformset_factory(subject_parent,subject_child,fields=('name','code', 'id'), can_delete=True) 
    formset = detailInlineFormSet(instance=entity)
    if request.method == 'POST':
        form = SubjectModelForm(request.POST, instance=entity)
        if form.is_valid():
            updated_obj = form.save(commit=False)
            formset = detailInlineFormSet(request.POST, instance=updated_obj)
            if formset.is_valid():
                updated_obj.save()
                formset.save()
                if 'saveadd' in request.POST:
                    success = '/subject/' + str(pk)
                elif 'update' in request.POST:
                    success = '/subject/'
                return HttpResponseRedirect(success)
    return render(request,'Voucher/subject_modifation.html',{'form':form,'formset':formset})
    


def subject_search(request):
    
    con = ''
    num_page = '1'
    if request.POST:
        con = request.POST.get('condition', '') 
    elif request.GET:
        con = request.GET.get('condition', '') 
        num_page = request.GET.get('page', 1) 
    entity = subject_parent.objects.filter(Q(name__contains=con) | Q(code__contains=con) | Q(category__contains=con))
    data_list = do_paginate(entity,num_page) 
    base_url = 'subject/filter/?condition=' + con + '&'
    return render(request,'Voucher/subjectList.html',{'page_obj': data_list, 'base_url': base_url})


def account_search(request):
    
    con = ''
    num_page = '1'
    if request.POST:
        con = request.POST.get('condition', '') 
    elif request.GET:
        con = request.GET.get('condition', '') 
        num_page = request.GET.get('page', 1) 
    entity = Account.objects.filter(Q(id__contains=con) | Q(producer__contains=con) )
    data_list = do_paginate(entity,num_page) 
    base_url = 'account/filter/?condition=' + con + '&'
    return render(request,'Voucher/accountList.html',{'page_obj': data_list, 'base_url': base_url})



def subjectList(request):
    
    entity = subject_parent.objects.all()
    num_page = request.GET.get('page', 1)
    data_list = do_paginate(entity,num_page)    
    base_url = '/subject/?'
    return render(request,'Voucher/subjectList.html',{'page_obj': data_list, 'base_url': base_url})



def accountList(request):
    entity = Account.objects.all()
    num_page = request.GET.get('page', 1)
    data_list = do_paginate(entity, num_page)
    base_url = '/account/?'
    return render(request, 'Voucher/accountList.html', {'page_obj': data_list, 'base_url':base_url})


def account_create(request):
    detailInlineFormSet = inlineformset_factory(Account, AccountDetail, fields=('content', 'account_sub','account','debit', 'credit'), extra=5)
    if request.method == 'POST':
        form = AccountModelForm(request.POST)
        formset = detailInlineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            created_parent = form.save()
            formset.instance = created_parent
            formset.save()
            return HttpResponseRedirect('/account/')
    else:
        formset = detailInlineFormSet()
        form = AccountModelForm()
    return render(request, 'Voucher/account_form.html', {'formset': formset, 'form': form})



def subject(request):
    detailInlineFormSet = inlineformset_factory(subject_parent,subject_child,fields=('name','code'), extra=3) 
    helper = SubjectFormSetHelper()
    if request.method == 'POST':
        form = SubjectModelForm(request.POST) 
        formset = detailInlineFormSet(request.POST)
        if  form.is_valid() and  formset.is_valid():
           created_parent = form.save()
           formset.instance = created_parent
           formset.save()
           return HttpResponseRedirect('/subject/')
    else:
        formset = detailInlineFormSet()
        form = SubjectModelForm()
    return render(request, 'Voucher/subject_form.html',{'formset':formset, 'form': form, 'helper': helper})



#def subject(request):
#    subjectdetail_formset = formset_factory(SubjectDetialForm, formset=BaseSubjectDetailFormSet,extra=3)
#    if request.method == 'POST':
#        form = SubjectForm(request.POST)
#        formset = subjectdetail_formset(request.POST)
#        if formset.is_valid() and form.is_valid():
#            parent_name = form.cleaned_data.get('name')
#            parent_code = form.cleaned_data.get('code')
#            parent_category = form.cleaned_data.get('category')
#            entity = Subject.objects.create(name=parent_name, code=parent_code, category=parent_category)
#            entity.save()
#            for form in formset:
#                child_name = form.cleaned_data.get('name')
#                child_code = form.cleaned_data.get('code')
#                child = subject_child.objects.create(name=child_name, code=child_code, subject=entity)
#                child.save()
#            return HttpResponseRedirect('/thanks/')
#
#    else:
#        formset = subjectdetail_formset()
#        form = SubjectForm()
#    return render(request,'Voucher/subject_create.html',{'formset': formset, 'form':form})
#
#

def index(request):
    return render(request,'Voucher/base.html')


class SubjectListView(LoginRequiredMixin, ListView):
    model = subject_parent
    template_name = 'Voucher/subjectList.html'
    context_object_name = 'subjects'
    paginate_by = 5



def do_paginate(data_list, num_page):
    
    # the number of per page
    num_per_page = 5

    paginator = Paginator(data_list, num_per_page)

    re_data_list = paginator.get_page(num_page)

    return re_data_list







