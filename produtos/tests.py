from django.test import TestCase
from produtos.models import Produto, Categoria
from produtos.serializers import ProdutoSerializer
# Create your tests here.


class ProdutoTesteUnitario(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome='Eletronicos',
            descricao = 'Categoria para Eletronicos e Informatica'
        )
        self.dados = {
            'categoria' : self.categoria.id,
            'nome' : 'Pendrive',
            'marca' : 'Xiaomi',
            'preco' : 50.00,
            'descricao' : 'Pendrive Chinês de alta qualidade',
            'ativo' : True,
        }
    # Remove espaços do início e do fim (strip) de nome e marca
    def test_nome_marca_espaco(self):
        self.dados = {
            'nome': '   Pendrive ',
            'marca': ' Xiaomi ',
            'preco': 50.00
        }

        serializer = ProdutoSerializer(data=
                                       self.dados)
        
        # Verificar se o serializer pegou algum erro
        self.assertTrue(serializer.is_valid(),
                        serializer.errors)
        
        self.assertEqual(
    serializer.validated_data['nome'], 'Pendrive')
        self.assertEqual(
    serializer.validated_data['marca'], 'Xiaomi'
        )

    def test_nome_invalido_menos_3_caracteres(self):
        self.dados = {
            'nome' : 'rp',
            'marca': 'xi',
            'preco' : 20.00
        }

        serializer = ProdutoSerializer(data=self.dados)

        # verificar se o serializer não esta valido
        self.assertFalse(serializer.is_valid())

        # ve se houve um erro de nome
        self.assertIn('nome', serializer.errors)
        # se houvesse mais de um erro para nome
        self.assertIn('Nome deve ter no mínimo 3 caracteres',
        serializer.errors['nome'][0])
    
    # Rejeita preco menor ou igual a zero
    def test_preco_invalido_menor_igual_zero(self):
        for preco in ['0.0', '-10.00']:
            self.dados = {
                'nome': 'Pendrive',
                'marca': 'Xiaomi',
                'preco': preco
            }
            serializer = ProdutoSerializer(data=self.dados)

            self.assertFalse(serializer.is_valid())

            self.assertIn('preco',serializer.errors)
            self.assertIn('O preço deve ser maior que zero.',
            serializer.errors['preco'][0])

    def test_descricao_invalida_menos_20_caracteres(self):
        self.dados = {
            'nome': 'Pendrive',
            'marca': 'Xiaomi',
            'preco': 50.00,
            'descricao': 'Menor que 20'
        }

        serializer = ProdutoSerializer(data=self.dados)

        self.assertFalse(serializer.is_valid())
        self.assertIn('descricao', serializer.errors)
        self.assertIn('A descrição deve ter no mínimo 20 caracteres',
            serializer.errors['descricao'][0])

    def test_preco_maior_0_e_descricao_maior_igual_20_caracteres(self):
        self.dados = {
            'nome':'Airfryer 3.5L',
            'marca': 'Arno',
            'preco': 350.00,
            'descricao': 'a'*25
        }
        serializer = ProdutoSerializer(data=self.dados)

        self.assertTrue(serializer.is_valid())

        self.assertGreater(serializer.validated_data['preco'], 0)
        self.assertGreater(
            len(serializer.validated_data['descricao']), 20
            )
