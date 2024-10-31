from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>", views.BlogView.as_view(), name="Blog_detail"),
    path("author/<str:fname>", views.render_author, name="Author_detail"),
    path("tag/<slug:slug>",views.render_tag,name="Tag_detail")
]
