# from crypt import methods
# from crypt import methods
# from crypt import methods
import os
from unicodedata import category
from flask import Flask, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_pages(request, data_needed):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_data_needed = [each_data.format() for each_data in data_needed]
    available_data = formatted_data_needed[start:end]

    return available_data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_available_categories():
        print(get_available_categories)
        categories = Category.query.order_by(Category.id).all()
        current_categories = {
            category.id: category.type for category in categories
        }
        # available_categories = paginate_pages(request, current_categories)

        if len(current_categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": current_categories,
                "all_categories": len(Category.query.all()),
            }
        )
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def get_paginated_questions():
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_pages(request, questions)

        all_categories = Category.query.order_by(Category.id).all()
        each_category = {}
        for category in all_categories:
            each_category[category.id] = category.type

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "categories": each_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            each_question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if each_question is None:
                abort(404)

            each_question.delete()
            return jsonify({
                "success": True,
                "deleted_question_id": question_id,
                "total_books": len(Question.query.all())
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # @app.route("/questions", methods=["POST"])
    # def create_question():

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"])
    def search_or_create_question():
        body = request.get_json()

        search_term = body.get("searchTerm", None)
        try:
            if search_term:
                results = Question.query.filter(Question.question.ilike("%{}%".format(
                    search_term)))

                formatted_results = [result.format() for result in results]

                return jsonify({
                    "success": True,
                    "questions": formatted_results,
                    "total_questions": len(formatted_results)
                })
            else:
                question = body.get("question", None)
                answer = body.get("answer", None)
                category = body.get("category", None)
                difficulty = body.get("difficulty", None)

                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()

                questions = Question.query.all()
                paginated_questions = paginate_pages(request, questions)

                return jsonify({
                    "success": True,
                    "question_id": new_question.id,
                    "question_created": paginated_questions,
                    "total_questions": len(questions)
                })
        except:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_question_based_on_catgory(category_id):
        try:
            category = Category.query.order_by(Category.id).filter(
                Category.id == category_id).one_or_none()
            if category is None:
                abort(404)
            question = Question.query.filter(
                Question.category == category_id).all()
            paginated_questions = paginate_pages(request, question)
            return jsonify({
                "success": True,
                "questions": paginated_questions,
                "total_questions": len(question),
                "category": category_id,
                "current_category": category.type
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_questions_to_play_quiz():
        try:
            body = request.get_json()

            prev_question = body.get("previous_questions", None)
            category = body.get("quiz_category", None)

            # if prev_question or category is None:
            #     abort(404)
            # if not ('quiz_category' in body and 'previous_questions' in body):
            #     abort(422)

            if not prev_question:
                if category is None:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.category == Category.id, Question.category == category["id"]).all()
            else:
                if category is None:
                    questions = Question.query.filter(
                        Question.id.notin_(prev_question)).all()
                else:
                    questions = Question.query.filter(Question.category == Category.id,
                                                      Question.category == category["id"], Question.id.notin_(prev_question)).all()
            formatted_questions = [question.format() for question in questions]
            total_questions = len(formatted_questions)

            random_integer = random.randint(0, total_questions - 1)
            random_question = formatted_questions[random_integer]

            return jsonify({
                "success": True,
                "question": random_question
            })

        except:
            abort(404)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def Request_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Requested resource could not be found"
        }), 404

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "The requested resource could not be processed"
        }), 422

    @app.errorhandler(400)
    def Bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "This seems like a bad request, please try again"
        }), 400

    return app
