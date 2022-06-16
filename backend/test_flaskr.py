import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # ----------------------------------------------------------------------------#
    # Tests to GET all available Categories
    # ----------------------------------------------------------------------------#

    def test_get_all_available_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    # ----------------------------------------------------------------------------#
    # Tests to GET requests for questions, including pagination (every 10 questions).
    # ----------------------------------------------------------------------------#
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["total_questions"])
        self.assertEqual(len(data["categories"]))

    def test_not_valid_paginated_questions_(self):
        res = self.client().get("/questions?page=100000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Page not Found")
        self.assertEqual(data["success"], False)
    # ----------------------------------------------------------------------------#
    # Tests to DELETE question using a question ID.
    # ----------------------------------------------------------------------------#

    def test_delete_question_with_id(self):
        # create a new question to be tested
        question = {
            "question": "what's your name?",
            "id": "4",
            "category": "2"
        }
        question_id = question["id"]  # this gets the id of the question
        # create a new question in json format
        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)
        # delete the newly created question with its id
        res = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # check if question is none after deletion
        self.assertEqual(question, None)

    def test_delete_question_with_id_error_404(self):
        res = self.client().delete("/questions/{2000}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    # ----------------------------------------------------------------------------#
    # Tests to DELETE question using a question ID.
    # ----------------------------------------------------------------------------#

    def test_create_new_question(self):
        question = {
            "question": "what is your name",
            "answer": "i am udacity",
            "category": "4",
            "difficulty": "4"
        }

        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_question_422_fail(self):
        # will ail if a required parameter is missing
        question = {
            "question": "what is your name",
            "answer": "i am udacity",
            "category": "4"
        }
        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"], "Unprocessable, a parameter could be missing")
    # ----------------------------------------------------------------------------#
    # Tests to GET questions based on a search term.
    # ----------------------------------------------------------------------------#

    def test_question_from_search_term(self):
        search_term = {
            "search": "i am a man"
        }

        res = self.client().post("/questions", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"])
        self.assertEqual(len(data["questions"]))

    def test_question_from_search_term_422_fail(self):
        res = self.client().post("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"], "Unprocessable, please input a valid search term")

    # ----------------------------------------------------------------------------#
    # Tests to GET questions based on category.
    # ----------------------------------------------------------------------------#
    def test_question_by_category(self):
        category = {
            "id": 1
        }
        category_id = category["1"]
        res = self.client().get("/categories/{}/questions".format(category_id), json=category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["total_categories"]))

    def test_question_by_category_400(self):
        category = {
            "id": 1000
        }
        category_id = category["id"]
        res = self.client().get("/categories/{}/questions".format(category_id), json=category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success", False])
        self.assertEqual(data["message"], "Bad Request, id not found")
    # ----------------------------------------------------------------------------#
    # Tests to GET questions to play the quiz.
    # ----------------------------------------------------------------------------#

    def test_get_questions_to_play_quiz(self):
        new_quiz = {
            "previous_questions": [6, 7],
            "quiz_category": {
                "type": "foods",
                "id": 5
            }
        }

        res = self.client().post("/quizzes", json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_error_400_questions_to_play_quiz(self):
        # quiz has no parameter
        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request, no parameter passed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
