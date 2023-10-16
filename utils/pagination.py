import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range: stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, queryset, per_page):
    # A variável recebe uma query string chamada 'page' caso nela não exista nada retornara o valor 1 # noqa
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    # A variável recebe um objeto paginator que irá retornar os objetos 'recipes' de acordo com a quantidade definida no segundo parâmetro # noqa
    paginator = Paginator(queryset, per_page)
    # A variável recebe o objeto que irá retornar uma página, como no parâmetro está sendo passado o 'current_page' a página exibida será determinada pelo valor da query string nele atribuida # noqa
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return page_obj, pagination_range
