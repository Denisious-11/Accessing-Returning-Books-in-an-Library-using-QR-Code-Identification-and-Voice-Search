from django.db import models

# Create your models here.
class Requests(models.Model):
    r_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    age=models.CharField(max_length=255)
    email=models.CharField(max_length=255)

class Users(models.Model):
    u_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    age=models.CharField(max_length=255)
    email=models.CharField(max_length=255)

class Books(models.Model):
    b_id=models.IntegerField(primary_key=True)
    book_name=models.CharField(max_length=255)
    author_name=models.CharField(max_length=255)
    publication=models.CharField(max_length=255)
    year=models.CharField(max_length=255)
    rack_number=models.CharField(max_length=255)
    identifer=models.CharField(max_length=255)


class Book_issue(models.Model):
    issue_id=models.IntegerField(primary_key=True)
    b_id=models.CharField(max_length=255)
    book_name=models.CharField(max_length=255)
    rack_number=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    i_date=models.CharField(max_length=255)
    status=models.CharField(max_length=255)

class Book_return(models.Model):
    return_id=models.IntegerField(primary_key=True)
    issue_id=models.CharField(max_length=255)
    b_id=models.CharField(max_length=255)
    book_name=models.CharField(max_length=255)
    rack_number=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    i_date=models.CharField(max_length=255)
    r_date=models.CharField(max_length=255)
    status=models.CharField(max_length=255)