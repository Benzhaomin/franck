from setuptools import setup, find_packages

setup(
    name = 'franck',
    version = '0.5.3',
    packages = find_packages(),
    scripts = ['http/franck-http', 'cli/franck-cli'],
    test_suite = 'tests',

    install_requires = [
        'appdirs >= 1.4.0',
        'beautifulsoup4 >= 4.3.2',
        'bottle >= 0.12.8',
        'requests >= 2.7.0',
    ],

    # metadata
    author = 'Benjamin Maisonnas',
    author_email = 'ben@wainei.net',
    description = 'Get video files from JeuxVideo.com video pages.',
    license = 'GPLv3',
    #keywords = "",
    url = 'http://github.com/benzhaomin/franck',
)
