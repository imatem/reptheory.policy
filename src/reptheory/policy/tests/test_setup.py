# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from reptheory.policy.testing import IntegrationTestCase
# from plone.app.event.base import default_timezone
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class TestsInstall(IntegrationTestCase):
    """Test installation of omdf.policy into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_product_installed(self):
        """Test if omdf.policy is installed in portal_wuickinstaller."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('reptheory.policy'))

    def test_dependencies_installed(self):
        """Test that all product dependencies are installed."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('ContentWellPortlets'))

    # def test_portal_title(self):
    #     self.assertEqual(
    #         self.portal.getProperty('title'),
    #         "Olimpiada Matemática del Distrito Federal")

    # def test_portal_description(self):
    #     self.assertEqual(
    #         self.portal.getProperty('description'),
    #         "Bienvenido a la Olimpiada Matématica")

    # def test_default_timezone(self):
    #     self.assertEqual(default_timezone(), 'Mexico/General')

    # def test_default_language(self):
    #     # acording to documentation this must be in afterSetUp()
    #     ltool = self.portal.portal_languages
    #     ltool.setLanguageBindings()

    #     portal_state = getMultiAdapter(
    #         (self.portal, self.request), name=u'plone_portal_state')
    #     current_language = portal_state.language()
    #     self.assertEqual(current_language, 'es')


def test_suite():
    """This """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
