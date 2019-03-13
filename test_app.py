import unittest
import os
import json
import sys
import app
import platform


class TestApp(unittest.TestCase):

    # Set up app test client to test api calls
    def setUp(self):
        self.app = app.app.test_client()

    def test_ping(self):
        # Google is considered a trusted site that should work almost always
        # This will test if google is accessible, so should pond5.com
        # and if not, this is a crude test that there is not internet access.
        URL = "www.google.com"
        ping = os.system(" ping -c 1 " + URL)
        if ping==0:
            testPing =  '"Pong"'
        else:
            testPing = '"Unable to ping"'
        response = self.app.get('/ping')
        self.assertEqual(response.get_data().decode().strip(),testPing)

    def test_media_response(self):
        # Test the that two samples retrun the correct information
        responseA = self.app.get('/mediainfo/11497188')
        responseB = self.app.get('/mediainfo/11497190')

        self.assertEqual(
        json.loads(responseA.get_data().decode(sys.getdefaultencoding()))['name'],
         "Samuel Beckett Bridge in Dublin, Ireland. Stock Photos")

        self.assertEqual(
        json.loads(responseA.get_data().decode(sys.getdefaultencoding()))['source'],
         "https://images.pond5.com/samuel-beckett-bridge-dublin-ireland-photo-011497188_iconl.jpeg")

        self.assertEqual(
         int(json.loads(responseA.get_data().decode(sys.getdefaultencoding()))
         ['size']), 25037)

        self.assertEqual(
         json.loads(responseA.get_data().decode(sys.getdefaultencoding()))
         ['dimensions']['height'], 316)

        self.assertEqual(
         json.loads(responseA.get_data().decode(sys.getdefaultencoding()))
         ['dimensions']['width'],
          480)

        self.assertEqual(
         json.loads(responseB.get_data().decode(sys.getdefaultencoding()))['name'],
          "Protest in Dublin, Ireland. Stock Photos")

        self.assertEqual(
         json.loads(responseB.get_data()
         .decode(sys.getdefaultencoding()))['source'],
          "https://images.pond5.com/protest-dublin-ireland-photo-011497190_iconl.jpeg")

    def test_system_response(self):
        # Test that the system information is being transmitted correctly
        # through the API
        system = platform.uname().system
        release = platform.release()
        version = platform.uname().version
        architecture = platform.architecture()
        machine = platform.machine()

        response = self.app.get('/system')

        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['system'], system)

        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['release'], release)

        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['version'], version)

        # Architecture returns tuple or list so compare each value to avoid
        # type errors.
        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['architecture'][0], architecture[0])

        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['architecture'][1], architecture[1])

        self.assertEqual(
         json.loads(response.get_data()
         .decode(sys.getdefaultencoding()))['machine'], machine)


if __name__ == '__main__':
    unittest.main()
