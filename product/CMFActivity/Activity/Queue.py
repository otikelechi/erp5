##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

import pickle
from Acquisition import aq_base
from Products.CMFActivity.ActivityTool import Message
from zLOG import LOG

class Queue:
  """
    Step 1: use lists

    Step 2: add some object related dict which prevents calling twice the same method

    Step 3: add some time information for deferred execution

    Step 4: use MySQL as a way to store events (with locks)

    Step 5: use periodic Timer to wakeup Scheduler

    Step 6: add multiple threads on a single Scheduler

    Step 7: add control thread to kill "events which last too long"

    Some data:

    - reindexObject = 50 ms

    - calling a MySQL read = 0.7 ms

    - calling a simple method by HTTP = 30 ms

    - calling a complex method by HTTP = 500 ms

    References:

    http://www.mysql.com/doc/en/InnoDB_locking_reads.html
    http://www.python.org/doc/current/lib/thread-objects.html
    http://www-poleia.lip6.fr/~briot/actalk/actalk.html
  """

  #scriptable_method_id_list = ['appendMessage', 'nextMessage', 'delMessage']

  def __init__(self):
    self.is_alive = {}
    self.is_awake = {}
    self.is_initialized = 0

  def initialize(self, activity_tool):
    # This is the only moment when
    # we can set some global variables related
    # to the ZODB context
    if not self.is_initialized:
      self.activity_tool = activity_tool
      self.is_initialized = 1

  def queueMessage(self, activity_tool, m):
    pass

  def dequeueMessage(self, activity_tool, processing_node):
    pass

  def tic(self, activity_tool, processing_node):
    # Tic should return quickly to prevent locks or commit transactions at some point
    if self.dequeueMessage(activity_tool, processing_node):
      self.sleep(activity_tool, processing_node)

  def distribute(self, activity_tool, node_count):
    pass

  def sleep(self, activity_tool, processing_node):
    self.is_awake[processing_node] = 0

  def wakeup(self, activity_tool, processing_node):
    self.is_awake[processing_node] = 1

  def terminate(self, activity_tool, processing_node):
    self.is_awake[processing_node] = 0
    self.is_alive[processing_node] = 0

  def validate(self, activity_tool, message, wait_for=None, **kw):
    try:
      if activity_tool.unrestrictedTraverse(message.object_path) is None:
        # Do not try to call methods on objects which do not exist
        LOG('WARNING ActivityTool', 0,
           'Object %s does not exist' % '/'.join(message.object_path))
        return 0
    except:
      LOG('WARNING ActivityTool', 0,
           'Object %s could not be accessed' % '/'.join(message.object_path))
      # Do not try to call methods on objects which cause errors
      return 0
    if wait_for is not None:
      if wait_for():
        return 0
    return 1

  def isAwake(self, activity_tool, processing_node):
    return self.is_awake[processing_node]

  def hasActivity(self, activity_tool, object, **kw):
    return 0

  def flush(self, activity_tool, object, **kw):
    pass

  def loadMessage(self, s):
    return pickle.loads(s)

  def dumpMessage(self, m):
    return pickle.dumps(m)

  def getMessageList(self, activity_tool, processing_node=None):
    return []
