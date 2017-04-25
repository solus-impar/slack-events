import os.path
from setuptools import setup, find_packages
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

requirements_path = os.path.join(here, 'requirements.txt')
install_requirements = parse_requirements(requirements_path, session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='slack-events',
    version='0.7.1',
    description='A python3 slack events bot.',
    author='Mike Canoy',
    author_email='canoym@wwu.edu',
    url='https://github.com/solus-impar/slack-events',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    keywords='events bot slack',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    py_modules=['slack-events', 'events'],
    entry_points={
        'console_scripts': [
            'slack-events=slack_events.slack_events:main',
        ]
    },
)
