import unittest
import sys
import json
from io import StringIO
from commands.langoon import Command

class TestCommand(Command, unittest.TestCase):

    def setUp(self):
        sys.argv = ['name-of-command.py', '-first,111', '-second,222']
        self.parse_options(first=111, second=222, third=333)

    def test_parse_options(self):
        self.assertDictEqual(self.options, {'first': 111, 'second': 222, 'third': 333})

    def test_send_response(self):
        sys.stdout = StringIO()
        self.send_response({ "first": 111, "second": 222 })
        response = sys.stdout.getvalue()
        sys.stdout.close()
        self.assertDictEqual(json.loads(response), {"command": "_run_code", "options": {"first": 111, "second": 222, "third": 333}, "data": {"first": 111, "second": 222}})

if __name__ == '__main__':
    unittest.main()
