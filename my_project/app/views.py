from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from app.models import Post


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.all()
    return render(
        request,
        "app/index.html",
        {
            "post_list": qs
        }
    )


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)  # 예외처리
    return render(request, "app/post_detail.html", {
        "post": post
    })
