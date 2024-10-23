import argparse
import sys
import json
import os
import requests


# CHAT_BACKEND_URL
ANNOTATION_URL = 'http://46.4.115.181:5000/query'

def get_template(file_name):

    if file_name == 'init': 
        # make an initializer json for the visualizer
        sys.exit(0)
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the file
    file_path = os.path.join(current_dir, 'test-data', f'{file_name}.json')

    # Open the file using the absolute path
    with open(file_path, 'r') as file:
        query_req = json.load(file)

    return query_req


def call_chat_backend(data):
    return 1


def call_annotation_service(query):

    query_req = None

    query_req = get_template(query)

    response = requests.post(url=ANNOTATION_URL, json=query_req)

    if response.status_code != 200:
      exit_code = 1
      sys.exit(exit_code)

    return response.json()

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = _parser().parse_args(argv)

    prompt = args.prompt
    query = args.query
    hg = args.hg


    if prompt == None and query == None:
        raise ValueError('argument can not be empty')

    response = call_annotation_service(query[1]) if query != None else call_chat_backend()

    print(response)

    exit_code = 0
    sys.exit(exit_code)

def _parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-file", type=str, help="files to export")
    parser.add_argument("-prompt", type=str, help="NL prompt", default='No prompt')
    parser.add_argument("-query",nargs='+' , type=str, help="list of arguments", default=None)
    parser.add_argument("-hg",nargs='+' , type=str, help="list of arguments", default=None)
    return parser


if __name__ == "__main__":
    main()