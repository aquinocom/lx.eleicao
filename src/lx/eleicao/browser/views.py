# encoding: utf-8
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from plone import api
from datetime import datetime
import random
import logging


class VotacaoView(BrowserView):
    """ view votacao
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.errors = {}
        self.url_sucess = self.context.absolute_url()
        self.utils = getToolByName(self.context, 'plone_utils')
        self.tela_votacao = self.context.absolute_url()+"/votacao-conselho-deliberativo"
        self.tela_posvotacao = self.context.absolute_url()+"/pos-votacao"

        if 'codigo_socio' in request.form:
            codigo_socio_ = request.form['codigo_socio']
            request.set('codigo_socio', codigo_socio_)


    def __call__(self):
        if "codigo_socio" in self.request.form:
            self.validarCodigo(self.request.form['codigo_socio'])

        if "form_votar" in self.request.form:
            self.validarVoto(self.request.form, 'errado')
        return self.index()

    def validarCodigo(self, codigo):
        """Validação do codigo socio.
        """

        lista_codigos_socio = api.content.find(portal_type='socio')
        lista_codigos_socio_ = [x.getObject().codigo_do_socio for x in lista_codigos_socio]
        socio_existe = False
        if codigo in lista_codigos_socio_:
            socio_existe = True
        if codigo != '' and socio_existe == True:
            self.request.response.redirect(self.tela_votacao)
        else:
            getToolByName(self.context, 'plone_utils').addPortalMessage("Informar o código correto.", type='error')

    def validarVoto(self, voto, codigo):
        """Validação do codigo socio.
        """
        if 'voto' not in voto.keys():
            getToolByName(self.context, 'plone_utils').addPortalMessage("Selecionar uma chapa, ou votar nulo.", type='error')
        else:
            self.setVoto(self.request.form['voto'])


    def getCandidatos(self):
        lista_candidatos = []
        candidatos = api.content.find(portal_type='chapa',
                                      path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1})
        for item in candidatos:
            item = item.getObject()
            dado = {'id': item.id,
                    'nome_chapa': item.Title,
                    'presidente': item.presidente,
                    'vice_presidente': item.vice_presidente,
                    'foto_presidente': item.foto_presidente,
                    'foto_vice_presidente': item.foto_vice_presidente,
                    'url': item.absolute_url()
                    }
            lista_candidatos.append(dado)
        return lista_candidatos

    def setVoto(self, voto_eleitor):
        # import pdb; pdb.set_trace()
        portal = api.portal.get()['eleicao-conselho-deliberativo']['urna']
        dados_form = self.request.form
        if dados_form['voto'] == 'nulo':
            anulado = True
        else:
            anulado = False

        id_voto = "voto-{0}".format(datetime.now().strftime("%d%m%y%f"))
        titulo_voto = "{0}-{1}-{2}".format(id_voto, dados_form['voto'], datetime.now().strftime("%d/%m/%y"))
        _createObjectByType('voto',
                            portal,
                            id=id_voto,
                            title=titulo_voto,
                            id_chapa=dados_form['voto'],
                            codigo_eleitor='avulso',
                            voto_nulo=anulado,
                            data_voto=datetime.now()
                            )

        self.request.response.redirect(self.tela_posvotacao)

    def getVotos(self):
        lista_votos = []
        votos = api.content.find(portal_type='voto',
                                      path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1})
        for item in votos:
            item = item.getObject()
            dado = {'id': item.id,
                    'titulo_voto': item.Title,
                    'data': item.data_voto,
                    'id_chapa': item.id_chapa,
                    'codigo_eleitor': item.codigo_eleitor,
                    'voto_nulo': item.voto_nulo,
                    'url': item.absolute_url()
                    }
            lista_votos.append(dado)
        return lista_votos

    def votosTotal(self):
        return len(self.getVotos())

    def votosNulos(self):
        """
        quantidade votos nulos
        """
        lista_nulos = []
        lista_nulo = [x['voto_nulo'] for x in self.getVotos() ]
        for v in lista_nulo:
            if v == True:
                lista_nulos.append(v)
        return len(lista_nulos)

    def votosChapas(self, chapa):
        """
        quantidade votos chapa
        """
        lista_chapas = []
        lista_chapa = [x['id_chapa'] for x in self.getVotos() ]
        for v in lista_chapa:
            if v == chapa:
                lista_chapas.append(v)
        return len(lista_chapas)

class SocioCreate(BrowserView):
    """ view socio
    """
    def __call__(self):


        listaEleitor = [
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
        portal = api.content.get(path='/sistema-votacao/socios/')
        for socio in listaEleitor:
            cod = random.randint(1000, 9999)
            try:
                obj = api.content.create(
                                    type='socio',
                                    title=socio,
                                    codigo_do_socio=str(cod),
                                    id = str(cod),
                                    container=portal)
            except:
                obj = api.content.create(
                                    type='socio',
                                    title=socio,
                                    codigo_do_socio=str(cod-1),
                                    id = str(cod-1),
                                    container=portal)
            



