# Payments Alert Generation

Cube Test - Currently implemented without the timestamp conditions, I wasn't sure how that should be done without actually having a stream of data (for manual inputs I was not sure how the duration conditions were to be given). Everything else works.

For scalability: I thought of implementing python threads to have concurrent functions for timely alerts but I wasn't sure if that was in the scope of the project.

I am open to updating my code with updates on above as per need. Thank you :)

## Getting Started

Find the project here: https://hub.docker.com/r/raghavmittal97/cube_t

### Prerequisites

Make sure to have flask and flask_mysqldb installed on your system.

```
pip install Flask
pip install Flask-MySQLdb
```

### Installing

If the docker file does not run:

```
Unzip the cube.zip file
```

And then

```
run Cube.py in the directory
```
Finally

```
visit 127.0.0.1:5000 (default) in your browser
```
## Deployment

Open your browser, by default the homepage should run on 127.0.0.1:5000. 

Enter details manually for a test run (make sure you have logs.txt in the directory and make sure to run Cube.py before you do this!).

Comment out line 39 in Cube.py once you have created the table.

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used

## Authors

* **Raghav Mittal** - [Raghav](https://github.com/raghavmittal97/)

## License

This project is not licensed.

## Acknowledgments

* Thanks to Google for all the love
