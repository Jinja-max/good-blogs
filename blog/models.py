from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# Create your models here.


# blog model
class Blog(models.Model):
    # this models primary key is id
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    # image = models.CharField(max_length=100)
    image = models.ImageField(
        _("relevant image"), upload_to="relevant_images", null=True, blank=True
    )
    date = models.DateField(_("date"), auto_now_add=True, blank=True)
    slug = models.SlugField(_("blog_slug"), blank=True, null=True)
    content = models.TextField(_("content"))
    author = models.ForeignKey(
        "blog.Author",
        null=True,
        verbose_name=_("this blog author"),
        on_delete=models.SET_NULL,
        related_name="blogs_written",
    )

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Blog_detail", kwargs={"slug": self.slug})

    def save(self):
        self.slug = slugify(self.title)
        return super().save()


# author model
class Author(models.Model):
    fname = models.CharField(_("first name"), max_length=30)
    lname = models.CharField(_("last name"), max_length=30)
    mail = models.EmailField(_("email address"), max_length=254)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        return f"{self.fname} {self.lname}"

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"fname": self.fname})


# Tag model
class Tag(models.Model):
    slug = models.SlugField(_("caption slug"))
    caption = models.CharField(_("tags of posts"), max_length=50)
    posts = models.ManyToManyField(
        "blog.Blog", verbose_name=_("posts with this tag"), related_name="tags"
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse("Tag_detail", kwargs={"slug": self.slug})

    def save(self):
        self.slug = slugify(self.caption)
        return super().save()


class Comment(models.Model):

    comment = models.TextField(_("comment"))
    time_stamp = models.DateTimeField(_("time stamp"),auto_now_add=True)
    blog = models.ForeignKey(
        "blog.Blog",
        verbose_name=_("respective blog"),
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return str(self.time_stamp)

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})


class Credential(models.Model):
    username = models.CharField(_("username"), max_length=50)
    password = models.BigIntegerField(_("password"))  

    class Meta:
        verbose_name = _("credential")
        verbose_name_plural = _("credentials")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("credential_detail", kwargs={"pk": self.pk})

     