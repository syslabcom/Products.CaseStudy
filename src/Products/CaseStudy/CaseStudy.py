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

import re

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from DateTime import DateTime

from zope.i18n import translate
from zope.interface import implements

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import DisplayList
from Products.ATCountryWidget.Widget import MultiCountryWidget
from Products.ATVocabularyManager import NamedVocabulary
from collective.dynatree.atwidget import DynatreeWidget
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils as ploneutils
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone import PloneMessageFactory as _plone_message_factory
from Products.CaseStudy import CaseStudyMessageFactory as _
from Products.CaseStudy.config import *
from Products.CaseStudy.validators import CaseStudyTextSizeValidator
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.document import ATDocumentBase

import interfaces

CSTV = CaseStudyTextSizeValidator('max350Words', words=350)


schema = Schema((

    TextField(
        name='description',
        required=False,
        widget=TextAreaWidget(
            label=_plone_message_factory(u"Description"),
            visible={'edit': False, 'view': True},
        ),
        default_output_type="text/plain",
        default_content_type="text/plain",
        accessor="Description",
        searchable=True,
    ),
    # TextField('seoDescription',
    #         schemata='default',
    #         widget=TextAreaWidget(
    #             label=_(
    #                 u'osha_seo_description_label',
    #                 default=u'SEO Description'
    #                 ),
    #             description=_(u'osha_seo_description_description',
    #                 default=(
    #                     u"Provide here a description that is purely for SEO "
    #                     "(Search Engine Optimisation) purposes. It will "
    #                     "appear in the <meta> tag in the "
    #                     "<head> section of the HTML document, but nowhere "
    #                     "in the actual website content.")
    #                     ),
    #             visible={'edit': 'visible', 'view': 'invisible'},
    #         ),
    #     ),
    TextField(
        name='text',
        validators=CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_text_label', default=u'The issue'),
            description=_(u'casestudy_text_description',
                default=(u"Enter the issue of the case study. Note that the "
                         u"total length of Issue, Action and Results may not "
                         u"exceed 350 words.")),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    TextField(
        name='action',
        validators=CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_action_label', default=u"The action"),
            description=_(u'casestudy_action_description',
                default=u"Enter the action of the case study. Note that the "
                          u"total length of Issue, Action and Results may not "
                          u"exceed 350 words."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    TextField(
        name='results',
        validators=CSTV,
        required=True,
        widget=RichWidget(
            label=_(u'casestudy_results_label', default=u"The results"),
            description=_(u'casestudy_results_description',
                default=u"Enter the results of the case study. Note that the "
                          u"total length of Issue, Action and Results may not "
                          u"exceed 350 words."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    IntegerField(
        name='publication_year',
        validators='isInt',
        vocabulary='yearVocabulary',
        widget=SelectionWidget(
            label=_(u'casestudy_publication_year_label',
                    default=u"Publication year by Agency"),
            description=_(u'casestudy_publication_year_description',
                default=u"The year in which the case study was first "
                          u"published"),
        ),
    ),
    TextField(
        name='organisation',
        required=False,
        languageIndependent=True,
        widget=RichWidget(
            label=_(u'casestudy_organisation_label',
                    default=u"Name of the organisation(s)"),
            description=_(u'casestudy_organisation_description',
                default=u"Type the name of organisation(s) that carried out "
                          u"the case study"),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        searchable=1,
    ),
    LinesField(
        name='remoteLanguage',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u'casestudy_remoteLanguage_label',
                    default=u"Case Study Language"),
            description=_(u'casestudy_remoteLanguage_description',
                          default=u"The language of the linked contents"),
            rows=5,
        ),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary='getFilteredLanguages',
        required=True,
    ),
    StringField(
        name='remoteUrl',
        widget=StringField._properties['widget'](
            i18n_domain="casestudy",
            label=_(u'casestudy_remoteUrl_label', default=u"Case Study URL"),
            description=_(u'casestudy_remoteUrl_description',
                default=u"Paste here the location of the case study document "
                          u"or chapter in the agency publication."),
            macro="urlwidget",
            size=60,
        ),
    ),
    BooleanField(
        name='displayAttachments',
        default=True,
        widget=BooleanField._properties['widget'](
            condition="python:'portal_factory' not in object.getPhysicalPath()",
            description=_(
                u'casestudy_displayAttachments_description',
                default=u"If selected, uploaded files will be available " \
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
    # LinesField('country',
    #         schemata='default',
    #         enforceVocabulary=False,
    #         languageIndependent=True,
    #         required=False,
    #         multiValued=True,
    #         widget=MultiCountryWidget(
    #             label="Countries",
    #             description=(
    #                 u'Select one or more countries appropriate for this '
    #                 u'content'),
    #             description_msgid='help_country',
    #             provideNullValue=1,
    #             nullValueTitle="Select...",
    #             label_msgid='label_country',
    #             i18n_domain='osha',
    #         ),
    #     ),
    # LinesField('subcategory',
    #         schemata='default',
    #         enforceVocabulary=False,
    #         languageIndependent=True,
    #         multiValued=True,
    #         vocabulary=NamedVocabulary("Subcategory"),
    #         widget=DynatreeWidget(
    #             label=u"Subcategory",
    #             description=u"Pick one or more values by ticking a checkbox" \
    #             " in the tree. You can use the quick search field below to " \
    #             "find values by typing the first letters. Click 'Close' " \
    #             "when you are finished picking values.",
    #             selectMode=2,
    #             rootVisible=False,
    #             minExpandLevel=1,
    #             overlay=True,
    #             flatlist=True,
    #         ),
    #     ),
    # LinesField('nace',
    #         schemata='default',
    #         languageIndependent=True,
    #         multiValued=True,
    #         vocabulary=NamedVocabulary("NACE"),
    #         widget=DynatreeWidget(
    #             label=u"Sector (NACE Code)",
    #             description=u"Pick one or more values by ticking a checkbox" \
    #             " in the tree. You can use the quick search field below to " \
    #             "find values by typing the first letters. Click 'Close' " \
    #             "when you are finished picking values.",
    #             selectMode=2,
    #             showKey=True,
    #             rootVisible=False,
    #             minExpandLevel=1,
    #             overlay=True,
    #             flatlist=True,
    #         ),
    #     ),
    # LinesField('multilingual_thesaurus',
    #         schemata='default',
    #         enforceVocabulary=False,
    #         languageIndependent=True,
    #         required=False,
    #         multiValued=True,
    #         vocabulary=NamedVocabulary("MultilingualThesaurus"),
    #         widget=DynatreeWidget(
    #             label=u"Multilingual Thesaurus Subject",
    #             description=u"Pick one or more values by ticking a checkbox" \
    #             " in the tree. You can use the quick search field below to " \
    #             "find values by typing the first letters. Click 'Close' " \
    #             "when you are finished picking values.",
    #             selectMode=2,
    #             showKey=True,
    #             rootVisible=False,
    #             minExpandLevel=1,
    #             overlay=True,
    #             flatlist=True,
    #         ),
    #     ),
),
)

CaseStudy_schema = BaseSchema.copy() + ATDocumentSchema.copy() + schema.copy()
CaseStudy_schema.moveField('displayAttachments', after='remoteUrl')

finalizeATCTSchema(CaseStudy_schema)

unwantedFields = (
    'allowDiscussion',
    'nextPreviousEnabled',
    'subject',
    'excludeFromNav',
    'tableContents',
    'presentation',
    'relatedItems',
    'location')

cfields = [x for x in CaseStudy_schema.fields()
           if x.schemata == 'categorization']
for field in cfields:
    CaseStudy_schema.changeSchemataForField(field.getName(), 'default')

CaseStudy_schema.changeSchemataForField('language', 'other')

ofields = [x for x in CaseStudy_schema.fields()
           if x.schemata == 'ownership']
for field in ofields:
    CaseStudy_schema.changeSchemataForField(field.getName(), 'other')

for name in unwantedFields:
    if CaseStudy_schema.get(name, None):
        CaseStudy_schema[name].widget.visible['edit'] = 'invisible'
        CaseStudy_schema[name].widget.visible['view'] = 'invisible'


class CaseStudy(OrderedBaseFolder, ATDocumentBase, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICaseStudy)

    meta_type = 'CaseStudy'
    _at_rename_after_creation = True

    schema = CaseStudy_schema

    security.declareProtected('View', 'Description')
    def Description(self):
        """Override default method to return html-stripped and shortened
        veriosn of the abstract.
        """
        patt_html = re.compile('<.*?>')
        patt_entity = re.compile('&.{1,6};')
        text = re.sub(patt_entity, ' ', re.sub(patt_html, ' ', self.getText()))
        return self.cropText(
            text, 300, ellipsis='...')

    def cropText(self, text, length, ellipsis='...'):
        """Crop text on a word boundary
           Copied from the @@plone BrowserView, since fetching this view requires
           the presence of a REQUEST which we don't have in an async context
        """
        converted = False
        if not isinstance(text, unicode):
            encoding = ploneutils.getSiteEncoding(aq_inner(self))
            text = unicode(text, encoding)
            converted = True
        if len(text) > length:
            text = text[:length]
            l = text.rfind(' ')
            if l > length / 2:
                text = text[:l + 1]
            text += ellipsis
        if converted:
            # encode back from unicode
            text = text.encode(encoding)
        return text


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
        now = DateTime().year() + 1
        vocab = [(str(x), x) for x in range(1996, now)]
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
