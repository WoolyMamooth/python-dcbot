from setuptools import setup

setup(
    name='dcbot',
    version='0.7.5',
    packages=['wooly_dcbot','wooly_dcbot/games','wooly_dcbot/net'],
    url='',
    license='',
    author='Wooly',
    author_email='',
    description='simple discord bot',
    install_requires=['beautifulsoup4==4.12.3','selenium==4.20.0',
                      'requests==2.31.0','python-dotenv==1.0.1','discord==2.3.2']
)