from django.db import models


class ExcelUpload(models.Model):
    excel = models.FileField()

    class Meta:
        db_table = 'excel_files'


class DataLog(models.Model):
    data_str = models.TextField()
    item_count = models.IntegerField()
    index = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        db_table = 'data_log'
