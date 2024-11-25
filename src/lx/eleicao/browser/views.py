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
        self.tela_pos_votacao_deliberativo = self.context.absolute_url()+"/pos-votacao-deliberativo"
        self.tela_posvotacao = self.context.absolute_url()+"/pos-votacao"

        if 'codigo_socio' in request.form:
            codigo_socio_ = request.form['codigo_socio']
            request.set('codigo_socio', codigo_socio_)


    def __call__(self):
        if "codigo_socio" in self.request.form:
            self.validarCodigo(self.request.form['codigo_socio'])

        if "form_votar" in self.request.form:
            self.validarVoto(self.request.form, 'errado')

        if "form_votar_fiscal" in self.request.form:
            self.validarVotoFiscal(self.request.form, 'errado')
        return self.index()

    def validarCodigo(self, codigo):
        """Validação do codigo socio.
        """

        # lista_codigos_socio = api.content.find(portal_type='socio')
        # lista_codigos_socio_ = [x.getObject().codigo_do_socio for x in lista_codigos_socio]
        # socio_existe = False
        try:
            obj_socio = api.content.get(path='/sistema-votacao/socios/'+codigo)
            confirma_voto = obj_socio.votou
        except:
            codigo = ""


        if codigo != '' and confirma_voto==False:
                obj_socio.votou = True
                self.request.response.redirect(self.tela_votacao)
        elif codigo != '' and confirma_voto==True:
            getToolByName(self.context, 'plone_utils').addPortalMessage("O sócio já votou.", type='error')
        else:
            getToolByName(self.context, 'plone_utils').addPortalMessage("Informar o código correto. ", type='error')



    def validarVoto(self, voto, codigo):
        """Validação do codigo socio.
        """
        if 'voto' not in voto.keys():
            getToolByName(self.context, 'plone_utils').addPortalMessage("Selecionar uma chapa, ou votar nulo.", type='error')
        else:
            self.setVoto(self.request.form['voto'])

    def validarVotoFiscal(self, voto, codigo):
        """Validação do codigo socio.
        """
        if 'voto' not in voto.keys():
            getToolByName(self.context, 'plone_utils').addPortalMessage("Selecionar uma chapa, ou votar nulo.", type='error')
        else:
            self.setVotoFiscal(self.request.form['voto'])

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
                    'membro': item.membro,
                    'primeiro_suplente': item.primeiro_suplente,
                    'segundo_suplente': item.segundo_suplente,
                    'terceiro_suplente': item.terceiro_suplente,
                    'foto_presidente': item.foto_presidente,
                    'foto_vice_presidente': item.foto_vice_presidente,
                    'foto_membro': item.foto_membro,
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

        self.request.response.redirect(self.tela_pos_votacao_deliberativo)

    def setVotoFiscal(self, voto_eleitor):
        # import pdb; pdb.set_trace()
        portal = api.portal.get()['eleicao-conselho-fiscal']['urna']
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

    def getVotos(self, path):
        lista_votos = []
        votos = api.content.find(portal_type='voto',
                                      path={'query': str(path), 'depth': 1})
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

    def votosTotal(self, path):
        return len(self.getVotos(path))

    def votosNulos(self, path):
        """
        quantidade votos nulos
        """
        lista_nulos = []
        lista_nulo = [x['voto_nulo'] for x in self.getVotos(path) ]
        for v in lista_nulo:
            if v == True:
                lista_nulos.append(v)
        return len(lista_nulos)

    def votosChapas(self, chapa, path):
        """
        quantidade votos chapa
        """
        lista_chapas = []
        lista_chapa = [x['id_chapa'] for x in self.getVotos(path) ]
        for v in lista_chapa:
            if v == chapa:
                lista_chapas.append(v)
        return len(lista_chapas)

    def getApuracaoVotos(self, path):
        lista_votos = []

        votos = api.content.find(portal_type='voto',
                                 path={'query': '/sistema-votacao/'+path, 'depth': 1})
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
        return len(lista_votos)

    def getApuracaoSociosVotaram(self):
        lista_socios_que_votaram = []

        socios = api.content.find(portal_type='socio')
        for socio in socios:
            if socio.getObject().votou == True:
                lista_socios_que_votaram.append(socio.id)

        return len(lista_socios_que_votaram)


class SocioCreate(BrowserView):
    """ view socio
    """
    def __call__(self):


        lista_eleitor = [
"Abdoral De Souza Filho",
"Adalberto Patrocínio Correa de Araujo",
"Ademir Francisco Serejo",
"Adilson dos Reis Velasco",
"Adler Gabriel da Silva Campos",
"Agricio Braga Filho",
"Alberto Carlos da Silva Mohammed",
"Alessandro Silva de Oliveira",
"Alex Luiz Rocha",
"Alexandre Peligrini",
"Alfredo Alves Braga",
"Altair dos Santos Barreto",
"Alysson Rodrigues de Queiroz",
"Amanda Karen da Silva Campos",
"Anderson de Oliveira Braga",
"André Botelho Vilaron",
"André Luiz Chaves Mendes",
"Andrei Augusto de Sousa Matheus",
"Antilhon Saraiva do Santos",
"Antonio Alves do Nascimento Neto",
"Antonio Candido de Moura",
"Antonio Teles Sobrinho",
"Antonio Walmir Campelo Bezerra",
"Arggeu Bredda Pessoa de Mello",
"Bernardo José de Sales",
"Breno Rodrigo Carvalho Serejo ",
"Bruno Chaves Mendes",
"Caio Madureira",
"Caio Rodrigo Santos Moreira",
"Carlos Roberto Garcia Junior",
"Carlos Rubens Barbosa",
"Carlos W. Ribeiro dos Santos",
"Cauã Bruno Medeiros Gomes",
"Cayo Fernando Menezes Costa",
"Cláudio Renato Campos",
"Cleber Roberto Pires",
"Cristiano Caruso Rinaldi dos Santos",
"Daniel Bruno Gomes",
"Daniel Jaculli Lira",
"Daniel Klinger Vianna",
"Daniel Morais de Almeida",
"Daniel Moreira dos Santos",
"Danilo Rinaldi dos Santos Junior",
"David Da Mata",
"Débora Natalya da Silva Nascimento",
"Denis Paulinho Zaleski",
"Diego Soares Lima",
"Dirceu Rodrigues Bragança",
"Edinilson Ferreira de Souza",
"Eduardo Caetano de Souza",
"Eduardo Weyne Pedrosa",
"Elielson George de Freitas Queiroz",
"Emerson Santos Silva",
"Erasmo Luiz Rodrigues da Silva",
"Evanuir de Souza Amaral",
"Expedito Monte Moreira",
"Fabiano Alvs dos Santos",
"Fabiano Felix Figueiredo da Costa",
"Fabio Araujo Guimarães",
"Felipe Cavalcante Machado",
"Felipe Dutra de Carvalho Heimburger",
"Felipe Lima Marinho",
"Filipe Cauan Silva Ferreira",
"Flávio Cavalcante de Oliveira",
"Flávio da Silveira Campos",
"Francisco Almeida Ferreira",
"Gabriel Caetano Cardoso Silva",
"Gabriel Soares Nunes",
"Gabrielle Alves Rodrigues",
"Gehad Santa Cruz Abdel Hadi ",
"Geraldo Cardoso Moitinho",
"Gilberto Gomes de Sena",
"Gildasio Alves de Oliveira Silva",
"Giulianny Santana Costa",
"Grediston Pires de Souza",
"Guilherme Augusto Caputo Bastos",
"Guilherme Yasser Lopes Lima",
"Gustavo José de Carvalho de Sousa",
"Henrique Glasmeyer",
"Iannes Konstantinos Zezelis",
"Ícaro Policarpo Soares Peres",
"Idair Paulino Capelesso",
"Irivan Da Silva Freire",
"Isabella C. Tavares da Queiroz",
"Janaína da Costa Tavares",
"Jean Rodrigues Ferreira",
"Jefferson Luiz Batista",
"Jeová de Alcântara Lopes",
"Jhony Roger Ayres Ferraz",
"Joanildes Henrique Linhares",
"João Elisio de Lima Silva",
"João Sotero Pereira",
"Joaquim Carlos Gonçalves de Carvalho",
"Jocenildo Alves de Souza",
"Jose Antônio Alves",
"José da Conceição Cruzeiro",
"José E. de Queiroz Jr.",
"Jose Pacifico Neto",
"Junio Augusto Pereira",
"Larissa Valentim Gomes Neves",
"Leandro Gomes",
"Leon Heimburger",
"Leonardo Jorge da Matta Campos Frechiani",
"Leonardo Martins Amorim Silva",
"Lucas de Oliveira França Teles",
"Luciano Lucio Ferreira Xavier",
"Luciano Maciel Lobato",
"Luiz Evandro Rocha Alves",
"Luiz Flávio Sena e Silva Lelis",
"Luiz Gabriel Araújo Gomes",
"Luiz Henrique Nuñes de Oliveira",
"Luiz Jose Guimaraes Falcão Neto",
"Manoel Dias Quixadá",
"Manoel Mardonio Soares Bezerra",
"Marcelo das Neves Grilo",
"Marcelo de Carvalho Gonçalo",
"Marcio Silva de Almeida",
"Marcos Antonio Ferreira",
"Marcos Antonio Rodrigues",
"Marcos Antonio Romão",
"Marcos de Oliveira",
"Maria C. Silva de Almeida",
"Mariano Pereira da Costa",
"Matheus Heimburger",
"Matheus Ritchelly Saúde",
"Mauro Souza Brito",
"Maxsuel Ferreira de Carvalho",
"Miguel Ferreira Peres",
"Moacir Vieira de Souza Junior",
"Nathalia de Sousa Matheus",
"Nilton Santos de Oliveira",
"Nivaldo Castro",
"Norberto Lopes",
"Oldemar Bezerra Antunes",
"Paulo Abdel Wadud",
"Paulo Cesar Pereira de Araujo",
"Paulo Henrique Soares Lima",
"Paulo Roberto Simões",
"Raelson Francisco da Silva Berto",
"Rafael Faria de Melo",
"Rafael Souza Gontijo",
"Raimundo Nonato Silva",
"Reginaldo Candido de Moura",
"Reginaldo Silva Martins",
"Renan Soares Duarte",
"Renato da Silva Araujo",
"Ricardo de Oliveira Matheus",
"Ricardo Viana Lopes",
"Richard Douglas Duarte Flausino",
"Rodrigo Ribeiro Peres",
"Romer Borges Veado",
"Rômulo Lopes Marques",
"Ronildo Martins da Silva",
"Roverson Lima da Costa",
"Saulo dos Santos Diniz",
"Sebastião Stenio Pinho",
"Sérgio Luiz Ferreira Batista",
"Sergio Luiz Lisboa de Almeida",
"Sergio Ubiratan Ferreira Albernaz Junior",
"Sergio Vinicius Monteiro Pereira",
"Simone Valeria Gonçalves Sena",
"Stephanie Ferreira de Melo Santos",
"Thiago Gomes da Costa",
"Thiago José Rodrigues de Queiroz",
"Tiago Favilla Vaz Vilaça",
"Tiago Vinicius Pontes",
"Valdecio José da Rocha",
"Valtonio Marinho Gomes",
"Verônica Gonçalves Borges",
"Victor Birnbaum Pessoa de Mello",
"Vilson de Sá",
"Vinicius Souza Lima",
"Vitor Fernandes Lima",
"Wagner Antonio Marques",
"Walter Rios Zambrana",
"Walter Teodoro de Paula",
"Wander Marques de Abdalla",
"Wanderley Ferreira dos Santos",
"Weber De Azevedo Magalhaes",
"Weliton José da Silva",
"Wellington Ferreira S. Jr.",
"Welthon Ferreira Bezerra",
"Wendel da Costa Fernandes Lopes",
"Wesclei da Silva Quirino",
"Wesley da Silva Quirino",
"William Silva de Almeida",
"Wilton Soares",
"Ygor Miranda Costa",
"Zacarias da Silva Almeida",
]
        portal = api.content.get(path='/sistema-votacao/socios/')
        for socio in lista_eleitor:
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
            api.content.transition(obj=obj, transition='publish')
