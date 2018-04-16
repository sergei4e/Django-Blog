# -*- coding: utf_8 -*-
from django.contrib.auth.models import User
from django.db import models
from datetime import date as dt
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1023, blank=True)
    h1 = models.CharField(max_length=255, blank=True)
    short = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    h1 = models.CharField(max_length=255)
    img = models.ImageField(max_length=255, upload_to='images', default='no-image.jpg')
    short = models.TextField()
    post = models.TextField()
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1023, blank=True)
    author = models.CharField(max_length=255, default='Admin')
    date = models.DateField(blank=True, default=dt.today().isoformat())
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=255, blank=True)
    source = models.URLField(max_length=1024, blank=True)
    automatic = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.h1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.h1)
        if not self.title:
            self.title = self.h1
        if not self.description:
            self.description = self.short[:200]
        super().save(*args, **kwargs)


class Page(models.Model):
    h1 = models.CharField(max_length=255)
    content = models.TextField()
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1023, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.h1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.h1)
        if not self.title:
            self.title = self.h1
        super().save(*args, **kwargs)
