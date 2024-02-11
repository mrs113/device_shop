from django.db.models import Q

from .models import Product
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)


def q_search(query):
    if query.isdigit() and len(query) <= 5: #and len(query) != 3 or len(query) != 1:
        return Product.objects.filter(id=int(query))
    # else:
    #     return Product.objects.filter(phone_memory=int(query))

    # vector = SearchVector('name', 'phone_color')
    # query = SearchQuery(query)
    #
    # result = Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by('-rank')
    #
    # result = result.annotate(headline=SearchHeadline('name', query, start_sel='<span style="background-color: green;">', stop_sel='</span>',))
    # # 1e-20
    #
    # return result

    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()

    for token in keywords:
        q_objects |= Q(name__icontains=token)
        q_objects |= Q(phone_color__icontains=token)

    search = Product.objects.filter(q_objects)

    return search
