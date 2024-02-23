from django.shortcuts import render, redirect
from . forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
# Import usado para autenticação login e logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    # Esta constante recebe os dados do formulário que foram passados na página HTML e ela foi definida como receptora desses dados na Action do formulário da página ou seja POST recebe os dados passados no formulário na requisição # noqa
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
        messages.success(request, 'Usuário criado com sucesso, faça login na aplicação!')
        # deleta os dados da session
        del (request.session['register_form_data'])

        return redirect('authors:login')
    else:
        # Aqui á view redireciona para a view a cima "register_view" e na outra view esses dados da session serão recebidos # noqa
        return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    login_url = reverse('authors:login')
    # Lembre-se de usar o requesr.POST sempre que quiser receber os dados do formulário # noqa
    form = LoginForm(request.POST)

    # Lembre-se de que esta parte não checa se o usuário está cadastrado, apenas checa se os dados informados nos campos são válidos # noqa

    # Esta linha verifica se os dados submetidos no formulário são válidos de acordo com as regras definidas no próprio formulário (LoginForm). # noqa
    if form.is_valid():
        # Esta linha tenta autenticar o usuário utilizando a função authenticate do Django. Retorna o nome de usuário # noqa 
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Log-in realizado com sucesso!')
            #  A função login é utilizada para efetuar o login do usuário autenticado. Isso cria uma sessão para o usuário no servidor, permitindo que ele permaneça autenticado em requisições subsequentes. # noqa

            # Além do user devemos sempre colocar o parametro "request" para que este usuário seja atrelado a requisição e seja enviado para que possamos enviar o usuário para o template, criar kookies entre outras coisas mais # noqa
            login(request, authenticated_user)
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    else:
        messages.error(request, 'Erro ao validar os dados do formulário.')

    return redirect(login_url)

# Este decorator é usado para declarar que está view só pode ser acessada se o login estiver feito. No primeiro parâmetro "login_url" é passado a url para qual o usuário será redirecionado caso tente acessar esta view sem fazer login # noqa

# O segundo parâmetro indica o nome do campo que será usado para armazenar a URL à qual o usuário será redirecionado após o login bem-sucedido. # noqa
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):

    if not request.POST:
        # Caso o usuário tente acessar o logout pela url ele retornará para a mesma página, pois como ele está logado continuará logado e na mesma página # noqa
        return redirect(reverse('authors:login'))
    # Testa se o usuário que está enviando a requisição POST para sair é o mesmo usuário que está logado # noqa
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))
