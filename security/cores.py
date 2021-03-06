import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import format_html, mark_safe
from django.utils.translation import ugettext_lazy as _

from is_core.generic_views.inlines.inline_form_views import TabularInlineFormView
from is_core.main import UIRESTModelISCore
from is_core.utils.decorators import short_description

from security.models import CommandLog, InputLoggedRequest, OutputLoggedRequest, OutputLoggedRequestRelatedObjects

from ansi2html import Ansi2HTMLConverter


def display_json(value):
    return json.dumps(value, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)


def display_as_code(value):
    return format_html('<code style="white-space:pre-wrap;">{}</code>', value) if value else value


class RequestsLogISCore(UIRESTModelISCore):

    abstract = True

    can_create = can_update = can_delete = False

    @short_description(_('queries'))
    def queries_code(self, obj=None):
        return display_as_code(display_json(obj.queries)) if obj else None

    @short_description(_('request body'))
    def request_body_code(self, obj=None):
        return display_as_code(obj.request_body) if obj else None

    @short_description(_('request headers'))
    def request_headers_code(self, obj=None):
        return display_as_code(display_json(obj.request_headers)) if obj else None

    @short_description(_('response body'))
    def response_body_code(self, obj=None):
        return display_as_code(obj.response_body) if obj else None

    @short_description(_('response headers'))
    def response_headers_code(self, obj=None):
        return display_as_code(display_json(obj.response_headers)) if obj else None

    @short_description(_('error description'))
    def error_description_code(self, obj=None):
        return display_as_code(obj.error_description) if obj else None


class InputRequestsLogISCore(RequestsLogISCore):

    model = InputLoggedRequest
    ui_list_fields = (
        'request_timestamp', 'response_timestamp', 'response_time', 'status', 'response_code', 'host', 'short_path',
        'slug', 'ip', 'user', 'method', 'type', 'short_response_body', 'short_request_body', 'short_queries',
        'short_request_headers'
    )

    form_fieldsets = (
        (_('Request'), {'fields': ('request_timestamp', 'host', 'method', 'path', 'queries_code',
                                   'request_headers_code', 'request_body_code', 'is_secure')}),
        (_('Response'), {'fields': ('response_timestamp', 'response_code', 'status', 'response_headers_code',
                                    'response_body_code', 'type', 'error_description_code')}),
        (_('User information'), {'fields': ('user', 'ip')}),
        (_('Extra information'), {'fields': ('slug', 'response_time', 'output_logged_requests')}),
    )

    abstract = True


class OutputLoggedRequestRelatedObjectsInlineFormView(TabularInlineFormView):

    model = OutputLoggedRequestRelatedObjects
    fields = ('display_object',)


class OutputRequestsLogISCore(RequestsLogISCore):

    model = OutputLoggedRequest
    ui_list_fields = (
        'request_timestamp', 'response_timestamp', 'response_time', 'status', 'response_code', 'host', 'short_path',
        'method', 'slug', 'short_response_body', 'short_request_body', 'input_logged_request', 'short_queries',
        'short_request_headers'
    )

    form_fieldsets = (
        (_('Request'), {'fields': ('request_timestamp', 'host', 'method', 'path', 'queries_code',
                                   'request_headers_code', 'request_body_code', 'is_secure')}),
        (_('Response'), {'fields': ('response_timestamp', 'response_code', 'status', 'response_headers_code',
                                    'response_body_code', 'error_description_code')}),
        (_('Extra information'), {'fields': ('slug', 'response_time', 'input_logged_request')}),
        (_('Related objects'), {'inline_view': OutputLoggedRequestRelatedObjectsInlineFormView}),
    )

    abstract = True


class CommandLogISCore(UIRESTModelISCore):

    model = CommandLog

    create_permission = False
    update_permission = False
    delete_permission = False

    ui_list_fields = ('command_name', 'start', 'stop', 'executed_from_command_line', 'is_successful')

    form_fieldsets = (
        (None, {
            'fields': ('command_name', 'command_options', 'output_html'),
            'class': 'col-sm-6'
        }),
        (None, {
            'fields': ('start', 'stop', 'executed_from_command_line', 'is_successful'),
            'class': 'col-sm-6'
        }),
    )

    abstract = True

    @short_description(_('command output'))
    def output_html(self, obj=None):
        if obj and obj.output is not None:
            conv = Ansi2HTMLConverter()
            output = mark_safe(conv.convert(obj.output, full=False))
            return display_as_code(output)
        return None
