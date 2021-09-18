import difflib
from pygls.lsp import CodeAction, CodeActionKind, Command, WorkspaceEdit, TextEdit, Range, Position
from ..util import load_document

def process_quick_fix(ls, diag, text_document):
    if diag.message.__contains__('Unknown object'):
        obj = diag.message.split('"')[1]

        print(obj)
        diag.range.end.character = diag.range.start.character + obj.__len__()

        new_text = determine_fix(obj, load_document(ls, text_document.uri), diag.message)
        fix = CodeAction(title='Fix typo',
                         kind=CodeActionKind.QuickFix,
                         edit=WorkspaceEdit(
                             changes={text_document.uri : [TextEdit(range=diag.range, new_text=new_text)] }
                         ))
        return [fix]


def determine_fix(obj, source, error_message):
    # TODO: setup logic
    return 'Real'