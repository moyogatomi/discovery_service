from setuptools import setup, find_packages

setup(
    name="discovery_service",
    version="0.2",
    packages=find_packages(),
    entry_points={'console_scripts': [
        'discovery = discovery_service.cli_interface:run_entrypoint',
    ],
	},
)