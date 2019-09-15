from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    hobby = request.args.get('hobby')
    if hobby != None:
        return contacts_hobby_query(hobby)
    return create_response({"contacts": db.get('contacts')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def get_contact_by_id(id):
    contact = db.getById('contacts', int(id))
    if contact is None:
        return create_response(status=404, message="No contact with this id exists")
    return create_response({"contacts": contact})

def contacts_hobby_query(hobby):
    filtered_contacts = [x for x in db.get('contacts') if x['hobby'] == hobby]
    if len(filtered_contacts) == 0:
        return create_response(status=404, message="No contacts with this hobby exist")
    else:
        return create_response({"contacts": filtered_contacts})

@app.route("/contacts", methods=['POST'])
def add_contact():
    req_data = request.get_json()
    try:
        name = req_data["name"]
        hobby = req_data["hobby"]
        nickname = req_data["nickname"]
    except KeyError:
        fail_message = f"Contact is missing key(s) {[x for x in ('name' , 'hobby', 'nickname') if x not in req_data]}"
        return create_response(status=422, message=fail_message)
    new_contact = db.create("contacts", {"name": name, "hobby": hobby, "nickname": nickname})
    return create_response(status=201, data={"contacts": new_contact})

@app.route("/contacts/<id>", methods=['PUT'])
def update_contact(id):
    try:
        req_data = request.get_json()
    except:
        return create_response(status=400, message="Update malformed")
    update_values = {key: val for (key, val) in req_data.items() if key in ('name', 'hobby', 'nickname')}
    updated_contact = db.updateById("contacts", int(id), update_values)
    if updated_contact is None:
        return create_response(status=404, message="No contact with this id exists")
    return create_response(status=201, data={"contacts": updated_contact})

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
