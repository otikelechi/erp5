import facebook
from Products.ERP5Security.ERP5ExternalOauth2ExtractionPlugin import getFacebookUserEntry

def getAccessTokenFromCode(self, code, redirect_uri):
  client_id, secret_key = self.ERP5Site_getFacebookClientIdAndSecretKey()
  return facebook.GraphAPI(version="2.7").get_access_token_from_code(
    code=code, redirect_uri=redirect_uri,
    app_id=client_id, app_secret=secret_key)

def unrestrictedSearchFacebookConnector(self):
  return self.getPortalObject().portal_catalog.unrestrictedSearchResults(
            portal_type="Facebook Connector",
            reference="default",
            validation_state="validated",
            limit=2)

def getUserEntry(token):
  return getFacebookUserEntry(token)
