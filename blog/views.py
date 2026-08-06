from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article

# جزئیات مقاله
from django.shortcuts import render, get_object_or_404

def article_list(request):
    articles_qs = Article.objects.filter(is_published=True).order_by("-created_at")


    paginator = Paginator(articles_qs, 6)
    page_number = request.GET.get('page', 1)

    try:
        articles_page = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        articles_page = paginator.get_page(1)


    current_page = articles_page.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + 4)

    if end_page - start_page < 4:
        start_page = max(1, end_page - 4)

    page_range = range(start_page, end_page + 1)

    context = {
        "articles": articles_page,
        "page_range": page_range,
        "total_pages": total_pages,
        "title": "مقالات",
    }

    return render(request, "blog/article_list.html", context)



def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )

    latest_articles = (
        Article.objects.filter(is_published=True)
        .exclude(id=article.id)
        .order_by("-created_at")[:4]
    )

    context = {
        "article": article,
        "latest_articles": latest_articles,
    }

    return render(request, "blog/detail_article.html", context)