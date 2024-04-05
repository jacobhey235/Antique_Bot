import setuptools

setuptools.setup(
  include_package_data=True,
  name='Antique_Bot',
  version='1.0',
  description='Antique Bot - an online auction telegram bot.',
  url='https://github.com/jacobhey235/Antique_Bot',
  author='Генг Яков Михайлович, Комбаров Игорь Антонович, Принцман Ева Леонидовна',
  author_email='jacobhey235@mail.ru',
  packages=setuptools.find_packages(),
  install_requiries=['telebot','json','setuptools']
  long_description='Antique Bot - an online auction telegram bot.',
  long_description_content_type='text/markdown',
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
)
