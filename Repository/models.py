from django.db import models

# Create your models here.


class MD5(models.Model):

    file_source_md5 = models.CharField(max_length=32, verbose_name="file_source_md5", null=True, blank=True, unique=True)
    file_source_address = models.CharField(max_length=255, verbose_name="file_source_name", null=True, blank=True)
    file_pdf_md5 = models.CharField(max_length=32, verbose_name="file_pdf_md5", null=True, blank=True, unique=True)
    file_pdf_address = models.CharField(max_length=255, verbose_name="file_pdf_address", null=True, blank=True)
    
    def __str__(self):
        return self.file_source_md5