from setuptools import setup


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='flask_session_mysql',
    version='0.0.1',
    description='flask_session_mysql adds server side session manager making applications for flask more secure and efficient in mysql',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Fabioblyk/flask-session-mysql',
    author='Fabioblyk',
    author_email='fabioblyk12@gmail.com',
    license='MIT',
    packages=['flask_session_mysql'],
    install_requires=['flask', 'mysql-connector-python'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)