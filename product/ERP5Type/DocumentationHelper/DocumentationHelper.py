##############################################################################
#
# Copyright (c) 2007-2008 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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

from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.ERP5Type import Permissions
from App.config import getConfiguration
from zLOG import LOG, INFO
import os

class DocumentationHelper(Implicit):
  """
    Example URIs

    person_module/23
    person_module/23#title
    person_module/23#getTitle
    portal_worklows/validation_workflow
    portal_worklows/validation_workflow/states/draft
    portal_worklows/validation_workflow/states/draft#title
    Products.ERP5Type.Document.Person.notify
    Products.ERP5Type.Document.Person.isRAD
    portal_types/Person
    portal_types/Person/actions#view
  """
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Methods to override
  def __init__(self, uri):
    self.uri = uri

  def getDocumentedObject(self):
    if self.uri.startswith('portal_classes/temp_instance'):
      url, method = self.uri.split('#')           
      portal_type = url.split('/')[-1]           
      temp_folder = self.getPortalObject().portal_classes.newContent(id='temp_instance', portal_type='Folder', temp_object=1)
      temp_object = temp_folder.newContent(id=portal_type, portal_type=portal_type, temp_object=1)
      if '/' not in method:
        documented_object = getattr(temp_object, method, None)
      else:
        path_method = method.split('/')
        wf_method = path_method[len(path_method)-1]
        documented_object = getattr(temp_object, wf_method, None)
    elif self.uri.endswith('.py'):
      instance_home = getConfiguration().instancehome
      file_name = self.uri.split('/')[-1]
      file_url = ''
      list_path = os.listdir(instance_home+'/Products')
      zope_property_sheet = instance_home + '/PropertySheet' 
      list_propertysheets = [zope_property_sheet,]
      for path in list_path:
        full_path = instance_home+'/Products/'+path      
        if os.path.isdir(full_path) and os.path.exists(full_path+'/PropertySheet'): 
          list_propertysheets.append(full_path+'/PropertySheet')
      for propertysheet_directory in list_propertysheets:
        if os.path.exists(propertysheet_directory+'/'+file_name):              
          file_url = propertysheet_directory+'/'+file_name
      documented_object = open(file_url)
    elif '/' in self.uri and '#' not in self.uri:
      # URI refers to a portal object
      # and is a relative URL
      try:
        documented_object = self.getPortalObject().portal_categories.resolveCategory(self.uri)
      except:
        documented_object = None      
      if documented_object is None:
         documented_object = self.getPortalObject().unrestrictedTraverse(self.uri)
    elif '/' in self.uri and '#' in self.uri:
      if '?' in self.uri:
        base_url, url = self.uri.split('?')
        type, name = url.split('#')
        parent_object = self.getPortalObject().unrestrictedTraverse(base_url)
        object_list = getattr(parent_object, type, None)
        documented_object = None
        if object_list is not None:
          for obj in object_list:
            if obj.__name__ == name:
              documented_object = obj    
      else:
        url, method = self.uri.split('#')
        documented_object = self.getPortalObject().unrestrictedTraverse(url)
        if '/' not in method:
          documented_object = self.getPortalObject().unrestrictedTraverse(url)
          documented_object = getattr(documented_object, method, None)
        else:
          path_method = method.split('/')
          wf_method = path_method[len(path_method)-1]
          documented_object = getattr(documented_object, wf_method, None)
    else:
      # URI refers to a python class / method
      import imp
      module_list = self.uri.split('.')
      base_module = module_list[0]
      if base_module == 'Products':
        # For now, we do not even try to import
        # or locate objects which are not in Products
        import Products
        documented_object = Products
        for key in module_list[1:]:
          #LOG('Baye, loop in module_list', 0,'do=%s et uri=%s' % (repr(documented_object), self.uri))
          documented_object = getattr(documented_object, key)
      else:
        raise NotImplemented
        #fp, pathname, description = imp.find_module(base_module)
        #documented_object = imp.load_module(fp, pathname, description)
    return documented_object

  def getTitle(self):
    """
    Returns the title of the documentation helper
    (ex. class name)
    """
    raise NotImplemented

  def getType(self):
    """
    Returns the type of the documentation helper
    (ex. Class, float, string, Portal Type, etc.)
    """
    raise NotImplemented

  security.declareProtected(Permissions.AccessContentsInformation, 'getSectionList')
  def getSectionList(self):
    """
    Returns a list of documentation sections
    """
    return []

  security.declareProtected(Permissions.AccessContentsInformation, 'getURI')
  def getURI(self):
    """
    Returns a URI to later access this documentation
    from portal_classes
    """
    return self.uri

  # Generic methods which all subclasses should inherit
  security.declareProtected(Permissions.AccessContentsInformation, 'getClassName')
  def getClassName(self):
    """
    Returns our own class name
    """
    return self.__class__.__name__

  security.declareProtected(Permissions.AccessContentsInformation, 'view')
  def view(self):
    """
    Renders the documentation with a standard form
    ex. PortalTypeInstanceDocumentationHelper_view
    """
    return getattr(self, '%s_view' % self.getClassName())()

  security.declareProtected(Permissions.AccessContentsInformation, '__call__')
  def __call__(self):
    return self.view()

InitializeClass(DocumentationHelper)
