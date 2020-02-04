##############################################################################
# Copyright (c) 2019-2020 Nexedi SA and Contributors. All Rights Reserved.
#                     Kazuhiko <kazuhiko@nexedi.com>
#                     Vincent Pelletier <vincent@nexedi.com>
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
from Products.ERP5Type.Timeout import getPublisherDeadlineValue
from ZPublisher import Publish
from ZPublisher.Publish import *

def publish(request, module_name, after_list, debug=0,
            # Optimize:
            call_object=call_object,
            missing_name=missing_name,
            dont_publish_class=dont_publish_class,
            mapply=mapply,
            ):

    (bobo_before, bobo_after, object, realm, debug_mode, err_hook,
     validated_hook, transactions_manager)= get_module_info(module_name)

    parents=None
    response=None

    try:
        with getPublisherDeadlineValue(request):
            notify(PubStart(request))
            # TODO pass request here once BaseRequest implements IParticipation
            newInteraction()

            request.processInputs()

            request_get=request.get
            response=request.response

            # First check for "cancel" redirect:
            if request_get('SUBMIT', '').strip().lower() == 'cancel':
                cancel = request_get('CANCEL_ACTION', '')
                if cancel:
                    # Relative URLs aren't part of the spec, but are accepted by
                    # some browsers.
                    for part, base in zip(urlparse(cancel)[:3],
                                          urlparse(request['BASE1'])[:3]):
                        if not part:
                            continue
                        if not part.startswith(base):
                            cancel = ''
                            break
                if cancel:
                    raise Redirect, cancel

            after_list[0]=bobo_after
            if debug_mode:
                response.debug_mode=debug_mode
            if realm and not request.get('REMOTE_USER',None):
                response.realm=realm

            if bobo_before is not None:
                bobo_before()

            # Get the path list.
            # According to RFC1738 a trailing space in the path is valid.
            path=request_get('PATH_INFO')

            request['PARENTS']=parents=[object]

            if transactions_manager:
                transactions_manager.begin()

            object=request.traverse(path, validated_hook=validated_hook)

            notify(PubAfterTraversal(request))

            if transactions_manager:
                transactions_manager.recordMetaData(object, request)

            result=mapply(object, request.args, request,
                          call_object,1,
                          missing_name,
                          dont_publish_class,
                          request, bind=1)

            if result is not response:
                response.setBody(result)

            notify(PubBeforeCommit(request))

            if transactions_manager:
                transactions_manager.commit()
            endInteraction()

            notify(PubSuccess(request))

            return response
    except:
        # save in order to give 'PubFailure' the original exception info
        exc_info = sys.exc_info()
        # DM: provide nicer error message for FTP
        sm = None
        if response is not None:
            sm = getattr(response, "setMessage", None)

        if sm is not None:
            from asyncore import compact_traceback
            cl,val= sys.exc_info()[:2]
            sm('%s: %s %s' % (
                getattr(cl,'__name__',cl), val,
                debug_mode and compact_traceback()[-1] or ''))

        # debug is just used by tests (has nothing to do with debug_mode!)
        if not debug and err_hook is not None:
            retry = False
            if parents:
                parents=parents[0]
            try:
                try:
                    with getPublisherDeadlineValue(request):
                        return err_hook(parents, request,
                                        sys.exc_info()[0],
                                        sys.exc_info()[1],
                                        sys.exc_info()[2],
                                        )
                except Retry:
                    if not request.supports_retry(request):
                        with getPublisherDeadlineValue():
                            return err_hook(parents, request,
                                            sys.exc_info()[0],
                                            sys.exc_info()[1],
                                            sys.exc_info()[2],
                                            )
                    retry = True
            finally:
                # Note: 'abort's can fail. Nevertheless, we want end request handling
                try:
                    try:
                        notify(PubBeforeAbort(request, exc_info, retry))
                    finally:
                        if transactions_manager:
                            transactions_manager.abort()
                finally:
                    endInteraction()
                    notify(PubFailure(request, exc_info, retry))

            # Only reachable if Retry is raised and request supports retry.
            newrequest=request.retry()
            request.close()  # Free resources held by the request.

            # Set the default layer/skin on the newly generated request
            if ISkinnable.providedBy(newrequest):
                setDefaultSkin(newrequest)
            try:
                return publish(newrequest, module_name, after_list, debug)
            finally:
                newrequest.close()

        else:
            # Note: 'abort's can fail. Nevertheless, we want end request handling
            try:
                try:
                    notify(PubBeforeAbort(request, exc_info, False))
                finally:
                    if transactions_manager:
                        transactions_manager.abort()
            finally:
                endInteraction()
                notify(PubFailure(request, exc_info, False))
            raise

Publish.publish = publish
