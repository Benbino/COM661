from flask import Flask, jsonify, make_response, request
import uuid, random

app = Flask(__name__)

businesses = []

#git_test

def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast', 'Lisburn', 'Balllymena', 'Derry', 'Newry', 'Enniskillen', 'Omagh',
             'Newcastle']
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i + 1)
        town = towns[random.randint(0, len(towns) - 1)]
        rating = random.randint(0, 5)
        business_dict[id] = {
            "name": name, "town": town, "rating": rating, "reviews": {}
        }
    return business_dict


@app.route("/", methods=["GET"])
def index():
    return make_response("<h1>Hello world</h1>", 200)


@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_buisnesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    businesses_list = [{k: v} \
                       for k, v in businesses.items()]

    data_to_return = businesses_list[page_start:page_start + page_size]
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    if id in businesses:
        return make_response(jsonify(businesses[id]), 200)
    else:
        return make_response(jsonify({"error": "Invalid Business ID"}), 404)


@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" in request.form and \
            "town" in request.form and \
            "rating" in request.form:
        next_id = str(uuid.uuid1())
        new_business = {
            "name": request.form["name"],
            "town": request.form["town"],
            "rating": request.form["rating"],
            "reviews": {}
        }
        businesses[next_id] = new_business
        return make_response(jsonify({next_id: new_business}), 201)
    else:
        return make_response(jsonify({"Error": "Missing form data"}), 404)


@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response(jsonify({"Error": "Invalid Business ID"}), 404)
    else:
        if "name" not in request.form and \
                "town" not in request.form and \
                "rating" not in request.form:
            return make_response(jsonify({"Error": "Missing form data"}), 404)
        else:
            if "name" in request.form:
                businesses[id]["name"] = request.form["name"]
            if "town" in request.form:
                businesses[id]["town"] = request.form["town"]
            if "rating" in request.form:
                businesses[id]["rating"] = request.form["rating"]
            return make_response(jsonify({id: businesses[id]}), 200)


@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"Error": "Invalid Business ID"}), 404)


@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    reviews_list = [{k: v} \
                    for k, v in businesses[id]["reviews"].items()]

    data_to_return = reviews_list[page_start:page_start + page_size]
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    if b_id not in businesses:
        return make_response(jsonify({"Error": "Invalid Business ID"}), 404)
    else:
        if "username" in request.form and \
                "comment" in request.form and \
                "stars" in request.form:
            r_id = str(uuid.uuid1())
            new_review = {
                "username": request.form["username"],
                "comment": request.form["comment"],
                "stars": request.form["stars"]
            }
            businesses[b_id]["reviews"][r_id] = new_review
            return make_response(jsonify({r_id: new_review}), 200)
        else:
            return make_response(jsonify({"Error": "Missing form data"}), 404)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"Error": "Invalid Business ID"}), 404)
    elif r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"Error": "Invalid Business ID"}), 404)
    else:
        if "username" not in request.form and \
                "comment" not in request.form and \
                "stars" not in request.form:
            return make_response(jsonify({"Error": "Missing form data"}), 404)
        else:
            if "username" in request.form:
                businesses[b_id]["reviews"][r_id]["username"] = request.form["username"]
            if "comment" in request.form:
                businesses[b_id]["reviews"][r_id]["comment"] = request.form["comment"]
            if "stars" in request.form:
                businesses[b_id]["reviews"][r_id]["stars"] = request.form["stars"]
            return make_response(jsonify({r_id: businesses[b_id]["reviews"][r_id]}), 200)


@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    del businesses[b_id]["reviews"][r_id]
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)
