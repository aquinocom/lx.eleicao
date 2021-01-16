# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from lx.eleicao.testing import LX_ELEICAO_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that lx.eleicao is properly installed."""

    layer = LX_ELEICAO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lx.eleicao is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'lx.eleicao'))

    def test_browserlayer(self):
        """Test that ILxEleicaoLayer is registered."""
        from lx.eleicao.interfaces import (
            ILxEleicaoLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ILxEleicaoLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LX_ELEICAO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['lx.eleicao'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if lx.eleicao is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'lx.eleicao'))

    def test_browserlayer_removed(self):
        """Test that ILxEleicaoLayer is removed."""
        from lx.eleicao.interfaces import \
            ILxEleicaoLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ILxEleicaoLayer,
            utils.registered_layers())
