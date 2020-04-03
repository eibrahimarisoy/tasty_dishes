# tasty_dishes
This is a simple recipe sharing application.

# General Features
- Registered users can share and search recipes for tasty dishes.
- And edit and delete recipe, also update their own profile(email, password etc).
- Anonymous people can only search and look into recipes.

# Recipe Features
- Name, Difficulty, Image, Description and Ingredients that may be expanded.

# Installation
```sh
$ git clone https://github.com/eibrahimarisoy/tasty_dishes.git
$ cd tasty_dishes/
$ virtualenv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py runserver
$ open http://127.0.0.1:8000/
```
