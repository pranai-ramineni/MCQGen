from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='pranai raminei',
    author_email='pr.ramineni@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)

# pip install requirements.txt
from setuptools import find_packages,setup
