from setuptools import setup, find_packages

setup(
    name='TrajectoryOracle',
    version='1.0.0',
    description='A comprehensive tool for advanced color picking, bullet trajectory prediction, and anomaly avoidance.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://yourprojecturl.com',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'psutil',
        'cryptography',
        'python-decouple',
        'requests',
        'werkzeug',
        'pyotp',
        'pytest',
        'mss',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'trajectory_oracle = main:run_bullseye',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
