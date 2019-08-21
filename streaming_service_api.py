from flask import Flask, request
from streaming_service import StreamingService
from movie import Movie
from tv_series import TVSeries
import json

app = Flask(__name__)

ENT_DB = 'entertainments.sqlite'
streaming_service = StreamingService(ENT_DB)


@app.route('/streamingservice/entertainment', methods=['POST'])
def add_entertainment():
    """ Adds a movie or tv series to streaming service if not already exists """
    try:
        content = request.json

        if content['type'] == "Movie":
            movie = Movie(content['id'], content['name'], content['year_released'], content['director'],
                                      content['rating'], content['type'], content['length'])

            id = streaming_service.add(movie)
            response = app.response_class(
                response=("Movie or tv series with id ", str(id), " added successfully"),
                status=200
            )
            return response

        elif content['type'] == "TV series":
            tv_series = TVSeries(content['id'], content['name'], content['year_released'], content['director'],
                                 content['rating'], content['type'])
            id = streaming_service.add(tv_series)
            response = app.response_class(
                response=("Movie or tv series with id ", str(id), " added successfully"),
                status=200
            )

            return response
        else:
            raise ValueError("Type is invalid")

    except ValueError:
        response = app.response_class(
            response="Movie or tv series is invalid",
            status=400
        )
        return response


@app.route('/streamingservice/entertainment/<int:ent_id>', methods=['PUT'])
def update(ent_id):
    """ Updates an existing movie or tv series """
    try:
        content = request.json

        if content['type'] == "Movie":
            movie = Movie(ent_id, content['name'], content['year_released'], content['director'],
                      content['rating'], content['type'], content['length'])

            streaming_service.update(movie)

            response = app.response_class(
                status=200
            )
            return response

        elif content['type'] == "TV series":
            tv_series = TVSeries(ent_id, content['name'], content['year_released'], content['director'],
                             content['rating'], content['type'])

            streaming_service.update(tv_series)

            response = app.response_class(
                status=200
            )
            return response

    except ValueError as e:
        if str(e) == "Movie or TV series not found":
            response = app.response_class(
                status=404,
                response=str(e)
            )
        else:
            response = app.response_class(
                status=400,
                response=str(e)
            )

        return response


@app.route('/streamingservice/entertainment/<int:ent_id>', methods=['DELETE'])
def delete(ent_id):
    """ Deletes a movie or a tv series based on id """
    try:
        content = request.json

        if content['type'] == "Movie":
            streaming_service.delete(ent_id)
            response = app.response_class(
                status=200
            )
            return response
        if content['type'] == "TV series":
            streaming_service.delete(ent_id)
            response = app.response_class(
                status=200
            )

            return response

    except ValueError as e:
        if str(e) == "Movie or TV series not found":
            response = app.response_class(
                response=str(e),
                status=404
            )
        else:
            response = app.response_class(
                response="ID is invalid",
                status=400
            )

        return response


@app.route('/streamingservice/entertainment/<int:ent_id>', methods=['GET'])
def get_by_id(ent_id):
    """ Retrieves an existing movie or tv series """
    try:
        ent = streaming_service.get(ent_id)
        response = app.response_class(
            status=200,
            response=json.dumps(ent.to_dict()),
            mimetype='application/json'
        )
        return response

    except ValueError as e:
        if str(e) == "Movie or TV series does not exist":
            response = app.response_class(
                status=404,
                response=str(e)
            )
            return response
        else:
            response = app.response_class(
                status=400,
                response=str(e)
            )
            return response


@app.route('/streamingservice/entertainment/all', methods=['GET'])
def get_all():
    """ Retrieve all movies and tv series """

    entertainment = streaming_service.get_all()

    entertainment_list = []

    for ent in entertainment:
        entertainment_list.append(ent.to_dict())

    response = app.response_class(
        status=200,
        response=json.dumps(entertainment_list),
        mimetype='application/json'
        )
    return response


@app.route('/streamingservice/entertainment/all/<string:ent_type>', methods=['GET'])
def get_by_type(ent_type):
    """ Retrieve all movies or TV series based on type """
    try:
        if ent_type == "Movie" or ent_type == "TV series":
            entertainment = streaming_service.get_all_by_type(ent_type)

            entertainment_list = []

            for ent in entertainment:
                entertainment_list.append(ent.to_dict())

            response = app.response_class(
                status=200,
                response=json.dumps(entertainment_list),
                mimetype='application/json'
            )
            return response
        else:
            raise ValueError("Type is invalid")

    except ValueError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response


if __name__ == "__main__":
    app.run()
