# -*- coding: utf-8 -*-
#
# File: CaseStudy.py
#
__author__ = """Syslab.com GmbH <info@syslab.com>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('CaseStudy')
logger.debug('Installing Product')

import os
import os.path
from Globals import package_home
import Products.CMFPlone.interfaces
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from config import *


from zope.i18nmessageid import MessageFactory
CaseStudyMessageFactory = MessageFactory('CaseStudy')

import CaseStudy

DirectoryView.registerDirectory('skins', product_globals)


from Products.validation import validation
from Products.CaseStudy.validators import validatorList
import adapter


def initialize(context):
    """initialize product (called by zope)"""

    for validator in validatorList:
        validation.register(validator)

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)


