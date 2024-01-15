from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

# Create your views here.


def register_view(request):
    # Recebe o formulário que foi armazenado na session caso não exista nada receberá o None retornado # noqa
    register_form_data = request.session.get('register_form_data', None)
    # Esta variável recebe um objeto de formulário que foi criado no arquivo form.py deste app. E este objeto recebe os dados da variável a cima # noqa
    form = RegisterForm(register_form_data)
    # Retorna o template de registro e as informações salvas na session no contexto # noqa
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    # Se o usuário tentar acessar esta view diretamento por um methodo que não seja POST isso retornará um erro 404 # noqa
    if not request.POST:
        raise Http404()
    # Esta constante recebe os dados do formulário que foram passados na página HTML e ela foi definida como receptora desses dados na Action fo formulário da página # noqa
    POST = request.POST
    # Aqui criamos uma nova chave dentro da nossa session chamada de register_form_data, e essa chave irá receber todos os dados da constante POST # noqa
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    # validação para salvar dados na base de dados
    # se o formulário for válido
    if form.is_valid():
        # as informações do formulário serão salvas na base de dados (se tiver sem o commit=False)
        user = form.save(commit=False)
        # Aqui está sendo configurado o campo de senha para ser criptografado e salvo na base de dados
        user.set_password(user.password)
        user.save()
        # returna uma mensagem de sucesso ao salvar os dados
        messages.success(request, 'Usuário criado com sucesso !')
        # deleta os dados da session
        del (request.session['register_form_data'])

    # Aqui á view redireciona para a view a cima "register_view" e na outra view esses dados da session serão recebidos # noqa
    return redirect('authors:register')

def login_view(request):

    return render(request, 'authors/pages/login.html')

def login_create(request):

    return render(request, 'authors/pages/login.html')