

# Ants

Ants is a "wiki" website where the content is generated by its users. 
It is built with [Python][0] using the [Django Web Framework][1], 

It uses the wonderful [Waliki project](https://github.com/mgaitan/waliki) and leverages from waliki models' Page.

This project has the following basic apps:

* [Waliki](https://github.com/mgaitan/waliki) (A wiki engine that kicks up Git as a text database)
* Homepage: A dummy cms that builds itelf up from the wiki. Its goal is to promote the content of the wiki to the non- or anonymous-user.

To come:

*  Stats (A text miner because its fun :)

## Installation

### Quick start

To set up a development environment quickly, first install Python 2.7. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ virtualenv env`
    2. `$ . env/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Detailed instructions

Static settings:

the "static" folder contains the initial general static files and are there as primary source.
The "staticfiles" folder contains the files gathered from all staticfiles directories (apps and general).

Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
