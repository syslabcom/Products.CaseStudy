from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('CMFLinkChecker')
ztc.installProduct('CaseStudy')
ztc.installProduct('ZCatalog')

ptc.setupPloneSite(products=['CaseStudy', 'CMFLinkChecker'])

class CaseStudyTestCase(ptc.PloneTestCase):
    pass
    
class CaseStudyFunctionalTestCase(ptc.FunctionalTestCase):
    pass