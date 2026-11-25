"""Practice problems for modules 06 and 07."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-normalize-name",
    "Normalize Name",
    "easy",
    ["python", "unicode"],
    "Implement `solve(text)`. Apply NFC, strip, casefold, and collapse internal whitespace to a single space. Return the resulting string. Empty after strip stays empty.",
    ["Use unicodedata.normalize NFC before casefold", "Whitespace runs become one space"],
    [
        "unicodedata.normalize('NFC', text) first.",
        "strip, then casefold.",
        "Split on whitespace and join with a single space so tabs and repeated spaces collapse.",
    ],
    "Name matching fails when one side is decomposed Unicode, the other is composed, or the spaces differ. NFC makes the code points comparable, casefold handles case, and splitting on whitespace collapses every run. Doing casefold before NFC is usually fine for these inputs. The specified order is NFC, strip, casefold, collapse.",
    "O(n)",
    "O(n)",
    """
def solve(text):
    import unicodedata
    normalized = unicodedata.normalize("NFC", text).strip().casefold()
    return " ".join(normalized.split())
""",
    [
        {"text": "  Ada   Lovelace "},
        {"text": "GRACE"},
        {"text": "  "},
        {"text": "Cafe\u0301"},
    ],
)

add(
    "python-ex-palindrome",
    "Palindrome",
    "easy",
    ["python", "strings"],
    "Implement `solve(text)`. Return 1 when the letters and digits, casefolded, form a palindrome. Ignore every other character. An empty selection is a palindrome and returns 1.",
    ["Only alphanumeric characters count", "Case does not matter"],
    [
        "Keep characters that are alphanumeric, and casefold them.",
        "Compare the sequence to its reverse.",
        "Return 1 or 0.",
    ],
    "The palindrome is on the filtered sequence, not on the raw string. Spaces and punctuation would make a sentence fail even when the letters read the same backward. Two pointers on the filtered list, or a reverse compare, are both linear.",
    "O(n)",
    "O(n)",
    """
def solve(text):
    chars = [ch.casefold() for ch in text if ch.isalnum()]
    return 1 if chars == chars[::-1] else 0
""",
    [
        {"text": "A man, a plan, a canal: Panama"},
        {"text": "race a car"},
        {"text": ""},
        {"text": "0P"},
    ],
    companies=["Facebook", "Microsoft"],
)

add(
    "python-ex-join-words",
    "Join Words",
    "easy",
    ["python", "strings"],
    "Implement `solve(words, sep)`. Strip each word, drop empties, and join the rest with `sep`. Do not put the separator before the first word or after the last.",
    ["sep is a string", "Empty words disappear"],
    [
        "Strip first, then filter.",
        "str.join inserts the separator between items only.",
        "No surviving words returns an empty string.",
    ],
    "join is the linear way to build this string. Concatenating in a loop copies a growing buffer. Filtering blanks first keeps the separator from doubling up around empty slots.",
    "O(n)",
    "O(n)",
    """
def solve(words, sep):
    cleaned = [word.strip() for word in words if word.strip()]
    return sep.join(cleaned)
""",
    [
        {"words": [" a ", "", "b"], "sep": ","},
        {"words": ["  "], "sep": "-"},
        {"words": ["a", "b", "c"], "sep": ""},
        {"words": [], "sep": ","},
    ],
)

add(
    "python-ex-remove-prefix",
    "Remove Prefix",
    "easy",
    ["python", "strings"],
    "Implement `solve(text, prefix)`. If `text` starts with `prefix`, return the remainder. Otherwise return `text` unchanged. Remove the prefix only once. An empty prefix returns `text`.",
    ["Use startswith or removeprefix", "Do not remove a match in the middle"],
    [
        "startswith is the test.",
        "Slice off len(prefix) only when the test passes.",
        "A prefix longer than the text fails the test and returns the text.",
    ],
    "removeprefix does this and leaves the string alone when the prefix is absent. A replace would also delete a later copy. The contract is one leading removal.",
    "O(n)",
    "O(n)",
    """
def solve(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
""",
    [
        {"text": "unittest", "prefix": "unit"},
        {"text": "test", "prefix": "unit"},
        {"text": "aaa", "prefix": "a"},
        {"text": "abc", "prefix": ""},
    ],
)

add(
    "python-ex-anagram",
    "Anagram",
    "medium",
    ["python", "strings"],
    "Implement `solve(left, right)`. Return 1 when the two strings are anagrams after casefold and after removing spaces. Punctuation, if present, counts. Return 0 otherwise.",
    ["Spaces are ignored", "Case is ignored"],
    [
        "casefold and delete spaces on both sides.",
        "Compare Counter values, or sorted strings.",
        "Different lengths after cleaning cannot be anagrams.",
    ],
    "An anagram is the same multiset of characters. Sorting both cleaned strings makes that equality obvious. Counter is the same test and is linear. Forgetting to remove spaces makes a phrase fail against its squashed form.",
    "O(n log n)",
    "O(n)",
    """
def solve(left, right):
    def clean(text):
        return sorted(ch for ch in text.casefold() if ch != " ")
    return 1 if clean(left) == clean(right) else 0
""",
    [
        {"left": "Anagram", "right": "Nag a ram"},
        {"left": "ab", "right": "a"},
        {"left": "Aa", "right": "aa"},
        {"left": "a b", "right": "ba"},
    ],
    companies=["Amazon", "Bloomberg"],
)

add(
    "python-ex-utf8-size",
    "UTF-8 Size",
    "medium",
    ["python", "unicode"],
    "Implement `solve(text)`. Return the number of bytes in the UTF-8 encoding of `text`. Do not change the text. The string length in code points is not the answer when a character needs more than one byte.",
    ["Encode as utf-8", "Return an integer byte count"],
    [
        "text.encode('utf-8') produces the bytes.",
        "len of those bytes is the size.",
        "An empty string is 0 bytes.",
    ],
    "len(text) counts code points. UTF-8 uses one byte for ASCII and more for many other characters. The size on the wire or in a file is the encoded length. Encoding does not modify the str you still hold.",
    "O(n)",
    "O(n)",
    """
def solve(text):
    return len(text.encode("utf-8"))
""",
    [
        {"text": "abc"},
        {"text": "é"},
        {"text": ""},
        {"text": "ह"},
    ],
)

add(
    "python-ex-parse-ids",
    "Parse Ids",
    "easy",
    ["python", "files"],
    "Implement `solve(lines)`. Skip lines that are blank after stripping and lines whose stripped text starts with `#`. Return the remaining lines stripped, in order.",
    ["A comment may have leading spaces", "Do not parse the ids further"],
    [
        "Strip once and reuse that string.",
        "Continue on empty or hash-leading lines.",
        "Append the stripped text.",
    ],
    "An id file is a line protocol with comments. The strip has to happen before the comment test, or a space before the hash becomes an id. The result is the ids, not the raw lines.",
    "O(n)",
    "O(n)",
    """
def solve(lines):
    out = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        out.append(text)
    return out
""",
    [
        {"lines": [" a ", "", "# c", "b"]},
        {"lines": ["# only"]},
        {"lines": []},
        {"lines": ["  # indented", "id"]},
    ],
)

add(
    "python-ex-safe-join",
    "Safe Join",
    "medium",
    ["python", "pathlib"],
    "Implement `solve(base, name)`. `base` and `name` are POSIX-style paths using `/`. Join `name` onto `base` and return the normalized path only when it stays inside `base`. If `name` is absolute or the result escapes `base` with `..`, return the string `error`. Normalization uses lexical `.` and `..` only. Do not touch the filesystem.",
    ["Paths use forward slashes", "An escaping join is error"],
    [
        "Reject a name that starts with /.",
        "Split the joined path and apply . and .. lexically.",
        "The result must equal base or have base plus a slash as a prefix of a segment boundary, not a string prefix of a sibling folder.",
    ],
    "Path traversal is a join that leaves the root you intended. Lexical normalization resolves .. before you check the prefix. A string startswith is not enough if base is /var/app and the result is /var/apple. Compare path segments.",
    "O(n)",
    "O(n)",
    """
def solve(base, name):
    if name.startswith("/"):
        return "error"

    def norm(path):
        parts = []
        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if not parts:
                    return "error"
                parts.pop()
            else:
                parts.append(part)
        return "/" + "/".join(parts)

    base_n = norm(base)
    if base_n == "error":
        return "error"
    joined = base.rstrip("/") + "/" + name
    full = norm(joined)
    if full == "error":
        return "error"
    if full == base_n or full.startswith(base_n + "/"):
        return full
    return "error"
""",
    [
        {"base": "/var/app", "name": "files/a.txt"},
        {"base": "/var/app", "name": "../secret"},
        {"base": "/var/app", "name": "/etc/passwd"},
        {"base": "/var/app", "name": "files/../../app/ok"},
    ],
)

add(
    "python-ex-suffix-swap",
    "Suffix Swap",
    "easy",
    ["python", "pathlib"],
    "Implement `solve(path, new_suffix)`. `path` is a POSIX path. Replace the final suffix, including the dot, with `new_suffix`. `new_suffix` includes the leading dot when you want one. A name with no suffix gains `new_suffix`. Return the path string. Do not change directories.",
    ["Only the last suffix changes", "new_suffix may be an empty string, which removes the suffix"],
    [
        "Split off the last slash so the directory is untouched.",
        "If the filename contains a dot and is not a dotfile with no further dot, replace from the last dot. A leading-dot name like .gitignore has no suffix to replace. Treat a name that starts with a dot and has no other dot as having no suffix.",
        "Append or replace, then rejoin the directory.",
    ],
    "pathlib.Path.with_suffix replaces the last suffix and leaves the parent. A string replace of .txt can hit a directory name. Operating on the final segment only is the safe version of the same idea.",
    "O(n)",
    "O(n)",
    """
def solve(path, new_suffix):
    if "/" in path:
        parent, name = path.rsplit("/", 1)
        prefix = parent + "/"
    else:
        name = path
        prefix = ""
    if name.startswith(".") and name.count(".") == 1:
        stem = name
    elif "." in name:
        stem = name.rsplit(".", 1)[0]
    else:
        stem = name
    return prefix + stem + new_suffix
""",
    [
        {"path": "/tmp/a.txt", "new_suffix": ".md"},
        {"path": "a", "new_suffix": ".txt"},
        {"path": "/tmp/.gitignore", "new_suffix": ".bak"},
        {"path": "a.tar.gz", "new_suffix": ".bz2"},
    ],
)

add(
    "python-ex-atomic-names",
    "Atomic Plan",
    "medium",
    ["python", "files"],
    "Implement `solve(destination)`. Return `{\"tmp\": ..., \"final\": destination}`. `tmp` is the destination plus the suffix `.tmp` in the same directory. This is the plan for writing beside the target and then replacing it. Do not invent a different directory.",
    ["final is the destination unchanged", "tmp is destination plus .tmp"],
    [
        "Do not strip an existing suffix before adding .tmp. Add it at the end.",
        "The directory stays whatever the destination already had.",
        "Return both names.",
    ],
    "An atomic replace writes a complete temp file next to the target, then os.replace swaps the name. The temp name has to be on the same filesystem, which a same-directory suffix guarantees in this lexical plan. A temp directory on another drive would make the replace a copy.",
    "O(n)",
    "O(n)",
    """
def solve(destination):
    return {"tmp": destination + ".tmp", "final": destination}
""",
    [
        {"destination": "/var/app/data.json"},
        {"destination": "data.json"},
        {"destination": "/tmp/a"},
        {"destination": "dir/file.txt"},
    ],
)

add(
    "python-ex-rstrip-newline",
    "Line Strip",
    "easy",
    ["python", "files"],
    "Implement `solve(line)`. Remove a single trailing newline sequence if present: `\\r\\n`, or a final `\\n`, or a final `\\r`. Leave other trailing spaces in place. Do not strip the whole line.",
    ["Only one trailing newline sequence", "Spaces stay"],
    [
        "Check endswith for the two-character sequence first.",
        "Then check the single characters.",
        "If none match, return the line unchanged.",
    ],
    "rstrip() would eat the trailing spaces a fixed-width field might need. A newline at the end of a readline result is the only thing to remove. Checking CRLF first avoids leaving a CR behind when you only strip LF.",
    "O(n)",
    "O(n)",
    """
def solve(line):
    if line.endswith("\\r\\n"):
        return line[:-2]
    if line.endswith("\\n") or line.endswith("\\r"):
        return line[:-1]
    return line
""",
    [
        {"line": "ada\n"},
        {"line": "ada\r\n"},
        {"line": "ada  "},
        {"line": "ada"},
    ],
)

add(
    "python-ex-parse-user",
    "Parse Users",
    "medium",
    ["python", "json"],
    "Implement `solve(payload)`. `payload` is a JSON object string with `name` and `age`. Parse it with the json module. Return `{\"name\": ..., \"age\": ...}` when name is a non-empty string and age is an int that is not a bool and is >= 0. Otherwise return the string `error`. Do not use eval.",
    ["json.loads only", "bool is not an acceptable age"],
    [
        "json.loads the string.",
        "Reject a name that is not a non-empty string.",
        "Reject an age whose type is not exactly int, and reject negatives. type(True) is bool.",
    ],
    "json.loads understands true as a bool, and bool is a subclass of int, so isinstance(age, int) accepts true. type(age) is int is the check that refuses it. eval would execute text. The parser is the json module.",
    "O(n)",
    "O(n)",
    """
def solve(payload):
    import json
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return "error"
    name = data.get("name")
    age = data.get("age")
    if type(name) is not str or not name.strip():
        return "error"
    if type(age) is not int or age < 0:
        return "error"
    return {"name": name, "age": age}
""",
    [
        {"payload": "{\"name\": \"ada\", \"age\": 36}"},
        {"payload": "{\"name\": \"ada\", \"age\": true}"},
        {"payload": "{\"name\": \"\", \"age\": 1}"},
        {"payload": "{\"name\": \"ada\", \"age\": -1}"},
    ],
)

add(
    "python-ex-csv-quoted",
    "CSV Fields",
    "medium",
    ["python", "csv"],
    "Implement `solve(text)`. `text` is one CSV line with header `name,note` already known. The line is a data row, not a header. Parse it with the csv module and return `[name, note]`. A quoted comma stays inside the note. Do not split on every comma yourself.",
    ["Use the csv module", "The row has two fields"],
    [
        "csv.reader on an iterable of one line respects quotes.",
        "Take the first row.",
        "Return the two fields as a list.",
    ],
    "str.split on comma breaks a quoted field that contains a comma. The csv module implements those quotes. DictReader is the same parser with headers. This row is positional: the first field is the name and the second is the note.",
    "O(n)",
    "O(n)",
    """
def solve(text):
    import csv
    import io
    row = next(csv.reader(io.StringIO(text)))
    return [row[0], row[1]]
""",
    [
        {"text": "ada,\"hello, world\""},
        {"text": "grace,plain"},
        {"text": "\"a,b\",c"},
        {"text": "lin,\"x\""},
    ],
)

add(
    "python-ex-json-lines",
    "JSON Lines",
    "medium",
    ["python", "json"],
    "Implement `solve(lines)`. Each non-blank line is a JSON value. Skip blank lines. Collect successful values in `values` and the 1-based line numbers of failures in `errors`. A line number counts every line, including blanks. Return `{\"values\": [...], \"errors\": [...]}`. Do not use eval.",
    ["Blank lines are skipped and are not errors", "Line numbers are 1-based"],
    [
        "enumerate from 1.",
        "json.loads each non-blank line inside a try.",
        "Append the value or the line number. A blank line does neither.",
    ],
    "JSON Lines is one JSON value per line. One bad line should not throw away the file. Recording the line number lets a caller fix the file. eval is the wrong parser because a line can be hostile text, and json.loads will not execute it.",
    "O(n)",
    "O(n)",
    """
def solve(lines):
    import json
    values = []
    errors = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            values.append(json.loads(line))
        except json.JSONDecodeError:
            errors.append(number)
    return {"values": values, "errors": errors}
""",
    [
        {"lines": ["1", "", "{\"a\": 1}", "nope"]},
        {"lines": []},
        {"lines": [" ", "2"]},
        {"lines": ["[", "3"]},
    ],
)

add(
    "python-ex-unknown-keys",
    "Reject Extra",
    "easy",
    ["python", "json"],
    "Implement `solve(payload, allowed)`. `payload` is a dict and `allowed` is a list of keys. Return the sorted list of keys present in the payload that are not allowed. An empty list means the payload has no extras.",
    ["Return sorted keys", "Allowed keys that are absent are fine"],
    [
        "Set of payload keys minus set of allowed keys.",
        "Sort the difference.",
        "Do not return the allowed keys.",
    ],
    "An extra key is how a client smuggles a field your model should reject, or how you notice a typo. The difference of the two sets is the unknown keys. Sorting makes the report stable.",
    "O(n log n)",
    "O(n)",
    """
def solve(payload, allowed):
    return sorted(set(payload) - set(allowed))
""",
    [
        {"payload": {"name": "ada", "role": "admin"}, "allowed": ["name"]},
        {"payload": {"name": "ada"}, "allowed": ["name", "age"]},
        {"payload": {}, "allowed": ["name"]},
        {"payload": {"b": 1, "a": 2}, "allowed": []},
    ],
)

add(
    "python-ex-money-string",
    "Money String",
    "medium",
    ["python", "json"],
    "Implement `solve(raw)`. `raw` is a string the caller claims is a money amount. If it is not a string, return `error`. This includes the case where you would have received a JSON number. The tests pass either a string or the token `float`. Accept a string of digits with an optional decimal point and exactly two decimal places when a point is present, or digits only. Return the normalized two-decimal string using Decimal. Reject a leading sign, spaces, and anything else with `error`.",
    ["The token float means the input was a binary float and is rejected", "No signs"],
    [
        "If raw is the string float, return error immediately.",
        "Parse other strings with Decimal only when the text matches digits and an optional .dd.",
        "Quantize to two places and return str.",
    ],
    "A JSON number is a binary float by the time many stacks hand it to you, and money cannot round-trip through that. Requiring a string keeps the exact digits. The pattern check rejects signs and extra dots before Decimal sees them.",
    "O(n)",
    "O(1)",
    """
def solve(raw):
    import re
    from decimal import Decimal, InvalidOperation
    if raw == "float":
        return "error"
    if not re.fullmatch(r"\\d+(\\.\\d{2})?", raw):
        return "error"
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return "error"
    return str(amount.quantize(Decimal("0.01")))
""",
    [
        {"raw": "10.50"},
        {"raw": "10"},
        {"raw": "float"},
        {"raw": "-1.00"},
    ],
)

add(
    "python-ex-parse-positive",
    "Parse Positive",
    "easy",
    ["python", "exceptions"],
    "Implement `solve(text)`. `text` should be a base-10 integer greater than 0. Return the integer when it is. Return the string `error` when the text is not an integer or the integer is less than 1. A boolean is not part of the input. Do not accept a trailing word.",
    ["1 is valid", "0 and negatives are error"],
    [
        "int(text) inside try, and catch ValueError.",
        "Reject values less than 1 after a successful parse.",
        "Do not use a bare except.",
    ],
    "int() raises ValueError on a bad string. Catching that one type, then checking the range, keeps a programming bug from disappearing into the same error string only if you do not catch Exception. The function still returns error for both the parse failure and the range failure because the caller asked for one result channel.",
    "O(n)",
    "O(1)",
    """
def solve(text):
    try:
        value = int(text)
    except ValueError:
        return "error"
    if value < 1:
        return "error"
    return value
""",
    [
        {"text": "3"},
        {"text": "0"},
        {"text": "nope"},
        {"text": "-2"},
    ],
)

add(
    "python-ex-first-present-dict",
    "First Present",
    "medium",
    ["python", "dicts"],
    "Implement `solve(payload, key)`. `payload` is a dict of strings. Return the value for `key` when the key is present, including when the value is an empty string. Return the string `missing` when the key is absent. Do not use a truthiness test that treats an empty string as absent.",
    ["An empty string is a present value", "A missing key is the string missing"],
    [
        "Use key in payload, not payload.get(key) or default, if the default could collide. Or get a unique sentinel.",
        "A present empty string is returned as empty.",
        "Only a missing key returns missing.",
    ],
    "dict.get returns the default for a missing key and also forces you to pick a default that is not a real value. The in test separates absence from a stored empty string. Truthiness collapses both, and also collapses a stored 0 if you ever store numbers. Here the values are strings, and empty is still real.",
    "O(1)",
    "O(1)",
    """
def solve(payload, key):
    if key in payload:
        return payload[key]
    return "missing"
""",
    [
        {"payload": {"name": ""}, "key": "name"},
        {"payload": {}, "key": "name"},
        {"payload": {"name": "ada"}, "key": "name"},
        {"payload": {"name": "ada"}, "key": "role"},
    ],
)

add(
    "python-ex-handler-order",
    "Handler Order",
    "medium",
    ["python", "exceptions"],
    "Implement `solve(raised, handlers)`. `handlers` is a list of exception names from the first except clause to the last. `raised` is the type that was raised. A handler matches when it equals `raised` or when it is a listed base of `raised`. The bases you must honor are: `FileNotFoundError` is a `OSError`, and `OSError` is an `Exception`. Return the first matching handler name. If none match, return `uncaught`.",
    ["First match wins", "Subclass before base is the useful order"],
    [
        "Walk handlers in order.",
        "A handler matches the raised type or one of its bases from the chain above.",
        "Return the first match. Do not prefer a more specific later handler.",
    ],
    "except clauses are tried in source order, and a base class earlier than a subclass makes the subclass clause dead. This function is that scan. The inheritance you need is only the small chain in the statement, not a full MRO of the interpreter.",
    "O(h)",
    "O(1)",
    """
def solve(raised, handlers):
    chain = {
        "FileNotFoundError": ["FileNotFoundError", "OSError", "Exception"],
        "OSError": ["OSError", "Exception"],
        "Exception": ["Exception"],
        "ValueError": ["ValueError", "Exception"],
    }
    lineage = chain.get(raised, [raised])
    for handler in handlers:
        if handler in lineage:
            return handler
    return "uncaught"
""",
    [
        {"raised": "FileNotFoundError", "handlers": ["OSError", "FileNotFoundError"]},
        {"raised": "FileNotFoundError", "handlers": ["FileNotFoundError", "OSError"]},
        {"raised": "ValueError", "handlers": ["OSError"]},
        {"raised": "OSError", "handlers": ["Exception"]},
    ],
)

add(
    "python-ex-chain-error",
    "Translate Error",
    "medium",
    ["python", "exceptions"],
    "Implement `solve(domain, cause)`. Return `{\"error\": domain, \"cause\": cause}`. Translating a low-level failure into a domain word must keep the original tag. Dropping `cause` is the bug this function refuses.",
    ["Both inputs are strings", "Both appear in the result"],
    [
        "Put the domain word under error.",
        "Put the original tag under cause.",
        "Do not return only the domain word.",
    ],
    "raise DomainError(...) from exc attaches the original exception as the cause. Logs and handlers can still see the OS error. A translation that returns only the domain word forces the next person to guess why it failed. The dict is that pair.",
    "O(1)",
    "O(1)",
    """
def solve(domain, cause):
    return {"error": domain, "cause": cause}
""",
    [
        {"domain": "BillingError", "cause": "timeout"},
        {"domain": "NotFound", "cause": "FileNotFoundError"},
        {"domain": "BillingError", "cause": "db"},
        {"domain": "ConfigError", "cause": "missing"},
    ],
)

add(
    "python-ex-safe-div",
    "Safe Div",
    "easy",
    ["python", "exceptions"],
    "Implement `solve(a, b)`. Return the integer `a // b` when `b` is not 0. When `b` is 0, return the string `error`. Do not return 0 or None for division by zero.",
    ["Use floor division", "Zero divisor is error"],
    [
        "Check b == 0 before dividing.",
        "Otherwise return a // b.",
        "The error result is the string error, which a caller cannot confuse with a quotient.",
    ],
    "Division by zero is a ValueError or ZeroDivisionError, not a missing result. Returning a sentinel number collides with a real quotient. The string error is the explicit failure. Floor division matches Python when the divisor is non-zero, including negatives.",
    "O(1)",
    "O(1)",
    """
def solve(a, b):
    if b == 0:
        return "error"
    return a // b
""",
    [
        {"a": 7, "b": 2},
        {"a": 7, "b": 0},
        {"a": -7, "b": 2},
        {"a": 0, "b": 5},
    ],
)

add(
    "python-ex-classify-status",
    "Classify Status",
    "medium",
    ["python", "exceptions"],
    "Implement `solve(status)`. Map an HTTP status integer to a billing failure class. 404 returns `not-found`. 408, 429, and any 500 through 599 return `transient`. Every other code returns `billing-failure`. This is the exception class you would raise, named as a string.",
    ["404 is not transient", "500 through 599 are transient"],
    [
        "Check 404 first.",
        "Then 408, 429, and the 5xx range.",
        "The default is billing-failure, including other 4xx codes such as 400.",
    ],
    "Not every failure should retry. 404 is a missing invoice, and retrying it will not create the row. 408, 429, and 5xx are the transient set in this contract. A generic 400 is the caller's bug and stays a billing failure rather than a retry.",
    "O(1)",
    "O(1)",
    """
def solve(status):
    if status == 404:
        return "not-found"
    if status in (408, 429) or 500 <= status <= 599:
        return "transient"
    return "billing-failure"
""",
    [
        {"status": 404},
        {"status": 503},
        {"status": 400},
        {"status": 429},
    ],
)

add(
    "python-ex-retry-policy",
    "Retry Policy",
    "medium",
    ["python", "exceptions"],
    "Implement `solve(kind, idempotent)`. `kind` is `timeout`, `value`, or `unavailable`. `idempotent` is 0 or 1. Return `retry` only for `timeout` or `unavailable` when `idempotent` is 1. Return `stop` for a `value` error always, and for a non-idempotent call even if the kind is transient.",
    ["value errors never retry", "A timeout on a non-idempotent call stops"],
    [
        "If kind is value, return stop.",
        "If idempotent is 0, return stop.",
        "Otherwise timeout and unavailable retry. Any other kind stops.",
    ],
    "Retrying a timeout can repeat a charge when the first request landed. The idempotent flag is the permission to try again. A value error is a bug in the request and will fail the same way. The policy is a conjunction, not a retry of every exception.",
    "O(1)",
    "O(1)",
    """
def solve(kind, idempotent):
    if kind == "value" or idempotent == 0:
        return "stop"
    if kind in ("timeout", "unavailable"):
        return "retry"
    return "stop"
""",
    [
        {"kind": "timeout", "idempotent": 1},
        {"kind": "timeout", "idempotent": 0},
        {"kind": "value", "idempotent": 1},
        {"kind": "unavailable", "idempotent": 1},
    ],
)

add(
    "python-ex-safe-message",
    "Safe Message",
    "easy",
    ["python", "exceptions"],
    "Implement `solve(invoice_id, secret)`. Return the string `invoice {id} failed` with the id interpolated. The `secret` argument must not appear in the result. Ignoring the secret on purpose is the behavior.",
    ["The id is included", "The secret is not"],
    [
        "Build the message from the id only.",
        "Do not concatenate secret.",
        "A test will pass a secret that must be absent. You can assert that by simply never reading it into the string.",
    ],
    "Exception messages end up in logs and in API bodies. An invoice id is useful. A card number or token that happened to be in scope is not. Leaving the secret out of the format string is the fix. The unused argument is the temptation.",
    "O(n)",
    "O(n)",
    """
def solve(invoice_id, secret):
    del secret
    return f"invoice {invoice_id} failed"
""",
    [
        {"invoice_id": "i1", "secret": "4242"},
        {"invoice_id": "i2", "secret": ""},
        {"invoice_id": "abc", "secret": "token"},
        {"invoice_id": "0", "secret": "0"},
    ],
)

add(
    "python-ex-cause-chain",
    "Cause Chain",
    "medium",
    ["python", "exceptions"],
    "Implement `solve(tags)`. `tags` is a list from the outermost translated error to the original cause, so the last item is the root. Return the list from the root up to the outer error, which is the order you walk `__cause__` links if each translation wrapped the previous one and you start at the outside... Return the tags reversed: root first.",
    ["The last input is the original cause", "Do not drop the outer tag"],
    [
        "Reverse the list.",
        "The first element of the result is the root cause.",
        "A single tag returns a one-element list.",
    ],
    "raise New from old sets __cause__. Walking the chain from the exception you caught reaches the original failure last if you start at the outside and follow cause. Reversing the outside-to-root list puts the root first, which is the order this report wants.",
    "O(n)",
    "O(n)",
    """
def solve(tags):
    return list(reversed(tags))
""",
    [
        {"tags": ["BillingError", "Timeout", "socket"]},
        {"tags": ["NotFound"]},
        {"tags": []},
        {"tags": ["Outer", "Inner"]},
    ],
)

add(
    "python-ex-redact",
    "Redact",
    "easy",
    ["python", "logging"],
    "Implement `solve(fields)`. `fields` is a dict. Drop the keys `password`, `token`, and `secret` if present. Return the remaining dict. Do not modify values of other keys.",
    ["Those three names are the secret keys", "Other keys stay, including authorization if it is not in the list"],
    [
        "Copy the dict.",
        "Delete the three names when they exist.",
        "Return the copy.",
    ],
    "A log line of the request body will include a password if you log the dict you were given. Deleting the known secret keys before formatting is the minimum redact. It is not a full DLP pass. The copy protects the caller's mapping.",
    "O(n)",
    "O(n)",
    """
def solve(fields):
    hidden = {"password", "token", "secret"}
    return {key: value for key, value in fields.items() if key not in hidden}
""",
    [
        {"fields": {"user": "ada", "password": "x"}},
        {"fields": {"token": "t", "secret": "s"}},
        {"fields": {}},
        {"fields": {"note": "hi"}},
    ],
)

add(
    "python-ex-log-level",
    "Level Choice",
    "medium",
    ["python", "logging"],
    "Implement `solve(outcome)`. Map `debug` to `DEBUG`, `started` to `INFO`, `retry` to `WARNING`, `handled` to `ERROR`, and `bug` to `ERROR`. Any other word returns `INFO`. These are level names, not numbers.",
    ["retry is a warning, not an error, until the retries are exhausted", "Unknown outcomes are INFO"],
    [
        "Use a dict for the known words.",
        "Default to INFO.",
        "Return the level name exactly.",
    ],
    "A retry that may still succeed is a warning. A handled failure the user sees is an error. A bug you did not expect is also an error, and the traceback belongs there. Logging every expected branch at ERROR trains people to ignore the channel. The default INFO keeps an unknown business event visible without paging anyone.",
    "O(1)",
    "O(1)",
    """
def solve(outcome):
    return {
        "debug": "DEBUG",
        "started": "INFO",
        "retry": "WARNING",
        "handled": "ERROR",
        "bug": "ERROR",
    }.get(outcome, "INFO")
""",
    [
        {"outcome": "retry"},
        {"outcome": "handled"},
        {"outcome": "started"},
        {"outcome": "other"},
    ],
)

add(
    "python-ex-lazy-log",
    "Format Lazy",
    "easy",
    ["python", "logging"],
    "Implement `solve(enabled, message)`. `enabled` is 1 when DEBUG is on and 0 otherwise. Return the message only when enabled is 1. Return an empty string when debugging is off. Building the message is the caller's cost. Your job is to drop it when the level is disabled.",
    ["enabled is 0 or 1", "A disabled logger returns an empty string"],
    [
        "If enabled is 0, return an empty string without inventing a substitute.",
        "If enabled is 1, return message.",
        "Do not return the message in both cases.",
    ],
    "Logging debug with an f-string builds the string even when the logger will throw it away. The guard is to ask the level first, or to pass a format and arguments the logger interpolates only if the record is emitted. This function is that guard: disabled means no message.",
    "O(1)",
    "O(1)",
    """
def solve(enabled, message):
    if enabled:
        return message
    return ""
""",
    [
        {"enabled": 0, "message": "huge"},
        {"enabled": 1, "message": "huge"},
        {"enabled": 0, "message": ""},
        {"enabled": 1, "message": ""},
    ],
)

add(
    "python-ex-retry-lines",
    "Retry Lines",
    "medium",
    ["python", "logging"],
    "Implement `solve(results)`. `results` is a list of `fail` or `ok`, the attempts in order. Return a list of level names of the same length. A `fail` that is not the last item is `WARNING`. A final `fail` is `ERROR`. An `ok` is `INFO`, and it should be the last attempt when the caller stopped, but if an `ok` appears earlier the later items are still leveled the same way: a non-final fail is WARNING, a final fail is ERROR, and ok is INFO.",
    ["The last index is special only for fail", "ok is always INFO"],
    [
        "enumerate so you know the last index.",
        "ok maps to INFO.",
        "fail maps to ERROR only on the last position, otherwise WARNING.",
    ],
    "The attempt log should not shout ERROR for a failure you are about to retry. WARNING is the intermediate. The final failure is the ERROR, because nothing will follow it. Success is INFO. The index is what distinguishes the two failure levels.",
    "O(n)",
    "O(n)",
    """
def solve(results):
    last = len(results) - 1
    out = []
    for index, result in enumerate(results):
        if result == "ok":
            out.append("INFO")
        elif index == last:
            out.append("ERROR")
        else:
            out.append("WARNING")
    return out
""",
    [
        {"results": ["fail", "fail", "ok"]},
        {"results": ["fail", "fail"]},
        {"results": ["ok"]},
        {"results": []},
    ],
)
