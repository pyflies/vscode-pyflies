def load_document(ls, uri):
    text_doc = ls.workspace.get_document(uri)

    return text_doc.source

def get_entire_string_from_index(ind, source):
    start_ind = ind
    while not source[start_ind].isspace():
        start_ind -= 1

    end_ind = ind
    while not source[end_ind].isspace() and not source[end_ind] == '(':
        end_ind += 1

    return source[start_ind+1:end_ind]
