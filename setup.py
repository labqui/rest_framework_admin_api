from setuptools import setup

REQUIREMENTS = (
    'Django==3.1.13',
    'djangorestframework'
)
TEST_REQUIREMENTS = (

)

setup(
    name='rest_framework_admin_api',
    version='0.0.1',
    packages=[''],
    long_description=open('README.md', 'rt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/labqui/rest_framework_admin_api',
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    license='MIT',
    author='Thalles Rosa',
    author_email='labufes@gmail.com',
    description='Um pacote que expõe o admin do django para uma API REST.'
)
