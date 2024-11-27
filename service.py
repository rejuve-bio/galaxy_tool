import argparse
import sys
import json
import os
import requests


# CHAT_BACKEND_URL
ANNOTATION_URL = 'http://46.4.115.181:5000/query'
HYPOTHESIS_GENERATION_URL = 'http://100.67.47.42:5051'

def get_template(file_name):

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the file
    file_path = os.path.join(current_dir, 'test-data', f'{file_name}.json')

    # Open the file using the absolute path
    with open(file_path, 'r') as file:
        query_req = json.load(file)
    
    return query_req

def call_chat_backend(prompt):
   
    return prompt

def call_annotation_service(query, argv=None):

    if argv is None:
        argv = sys.argv[1:]
    args = _parser().parse_args(argv)

    viz = args.viz

    query_req = None

    query_req = get_template(query)
    query = {"query": query_req}

    if viz:
        # Rename the 'predicates' key to 'edges'
        if "+" in query_req:
            query_req["edges"] = query_req.pop("predicates")
        
        query = {"query": query_req}
        print(query)
        exit_code = 0
        sys.exit(exit_code)
    else:
        query_req = {"requests": query_req}

    response = requests.post(url=ANNOTATION_URL, json=query_req)
    # wrap the result in a result to detect and send it to the cytoscape result viewer

    if response.status_code != 200:
      exit_code = 1
      sys.exit(exit_code)

    parse_json = response.json()
    table_output = ""
    for edge in parse_json["edges"]:
        edge_data = edge["data"]
        table_output += (f"{edge_data['source']}\t{edge_data['label']}\t{edge_data['target']}\n")

    return table_output

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = _parser().parse_args(argv)

    prompt = args.prompt
    query = args.query
    hg = args.hg

    if prompt == None and query == None:
        raise ValueError('argument can not be empty')

    response = call_annotation_service(query[0]) if query != None else call_chat_backend(prompt)

    print(response)

    exit_code = 0
    sys.exit(exit_code)

def _parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-file", type=str, help="files to export")
    parser.add_argument("-prompt", type=str, help="NL prompt", default='No prompt')
    parser.add_argument("-query",nargs='+' , type=str, help="list of arguments", default=None)

    parser.add_argument('-viz', action='store_true')
    parser.set_defaults(viz=False)

    parser.add_argument("-hg",nargs='+' , type=str, help="list of arguments", default=None)
    return parser


if __name__ == "__main__":
    main()