# encoding: utf-8
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from plone import api

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
        self.tela_votacao = self.context.absolute_url()+"/urna/++add++voto"

        if 'codigo_socio' in request.form:
            codigo_socio_ = request.form['codigo_socio']
            request.set('codigo_socio', codigo_socio_)

    def __call__(self):
        if "codigo_socio" in self.request.form:
            self.validarCodigo(self.request.form['codigo_socio'])
        return self.index()

    def validarCodigo(self, codigo):
        """Validação do codigo socio.
        """
        if codigo == '':
            getToolByName(self.context, 'plone_utils').addPortalMessage("Informar o código.", type='error')
            # codigo = self.request.get('codigo_socio', None)
        else:
            self.request.response.redirect(self.tela_votacao)


        
