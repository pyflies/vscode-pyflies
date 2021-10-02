import json
import re

from pygls.lsp.types.language_features import completion
from textx.exceptions import TextXError, TextXSyntaxError
from textx import metamodel_for_language
from ..util import load_snippets, load_document, get_model_from_source
from .validate import construct_diagnostic, validate
from pygls.lsp import CompletionList, CompletionItem, CompletionParams, CompletionItemKind, InsertTextFormat

def trigger_characters():
    return ['t', 's', 'f', 'i', 'l', 'r', 'a', 'k', 'm']

def filter_snippets(trigger_character, snippets:json):
    if trigger_character is None:
        return snippets
    else:
        snippets_final = {}
        for k in snippets.keys():
            if k.startswith(trigger_character):
                snippets_final[k] = snippets[k]
        return snippets_final

def check_snippet(snippet, metamodel, model, offset):

    # Replaces dynamic parts of the snippet body with a hardcoded variable name to prevent false syntax errors
    snippet_body = snippet['body'].replace('${0}','')
    test_body = re.sub('\${([0-9]:[A-Za-z]*|[0-9])}', 'var1', snippet_body)
    test_source = model[:offset] + test_body + model[offset:]

    try:
        metamodel.model_from_str(test_source)
    except TextXError as err:
        if err.__class__ == TextXSyntaxError:
            return False

    return True

def resolve_completion_items(server, snippets, position, uri):

    doc = load_document(server, uri)
    mm = metamodel_for_language('pyflies')

    offset = doc.offset_at_position(position)
    completion_items = []

    for snippet in snippets.values():

        if check_snippet(snippet, mm, doc.source, offset) is False:
            continue

        completion_items.append(CompletionItem(
            label=snippet['prefix'],
            kind=CompletionItemKind.Snippet,
            insert_text=snippet['body'],
            insert_text_format=InsertTextFormat.Snippet,
        ))

    return completion_items

def process_completions(server, params: CompletionParams):

    snippets = filter_snippets(params.context.trigger_character, load_snippets())
    completion_items = resolve_completion_items(server, snippets, params.position, params.text_document.uri)

    return CompletionList(
        is_incomplete=False,
        items = completion_items
    )
