# O render é importado para ser retornado posteriormente ele recebe request como primeiro parametroe pode retornar HTML, e receber variáveis para serem usadas no template    # noqa

# o get_list e o get_ object ambos recebem uma lista ou um objeto, caso n seja encontrado nada, ele irá retornar um erro 404 para não quebrar a sua aplicação    # noqa

from django.shortcuts import render, get_list_or_404, get_object_or_404
from . models import Recipe
from django.http import Http404
# Este import é para que o django consiga usar um OR em uma busca por titulo ou descrição que estejam contidos em uma receita   # noqa
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):

    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    # A variável recebe uma query string chamada 'page' caso nela não exista nada retornara o valor 1 # noqa
    current_page = request.GET.get('page', 1)
    # A variável recebe um objeto paginator que irá retornar os objetos 'recipes' de acordo com a quantidade definida no segundo parâmetro # noqa
    paginator = Paginator(recipes, 6)
    # A variável recebe o objeto que irá retornar uma página, como no parâmetro está sendo passado o 'current_page' a página exibida será determinada pelo valor da query string nele atribuida # noqa
    page_obj = paginator.get_page(current_page)

    return render(request, 'recipes/pages/home.html', context={
        # Aqui é atribuido ao valor 'recipes' o page_obj que irá retornar as páginas de acordo com a regra de paginação definida a cima # noqa
        'recipes': page_obj,
    })


def category(request, category_id):
    # recipes recebe todos os objetos de Recipe filtrados por(que tenham o mesmo id de category, e que estejam publicados) os objetos serão ordenados por ordem decrescente dos ID    # noqa
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))    # noqa

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}  - Category'
    })


def recipe(request, id):
    # Lembre-se que os filtros não são pk recebe id, mas se pk for igual ao id, ou seja etá mais pra um if do que um recebe    # noqa
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'contador': recipe,
        'is_detail_page': True,
    })


def search(request):
    # A variável recebe o valor de "q" através da chave que é o próprio 'q', Buscando desta forma a variável receberá uma string vazia caso o seu valor não exista ao invés d retornar um erro   # noqa
    # O "strip()" é uma função do próprio python que serve para remover espaços laterais de uma string  # noqa
    search_term = request.GET.get('q', '').strip()
    # Caso a variável não contenha nenhum valor ou seu valor seja semelhante a falso    # noqa
    if not search_term:
        # Ele irá retornar um status_code de 404
        raise Http404()

    receitas = Recipe.objects.filter(
        # Aqui é usado esta função para que no banco de dados possa ser realizada a busca caso uma das duas condições seja verdade, ou seja um OR, ao invés de buscar somente se as duas condições forem verdadeiras, um AND que é o que o django faria por padrão caso não fosse usado nenhum recurso  # noqa

        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),

        is_published=True
    ).order_by('-id')

    # A página só será renderisada se a condição acima for falsa
    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for {search_term}',
        'search_term': search_term,
        'recipes': receitas,
    })
