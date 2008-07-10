import RDF
from cc.license.lib.interfaces import ILicenseSelector, ILicense
from cc.license.lib import rdf_helper

import zope.interface
import glob
import os

class PdLicense(object):
    zope.interface.implements(ILicense)
    def __init__(self, model, uri):
        assert uri == 'http://creativecommons.org/licenses/publicdomain/'
        self.license_class = 'publicdomain' # LAME, should pull from RDF
        self.version = 'Your mom' # Is there a version for the PD deed?
        self.jurisdiction = 'Your mom' # Is there a juri?  US?  (Not in the RDF)
        self.uri = uri
        self.current_version = 'Your mom' # Is there versioning for PD?
        self.deprecated = False # I think
        self.superseded = False # I think
        self.license_code = 'publicdomain' # Based on assertion at top of init
        self.libre = True # Sure, I think?  Not in the RDF.
        self._names = rdf_helper.query_to_language_value_dict(model,
             RDF.Uri(self.uri),
             RDF.Uri('http://purl.org/dc/elements/1.1/title'),
             None)
    def name(self, language = 'en'):
        return self._names[language]
        

# TODO: pull id and title from license.rdf
class Selector(object):
    zope.interface.implements(ILicenseSelector)
    id = 'publicdomain'
    title = 'Public Domain'
    def __init__(self):
        files = glob.glob(os.path.join(rdf_helper.LIC_RDF_PATH ,'*publicdomain*'))
        self.model = rdf_helper.init_model(*files)

    def by_code(self, code):
        if code == 'publicdomain':
            return self.by_uri('http://creativecommons.org/licenses/publicdomain/')
    
    def by_uri(self, uri):
        return PdLicense(self.model, uri)
