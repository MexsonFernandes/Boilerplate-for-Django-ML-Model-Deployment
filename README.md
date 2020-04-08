# Boilerplate for Django Machine Learning Model Deployment
<a href='https://ko-fi.com/Y8Y31LBT4' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi3.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Technology stack:
* Django (Python web framework)
* R

## Get started:
  - Make sure you have `R` installed in your system
    * Install R dependencies.
    
      `install.packages('nnet')`

  - Add your username and password in https://github.com/MexsonFernandes/RegressionModelBuilding-Django/blob/master/ModelBuilding/settings.py
    - EMAIL_HOST_USER = '<user_name>@gmail.com'
    - EMAIL_HOST_PASSWORD = 'abcd123'
  - Make sure that you are able to execute 'Rscript' command from terminal or command prompt.



## Start server:
  * Create or start virtual environment using `pipenv`.

    `pipenv shell`
  * Install dependencies.

    `pip install -r requirements.txt`
  * Start Django server.

    `python manage.py runserver`
