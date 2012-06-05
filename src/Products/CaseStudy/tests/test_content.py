from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from Products.CaseStudy.tests.base import INTEGRATION_TESTING

import unittest2 as unittest


class TestCaseStudy(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # Login as manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_create(self):
        """Ensure that we can create a CaseStudy without error"""

        self.portal.invokeFactory(
            'CaseStudy', 'case-study', title=u"Case study")
