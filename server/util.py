def load_document(ls, uri):
    text_doc = ls.workspace.get_document(uri)

    return text_doc.source
