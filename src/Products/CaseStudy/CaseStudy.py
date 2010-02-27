# -*- coding: utf-8 -*-
#
# File: CaseStudy.py
#
# Copyright (c) 2008 by Syslab.com GmbH [info@syslab.com]
#
# GNU General Public License (GPL)
#

__author__ = """Syslab.com Gmbh <info@syslab.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope.interface import implements
import interfaces
from DateTime import DateTime

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CaseStudy.config import *
from Products.CaseStudy import CaseStudyMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _plone_message_factory

from Products.RichDocument.content.richdocument import RichDocument, RichDocumentSchema as BaseSchema
from Acquisition import aq_base, aq_parent, aq_base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.SimpleAttachment.widget import AttachmentsManagerWidget
from Products.VocabularyPickerWidget.VocabularyPickerWidget import VocabularyPickerWidget
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList
import re
from zope.i18n import translate


from Products.CaseStudy.validators import CaseStudyTextSizeValidator 
CSTV = CaseStudyTextSizeValidator('max350Words', words=350)


schema = Schema((

    TextField(
        name='description',
        required=False,
        widget=TextAreaWidget(
            label=_plone_message_factory(u"Description"),
            visible={'edit':False, 'view':True},
        ),
        default_output_type="text/plain",
        default_content_type="text/plain",
        accessor="Description",
        searchable=True,
    ),
    TextField(
        name='text',
        validators = CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_text_label', default=u'The issue'),
            description=_(u'casestudy_text_description', default=u"Enter the issue of the case study. Note that the total length of Issue, Action and Results may not exceed 350 words."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    TextField(
        name='action',
        validators = CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_action_label', default=u"The action"),
            description=_(u'casestudy_action_description', default=u"Enter the action of the case study. Note that the total length of Issue, Action and Results may not exceed 350 words."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    TextField(
        name='results',
        validators = CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_results_label', default=u"The results"),
            description=_(u'casestudy_results_description', default=u"Enter the results of the case study. Note that the total length of Issue, Action and Results may not exceed 350 words."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    IntegerField(
        name='publication_year',
        validators = 'isInt',
        vocabulary = 'yearVocabulary',
        widget = SelectionWidget(
            label=_(u'casestudy_publication_year_label', default=u"Publication year by Agency"),
            description=_(u'casestudy_publication_year_description', default=u"The year in which the case study was first published"),
        ),
    ),
    TextField(
        name='organisation',
        required=False,
        languageIndependent=True,
        widget=RichWidget(
            label=_(u'casestudy_organisation_label', default=u"Name of the organisation(s)"),
            description=_(u'casestudy_organisation_description', default=u"Type the name of organisation(s) that carried out the case study"),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),    
    LinesField(
        name='remoteLanguage',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u'casestudy_remoteLanguage_label', default=u"Case Study Language"),
            description=_(u'casestudy_remoteLanguage_description', default=u"The language of the linked contents"),
            rows=5,
        ),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary='getFilteredLanguages',
    ),
    StringField(
        name='remoteUrl',
        widget=StringField._properties['widget'](
            i18n_domain="casestudy",
            label=_(u'casestudy_remoteUrl_label', default=u"Case Study URL"),
            description=_(u'casestudy_remoteUrl_description', default=u"Paste here the location of the case study document or chapter in the agency publication."),
            macro="urlwidget",
            size=60,
        ),
    ),
    BooleanField(
        name='displayAttachments',
        default=True,
        widget=BooleanField._properties['widget'](
            condition="python:'portal_factory' not in object.getPhysicalPath()",
            description= _(
                u'casestudy_displayAttachments_description', 
                default=
                    u"If selected, uploaded files will be available " \
                    u"for download at the bottom of the page."
                ),
            label=_(
                    u'casestudy_displayAttachments_label', 
                    default=u"Display attachments box"
                   ),
            expanded=False,
            macro="widget_casestudy_attachmentmanager",
        ),
    ),
),
)

CaseStudy_schema = BaseSchema.copy() + schema.copy()

CaseStudy_schema.moveField('displayAttachments', after='remoteUrl')

finalizeATCTSchema(CaseStudy_schema)

CaseStudy_schema['displayImages'].widget.visible['edit'] = 'invisible'
CaseStudy_schema['displayImages'].widget.visible['view'] = 'invisible'

unwantedFields = ('allowDiscussion', 'nextPreviousEnabled',
    'excludeFromNav', 'tableContents', 'presentation', 'relatedItems', 'location')

cfields = [x for x in CaseStudy_schema.fields() if x.schemata=='categorization']
for field in cfields:
    CaseStudy_schema.changeSchemataForField(field.getName(), 'default')

CaseStudy_schema.changeSchemataForField('language', 'other')

ofields = [x for x in CaseStudy_schema.fields() if x.schemata=='ownership']
for field in ofields:
    CaseStudy_schema.changeSchemataForField(field.getName(), 'other')

for name in unwantedFields:
    if CaseStudy_schema.get(name, None):
        CaseStudy_schema[name].widget.visible['edit'] = 'invisible'
        CaseStudy_schema[name].widget.visible['view'] = 'invisible'


class CaseStudy(BaseContent, RichDocument, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICaseStudy)

    meta_type = 'CaseStudy'
    _at_rename_after_creation = True

    schema = CaseStudy_schema

    security.declareProtected('View', 'Description')
    def Description(self):
        """
        Override default method to return html-stripped and shortened veriosn of the abstract.
        """
        patt_html = re.compile('<.*?>')
        patt_entity = re.compile('&.{1,6};')
        text = re.sub(patt_entity, ' ', re.sub(patt_html,' ', self.getText()))
        return self.restrictedTraverse('@@plone').cropText(text, 300, ellipsis='...')

    def _Vocabulary(self, vocab_name):
        pv = getToolByName(self, 'portal_vocabularies')
        VOCAB = getattr(pv, vocab_name, None)
        if VOCAB:
            return VOCAB.getDisplayList(VOCAB)
        else:
            return DisplayList()

    def getFilteredLanguages(self):
        """ return the languages supported in the site """
        plt = getToolByName(self, 'portal_languages')
        langs = plt.listSupportedLanguages()
        L = []
        for l in langs:
            L.append((l[0], translate(l[1]) ))
        L.sort()
        return DisplayList(L)        

    def yearVocabulary(self):
        now = DateTime().year()+1
        vocab = [(x, str(x)) for x in range(1996,now)]
        vocab.reverse()
        return vocab

    def getCaseStudyAttachments(self):
        """ Return attachments of CaseStudy. Fall back to canonical if a
            translation doesn't have any.
        """
        attachments = [getattr(self, item['id']) for item in self._objects]
        if not attachments and not self.isCanonical():
            obj = self.getCanonical()
            attachments = [getattr(obj, item['id']) for item in obj._objects]
        return attachments


registerType(CaseStudy, PROJECTNAME)



