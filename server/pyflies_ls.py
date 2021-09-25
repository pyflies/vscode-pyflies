import time
from pygls.lsp.methods import (COMPLETION, DEFINITION, TEXT_DOCUMENT_DID_CHANGE,
                               CODE_ACTION, TEXT_DOCUMENT_DID_OPEN)

# from pygls.capabilities import COMPLETION, TEXT_DOCUMENT_DID_CHANGE
from typing import List, Optional, Union
from pygls.server import LanguageServer
from pygls.lsp import (CompletionItem, CompletionList, CompletionOptions,
                       CompletionParams, DefinitionParams, DidChangeTextDocumentParams,
                       DidOpenTextDocumentParams, CodeActionOptions, CodeActionKind,
                       CodeActionParams, CodeAction, Command, Location)
from pygls.workspace import Document
from .features.validate import validate
from .features.completion import process_completions, trigger_characters
from .features.code_actions import process_quick_fix
from .features.definitions import resolve_definition
from .util import load_document, get_entire_string_from_index

COUNT_DOWN_START_IN_SECONDS = 12
COUNT_DOWN_SLEEP_IN_SECONDS = 1

class PyfliesLanguageServer(LanguageServer):

    def __init__(self):
        super().__init__()

def _validate(ls, params):

    source = load_document(ls, params.text_document.uri)
    diagnostics = validate(source) if source else []

    ls.publish_diagnostics(params.text_document.uri, diagnostics)


pyflies_server = PyfliesLanguageServer()

@pyflies_server.feature(COMPLETION, CompletionOptions(trigger_characters=trigger_characters()))
def completions(params: CompletionParams):
    """Returns completion items."""

    return process_completions()


@pyflies_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate(ls, params)

@pyflies_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    _validate(ls, params)

@pyflies_server.feature(DEFINITION)
def definitions(ls, params: DefinitionParams):
    # source = load_document(ls, params.text_document.uri)
    text_doc = ls.workspace.get_document(params.text_document.uri)
    name = get_entire_string_from_index(text_doc.offset_at_position(params.position), text_doc.source)
    defs = resolve_definition(text_doc.source, name, params.text_document.uri)
    return [defs]

@pyflies_server.feature(CODE_ACTION, CodeActionOptions(code_action_kinds=[CodeActionKind.Refactor]))
def code_actions(ls, params: CodeActionParams) -> Optional[List[Union[Command, CodeAction]]]:
    diag = params.context.diagnostics
    if diag.__len__() == 0:
        return None
    else:
        return process_quick_fix(ls, diag[0], params.text_document)
