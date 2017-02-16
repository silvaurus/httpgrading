import argparse
import subprocess
import requests
import time
from test.support import resource


STATIC_RESOURCES = 'www'


class HttpTester(object):
    """
    List of expected objects
    """
    expected_resources = [
        '/index.html',
        '/foo/bar.html',
        '/images/uchicago/logo.png',
    ]

    """
    List of expected redirects
    """
    expected_redirects = {
        '/cats': 'http://en.wikipedia.org/wiki/Cat',
        '/uchicago/cs': 'http://www.cs.uchicago.edu/',
    }


    """
    List of non-existed objects
    """
    non_existed_objects = [
        '/indeex.html',
        '/foo/barr.html',
    ]

    def __init__(self, server_class, server_port):
        self.server_class = server_class
        self.server_port = server_port
        self.server_process = None
        self.http_host = 'http://localhost:{}'.format(server_port)

    def create_server(self):
        server_start_command = [
            'java',
            self.server_class,
            '--serverPort={}'.format(self.server_port),
        ]
        print('starting server with command')
        print(server_start_command)
        try:
            self.server_process = subprocess.Popen(server_start_command)
            print('Got server process')
            print(self.server_process.pid)
            time.sleep(0.1)
        except Exception as e:
            print('got exception when trying to open server process')
            print(e)

    def check_expected_resources(self):
        for resource in self.expected_resources:
            try:
                res = requests.get('{}{}'.format(self.http_host, resource))
                assert res.status_code == 200
            except IOError as e:
                print('Got io error in getting expected resources')
                print('Error: {}'.format(str(e)))
        print('Success! Checking expected resources.')
        
        
    def check_expected_redirects(self):
        for redirect in self.expected_redirects:
            try:
                res = requests.head('{}{}'.format(self.http_host, redirect))
                assert res.status_code == 301
            except IOError as e:
                print('Got io error in redirect')
                print('Error: {}'.format(str(e)))
        print('Success! Checking redirect resources.')
        
    def check_non_existed_objects(self):
        for object in self.non_existed_objects:
            try:
                res = requests.get('{}{}'.format(self.http_host, object))
                assert res.status_code == 404
            except IOError as e:
                print('Got io error in non-existed objects')
                print('Error:{}'.format(str(e)))
        print('Success! Checking non-existed objects.')
                
    def check_post_request(self):
        for resource in self.expected_resources:
            try:
                res = requests.post('{}{}'.format(self.http_host, resource))
                assert res.status_code == 403
            except IOError as e:
                print('Got io error in POST requests')
                print('Error:{}'.format(str(e)))
        print('Success! Checking post requests.')
                
    def check_head_request(self):
        for resource in self.expected_resources:
            try:
                res = requests.head('{}{}'.format(self.http_host, resource))
                assert res.status_code == 200
            except IOError as e:
                print('Got io error in HEAD requests')
                print('Error:{}'.format(str(e)))
                        
        for redirect in self.expected_redirects:
            try:
                res = requests.head('{}{}'.format(self.http_host, redirect))
                assert res.status_code == 301
            except IOError as e:
                print('Got io error in HEAD requests')
                print('Error: {}'.format(str(e)))
                        
        print('Success! Checking head requests.')


    def destroy_server(self):
        self.server_process.kill()


parser = argparse.ArgumentParser()
parser.add_argument('--server-class', default='Server')
parser.add_argument('--server-port', default=8888)

args = parser.parse_args()

tester = HttpTester(
    args.server_class,
    args.server_port,
)
#tester.create_server()
tester.check_expected_resources()
tester.check_expected_redirects()
tester.check_non_existed_objects()
tester.check_post_request()
tester.check_head_request()
#tester.destroy_server()
