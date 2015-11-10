import os
import sys
from netmiko import ConnectHandler

USERNAME = cisco
PASSWORD = !cisco123!
HOSTNAME = 68.170.147.164
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
            ip=HOSTNAME,
            username=USERNAME,
            password=PASSWORD,
            verbose=False)

    def setUp(self):
        self.failure = False
        self.login()
        self.cisco_switch.send_command('checkpoint ' + CHECKPOINT_NAME)

    def test_snippets(self):
        for snippet_file in os.listdir(SNIPPET_DIR):
            self.cisco_switch.send_config_from_file(os.path.join(SNIPPET_DIR, snippet_file))
            ping_result = self.cisco_switch.send_command('ping 192.168.56.2')

            print "=========================="
            print snippet_file
            print "--------------------------"
            print ping_result

            if not ping_is_successful(ping_result):
                self.failure = True

    def tearDown(self):
        self.cisco_switch.send_command('rollback running-config checkpoint ' + CHECKPOINT_NAME)
        self.cisco_switch.send_command('no checkpoint ' + CHECKPOINT_NAME)
        self.cisco_switch.disconnect()


def run():
    connTest = ConnectivityTest()

    connTest.setUp() # Set up switch for testing by creating a checkpoint
    connTest.test_snippets() # Apply all config snippets and run ping_test
    connTest.tearDown() # Rollback to checkpoint created at start of testing and disconnect

    if connTest.failure:
        sys.exit(FAILURE)

    sys.exit(SUCCESS)


if __name__ == "__main__":
    run()
