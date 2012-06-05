from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.testing import z2


class CaseStudy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.CaseStudy
        self.loadZCML('configure.zcml', package=Products.CaseStudy)
        import gocept.linkchecker
        self.loadZCML('configure.zcml', package=gocept.linkchecker)
        import osha.adaptation
        self.loadZCML('configure.zcml', package=osha.adaptation)

        z2.installProduct(app, 'Products.ZCatalog')
        z2.installProduct(app, 'Products.CaseStudy')
        z2.installProduct(app, 'gocept.linkchecker')

    def setUpPloneSite(self, portal):
        # Needed to make skins work
        applyProfile(portal, 'Products.CMFPlone:plone')

        applyProfile(portal, 'Products.CaseStudy:default')
        applyProfile(portal, 'gocept.linkchecker:default')
        quickInstallProduct(portal, 'osha.adaptation')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.ZCatalog')
        z2.uninstallProduct(app, 'Products.CaseStudy')
        z2.uninstallProduct(app, 'gocept.linkchecker')


CASESTUDY_FIXTURE = CaseStudy()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(CASESTUDY_FIXTURE,),
    name="CaseStudy:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CASESTUDY_FIXTURE,),
    name="CaseStudy:Functional")
