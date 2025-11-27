import re

def classify_error(parsed):
    etype = (parsed.get("error_type") or "").strip()
    msg = (parsed.get("message") or "").strip().lower()

    # Normalize
    etype_lower = etype.lower()

    # ============================
    # NAME / VARIABLE RELATED
    # ============================
    if "nameerror" in etype_lower:
        if "not defined" in msg:
            return "UNDECLARED_VARIABLE"
        return "NAME_ERROR"

    # ============================
    # ATTRIBUTE ERROR
    # ============================
    if "attributeerror" in etype_lower:
        if "has no attribute" in msg:
            return "ATTRIBUTE_NOT_FOUND"
        return "ATTRIBUTE_ERROR"

    # ============================
    # INDEX / KEY ERRORS
    # ============================
    if "indexerror" in etype_lower:
        if "out of range" in msg:
            return "INDEX_OUT_OF_RANGE"
        return "INDEX_ERROR"

    if "keyerror" in etype_lower:
        return "KEY_NOT_FOUND"

    # ============================
    # TYPE ERRORS
    # ============================
    if "typeerror" in etype_lower:
        if "unsupported operand" in msg:
            return "TYPE_MISMATCH"
        if "not callable" in msg:
            return "CALLING_NON_CALLABLE"
        if "object is not subscriptable" in msg:
            return "TYPE_NOT_SUBSCRIPTABLE"
        if "object is not iterable" in msg:
            return "TYPE_NOT_ITERABLE"
        if "can only concatenate" in msg:
            return "TYPE_CONCAT_ERROR"
        return "TYPE_ERROR"

    # ============================
    # ZERO DIVISION
    # ============================
    if "zerodivisionerror" in etype_lower:
        return "ZERO_DIVISION"

    # ============================
    # SYNTAX / INDENTATION
    # ============================
    if "indentationerror" in etype_lower:
        return "INDENTATION_ERROR"

    if "syntaxerror" in etype_lower:
        if "expected" in msg and ":" in msg:
            return "SYNTAX_MISSING_COLON"
        if "unexpected eof" in msg:
            return "SYNTAX_UNEXPECTED_EOF"
        if "invalid syntax" in msg:
            return "SYNTAX_INVALID"
        if "invalid character" in msg:
            return "SYNTAX_INVALID_CHARACTER"
        return "SYNTAX_ERROR"

    # ============================
    # MODULE / IMPORT ERRORS
    # ============================
    if "modulenotfounderror" in etype_lower:
        return "MODULE_NOT_FOUND"

    if "importerror" in etype_lower:
        return "IMPORT_ERROR"

    # ============================
    # VALUE ERROR
    # ============================
    if "valueerror" in etype_lower:
        if "invalid literal" in msg:
            return "INVALID_LITERAL"
        return "VALUE_ERROR"

    # ============================
    # RECURSION
    # ============================
    if "recursionerror" in etype_lower:
        return "RECURSION_NO_BASE_CASE"

    # ============================
    # FILE ERRORS
    # ============================
    if "filenotfounderror" in etype_lower:
        return "FILE_NOT_FOUND"

    # ============================
    # DEFAULT
    # ============================
    return "UNKNOWN_ERROR"
