# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - See the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) for information on how to install the latest version of Python for your platform.

2. **Virtual Environment** Whenever you use Python for a project, we recommend working in a virtual environment. This separates and organizes the dependencies for each project. The [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) have instructions on how to set up a virtual environment for your platform.

3. **PIP Dependencies** - Once your virtual environment is up and running, navigate to the /backend directory and run the following command:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a microservices backend framework with a small weight. Requests and answers must be handled with Flask.

- To handle the lightweight SQL database, we'll use [SQLAlchemy](https://www.sqlalchemy.org/), a Python SQL toolkit and ORM. You'll mostly be working on 'app.py,' but'models.py' will come in handy.

- We'll utilize [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### API Documentation

### Gettting Started

- Base URL: This application is currently only available on a localhost5000. 'http://127.0.0.1:5000/'
- Authentication: Neither authentication nor API keys are required in this version.

### Eror Handling

## 400

`jsonify({ "success": False, "error": 400, "message": "This seems like a bad request, please try again" })`

## 404

`jsonify({ "success": False, "error": 404, "message": "Requested resource could not be found" })`

## 422

`jsonify({ "success": False, "error": 422, "message": "The requested resouce could not be processed" })`

API Error Messages

400 – This seems like a bad request, please try again
404 – Requested resource could not be found
422 – The requested resouce could not be processed

### EndPoints

`GET '/categories'`

Returns a list of categories of objects, success value, and all_categories
`curl http://127.0.0.1:5000/categories`

```
  "all_categories": 6,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```

`GET '/questions'`
-Returns a list of categories of objects, success value, and all_categories -`curl http://127.0.0.1:5000/questions`

```
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"questions": [
{
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
.......
],
"success": true,
"total_questions": 17
```

`DELETE "/questions/<int:question_id>"`
-Deletes question by id if it exists. Returns the deleted question, success value, total questions. -`curl -X DELETE http://127.0.0.1:5000/questions/4`

```
"deleted": 15,
"success": true,
"total_books": 11
}
```

`POST '/questions'`
-Returns a list of questions of objects, success value, id of question created, and total questions available

CREATE QUESTIONS
`curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is there love in sharing?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'`

```
  "question_created": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    .......
  ],
  "question_id": 28, (i.e id of the created question)
  "success": true,
  "total_questions": 21
}
```

SEARCH QUESTIONS
`curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "money"}' -H 'Content-Type: application/json'`

```
}
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 1
}

```

` GET /categories/<category_id>/questions`
-Returns a list of questions of objects, success value, category id, category type, and total questions available

`curl -X GET http://127.0.0.1:5000/categories/3/questions`

```
 "category": 3,
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "thats japa",
      "category": 3,
      "difficulty": 4,
      "id": 24,
      "question": "runnn"
    },
    {
      "answer": "thats japa",
      "category": 3,
      "difficulty": 4,
      "id": 25,
      "question": "runnn"
    }
  ],
  "success": true,
  "total_questions": 5
}
```

` POST /quizzes`
-Returns a dictionary of only one random question per time, its success value, question id, question, category id, difficulty, answer

`curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Art", "id" : "2"}} ' -H 'Content-Type: application/json'`

```
 "question": {
    "answer": "Escher",
    "category": 2,
    "difficulty": 1,
    "id": 16,
    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  },
  "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
