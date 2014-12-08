# -*- coding: utf-8 -*-
"""Base module for unittesting."""

# from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest2 as unittest


class RepTheoryPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import reptheory.policy
        self.loadZCML(package=reptheory.policy)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'reptheory.policy:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'reptheory.policy')


FIXTURE = RepTheoryPolicyLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="RepTheoryPolicyLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="RepTheoryPolicyLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """docstring for IntegrationTestCase"""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """docstring for FunctionalTestCase"""

    layer = FUNCTIONAL_TESTING
