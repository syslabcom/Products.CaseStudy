import unittest
import doctest
import zope.testing
from base import CaseStudyFunctionalTestCase
from Products.CaseStudy.adapter import lmsretrievers
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    return unittest.TestSuite((
            Suite('tests/lmsretrievers.txt',
                   optionflags=OPTIONFLAGS,
                   package='Products.CaseStudy',
                   test_class=CaseStudyFunctionalTestCase) ,



        ))