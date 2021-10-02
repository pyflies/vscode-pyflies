import json
from textx import metamodel_for_language

def load_document(ls, uri):
    return ls.workspace.get_document(uri)

def load_document_source(ls, uri):
    return load_document(ls, uri).source

def get_model_from_source(model):
    mm = metamodel_for_language('pyflies')
    return mm.model_from_str(model)

def load_snippets():
    snippets = {}
    with open('snippets/pyflies-snippets.json') as json_file:
        snippets = json.load(json_file)
    return snippets

def get_entire_string_from_index(ind, source):
    start_ind = ind
    while not source[start_ind].isspace():
        start_ind -= 1

    end_ind = ind
    while not source[end_ind].isspace() and not source[end_ind] == '(':
        end_ind += 1

    return source[start_ind+1:end_ind]
