from django.db import models
from django.urls import reverse
from uuslug import uuslug
from django.contrib.auth.models import User
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Entry(SortableMixin):
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, editable=False)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    initial_date = models.DateField()
    final_date = models.DateField()

    class Meta:
        ordering  = ['order', 'slug']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Entry, self).save(*args, **kwargs)

class Post(SortableMixin):
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, editable=False)
    text = models.TextField()
    author = models.ForeignKey(User)
    entry = SortableForeignKey(Entry)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    class Meta:
        ordering  = ['order', 'slug']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])
