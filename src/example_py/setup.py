from setuptools import find_packages, setup

package_name = "example_py"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="xiaoaug",
    maintainer_email="xiaoaug@foxmail.com",
    description="test the python",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "node_02 = example_py.node_02:main",
            "node_04 = example_py.node_04:main",
        ],
    },
)
