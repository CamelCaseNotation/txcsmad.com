import json

import sendgrid
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from config.settings.common import SENDGRID_MAILING_LIST_ID, SENDGRID_API_KEY


class OfficerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.is_officer()

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


# doesnt work
class TaOrOfficerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and (self.request.user.is_officer() or self.request.user.is_ta())

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


def add_analytics_context_processor(request):
    """
    A context processor that makes the Google Analytics ID available to the base template. This variable is only
    defined in production. This ID is not private information.
    :param request:
    :return:
    """
    if hasattr(settings, "GOOGLE_ANALYTICS_ID"):
        return {"GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID}
    else:
        return {}


def subscribe_to_newsletter(email, first_name, last_name):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Create/Find Sendgrid Recipient ID
    data = [
        {
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
    ]
    response = sg.client.contactdb.recipients.post(request_body=data)
    body_json = json.loads(response.body.decode('utf-8'))

    recipient_id = body_json['persisted_recipients'][0]

    # Put Sendgrid Recipient ID into mailing list
    sg.client.contactdb.lists._(SENDGRID_MAILING_LIST_ID).recipients._(recipient_id).post()


def subscribe_user_to_newsletter(user):
    name_list = user.full_name.split()
    first_name = name_list[0]
    last_name = name_list[1] if len(name_list) > 1 else ""
    subscribe_to_newsletter(user.email, first_name, last_name)


def unsubscribe_user_to_newsletter(email):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Find Recipient Sendgrid ID
    response = sg.client.contactdb.recipients.search.get(query_params={'email': email})
    body_json = json.loads(response.body.decode('utf-8'))
    print(response.body)
    print(response.status_code)

    # Remove Sendgrid Recipient ID from mailing list
    recipient_id = body_json['recipients'][0]['id']
    sg.client.contactdb.lists._(SENDGRID_MAILING_LIST_ID).recipients._(recipient_id).delete()
