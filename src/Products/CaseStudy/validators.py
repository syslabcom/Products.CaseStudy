from Products.validation.interfaces.IValidator import IValidator
from Acquisition import aq_base, aq_inner
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
import re

_marker = []

class CaseStudyTextSizeValidator:
    """Tests if the sum of Abstract, Action and Result does exceed 350 words in english 
    """
    implements(IValidator)
        
    def __init__(self, name, words=0, chars=0):
        self.name = name
        self.words = words
        self.chars = chars

    def __call__(self, value, *args, **kwargs):
        if self.words==0 and self.chars==0:
            return True
            
        REQUEST = kwargs.get('REQUEST', {})            
        instance = kwargs.get('instance', None)
        
        # Only check on the canonical as translations may exceed this.
        if instance.getCanonical() != instance:
            return True
        
        context = aq_inner(instance)
        portal_transforms = getToolByName(context, 'portal_transforms')
        conv = portal_transforms.convert
        

        text = conv('html_to_text', REQUEST.get('text', '')).getData()
        action = conv('html_to_text', REQUEST.get('action', '')).getData()
        results = conv('html_to_text', REQUEST.get('results', '')).getData()
        
        total = "%s %s %s" % (text, action, results)
        total = total.strip()
        total.replace("&nbsp;", "")
        total = re.sub('\s+', ' ', total)
        words = total.split(" ")
        
        
        if self.words >0 and len(words)>self.words:
            return ("Validation failed. Abstract, Action and Results have %s words (%s total allowed)" % (len(words), self.words))

        if self.chars>0 and len(total)>self.chars:
            return ("Validation failed. Abstract, Action and Results have %s characters (%s total allowed)" % (len(total), self.chars))

        return True


validatorList = [
    CaseStudyTextSizeValidator('CaseStudyTextSizeValidator'),
    ]

__all__ = ('validatorList', )

