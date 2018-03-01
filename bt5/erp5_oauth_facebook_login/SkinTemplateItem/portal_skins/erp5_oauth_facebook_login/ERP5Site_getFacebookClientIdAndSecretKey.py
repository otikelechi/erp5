if REQUEST is not None:
  raise ValueError("This script can't be called in the URL")

result_list = context.ERP5Site_getFacebookConnector()

assert result_list, "Facebook Connector not found"

if len(result_list) == 2:
  raise ValueError("Impossible to select one Facebook Connector")

facebook_connector = result_list[0]
return facebook_connector.getClientId(), facebook_connector.getSecretKey()
