# Copyright 2019 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import unittest

from vwo.event import event_dispatcher
from vwo.services import singleton


class DispatcherTest(unittest.TestCase):

    def setUp(self):
        self.dispatcher = event_dispatcher.EventDispatcher()

    def tearDown(self):
        singleton.forgetAllSingletons()

    # The method test_dispatch_fires_request has references from "Optimizely Python SDK, version 3.2.0",
    # Copyright 2016-2019, Optimizely, used under Apache 2.0 License.
    # Source - https://github.com/optimizely/python-sdk/blob/master/tests/test_event_dispatcher.py
    def test_dispatch_fires_request(self):
        """ Test that dispatch event fires off requests call with provided URL
        and params. """

        properties = {
            'uId': 'demo_user',
            'combination': 1,
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',
            'ed': '{"p": "server"}',
            'random': 0.7382938446947298,
            'ap': 'server',
            'u': '09CD6107E42B51F9BFC3DD97EA900990',
            'experiment_id': 229,
            'sId': 1565949670,
            'sdk-v': '1.0.2',
            'sdk': 'python',
            'account_id': 88888888,
        }

        with mock.patch('vwo.http.connection.Connection.get') as mock_request_get:
            mock_request_get.return_value = {'status_code': 200, 'text': ''}
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, True)

        url = properties.get('url')
        del properties['url']
        mock_request_get.assert_called_once_with(url, params=properties)

    def test_dispatch_error_status_code(self):
        """ Test that dispatch returns False if status_code != 200. """
        properties = {
            'uId': 'demo_user',
            'combination': 1,
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',
            'ed': '{"p": "server"}',
            'random': 0.7382938446947298,
            'ap': 'server',
            'u': '09CD6107E42B51F9BFC3DD97EA900990',
            'experiment_id': 229,
            'sId': 1565949670,
            'sdk-v': '1.0.2',
            'sdk': 'python',
            'account_id': 88888888,
        }

        with mock.patch('vwo.http.connection.Connection.get') as mock_request_get:
            mock_request_get.return_value.status_code = 503
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, False)
