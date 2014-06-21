# Note: this is a fix for very known issue with pytest and Django
# http://pytest-django.readthedocs.org/en/latest/faq.html#i-see-an-error-saying-could-not-import-myproject-settings
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

setup(name='atmatr')
