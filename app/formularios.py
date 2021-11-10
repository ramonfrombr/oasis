from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.fields.html5 import EmailField


# Create Login Form
class LoginForm(Form): 

    nome_usuario = StringField(
        '',
        [validators.length(min=1)],
        render_kw={
            'autofocus': True,
            'placeholder': 'Nome de usuário'}
    )
    
    
    senha = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Senha'})


class RegisterForm(Form):

    nome = StringField(
        '',
        [validators.length(min=3, max=50)],
        render_kw={
            'autofocus': True,
            'placeholder': 'Nome Completo'
        }
    )
    
    nome_usuario = StringField(
        '',
        [validators.length(min=3, max=25)],
        render_kw={'placeholder': 'Nome de Usuário'}
    )
    
    email = EmailField(
        '',
        [
            validators.DataRequired(),
            validators.Email(),
            validators.length(min=4, max=25)
        ],
        render_kw={'placeholder': 'Email'}
    )
    
    senha = PasswordField(
        '',
        [validators.length(min=3)],
        render_kw={'placeholder': 'Senha'}
    )
    
    telefone = StringField(
        '',
        [validators.length(max=15)],
        render_kw={'placeholder': 'Telefone'}
    )

class MessageForm(Form):  # Create Message Form
    conteudo = StringField(
        '',
        [validators.length(min=1)],
        render_kw={'autofocus': True}
    )

class OrderForm(Form):  # Create Order Form
    

    """
    Se tirar isto, vai bugar a página modal_pedido.html e as rotas do Blueprint 'seção'
    """
    produto_id = StringField(
        '',
        
       
    )


    nome = StringField(
        '',
        [validators.length(min=1), validators.DataRequired()],
        render_kw={
            'autofocus': True,
            'placeholder':
            'Nome Completo'
        }
    )
    
    telefone = StringField(
        '',
        [validators.length(min=1), validators.DataRequired()],
        render_kw={
            'autofocus': True,
            'placeholder': 'Telefone'
        }
    )
    
    quantidade = SelectField(
        '',
        [validators.DataRequired()],
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5')
        ]
    )

    pedido_local = StringField(
        '',
        [validators.length(min=1), validators.DataRequired()],
        render_kw={'placeholder': 'Local do Pedido'}
    )

class UpdateRegisterForm(Form):
    
    nome = StringField(
        'Nome Completo',
        [validators.length(min=3, max=50)],
        render_kw={
            'autofocus': True,
            'placeholder': 'Nome Completo'
        }
    )
    
    email = EmailField(
        'Email',
        [
            validators.DataRequired(),
            validators.Email(),
            validators.length(min=4, max=25)
        ],
        render_kw={'placeholder': 'Email'}
    )
    
    senha = PasswordField(
        'Senha',
        [validators.length(min=3)],
        render_kw={'placeholder': 'Senha'}
    )
    
    telefone = StringField(
        'Telefone',
        [validators.length(min=11, max=15)],
        render_kw={'placeholder': 'Telefone'}
    )


class DeveloperForm(Form): 

    id = StringField(
        '',
        [validators.length(min=1)],
        render_kw={'placeholder': 'Digite o id de um produto...'}
    )
