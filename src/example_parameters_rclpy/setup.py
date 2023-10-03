from setuptools import find_packages, setup

package_name = "example_parameters_rclpy"

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
    description="test the parameters python",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "parameters_basic = example_parameters_rclpy.parameters_basic:main"
        ],
    },
)
