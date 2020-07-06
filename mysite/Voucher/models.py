from django.db import models
from django.urls import reverse

# Create your models here.


SUBJECT_CATEGORY_CHOICES=[('debit','借'),
                          ('credit','贷'),]




class Account(models.Model):
    account_date = models.DateField(verbose_name='记账日期')
    file_count = models.IntegerField(null=True)
    sum_total = models.CharField(max_length=50, verbose_name='合计')
    sum_de = models.DecimalField(max_digits=10, decimal_places=2)
    sum_cr = models.DecimalField(max_digits=10, decimal_places=2)
    producer = models.CharField(max_length=50)
    audit = models.CharField(max_length=50)
    cashier = models.CharField(max_length=50)







class AccountDetail(models.Model):
    voucher = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    account_sub = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    debit = models.DecimalField(max_digits=10, decimal_places=2)
    credit = models.DecimalField(max_digits=10, decimal_places=2)






class Subject(models.Model):
    name = models.CharField(max_length=50,verbose_name='科目名称', unique=True)
    code = models.CharField(max_length=50, verbose_name='科目编码', unique=True)
    category = models.CharField(max_length=20,verbose_name='类别', choices=SUBJECT_CATEGORY_CHOICES)
     

    class Meta:
        verbose_name = '会计科目'
        verbose_name_plural = '会计科目'


    def __str__(self):
        return self.name + "-" + self.code

    
    def get_absolute_url(self):
        return reverse('voucher:subject-detail', kwargs={'pk': self.pk})


class SubjectDetail(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='科目名称')
    code = models.CharField(max_length=50, verbose_name='科目编码', unique=True)

    class Meta:
        verbose_name = '二级会计科目'
        verbose_name_plural = '二级会计科目'
