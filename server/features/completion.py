from pygls.lsp import CompletionList, CompletionItem

def trigger_characters():
    return ['t', 's', 'f', 'c']

def process_completions():
    return CompletionList(
        is_incomplete=False,
        items=[
            CompletionItem(label='test'),
            CompletionItem(label='screen'),
            CompletionItem(label='flow'),
            CompletionItem(label='target'),
            CompletionItem(label='common'),
        ]
    )
