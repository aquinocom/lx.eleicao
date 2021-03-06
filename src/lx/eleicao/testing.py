# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import lx.eleicao


class LxEleicaoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=lx.eleicao)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'lx.eleicao:default')


LX_ELEICAO_FIXTURE = LxEleicaoLayer()


LX_ELEICAO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LX_ELEICAO_FIXTURE,),
    name='LxEleicaoLayer:IntegrationTesting',
)


LX_ELEICAO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LX_ELEICAO_FIXTURE,),
    name='LxEleicaoLayer:FunctionalTesting',
)


LX_ELEICAO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LX_ELEICAO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='LxEleicaoLayer:AcceptanceTesting',
)
