from setuptools import setup, find_packages

# cool stuff

setup(
    name="q2-nested-classification",
    version='0.0.1',
    packages=find_packages(),
    url="https://qiime2.org",
    license="BSD-3-Clause",
    description="what this thing does",
    entry_points={
        "qiime2.plugins":
        ["q2-nested-classification=q2_nc.plugin_setup:plugin"]
    },
    package_data={
        'q2_nc.tests': [],  # any support data that might be needed
                          # for unit tests
        'q2_nc': []  # assets for q2 visualizations
    },
    zip_safe=False,
)
