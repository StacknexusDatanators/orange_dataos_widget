from setuptools import setup

setup(
    name="dataos",
    packages=["orange_dataos"],
    package_data={"orange_dataos": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "dataos = orange_dataos"},
)