import os
import sys
from netmiko import ConnectHandler

USERNAME = os.getenv('SWITCH_USERNAME')
PASSWORD = os.getenv('SWITCH_PASSWORD')
SNIPPET_DIR = 'snippets'
CHECKPOINT_NAME = 'my_checkpoint'

SUCCESS = 0
FAILURE = 1

def ping_is_successful(ping_result):
    return True if '64 bytes' in ping_result else False

class ConnectivityTest:
    def login(self):
        self.cisco_switch = ConnectHandler(
            device_type='cisco_nxos',
            ip='n9k1',
            username=USERNAME,
            password=PASSWORD)

    def setUp(self):
        self.failure = False
        self.login()
        self.cisco_switch.send_command('checkpoint ' + CHECKPOINT_NAME)

    def test_snippets(self):
        for snippet_file in os.listdir(SNIPPET_DIR):
            self.cisco_switch.send_config_file(snippet_file)
            ping_result = self.cisco_switch.send_command('ping 192.168.56.2')

            if not ping_is_successful(ping_result):
                self.failure = True

    def tearDown(self):
        self.cisco_switch.send_command('rollback running-config checkpoint ' + self.checkpoint_name)
        self.cisco_switch.send_command('no checkpoint ' + self.checkpoint_name)


def run():
    connTest = ConnectivityTest()

    connTest.setUp() # Set up switch for testing by creating a checkpoint
    connTest.test_snippets() # Apply all config snippets and run ping_test
    connTest.tearDown() # Rollback to checkpoint created at start of testing

    if connTest.failue:
        sys.exit(FAILURE)

    sys.exit(SUCCESS)


if __name__ == "__main__":
    run()
