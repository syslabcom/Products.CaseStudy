"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""


from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc

from Products.Five import fiveconfigure, zcml
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class CaseStudyLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        ztc.installProduct('CaseStudy')
        ztc.installProduct('LinguaPlone')
        ptc.setupPloneSite(products=['CaseStudy'])
        SiteLayer.setUp()

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    layer = CaseStudyLayer

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    layer = CaseStudyLayer

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        ptc.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
