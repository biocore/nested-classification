from setuptools import setup, find_packages


setup(
    name="q2-nested-classification",
    version='0.0.30',
    packages=find_packages(),
    url="https://qiime2.org",
    license="BSD-3-Clause",
    description="QIIME2 package meant for nested-classification in a taxonomic hierachy tree. Utilizing q2-sample-classifiers, classifiers are trained with metadata-subsets at every unique node in the taxonomic tree. New feature-table can be inserted to predict evolutionary classification if the metadata is identical.",
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
