from setuptools import setup, find_packages

# 从 requirements.txt 中读取依赖
def read_requirements(file_name):
    with open(file_name, 'r') as f:
        return [line.strip() for line in f.readlines() if line and not line.startswith('#')]


setup(name='weather_tool',
      version='0.2',
      description='the simple tool to query weather',
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
      ],
      url='https://github.com/Terrdi/simple-weather-query-tool',
      author='Terrdi',
      author_email='675464934@qq.com',
      license='MIT',
      packages=find_packages(),
      install_requires=read_requirements('requirements.txt'),
      zip_safe=True
)
