# Create your models here.


from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# study modules
# class Person(models.Model):
#     db_table = '"table_person"'
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)


# Musician, Album
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()


# person, group, membership
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


# one to one field
# from geography.models import ZipCode
# class Restaurant(models.Model):
#     zip_code = models.ForeignKey(
#         ZipCode,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#     )


# Meta options
class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"


# abstract base classes
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta):
        db_table = 'student_info'


# related name and related auery name
# class Base(models.Model):
#     m2m = models.ManyToManyField(
#         OtherModel,
#         related_name="%(app_label)s_%(class)s_related",
#         related_query_name="%(app_label)s_%(class)ss",
#     )
#
#     class Meta:
#         abstract = True
#
# class ChildA(Base):
#     pass
#
# class ChildB(Base):
#     pass


# proxy models
# class Person(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#
# class MyPerson(Person):
#     class Meta:
#         proxy = True
#
#     def do_something(self):
#         # ...
#         pass


# blog, author, entry
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline


'''
queries

# 1
b2 = Blog.objects.get(name="New2")

# 2
>>> Entry.objects.filter(headline__startswith='Entry').exclude(pub_date__gte=datetime.date.today()).filter(pub_date__gte=datetime.date(2020,
 3, 31))
<QuerySet [<Entry: Entry 1>]>
>>>

# 3
>>> Entry.objects.filter(headline__startswith='Entry')[0]
<Entry: Entry 1>
>>> Entry.objects.filter(headline__startswith='Entry')[0].pub_date
datetime.date(2020, 3, 31)
>>> Entry.objects.filter(headline__startswith='Entry')
<QuerySet [<Entry: Entry 1>, <Entry: Entry2>, <Entry: Entry3>]>
>>> Entry.objects.filter(headline__startswith='Entry')[1].pub_date
datetime.date(2020, 4, 1)
>>> Entry.objects.filter(headline__startswith='Entry')[2].pub_date
datetime.date(2020, 3, 30)
>>>

# 4
>>> q1 = Entry.objects.filter(headline__startswith="What")
>>> q2 = q1.exclude(pub_date__gte=datetime.date.today())
>>> q3 = q1.filter(pub_date__gte=datetime.date.today())

# 5
Entry.objects.filter(blog_id=1)

# 6 SQL JOINs
Entry.objects.filter(blog__name='New name')

# 7  F()
>>> from django.db.models import F
>>>
>>> Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
<QuerySet [<Entry: Entry3>]>
>>>

Entry.objects.filter(rating__lt=F('number_of_comments') + F('number_of_pingbacks'))

# 8 
>>> from datetime import timedelta
>>> Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))
<QuerySet []>
>>>


# 9 
>>> Blog.objects.get(id__exact=3)
<Blog: New3>
>>> Blog.objects.get(id=3)
<Blog: New3>
>>> Blog.objects.get(pk=3)
<Blog: New3>
>>>


# 10 
>>> Blog.objects.filter(pk__in=[1,2,3])
<QuerySet [<Blog: New name>, <Blog: New2>, <Blog: New3>]>
>>> Blog.objects.filter(pk__in=[1,2,4])
<QuerySet [<Blog: New name>, <Blog: New2>]>
>>>


# 11
>>> Entry.objects.filter(blog__id__exact=1)
<QuerySet [<Entry: Entry 1>, <Entry: Entry3>]>
>>> Entry.objects.filter(blog__id=1)
<QuerySet [<Entry: Entry 1>, <Entry: Entry3>]>
>>> Entry.objects.filter(blog__pk=1)
<QuerySet [<Entry: Entry 1>, <Entry: Entry3>]>
>>>


# 12
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

# 13
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset])
['Entry 1', 'Entry2', 'Entry3']
>>>
>>>
>>> print([p.pub_date for p in queryset])
[datetime.date(2020, 3, 31), datetime.date(2020, 4, 1), datetime.date(2020, 3, 30)]
>>>


# 14b

'''