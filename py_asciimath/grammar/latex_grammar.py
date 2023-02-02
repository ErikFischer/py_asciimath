from itertools import islice

from ..utils.utils import alias_string
from ..translation.latex2asciimath import (
    left_parenthesis,
    right_parenthesis,
    smb,
    unary_functions,
    binary_functions,
)

latex_grammar = r"""
    %import common.WS
    %import common.LETTER
    %import common.NUMBER
    %ignore WS
    %ignore "&"
    start: "\\[" exp "\\]" -> exp
        | "$$" exp "$$" -> exp
        | "$" exp "$" -> exp
        | "$" exp "$" -> exp
        | exp -> exp
    exp: i exp* -> exp
    i: s -> exp_interm 
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
    s: "{{}}" -> ignore
        | _l -> l
        | _r -> r
        | "\\begin{{matrix}}" row_mat (/\\\\/ row_mat?)* "\\end{{matrix}}" -> exp_mat
        | "\\begin{{array}}" centering exp (/\\\\/ exp?)* "\\end{{array}}" -> exp_arr
        | /\\sqrt/ "[" i+ "]" "{{" exp "}}" -> exp_binary
        | "{{" i+ "}}" -> exp
        | _u "{{" exp "}}" -> exp_unary
        | _b modifier? "{{" exp "}}" "{{" exp "}}" -> exp_binary
        | _latex1 -> symbol
        | _latex2 -> symbol
        | _c -> const
        | double_backslash literal -> literals
        | ";" -> literal
        | "?" -> literal
        | "\\phantom" "{{\\rule"("{{"NUMBER+ LETTER+"}}")*"}}" -> ignore
        | "\\displaystyle" -> ignore
        | "\\hspace{{" ignore_numbers ignore_letters "}}" -> ignore
        | "\\left" -> ignore
        | "\\right" -> ignore
        | "\\math" -> ignore
    double_backslash: "\\" -> ignore
    modifier: "[" LETTER+ "]" -> ignore
    centering: "{{" ignore_letters "}}" -> ignore
    ignore_letters: (ignore_letter)+ -> ignore
    ignore_numbers: (ignore_number)+ (ignore_dot ignore_number*)? -> ignore
    ignore_letter: "a".."z" -> ignore
    ignore_number: "0".."9"
    ignore_dot: "." -> ignore
    !literal: "#"|"$"|"§"|";"|"_"|"?"
    !_c: NUMBER
        | LETTER
    !row_mat: exp ("&" exp?)* -> row_mat
    !_l: {} // left parenthesis
    !_r: {} // right parenthesis
    !_b: {} // binary functions
    !_u: {} // unary functions
    !_latex1: {}
    !_latex2: {}
""".format(
    alias_string(left_parenthesis, alias=False, lang_from="latex"),
    alias_string(right_parenthesis, alias=False, lang_from="latex"),
    alias_string(binary_functions, alias=False, lang_from="latex"),
    alias_string(unary_functions, alias=False, lang_from="latex"),
    alias_string(
        dict(islice(smb.items(), len(smb) // 2)),
        alias=False,
        lang_from="latex",
    ),
    alias_string(
        dict(islice(smb.items(), len(smb) // 2, len(smb))),
        alias=False,
        lang_from="latex",
    ),
)
