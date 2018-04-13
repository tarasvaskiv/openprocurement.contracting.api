# -*- coding: utf-8 -*-
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.api.utils import update_logging_context, error_handler
from openprocurement.api.validation import validate_json_data, validate_data


def validate_contract_data(request):
    update_logging_context(request, {'contract_id': '__new__'})
    data = request.validated['json_data'] = validate_json_data(request)
    model = request.contract_from_data(data, create=False)

    return validate_data(request, model, data=data)


def validate_accreditation(request):
    model = request.validated['contract']
    content_conf = request.registry.queryMultiAdapter((model, request),
                                                      IContentConfigurator)

    if hasattr(request, 'check_accreditation') and not \
               request.check_accreditation(content_conf.create_accreditation):
        request.errors.add('contract', 'accreditation',
                'Broker Accreditation level does not permit contract creation')
        request.errors.status = 403
        raise error_handler(request.errors)
