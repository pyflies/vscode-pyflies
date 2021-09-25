from pygls.lsp.types.basic_structures import Location, Position
from textx import metamodel_for_language
from pygls.lsp import Location, Range, Position

def pos_to_range(position):
    return Range(
        start=Position(line=position[0]-1, character=position[1]),
        end=Position(line=position[0]-1, character=position[1]+1)
    )

def resolve_definition(model, param_name, uri):
    mm = metamodel_for_language('pyflies')
    m = mm.model_from_str(model)

    defs = [x for x in m.routine_types if x.name == param_name]
    return Location(uri=uri, range=pos_to_range(m._tx_parser.pos_to_linecol(defs[0]._tx_position)))
