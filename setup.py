import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
	name="chplot",
	version="1.0.0",
	author="Paul 'charon25' Kern",
	description="Fast plot any math expression",
	long_description=long_description,
    long_description_content_type='text/markdown',
	python_requires=">=3.9",
	url="https://www.github.com/charon25/Chplot",
	license="MIT",
	packages=setuptools.find_packages(),
	download_url="https://github.com/charon25/Chplot/archive/refs/tags/v1.0.0.tar.gz",
	install_requires=[
		'matplotlib>=3.6.1',
		'mpmath>=1.2.1',
		'numpy>=1.23.4',
		'scipy>=1.9.3',
		'shunting_yard>=1.0.11',
		'tqdm>=4.64.1',
	]
)
