from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock
import unittest


def mock_getUtility1(iface):
    return {}


def mock_getUtility2(iface):
    return {'plone.portal_timezone': None}


def mock_getUtility3(iface):
    return {'plone.portal_timezone': 'Europe/Amsterdam'}


def mock_getUtility4(iface):
    return {'plone.app.event.portal_timezone': 'Europe/Amsterdam'}


class TestControlPanel(unittest.TestCase):

    layer = PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @mock.patch('plone.app.controlpanel.overview.getUtility',
                new=mock_getUtility1)
    def test_timezone_warning__noreg(self):
        # If no registry key is available, return True
        view = self.portal.restrictedTraverse('@@overview-controlpanel')
        self.assertTrue(view.timezone_warning())

    @mock.patch('plone.app.controlpanel.overview.getUtility',
                new=mock_getUtility2)
    def test_timezone_warning__emptyreg(self):
        # If registry key value is empty, return True
        view = self.portal.restrictedTraverse('@@overview-controlpanel')
        self.assertTrue(view.timezone_warning())

    @mock.patch('plone.app.controlpanel.overview.getUtility',
                new=mock_getUtility3)
    def test_timezone_warning__set(self):
        # If new plone.portal_timezone is set, return False
        view = self.portal.restrictedTraverse('@@overview-controlpanel')
        self.assertFalse(view.timezone_warning())

    @mock.patch('plone.app.controlpanel.overview.getUtility',
                new=mock_getUtility4)
    def test_timezone_warning__paeset(self):
        # If old plone.app.event.portal_timezone is set, return False
        view = self.portal.restrictedTraverse('@@overview-controlpanel')
        self.assertFalse(view.timezone_warning())
