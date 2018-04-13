# -*- coding: utf-8 -*-
import unittest

from pyramid.interfaces import IRequest
from uuid import uuid4
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.api.tests.base import snitch
from openprocurement.contracting.api.tests.base import (
    BaseWebTest, Contract, ContractConfigurator
)
from openprocurement.contracting.api.tests.contract_blanks import (
    # ContractResourceTest
    empty_listing,
)


class ContractResourceTest(BaseWebTest):
    """ contract resource test """

    test_empty_listing = snitch(empty_listing)


class ContractPostViewTest(BaseWebTest):

    def setUp(self):
        super(ContractPostViewTest, self).setUp()
        self.test_data = {
            "contractType": "common",
            "dateModified": "2017-06-21T16:02:54.560542+03:00",
            "documents": [{'id': uuid4().hex, 'url': 'fake_url',
                           'title': 'fake_title',
                           'format': 'application/msword'}]
        }

        self.app.app.registry.contract_contractTypes = {'common': Contract}
        self.app.app.registry.registerAdapter(ContractConfigurator, (Contract, IRequest),
                                    IContentConfigurator)

    def test_post_view(self):
        self.app.authorization = ('Basic', ('contracting', ''))
        response = self.app.post_json('/contracts', {'data': self.test_data})

        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn('access', response.json)
        self.assertIn('data', response.json)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContractResourceTest))
    suite.addTest(unittest.makeSuite(ContractPostViewTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
