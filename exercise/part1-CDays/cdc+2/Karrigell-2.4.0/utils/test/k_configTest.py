"""
File: k_configTest.py
Author: AN
Description:

Unit testing the k_config module.

We'll import k_config with known karrigell.ini files, and test the attributes
in the imported module.
"""
import os
import sys
import unittest

# Find the k_config module in the folder below this one.
sys.path.append('../core')

class KConfigTest(unittest.TestCase):
    """Test the k_config module"""

    def setUp(self):
        """Set attributes for all tests to use"""
        self.defaults = {
            'port': 80,
            'debug': False,
            'silent': False,
            'gzip': False,
            'persistentSession': False,
            'ignore': [],
            'globalScripts': [],
            'protectedDirs': [],
            'hide_extensions': [],
            'extensions_map': {},
            'alias': {},
            'language': '',
            # AN: Unsure about how this one works.
            # allow_directory_listing
            'base': '',
        }

    def setArgs(self, port=None, debug=False, silent=False, inifile=None):
        """Set the command line options for k_config to read."""
        args = [os.path.join('../','karrigell.py')]
        extend = args.extend
        if port:
            extend(['-P', port])
        if debug:
            extend(['-D'])
        if silent:
            extend(['-S'])
        if inifile:
            extend([inifile])
        # Now the imported k_config file will behave as though we'd specified
        # these through
        sys.argv = args

    def assertMatch(self, config, attribute, value):
        """Assert for the config module that <attribute> equals <value>"""
        self.failUnless(hasattr(config, attribute), 'No config item %s!' % attribute)
        configvalue = getattr(config, attribute)
        self.failUnlessEqual(configvalue, value,
            'k_config.%s == %s, should be %s' % \
                (attribute, configvalue, value))

    def assertMatches(self, config, valuedictionary):
        """Like assertMatch but supply all the values to test at once as
        a dictionary"""
        for attribute, value in valuedictionary.items():
            self.assertMatch(config, attribute, value)

    def testDefaultConfig(self):
        """Test the default config"""
        self.setArgs(inifile='TestKConfig1.ini')
        import k_config
        # AN: Need to reload the module in between tests.
        reload(k_config)
        self.assertEqual(k_config.initFile, 'TestKConfig1.ini')
        self.assertMatches(k_config, self.defaults)

    def checkVirtualHost(self, hosts, name, port, root):
        """Check that the given virtual host details exist in the
        given host dictionary"""
        self.failUnless(hosts.has_key(name), 'No virtual host "%s"' % name)
        host = hosts[name]
        self.failUnless(host.has_key('port'),
            'Virtual host "%s" has no port!' % name)
        self.failUnlessEqual(host['port'], port)
        self.failUnless(host.has_key('rootDir'),
            'Virtual host "%s" has no root!' % name)
        self.failUnlessEqual(host['rootDir'], root)

    def testUserConfig(self):
        """Test the config when all items are overidden in the ini file"""
        self.setArgs(inifile='TestKConfig2.ini')
        import k_config
        reload(k_config)
        self.assertEqual(k_config.initFile, 'TestKConfig2.ini')
        self.assertMatches(k_config, {
            'port': 9966,
            'debug': True,
            'silent': True,
            'gzip': True,
            'persistentSession': True,
            'ignore': ['foo', 'bar', 'baz'],
            'globalScripts': ['string', 'md5'],
            'protectedDirs': ['hiddenfolder', 'dangerousfolder'],
            'hide_extensions': ['exe', 'bat', 'com', 'pif', 'zip'],
            'extensions_map': {'.htm': 'text/html'},
            'alias': {'doc': 'documentation'},
            'language': 'German',
            'base': '',
            })

        # Test user specified virtual hosts.
        self.failUnless(hasattr(k_config, 'virtual_hosts'),
            'No virtual_hosts section!')
        hosts = k_config.virtual_hosts
        self.checkVirtualHost(hosts, 'test:8080', 8080, '.')
        self.checkVirtualHost(hosts, 'test2', 80, '../')

    def testCommandLineOptions(self):
        """Test that the command line options work and override the
        defaults and those specified in the ini file."""
        # Use the command line arguments
        self.setArgs(port=99, debug=1, silent=1, inifile='TestKConfig3.ini')
        import k_config
        reload(k_config)
        self.assertMatches(k_config, {
            'initFile': 'TestKConfig3.ini',
            'port': 99,
            'debug': True,
            'silent': True,
        })


if __name__ == '__main__':
    unittest.main()