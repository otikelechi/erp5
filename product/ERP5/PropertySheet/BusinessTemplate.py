##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#          Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

class BusinessTemplate:
  """
    Business templates properties and categories

    A business template contains all zope objects needed to add a given
    functionnality to ERP5, like accounting or pdf rendering.
  """

  _properties = (
    { 'id'          : 'template_portal_type_id',
      'description' : 'A list of ids of portal types used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_workflow_chain',
      'description' : 'A list of workflow chains of portal types used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_allowed_content_type',
      'description' : 'A list of allowed content types for portal types',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_hidden_content_type',
      'description' : 'A list of hidden content types for portal types',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_property_sheet',
      'description' : 'A list of property sheet for portal types',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_base_category',
      'description' : 'A list of base categories for portal types',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_module_id',
      'description' : 'A list of ids of modules used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_skin_id',
      'description' : 'A list of ids of skins used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_workflow_id',
      'description' : 'A list of ids of skins used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_product_id',
      'description' : 'A list of ids of products used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_document_id',
      'description' : 'A list of ids of documents used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_property_sheet_id',
      'description' : 'A list of ids of property sheets used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_constraint_id',
      'description' : 'A list of ids of constraints used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_role',
      'description' : 'A list of ids of roles used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_method_id',
      'description' : 'A list of ids of catalog methods used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_result_key',
      'description' : 'A list of ids of catalog result keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_related_key',
      'description' : 'A list of ids of catalog related keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_result_table',
      'description' : 'A list of ids of catalog result tables used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_keyword_key',
      'description' : 'A list of ids of catalog keyword keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_datetime_key',
      'description' : 'A list of ids of catalog DateTime keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },  
    { 'id'          : 'template_catalog_full_text_key',
      'description' : 'A list of ids of catalog full text keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_request_key',
      'description' : 'A list of ids of catalog request keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_multivalue_key',
      'description' : 'A list of ids of catalog multivalue keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_topic_key',
      'description' : 'A list of ids of catalog topic keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_catalog_scriptable_key',
      'description' : 'A list of ids of catalog scriptable keys used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_site_property_id',
      'description' : 'A list of ids of site properties used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_base_category',
      'description' : 'A list of ids of base categories used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_action_path',
      'description' : 'A list of ids of actions used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_extension_id',
      'description' : 'A list of ids of extensions used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_test_id',
      'description' : 'A list of ids of tests used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_path',
      'description' : 'A list of object paths used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_preference',
      'description' : 'A list of preferences used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_message_translation',
      'description' : 'A list of message translations used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_local_roles',
      'description' : 'A list of local roles used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_portal_type_roles',
      'description' : 'A list of ERP5Types for which we want to add the roles in the template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_tool_id',
      'description' : 'A list of Tool ids used by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'publication_url',
      'description' : 'A url on a webdav server which contains the business template source',
      'type'        : 'string',
      'mode'        : 'w', },
    { 'id'          : 'change_log',
      'description' : 'A change log',
      'type'        : 'text',
      'mode'        : 'w',
      'default'     : '' },
    { 'id'          : 'dependency',
      'description' : 'a list of template names required by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'provision',
      'description' : 'a list of template names provided by this template',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_format_version',
      'description' : 'Business Template format version',
      'type'        : 'int',
      'mode'        : 'w',
      'default'     : 0 },
    { 'id'          : 'license',
      'description' : 'License',
      'type'        : 'text',
      'mode'        : 'w',
      'default'     : '' },
    { 'id'          : 'copyright',
      'description' : 'A list of copyright holders',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'maintainer',
      'description' : 'A list of maintainers',
      'type'        : 'lines',
      'mode'        : 'w',
      'default'     : () },
    { 'id'          : 'template_update_business_template_workflow',
      'description' : 'A flag indicating if we have to update business template workflows',
      'type'        : 'boolean',
      'mode'        : 'w',
      'default'     : 0 },
    { 'id'          : 'template_update_tool',
      'description' : 'A flag indicating if we have to update tools',
      'type'        : 'boolean',
      'mode'        : 'w',
      'default'     : 0 },
 )

  _categories = ( )
