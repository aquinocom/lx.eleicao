# encoding: utf-8
import random
listaEleitor=[
    'Abdoral De Souza Filho',
    'Agricio Braga Filho',
    'Alberto Carlos da Silva Mohammed',
    'Alessando Silva de Oliveira',
    'Alfredo Alves Braga',
    'Antilhon Saraiva do Santos',
    'Antonio Alves do Nascimento Neto',
    'Antonio Candido de Moura',
    'AntonioEustaquio de Oliveira',
    'Antonio Rocha da Silva',
    'Antonio Walmir Campelo Bezerra',
    'Arggeu Bredda Pessoa de Mello',
    'Arilson Machado Pessoa',
    'Bernardo José de Sales',
    'Carlos Rubens Barbosa',
    'Cleber Roberto Pires',
    'Danilo Rinaldi dos Santos',
    'Danilo Rinaldi dos Santos Junior',
    'Davidson Luiz dos Santos Sá',
    'Fabiano Feliz F. da Costa',
    'Felipe Ferrari Rinaldi dos Santos.',
    'Gehad Santa Cruz Abdel Hadi',
    'Geraldo Magela de Oliveira',
    'Gustavo José de Carvalho de Sousa',
    'Ícaro Policarpo Soares Peres',
    'Joanildes Henrique Linhares',
    'João Sotero Pereira',
    'Joaquim Carlos Gonçalves de Carvalho',
    'Jocenildo Alves de Souza',
    'Jose Antônio Alves',
    'José da Conceição Cruzeiro',
    'José da Cruz Rezende Filho',
    'Jose de Ribamar Rodrigues Nogueira',
    'José Garcia de Araújo',
    'Jose Pacifico Neto',
    'Luiz Henrique Nuñes de Oliveira',
    'Marcelo de Carvalho Gonçalo',
    'Marcio Silva de Almeida',
    'Marcos Antonio Romão',
    'Marcos de Oliveira',
    'Miguel Ferreira Peres',
    'Norberto Lopes',
    'Oldemar Bezerra Antunes',
    'Paulo Roberto Simões',
    'Rafael Faria de Melo',
    'Reginaldo Candido de Moura',
    'Robson Marinho de Oliveira',
    'Rodolfo Prado da Silva',
    'Saulo dos Santos Diniz',
    'Sebastião Stenio Pinho',
    'Valdecio José da Rocha',
    'Vilson de Sá',
    'Vinicius Souza Lima',
    'Walter Rios Zambrana',
    'Walter Teodoro de Paula',
    'Wander Marques de Abdalla',
    'Weber De Azevedo Magalhaes',
    'Weliton José da Silva',
    'Wendel da Costa Fernandes Lopes',
    'Zacarias da Silva Almeida',
    'Manoel Mardonio Soares Bezerra',
    'Larissa Valentim Gomes Neves',
    'Vitor Fernandes Lima',
    'Marcos Antônio Romão',
    'José Garcia de Araújo',
    'Rafael Faria de Melo',
    'Valdécio José da Rocha',
    'Weliton José da Silva',
    'Altair dos Santos Barreto',
    'Breno Rodrigo Carvalho Serejo',
    'Daniel Klinger Viana',
    'Diego Soares Lima',
    'Fábio Araujo Guimarães',
    'Gustavo José de Carvalho Sousa',
    'Iannis Konstantinos Zezelis',
    'Jhony Roger Ayres Ferraz',
    'Paulo Henrique Soares Lima',
    'Wesclei da Silva Quirino',
]

relacaoVoto = []

listaRepetido = []

for item in listaEleitor:
    cod = random.randint(1000,9999)
    dicioVotos = {
        'nome' : item,
        'codigo': str(cod)
    }
    relacaoVoto.append(dicioVotos)




print(relacaoVoto)
