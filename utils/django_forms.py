import re
from django.core.exceptions import ValidationError

# Nesta função receberemos um campo, o widget que será alterado e o novo valor deste widget # noqa
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# esta função recebe um campo e uma string pare redefinir o placeholder
# Neste caso não re reescrevemos um field, apenas adicionamos imformações a ele
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


# Função para validação através de validators
def strong_password(password):
    # aqui será checado se existem letras de a-z minusculas, letras de A-Z maiusculas, números de 1-9 e se tem no mínimo 8 caracteres # noqa
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    # Se a senha não corresponder aos requisitos
    if not regex.match(password):

        raise ValidationError((
            'Sua senha deve conter '
            'no mínimo 8 caracteres '
            'letras maiusculas minúsculas e números'
        ),
            code='invalid'
        )
