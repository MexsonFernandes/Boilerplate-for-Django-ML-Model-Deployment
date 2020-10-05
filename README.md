# Boilerplate for Django Machine Learning Model Deployment
[![HitCount](http://hits.dwyl.com/MexsonFernandes/Boilerplate-for-Django-ML-Model-Deployment.svg)](http://hits.dwyl.com/MexsonFernandes/Boilerplate-for-Django-ML-Model-Deployment)

<a href='https://ko-fi.com/Y8Y31LBT4' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi3.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Technology stack:
* Django (Python web framework)
* R

## Get started:
  - Make sure you have `R` installed in your system
    * Install R dependencies.
    
      `install.packages('nnet')`

  - Make sure that you are able to execute `Rscript` command from terminal or command prompt.



## Start server:
  * Create or start virtual environment using `pipenv`.

    `pipenv shell`
  * Install dependencies.

    `pip install -r requirements.txt`

  * Start dummy email server or add your config in settings file.

    `python -m smtpd -n -DebuggingServer localhost:1025`

  * Start Django server.

    `python manage.py runserver`
