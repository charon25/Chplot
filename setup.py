import setuptools

with open("README.md", "r", encoding="utf-8") as fi:
    long_description = fi.read()

setuptools.setup(
	name="chplot",
	version="1.0.0",
	author="Paul 'charon25' Kern",
	description="Fast plot any math expression",
	long_description=long_description,
    long_description_content_type='text/markdown',
	python_requires=">=3.9",
	url="TODO",
	license="MIT",
	packages=setuptools.find_packages(),
	download_url="TODO",
	install_requires=[
		'shunting_yard>=1.0.5',
		'numpy>=1.23.4',
		'matplotlib>=3.6.1',
		'tqdm>=4.64.1',
	],
)
