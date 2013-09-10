#!flask/bin/python
from flask import Flask, jsonify
import json


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

roadmapData = [
  [
	{"rowTitle":"Holidays"}
    ,{"date":"2012/05/28","title":"Memorial Day"}
    ,{"date":"2012/07/04","title":"Independence\nDay"}
    ,{"date":"2012/09/03","title":"Labor Day"}
    ,{"date":"2012/11/22","title":"Thanksgiving"}
    ,{"date":"2012/12/25","title":"Christmas"}
  ]
  ,[
    {"rowTitle":"Events"}
    ,{"date":"2012/05/09","title":"May Event"}
    ,{"date":"2012/06/29","title":"June Event"}
    ,{"date":"2012/09/23","title":"September Event"}
  ]
  ,[
    {"rowTitle":"Milestones"}
    ,{"date":"2012/02/07","title":"Milestone 1"}
    ,{"date":"2012/06/25","title":"Milestone 2"}
    ,{"date":"2012/10/20","title":"Milestone 3"}
  ]
]

projectData = [
  [
    {"rowTitle":"Milestones"}
    ,{"date":"2012/02/07","title":"Milestone 1"}
    ,{"date":"2012/06/25","title":"Milestone 2"}
    ,{"date":"2012/10/20","title":"Milestone 3"}
  ]
]

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/rmap/data', methods = ['GET'])
@crossdomain(origin='*')
def get_rmap():
    print "returning json"
    return json.dumps(projectData)

if __name__ == '__main__':
    app.run(debug = True)
