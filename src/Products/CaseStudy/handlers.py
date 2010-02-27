def case_study_edited(obj, event, **args):
    """ Make sure all 'natural' languages are part of the list of
    remote languages """
    can = obj.getCanonical()
    langs = can.getTranslations().keys()
    remote_languages = [x for x in can.getRemoteLanguage()]
    [remote_languages.append(lang) for lang in langs if lang not in remote_languages]
    can.setRemoteLanguage(remote_languages)
    if obj != can:
        can.reindexObject()