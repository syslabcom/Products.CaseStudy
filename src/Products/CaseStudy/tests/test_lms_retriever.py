from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from Products.CaseStudy.tests.base import INTEGRATION_TESTING

import unittest2 as unittest


class TestLMSRetriever(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # Login as manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_retriever(self):
        # Create a CaseStudy
        self.portal.invokeFactory('CaseStudy', 'case-study')
        case_study = self.portal['case-study']
        case_study.setText('This is <a href="google.com">a link</a>.')
        case_study.setRemoteUrl('http://osha.europa.eu')

        from gocept.linkchecker.interfaces import IRetriever
        retriever = IRetriever(case_study)
        links = retriever.retrieveLinks()

        self.assertIn('google.com', links)
        self.assertIn('http://osha.europa.eu', links)
