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

    def getFolders(self):
        """
        """
        path = '/'.join(self.context.getPhysicalPath())
        
        return path
