from zope.interface import Interface
try:
    from slc.xliff.xliff import BaseAttributeExtractor
except:
    BaseAttributeExtractor = Interface


class CaseStudyAttributeExtractor(BaseAttributeExtractor):
    """ Adapter to retrieve attributes from a standard event based object """
    attrs = ['title', 'description', 'text', 'action', 'results']
