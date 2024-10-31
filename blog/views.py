from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseNotFound, HttpRequest
from django.shortcuts import get_object_or_404
from . import models
from django.views import View
from .forms import BlogForm, CommentForm, LoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.

# data = {
#     "Top Movies 2024": "2024 is shaping up to be a great year for movies. From action-packed blockbusters to thought-provoking dramas, there's something for everyone. Check out our list of the top 10 must-watch films of the year.",
#     "Rise of Esports": "Esports has grown from a niche hobby to a global phenomenon. Discover how competitive gaming has become a major industry and the impact it's having on traditional sports and entertainment.",
#     "Social Media Evolution": "Social media has transformed the way we communicate and share information. This blog explores the evolution of major social media platforms, their impact on society, and what the future might hold.",
#     "Celebrity Gossip": "Stay updated with the latest celebrity gossip and entertainment news. From high-profile breakups to new movie releases, get all the juicy details here.",
#     "AI in News": "AI is changing the landscape of journalism. Learn how artificial intelligence is being used to gather, analyze, and report news, and what this means for the future of journalism.",
#     "2024 Sports Highlights": "Catch up on the most exciting moments in sports for 2024. From record-breaking performances to major upsets, we've got all the highlights covered.",
#     "Best TV Shows": "Looking for something to watch? Check out our recommendations for the best TV shows to binge-watch this summer. Whether you love drama, comedy, or sci-fi, there's something here for everyone.",
#     "Influencer Marketing": "Influencers have become a powerful force in marketing. Explore how social media influencers are reshaping advertising strategies and what this means for brands and consumers alike.",
#     "Bharateeyudu-2 review": "With zero expectations it's one time watchable, but with high expectations you will feel bored",
# }


# def render_blog(request, slug):
#     blog = get_object_or_404(models.Blog, slug=slug)
#     tags = blog.tags.all()
#     return render(
#         request,
#         "blog/blog.html",
#         {
#             "blog": blog,
#             "tags": tags,
#         },
#     )


def checkLogin(request):
    if request.session.get("logged_in") in [None, False]:
        return HttpResponseRedirect(reverse_lazy("login"))


class BlogView(View):
    def get(self, request, slug):
        login_check = checkLogin(request)
        if login_check:
            return login_check
        blog = get_object_or_404(models.Blog, slug=slug)
        comments = blog.comments.all()
        tags = blog.tags.all()
        form = CommentForm()
        return render(
            request,
            "blog/blog.html",
            {
                "blog": blog,
                "comments": comments,
                "form": form,
                "tags": tags,
            },
        )

    def post(self, request, slug):
        login_check = checkLogin(request)
        if login_check:
            return login_check
        blog = get_object_or_404(models.Blog, slug=slug)
        comments = blog.comments.all()
        tags = blog.tags.all()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = models.Comment(comment=form.cleaned_data["comment"], blog=blog)
            comment.save()
            form = CommentForm()
        return render(
            request,
            "blog/blog.html",
            {
                "blog": blog,
                "comments": comments,
                "form": form,
                "tags": tags,
            },
        )


def render_author(request, fname):
    login_check = checkLogin(request)
    if login_check:
        return login_check
    auth = get_object_or_404(models.Author, fname=fname)
    blogs = auth.blogs_written.all()
    return render(
        request,
        "blog/author.html",
        {
            "auth": auth,
            "blogs": blogs,
        },
    )


def render_tag(request, slug):
    login_check = checkLogin(request)
    if login_check:
        return login_check
    tag = get_object_or_404(models.Tag, slug=slug)
    blogs = tag.posts.all()
    return render(
        request,
        "blog/tag.html",
        {
            "tag": tag,
            "blogs": blogs,
        },
    )


def index(request):
    login_check = checkLogin(request)
    if login_check:
        return login_check
    blogs = models.Blog.objects.all()
    return render(
        request,
        "blog/index.html",
        {
            "blogs": blogs,
        },
    )


def home(request):
    login_check = checkLogin(request)
    if login_check:
        return login_check
    return render(request, "home.html")


class AddBlogView(View):
    def get(self, request):
        login_check = checkLogin(request)
        if login_check:
            return login_check
        form = BlogForm()
        return render(
            request,
            "blog/add_blog.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        login_check = checkLogin(request)
        if login_check:
            return login_check
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(
                request,
                "thank_you.html",
            )
        else:
            return render(
                request,
                "blog/add_blog.html",
                {
                    "form": form,
                },
            )


def bestHash(password):
    # python int connot be stored in sqlite too large!
    # hash = 0
    # for ch in password:
    #     hash = hash * 101 + ord(ch)
    # return hash
    p = 29
    m = 4213
    hash = 0
    power = 1
    for ch in password:
        hash = hash + ((ord(ch) % m) * (power % m)) % m
        power = power * p
    return hash


class SignUpView(View):
    def get(self, request):
        form = LoginForm()
        return render(
            request,
            "blog/signup.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if len(models.Credential.objects.filter(username=username)) > 0:
                exists = True
                return render(
                    request,
                    "blog/signup.html",
                    {
                        "form": form,
                        "exists": exists,
                    },
                )
            else:
                hash = bestHash(form.cleaned_data["password"])
                models.Credential.objects.create(username=username, password=hash)
                return HttpResponseRedirect(reverse_lazy("login"))
        return render(
            request,
            "blog/signup.html",
            {
                "form": form,
            },
        )


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(
            request,
            "blog/login.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = models.Credential.objects.filter(
                username=form.cleaned_data["username"]
            )
            if len(username) == 0:
                return render(
                    request,
                    "blog/login.html",
                    {
                        "form": form,
                        "no_user": True,
                    },
                )
            elif len(username) == 1:
                hash = bestHash(form.cleaned_data["password"])
                if models.Credential.objects.get(username=username[0]).password == hash:
                    request.session["logged_in"] = True
                    return HttpResponseRedirect(reverse_lazy("home"))
                else:
                    return render(
                        request,
                        "blog/login.html",
                        {
                            "form": form,
                            "invalid_pass": True,
                        },
                    )
            else:
                raise Http404


class AuthorCreateView(CreateView):
    model = models.Author
    template_name = "blog/add_author.html"
    fields = "__all__"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        login_check = checkLogin(request)
        if login_check:
            return login_check
        return super().dispatch(request, *args, **kwargs)


def logout(request):
    request.session["logged_in"] = False
    return HttpResponseRedirect(reverse_lazy("login"))
