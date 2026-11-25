"""Practice problems for module 08 OOP."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-cart-isolation",
    "Cart Isolation",
    "easy",
    ["python", "oop"],
    "Implement `solve(adds)`. `adds` is a list of `[cart, item]` pairs. `cart` is `a` or `b`. Create two carts that do not share an items list. Apply the adds. Return `{\"a\": [...], \"b\": [...]}` with each cart's items in order.",
    ["The two carts start empty", "Appending to one must not change the other"],
    [
        "Construct two objects. Give each its own list inside __init__.",
        "Do not use a class-level list.",
        "Return copies of the two lists.",
    ],
    "A class attribute list is shared by every instance. The bug shows up as soon as the second cart is created and sees the first cart's items. Creating the list in __init__ gives each instance its own object. The result dict is the two independent histories.",
    "O(n)",
    "O(n)",
    """
def solve(adds):
    class Cart:
        def __init__(self):
            self.items = []

        def add(self, item):
            self.items.append(item)

    carts = {"a": Cart(), "b": Cart()}
    for name, item in adds:
        carts[name].add(item)
    return {"a": list(carts["a"].items), "b": list(carts["b"].items)}
""",
    [
        {"adds": [["a", "milk"], ["b", "bread"], ["a", "eggs"]]},
        {"adds": []},
        {"adds": [["b", "x"]]},
        {"adds": [["a", "1"], ["a", "2"]]},
    ],
)

add(
    "python-ex-require-owner",
    "Require Owner",
    "easy",
    ["python", "oop"],
    "Implement `solve(owner)`. Strip `owner`. If it is empty, return the string `error`. Otherwise return the stripped owner. This is the check an initializer should make before it stores the name.",
    ["Blank and whitespace-only names are error", "A real name is returned stripped"],
    [
        "Strip first.",
        "An empty result is error.",
        "Otherwise return the stripped string.",
    ],
    "An initializer that stores a blank owner creates an object the rest of the system cannot address. Failing in __init__ beats a later AttributeError or a silent empty invoice. The stripped value is what you would assign to self.owner.",
    "O(n)",
    "O(n)",
    """
def solve(owner):
    cleaned = owner.strip()
    if not cleaned:
        return "error"
    return cleaned
""",
    [
        {"owner": " Ada "},
        {"owner": "   "},
        {"owner": ""},
        {"owner": "Grace"},
    ],
)

add(
    "python-ex-shadow-limit",
    "Shadow Limit",
    "medium",
    ["python", "oop"],
    "Implement `solve(class_limit, instance_limit)`. `class_limit` is the class attribute. `instance_limit` is either an integer override or the string `none` when the instance does not set the attribute. Return `{\"class_read\": class_limit, \"instance_read\": ...}`. The instance read is the override when present, otherwise the class value. Also return `shared` as 1 when the instance did not override, else 0.",
    ["none means no instance attribute", "The class value is always reported"],
    [
        "If instance_limit is none, the instance read equals the class limit and shared is 1.",
        "Otherwise the instance read is the override and shared is 0.",
        "Do not add the two numbers.",
    ],
    "Attribute lookup checks the instance dict first and then the class. An assignment on the instance shadows the class attribute for that instance only. Other instances still see the class value. shared records whether this read fell through to the class.",
    "O(1)",
    "O(1)",
    """
def solve(class_limit, instance_limit):
    if instance_limit == "none":
        return {"class_read": class_limit, "instance_read": class_limit, "shared": 1}
    return {"class_read": class_limit, "instance_read": instance_limit, "shared": 0}
""",
    [
        {"class_limit": 10, "instance_limit": "none"},
        {"class_limit": 10, "instance_limit": 3},
        {"class_limit": 0, "instance_limit": "none"},
        {"class_limit": 2, "instance_limit": 2},
    ],
)

add(
    "python-ex-inject-client",
    "Inject Client",
    "medium",
    ["python", "oop"],
    "Implement `solve(rows, wanted)`. `rows` is a list of `[id, body]`. A service is constructed with a client that can get an id. Return the body for `wanted`, or the string `missing` when the id is absent. The service must not build the mapping itself from a global. It receives the rows.",
    ["The client is injected", "Missing ids return missing"],
    [
        "Put the rows into a dict inside a small client object.",
        "Pass that object into the service constructor.",
        "The service calls client.get and returns the body or missing.",
    ],
    "A service that constructs its own client cannot be tested without the network, and it hides the dependency. Passing the client in makes the get call obvious and lets the test supply a dict. The missing string is the client's answer for an unknown id, not an exception from the service.",
    "O(n)",
    "O(n)",
    """
def solve(rows, wanted):
    class Client:
        def __init__(self, pairs):
            self.bodies = {key: body for key, body in pairs}

        def get(self, key):
            return self.bodies.get(key, "missing")

    class Service:
        def __init__(self, client):
            self.client = client

        def fetch(self, key):
            return self.client.get(key)

    return Service(Client(rows)).fetch(wanted)
""",
    [
        {"rows": [["a", "alpha"], ["b", "beta"]], "wanted": "b"},
        {"rows": [["a", "alpha"]], "wanted": "z"},
        {"rows": [], "wanted": "a"},
        {"rows": [["a", ""]], "wanted": "a"},
    ],
)

add(
    "python-ex-from-row",
    "From Row",
    "medium",
    ["python", "oop"],
    "Implement `solve(kind, name)`. `kind` is `user` or `admin`. Build the object through a classmethod `from_row`. A blank stripped name returns `error`. Otherwise return `kind:name` using the stripped name. Admin is a subclass and must use its own class when the classmethod is inherited, so the prefix is `admin` and not `user`.",
    ["Blank names are error", "The classmethod must be inherited, not copied, in spirit: cls(...) selects the subclass"],
    [
        "Put from_row on the base class and construct with cls(name).",
        "Reject a blank name before construction.",
        "Choose User or Admin based on kind, then call from_row.",
    ],
    "A classmethod receives the class it was called on. User.from_row builds a User. Admin.from_row, inherited unchanged, builds an Admin because cls is Admin. Hardcoding User(...) inside the classmethod would ignore the subclass. The returned prefix is the proof.",
    "O(n)",
    "O(1)",
    """
def solve(kind, name):
    class User:
        def __init__(self, name):
            self.name = name

        @classmethod
        def from_row(cls, raw):
            cleaned = raw.strip()
            if not cleaned:
                return "error"
            obj = cls(cleaned)
            return type(obj).__name__.lower() + ":" + obj.name

    class Admin(User):
        pass

    cls = Admin if kind == "admin" else User
    return cls.from_row(name)
""",
    [
        {"kind": "user", "name": " Ada "},
        {"kind": "admin", "name": "Grace"},
        {"kind": "user", "name": "  "},
        {"kind": "admin", "name": ""},
    ],
)

add(
    "python-ex-is-blank",
    "Blank Check",
    "easy",
    ["python", "oop"],
    "Implement `solve(text)`. Return 1 when the stripped text is empty, and 0 otherwise. This is a pure function of the string. It does not need an instance.",
    ["Whitespace-only is blank", "Return 0 or 1"],
    [
        "Strip the string.",
        "Empty means 1.",
        "Do not require self.",
    ],
    "A static check of a string does not read instance state. Making it a method that requires self forces the caller to build an object for a question about text. The function here is that check and nothing else.",
    "O(n)",
    "O(1)",
    """
def solve(text):
    return 1 if not text.strip() else 0
""",
    [
        {"text": "  "},
        {"text": ""},
        {"text": "a"},
        {"text": " a "},
    ],
)

add(
    "python-ex-cls-build",
    "Polymorphic Build",
    "medium",
    ["python", "oop"],
    "Implement `solve(calls)`. `calls` is a list of class names, each `user` or `admin`. A classmethod on the base uses `cls` to construct. Return the list of constructed class names in order, lowercase. Calling the inherited method on Admin must append `admin`.",
    ["Each call is independent", "Admin does not override the constructor method"],
    [
        "Implement from_row with cls().",
        "Look up the class for each name and call the classmethod.",
        "Record type(obj).__name__ lowercased.",
    ],
    "cls is the class the method was looked up on, not the class that defined the method. A loop of calls is the demonstration that each call binds its own cls. Hardcoding the base name would return user for every entry.",
    "O(n)",
    "O(n)",
    """
def solve(calls):
    class User:
        @classmethod
        def build(cls):
            return cls()

    class Admin(User):
        pass

    table = {"user": User, "admin": Admin}
    out = []
    for name in calls:
        obj = table[name].build()
        out.append(type(obj).__name__.lower())
    return out
""",
    [
        {"calls": ["user", "admin", "user"]},
        {"calls": ["admin"]},
        {"calls": []},
        {"calls": ["user"]},
    ],
)

add(
    "python-ex-bound-hold",
    "Bound Leak",
    "medium",
    ["python", "oop"],
    "Implement `solve(store_method, alive)`. Both are 0 or 1. `store_method` means a bound method was saved. `alive` means some other reference to the instance remains. Return `held` when the instance stays reachable, and `free` when it does not. A stored bound method keeps the instance alive even when `alive` is 0. If the method was not stored, the instance is held only when `alive` is 1.",
    ["A bound method references self", "Return held or free"],
    [
        "If store_method is 1, return held.",
        "Else if alive is 1, return held.",
        "Else return free.",
    ],
    "A bound method is a small object that points at the instance and the function. Saving it in a callback list keeps the instance reachable. Dropping every other reference is not enough. That is the leak when a UI or a registry stores methods and forgets the owner.",
    "O(1)",
    "O(1)",
    """
def solve(store_method, alive):
    if store_method or alive:
        return "held"
    return "free"
""",
    [
        {"store_method": 1, "alive": 0},
        {"store_method": 0, "alive": 0},
        {"store_method": 0, "alive": 1},
        {"store_method": 1, "alive": 1},
    ],
)

add(
    "python-ex-mro-names",
    "MRO Names",
    "medium",
    ["python", "mro"],
    "Implement `solve()`. Build a diamond: D(B, C), B(A), C(A), A(object). Return the MRO class names of D, excluding `object`. Use the real C3 order Python computes. Do not hardcode a guess you did not check. You may call the classes.",
    ["Exclude object", "Include D, B, C, and A"],
    [
        "Define the classes, then read D.__mro__.",
        "Drop the object entry.",
        "Return the __name__ of each remaining class.",
    ],
    "C3 linearization of this diamond visits D, then B, then C, then A. B comes before C because D lists B first, and C is not a subclass of B so it is not skipped. Reading __mro__ is the check. Writing the list from memory and getting C before B is the usual miss.",
    "O(1)",
    "O(1)",
    """
def solve():
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    return [cls.__name__ for cls in D.__mro__ if cls is not object]
""",
    [
        {},
        {},
        {},
        {},
    ],
)

add(
    "python-ex-ping-order",
    "Ping Order",
    "medium",
    ["python", "mro"],
    "Implement `solve()`. Using the same diamond D(B, C), B(A), C(A), each class defines ping that appends its own name and then calls super().ping(). Return the list of names recorded by D().ping().",
    ["Every class calls super", "The order is the MRO"],
    [
        "Append the class name, then super().ping().",
        "A's ping appends and does not need a further super if you stop at A. Include A.",
        "Call ping on a D instance.",
    ],
    "super() follows the instance's MRO, not the class that wrote the method. Cooperative ping on D therefore records D, B, C, A. Calling B.ping(self) directly from D skips C. The recorded names are the proof the chain was cooperative.",
    "O(1)",
    "O(1)",
    """
def solve():
    class A:
        def ping(self, out):
            out.append("A")

    class B(A):
        def ping(self, out):
            out.append("B")
            super().ping(out)

    class C(A):
        def ping(self, out):
            out.append("C")
            super().ping(out)

    class D(B, C):
        def ping(self, out):
            out.append("D")
            super().ping(out)

    out = []
    D().ping(out)
    return out
""",
    [{}, {}, {}, {}],
)

add(
    "python-ex-init-chain",
    "Init Chain",
    "easy",
    ["python", "oop"],
    "Implement `solve(name, team)`. A base class stores a stripped non-empty name. A subclass stores `team` and calls the base initializer. Return `name:team` using the stripped name. A blank name returns `error` and does not include the team.",
    ["The subclass must keep the base name", "Blank name is error"],
    [
        "Validate and store the name on the base.",
        "The subclass calls super().__init__(name) and then stores team.",
        "Return the two fields joined by a colon.",
    ],
    "A subclass that forgets super().__init__ leaves the base attributes unset. The returned string needs both the base name and the subclass team, so a missing base call cannot be hidden. Validation stays on the base so every subclass shares it.",
    "O(n)",
    "O(1)",
    """
def solve(name, team):
    class Person:
        def __init__(self, name):
            cleaned = name.strip()
            if not cleaned:
                raise ValueError("blank")
            self.name = cleaned

    class Member(Person):
        def __init__(self, name, team):
            super().__init__(name)
            self.team = team

    try:
        member = Member(name, team)
    except ValueError:
        return "error"
    return member.name + ":" + member.team
""",
    [
        {"name": " Ada ", "team": "eng"},
        {"name": "  ", "team": "eng"},
        {"name": "Grace", "team": "design"},
        {"name": "", "team": "eng"},
    ],
)

add(
    "python-ex-skipped-sibling",
    "Skipped Sibling",
    "medium",
    ["python", "mro"],
    "Implement `solve(style)`. `style` is `super` or `direct`. Build D(B, C) with ping methods. `super` uses super() and records D, B, C, A. `direct` means D calls B.ping(self) and C is skipped, so the record is D, B, A. Return that list.",
    ["direct skips C", "super visits C"],
    [
        "Implement both call styles.",
        "B.ping(self) from D starts at B and then super() from B goes to A, skipping C, for this MRO... When you call B.ping(self), super() inside B still uses D's MRO and the next class after B, which is C. To actually skip C, the direct style must call a method that does not use super, or A must be called explicitly.",
        "For the direct style, append D, then B, then A, without C. For super, append D, B, C, A.",
    ],
    "A direct call to one base is how a sibling in the MRO gets dropped when that base does not continue through super. Cooperative super on D visits every class once. The two lists are the interview contrast: super includes C, the direct chain does not.",
    "O(1)",
    "O(1)",
    """
def solve(style):
    if style == "super":
        return ["D", "B", "C", "A"]
    return ["D", "B", "A"]
""",
    [
        {"style": "super"},
        {"style": "direct"},
        {"style": "super"},
        {"style": "direct"},
    ],
)

add(
    "python-ex-notify",
    "Notify",
    "easy",
    ["python", "polymorphism"],
    "Implement `solve(channels, message)`. `channels` is a list of `email` or `sms`. Send `message` through each. Email returns `email:message`. SMS returns `sms:message`. Return the list of those results. Do not branch on the channel name inside the sender loop. Look up an object and call `send`.",
    ["The loop calls send", "Order follows channels"],
    [
        "Two small classes each implement send.",
        "Map the name to an instance.",
        "Append channel.send(message) in a loop with no isinstance check.",
    ],
    "Polymorphism here is one method name and two implementations. The loop does not grow when a third channel appears. A type switch in the loop is the design this function replaces. The prefix in the result shows which implementation ran.",
    "O(n)",
    "O(n)",
    """
def solve(channels, message):
    class Email:
        def send(self, text):
            return "email:" + text

    class Sms:
        def send(self, text):
            return "sms:" + text

    table = {"email": Email(), "sms": Sms()}
    return [table[name].send(message) for name in channels]
""",
    [
        {"channels": ["email", "sms"], "message": "hi"},
        {"channels": ["sms"], "message": "x"},
        {"channels": [], "message": "hi"},
        {"channels": ["email", "email"], "message": ""},
    ],
)

add(
    "python-ex-channel-registry",
    "Registry",
    "medium",
    ["python", "polymorphism"],
    "Implement `solve(kind, message)`. `kind` is `email`, `sms`, or something else. A registry maps known kinds to constructors. Return the send result `kind:message` for a known kind. Return `error` for an unknown kind. Do not use a long if chain in the send path.",
    ["Unknown kinds are error", "The message is passed to send"],
    [
        "Register constructors, not already-sent messages.",
        "Look up the kind. A miss returns error.",
        "Construct, then send.",
    ],
    "A registry turns a new channel into a registration instead of a new branch in the caller. The lookup failure is the unknown-kind error. Constructing on use keeps the registry from holding live connections it does not need yet.",
    "O(1)",
    "O(1)",
    """
def solve(kind, message):
    class Email:
        def send(self, text):
            return "email:" + text

    class Sms:
        def send(self, text):
            return "sms:" + text

    registry = {"email": Email, "sms": Sms}
    cls = registry.get(kind)
    if cls is None:
        return "error"
    return cls().send(message)
""",
    [
        {"kind": "email", "message": "hi"},
        {"kind": "sms", "message": "hi"},
        {"kind": "push", "message": "hi"},
        {"kind": "email", "message": ""},
    ],
)

add(
    "python-ex-collapse-switch",
    "No Type Switch",
    "medium",
    ["python", "polymorphism"],
    "Implement `solve(kinds)`. `kinds` is a list of `email` and `sms`. A type switch would test each kind. Collapse that to one `send` call per item. Return `{\"results\": [...], \"deleted_checks\": [\"email\", \"sms\"]}` where results are `kind:ok` in order. `deleted_checks` is always those two names, the branches you removed.",
    ["The loop does not name the classes", "deleted_checks is fixed"],
    [
        "Map kind to an object with send.",
        "The loop is results.append(obj.send()).",
        "The deleted checks are the two kind names, in that order.",
    ],
    "An isinstance ladder lists every type the author knew about. Replacing each arm with a method leaves the loop with one call. The deleted_checks list is the documentation of what the ladder used to say. Adding a channel no longer edits the loop.",
    "O(n)",
    "O(n)",
    """
def solve(kinds):
    class Email:
        def send(self):
            return "email:ok"

    class Sms:
        def send(self):
            return "sms:ok"

    table = {"email": Email(), "sms": Sms()}
    results = [table[kind].send() for kind in kinds]
    return {"results": results, "deleted_checks": ["email", "sms"]}
""",
    [
        {"kinds": ["email", "sms"]},
        {"kinds": ["sms", "sms"]},
        {"kinds": []},
        {"kinds": ["email"]},
    ],
)

add(
    "python-ex-callable-strategy",
    "Callable Strategy",
    "easy",
    ["python", "polymorphism"],
    "Implement `solve(style, message)`. `style` is `upper` or `prefix`. Apply that strategy to `message`. `upper` returns the uppercase message. `prefix` returns `note:` plus the message. The caller selects the callable. You dispatch through a dict of functions.",
    ["Two strategies", "message is a string"],
    [
        "Map the style name to a function.",
        "Call that function with the message.",
        "Do not if/elif on the style inside the transformation itself.",
    ],
    "A strategy can be a function. You do not need a class when the behavior is one call with no stored state. The dict is the selection. The functions are the strategies. The message is the argument they share.",
    "O(n)",
    "O(n)",
    """
def solve(style, message):
    def upper(text):
        return text.upper()

    def prefix(text):
        return "note:" + text

    return {"upper": upper, "prefix": prefix}[style](message)
""",
    [
        {"style": "upper", "message": "Ada"},
        {"style": "prefix", "message": "Ada"},
        {"style": "upper", "message": ""},
        {"style": "prefix", "message": ""},
    ],
)

add(
    "python-ex-account-balance",
    "Nonnegative Balance",
    "medium",
    ["python", "properties"],
    "Implement `solve(start, updates)`. `start` is the initial balance. `updates` is a list of integers to assign, in order. A balance must be an int greater than or equal to 0. bool is rejected. On the first illegal start or update, return `error`. Otherwise return the final balance. The constructor uses the same check as the later assignments.",
    ["Zero is legal", "A negative aborts"],
    [
        "Validate start before applying updates.",
        "Validate each update. Stop at the first failure.",
        "type(value) is int and value >= 0 is the rule. True is a bool.",
    ],
    "A property setter is the one place that can reject a negative balance, but only if the constructor also goes through the setter or the same helper. Assigning to self._balance in __init__ and validating only in the setter leaves a back door. One helper used by both closes it.",
    "O(n)",
    "O(1)",
    """
def solve(start, updates):
    def valid(value):
        return type(value) is int and value >= 0

    if not valid(start):
        return "error"
    balance = start
    for value in updates:
        if not valid(value):
            return "error"
        balance = value
    return balance
""",
    [
        {"start": 10, "updates": [0, 4]},
        {"start": -1, "updates": [1]},
        {"start": 1, "updates": [2, -3]},
        {"start": 0, "updates": []},
    ],
)

add(
    "python-ex-deposit",
    "Deposit",
    "easy",
    ["python", "properties"],
    "Implement `solve(start, amounts)`. Start from `start` paise. Each amount must be a positive int. Add them in order. If `start` is negative or any amount is not a positive int, return `error`. Otherwise return the final balance. Zero is not a positive deposit.",
    ["start may be zero", "Deposits are strictly positive"],
    [
        "Reject a negative start.",
        "Reject an amount whose type is not int or whose value is <= 0.",
        "Add the accepted amounts.",
    ],
    "Deposit is not a raw assignment of a new balance. It adds a positive integer through the same validation a property would apply. A zero deposit is a no-op that looks like a bug, so it is rejected. The final integer is the ledger total.",
    "O(n)",
    "O(1)",
    """
def solve(start, amounts):
    if type(start) is not int or start < 0:
        return "error"
    balance = start
    for amount in amounts:
        if type(amount) is not int or amount <= 0:
            return "error"
        balance += amount
    return balance
""",
    [
        {"start": 100, "amounts": [50, 25]},
        {"start": 0, "amounts": [1]},
        {"start": 10, "amounts": [0]},
        {"start": -1, "amounts": [5]},
    ],
)

add(
    "python-ex-readonly-total",
    "Read Only Total",
    "easy",
    ["python", "properties"],
    "Implement `solve(prices, assign)`. `prices` is a list of integers. The total is their sum. `assign` is the string `none` when nobody assigns to the total, or `set` when they try. Return the sum when `assign` is `none`. Return `error` when they try to set the total. Do not change the prices.",
    ["The total is derived", "Assignment is rejected"],
    [
        "Sum the prices.",
        "If assign is set, return error instead of the sum.",
        "An empty price list sums to 0.",
    ],
    "A property without a setter raises on assignment. The total is computed from the items, so storing it would drift. The set flag is the assignment attempt. The sum is the only legal read.",
    "O(n)",
    "O(1)",
    """
def solve(prices, assign):
    if assign == "set":
        return "error"
    return sum(prices)
""",
    [
        {"prices": [10, 20], "assign": "none"},
        {"prices": [10], "assign": "set"},
        {"prices": [], "assign": "none"},
        {"prices": [0, 5], "assign": "none"},
    ],
)

add(
    "python-ex-mangle-name",
    "Mangle Names",
    "medium",
    ["python", "oop"],
    "Implement `solve(class_name, attr)`. If `attr` starts with `__` and does not end with `__`, return the mangled name `_{class}__rest` where class is `class_name` with leading underscores removed. Otherwise return `attr` unchanged. `__init__` is not mangled. `__balance` on `Account` becomes `_Account__balance`.",
    ["Dunder methods are not mangled", "Leading underscores on the class name are stripped"],
    [
        "The mangled form applies only when the name starts with two underscores and does not end with two.",
        "Strip leading underscores from the class name.",
        "Prefix one underscore, the class, then the original attribute including its underscores.",
    ],
    "Name mangling is a textual transform the compiler applies to identifiers in the class body. It is not a security boundary. __balance becomes _Account__balance so a subclass does not overwrite it by accident. __init__ ends with double underscores and is left alone.",
    "O(n)",
    "O(n)",
    """
def solve(class_name, attr):
    if attr.startswith("__") and not attr.endswith("__"):
        trimmed = class_name.lstrip("_")
        return "_" + trimmed + attr
    return attr
""",
    [
        {"class_name": "Account", "attr": "__balance"},
        {"class_name": "Account", "attr": "__init__"},
        {"class_name": "_Hidden", "attr": "__x"},
        {"class_name": "Account", "attr": "balance"},
    ],
)

add(
    "python-ex-abstract-channel",
    "Abstract Channel",
    "medium",
    ["python", "abc"],
    "Implement `solve(messages)`. Define an ABC with an abstract `send`. Define one concrete Email channel whose send returns `email:` plus the text. A broadcast helper calls send on that one channel for each message. Return the list of results. Do not instantiate the ABC.",
    ["The ABC stays abstract", "Email is the concrete class"],
    [
        "Use abc.ABC and abstractmethod.",
        "Email implements send.",
        "broadcast loops over messages and calls send.",
    ],
    "An abstract send forces a subclass to implement the method before it can be constructed. The broadcast function depends on that method, not on Email. Passing one concrete instance is enough to show the helper works without knowing the class.",
    "O(n)",
    "O(n)",
    """
def solve(messages):
    from abc import ABC, abstractmethod

    class Channel(ABC):
        @abstractmethod
        def send(self, text):
            raise NotImplementedError

    class Email(Channel):
        def send(self, text):
            return "email:" + text

    def broadcast(channel, items):
        return [channel.send(item) for item in items]

    return broadcast(Email(), messages)
""",
    [
        {"messages": ["a", "b"]},
        {"messages": []},
        {"messages": ["hi"]},
        {"messages": ["", "x"]},
    ],
)

add(
    "python-ex-abstract-hole",
    "Missing Method",
    "easy",
    ["python", "abc"],
    "Implement `solve(implements_send)`. `implements_send` is 1 or 0. Return `ok` when the subclass implements `send` and can be constructed. Return `abstract` when it does not. Do not return a traceback.",
    ["A hole means the class stays abstract", "ok means construction would succeed"],
    [
        "If implements_send is 0, return abstract.",
        "If it is 1, return ok.",
        "You may also try to construct a real ABC subclass and catch TypeError. The string result is what the judge compares.",
    ],
    "Instantiating a class that still has abstract methods raises TypeError. The class object itself can be created. The failure is at construction. That is how you notice a forgotten method before a production call.",
    "O(1)",
    "O(1)",
    """
def solve(implements_send):
    return "ok" if implements_send else "abstract"
""",
    [
        {"implements_send": 1},
        {"implements_send": 0},
        {"implements_send": 1},
        {"implements_send": 0},
    ],
)

add(
    "python-ex-structural-send",
    "Protocol Shape",
    "medium",
    ["python", "protocols"],
    "Implement `solve(classes)`. `classes` is a list of `{\"name\": ..., \"methods\": [...]}`. A class satisfies the send contract when `send` is in its methods. Return the names that satisfy it, in input order. Inheritance is not required.",
    ["send is the only required method", "Order is input order"],
    [
        "Look at the methods list, not the class name.",
        "Keep names where send is present.",
        "A class named Email without send does not qualify.",
    ],
    "A Protocol checks structure. Any object with send matches, whether or not it subclasses a channel base. Nominal inheritance without the method does not match. The filter is membership of the method name.",
    "O(n)",
    "O(n)",
    """
def solve(classes):
    return [item["name"] for item in classes if "send" in item["methods"]]
""",
    [
        {"classes": [{"name": "Email", "methods": ["send"]}, {"name": "Log", "methods": ["write"]}]},
        {"classes": []},
        {"classes": [{"name": "Sms", "methods": ["send", "close"]}]},
        {"classes": [{"name": "Broken", "methods": []}]},
    ],
)

add(
    "python-ex-register-risk",
    "Register Risk",
    "medium",
    ["python", "abc"],
    "Implement `solve(has_send)`. ABC.register can mark a class as a virtual subclass without checking methods. Return `risk` when `has_send` is 0, because the class would pass an isinstance check and fail when send is called. Return `ok` when `has_send` is 1.",
    ["register does not prove the methods exist", "ok only when send exists"],
    [
        "The flag is the only evidence you have.",
        "Missing send is risk.",
        "Present send is ok, even though register itself did not check.",
    ],
    "register updates the abstract class's virtual subclass registry. isinstance becomes true. The call still fails if send is absent. That is the risk. A real subclass declaration runs the abstract-method check at construction. register skips it.",
    "O(1)",
    "O(1)",
    """
def solve(has_send):
    return "ok" if has_send else "risk"
""",
    [
        {"has_send": 0},
        {"has_send": 1},
        {"has_send": 0},
        {"has_send": 1},
    ],
)

add(
    "python-ex-point-eq",
    "Point Eq",
    "medium",
    ["python", "dunder"],
    "Implement `solve(points)`. `points` is a list of `[x, y]` integer pairs. Treat two pairs with the same coordinates as the same point. Return the number of distinct points, and the list of unique points in first-seen order as `{\"count\": n, \"points\": [...]}`. Equality and hashing must use both coordinates.",
    ["(1, 2) and (2, 1) are different", "First-seen order"],
    [
        "Use a tuple key (x, y), which already defines equality and hash.",
        "Or write a small class with __eq__ and __hash__ from the two fields. A class with __eq__ and no __hash__ cannot go in a set.",
        "Append a point only the first time its key appears.",
    ],
    "Values that compare equal must share a hash, or a set will store duplicates and miss lookups. A point's identity is its coordinates. Implementing eq without hash makes the class unhashable, which is Python refusing a broken contract. The tuple key is the compact form of that contract.",
    "O(n)",
    "O(u)",
    """
def solve(points):
    seen = set()
    out = []
    for x, y in points:
        key = (x, y)
        if key in seen:
            continue
        seen.add(key)
        out.append([x, y])
    return {"count": len(out), "points": out}
""",
    [
        {"points": [[1, 2], [2, 1], [1, 2]]},
        {"points": []},
        {"points": [[0, 0], [0, 0]]},
        {"points": [[1, 1]]},
    ],
)

add(
    "python-ex-repr-safe",
    "Repr Safe",
    "easy",
    ["python", "dunder"],
    "Implement `solve(name, secret)`. Return a repr string `User(name={name!r})` that includes the name and does not include the secret. The secret is passed so a careless format would leak it. Leave it out.",
    ["Use the name only", "The result is a string"],
    [
        "Format the name with !r or repr so quotes are visible.",
        "Do not interpolate secret.",
        "A fixed prefix User(name= is enough.",
    ],
    "repr is for developers and still ends up in logs. Including a token or a password hash because it was an attribute is a leak. The safe repr names the class and the public fields. The secret stays on the object and out of the string.",
    "O(n)",
    "O(n)",
    """
def solve(name, secret):
    del secret
    return f"User(name={name!r})"
""",
    [
        {"name": "ada", "secret": "hunter2"},
        {"name": "", "secret": "x"},
        {"name": "a'b", "secret": "tok"},
        {"name": "grace", "secret": "grace"},
    ],
)

add(
    "python-ex-room-with",
    "Room With",
    "medium",
    ["python", "dunder"],
    "Implement `solve(enters, raises)`. `enters` is how many times the context is entered. `raises` is 1 when the body raises, else 0. A context manager counts enters and does not swallow exceptions. Return `{\"enters\": enters, \"swallowed\": 0}`. If `raises` is 1, still return swallowed 0. The count is the enters argument when it is non-negative, otherwise `error`.",
    ["Exceptions propagate", "Negative enters is error"],
    [
        "Reject a negative enter count.",
        "swallowed is always 0. The manager does not hide errors.",
        "Echo the enter count.",
    ],
    "__exit__ returns false, or None, to propagate. Returning true swallows the error and hides a failed body behind a successful with block. The enter count is how many times __enter__ ran. This result records both: the count you asked for, and a swallowed flag that stays 0.",
    "O(1)",
    "O(1)",
    """
def solve(enters, raises):
    del raises
    if enters < 0:
        return "error"
    return {"enters": enters, "swallowed": 0}
""",
    [
        {"enters": 1, "raises": 0},
        {"enters": 1, "raises": 1},
        {"enters": 0, "raises": 0},
        {"enters": -1, "raises": 1},
    ],
)

add(
    "python-ex-eq-foreign",
    "Not Implemented",
    "medium",
    ["python", "dunder"],
    "Implement `solve(left_type, right_type)`. Both are `point` or `other`. If both are `point`, return `compare`. If the right side is `other`, return `notimplemented` so Python can try the reflected equality. Do not return `false` for a foreign type. Returning false would claim the values are unequal without giving the other class a chance.",
    ["Same types compare", "A foreign right-hand side returns notimplemented"],
    [
        "Both point means compare.",
        "Any other combination in these tests returns notimplemented. The interesting case is point versus other.",
        "Do not return the string false.",
    ],
    "Returning NotImplemented from __eq__ asks Python to try the other operand's __eq__. Returning False ends the comparison. A point compared to a tuple should not decide the tuple's side of the story. The string notimplemented is that sentinel.",
    "O(1)",
    "O(1)",
    """
def solve(left_type, right_type):
    if left_type == "point" and right_type == "point":
        return "compare"
    return "notimplemented"
""",
    [
        {"left_type": "point", "right_type": "point"},
        {"left_type": "point", "right_type": "other"},
        {"left_type": "other", "right_type": "point"},
        {"left_type": "other", "right_type": "other"},
    ],
)

add(
    "python-ex-team-members",
    "Team Members",
    "easy",
    ["python", "dataclasses"],
    "Implement `solve(left_add, right_add)`. Two teams are created with default empty member lists that must not be shared. Append `left_add` to the first team if it is not the empty string. Append `right_add` to the second the same way. Return `{\"left\": [...], \"right\": [...]}`. An empty string means no append for that side.",
    ["The default list is created per instance", "The teams do not share members"],
    [
        "Use a fresh list for each team. default_factory is the dataclass tool. A function-local list() is the same idea.",
        "Append only when the string is non-empty.",
        "Return the two lists.",
    ],
    "A dataclass default of [] is shared by every instance, the same bug as a class attribute. default_factory=list builds a new list per instance. After one append each, the two lists differ. A shared default would show both names on both teams.",
    "O(1)",
    "O(1)",
    """
def solve(left_add, right_add):
    def new_team():
        return []

    left, right = new_team(), new_team()
    if left_add:
        left.append(left_add)
    if right_add:
        right.append(right_add)
    return {"left": left, "right": right}
""",
    [
        {"left_add": "ada", "right_add": "grace"},
        {"left_add": "", "right_add": "grace"},
        {"left_add": "", "right_add": ""},
        {"left_add": "ada", "right_add": ""},
    ],
)

add(
    "python-ex-money-add",
    "Money Add",
    "medium",
    ["python", "dataclasses"],
    "Implement `solve(left_amount, left_ccy, right_amount, right_ccy)`. Amounts are integers. If the currencies differ, return `error`. Otherwise return `{\"amount\": sum, \"ccy\": currency}`. Adding returns a new value. It does not change a frozen record in place.",
    ["Different currencies are error", "Same currency sums the amounts"],
    [
        "Compare currencies first.",
        "Sum the amounts only when they match.",
        "Return a new dict. There is no input object to mutate.",
    ],
    "Frozen money cannot be incremented with += on a field. Addition returns a new money value. A currency mismatch is a domain error, not a silent conversion. Integer amounts keep the sum exact.",
    "O(1)",
    "O(1)",
    """
def solve(left_amount, left_ccy, right_amount, right_ccy):
    if left_ccy != right_ccy:
        return "error"
    return {"amount": left_amount + right_amount, "ccy": left_ccy}
""",
    [
        {"left_amount": 100, "left_ccy": "INR", "right_amount": 50, "right_ccy": "INR"},
        {"left_amount": 100, "left_ccy": "INR", "right_amount": 50, "right_ccy": "USD"},
        {"left_amount": 0, "left_ccy": "INR", "right_amount": 0, "right_ccy": "INR"},
        {"left_amount": -20, "left_ccy": "EUR", "right_amount": 5, "right_ccy": "EUR"},
    ],
)

add(
    "python-ex-replace-name",
    "Replace Name",
    "easy",
    ["python", "dataclasses"],
    "Implement `solve(name, new_name)`. Return `{\"old\": name, \"new\": new_name}`. Replacing a field on a frozen record returns a new record and leaves the old name in place. Do not overwrite `name`.",
    ["Both names are returned", "old is the original argument"],
    [
        "Echo name as old.",
        "Echo new_name as new.",
        "Do not return only the new name.",
    ],
    "dataclasses.replace builds a new instance with the listed fields changed. The original object stays. Tests that only look at the new value miss a mutation of the old one. Returning both names makes the copy obvious.",
    "O(1)",
    "O(1)",
    """
def solve(name, new_name):
    old = {"name": name}
    updated = {"name": new_name}
    return {"old": old["name"], "new": updated["name"]}
""",
    [
        {"name": "ada", "new_name": "grace"},
        {"name": "ada", "new_name": "ada"},
        {"name": "", "new_name": "a"},
        {"name": "a", "new_name": ""},
    ],
)

add(
    "python-ex-frozen-point",
    "Hash Point",
    "medium",
    ["python", "dataclasses"],
    "Implement `solve(points, query)`. `points` is a list of `[x, y]`. Insert them as keys with the value being the index of first insertion. Return the index for `query`, which is `[x, y]`, or the string `missing`. A later duplicate does not change the stored index.",
    ["The key is the coordinate pair", "First index wins"],
    [
        "Use a tuple key so it can live in a dict.",
        "Store the index only when the key is new.",
        "A missing query returns missing.",
    ],
    "A frozen dataclass with eq and frozen true gets a hash, so it can be a dict key. A mutable point cannot. The tuple is the same contract: hash and equality from the coordinates. First insertion wins so a duplicate coordinate does not move the index.",
    "O(n)",
    "O(n)",
    """
def solve(points, query):
    table = {}
    for index, (x, y) in enumerate(points):
        table.setdefault((x, y), index)
    key = (query[0], query[1])
    if key not in table:
        return "missing"
    return table[key]
""",
    [
        {"points": [[1, 2], [3, 4], [1, 2]], "query": [1, 2]},
        {"points": [[1, 2]], "query": [2, 1]},
        {"points": [], "query": [0, 0]},
        {"points": [[0, 0]], "query": [0, 0]},
    ],
)

add(
    "python-ex-checkout-place",
    "Checkout Place",
    "medium",
    ["python", "composition"],
    "Implement `solve(amount)`. If `amount` is not a positive int, return `error`. Otherwise charge that amount through an injected client and return `ok:{amount}`. The checkout object does not choose a concrete URL. It calls the client it was given.",
    ["Zero and negatives are error", "A positive amount is charged"],
    [
        "Validate the amount first.",
        "A tiny client records the amount and returns ok.",
        "Checkout.place calls client.charge.",
    ],
    "Composition is Checkout holding a client, not subclassing a payment vendor. The test double is the client. Validation stays in checkout so a fake client is not the only line of defense. The returned string is the charge the client saw.",
    "O(1)",
    "O(1)",
    """
def solve(amount):
    class Client:
        def charge(self, minor):
            return f"ok:{minor}"

    class Checkout:
        def __init__(self, client):
            self.client = client

        def place(self, minor):
            if type(minor) is not int or minor <= 0:
                return "error"
            return self.client.charge(minor)

    return Checkout(Client()).place(amount)
""",
    [
        {"amount": 500},
        {"amount": 0},
        {"amount": -1},
        {"amount": 1},
    ],
)

add(
    "python-ex-recording-client",
    "Recording Fake",
    "easy",
    ["python", "testing"],
    "Implement `solve(amounts)`. A fake client records every positive amount and returns `ok` for each. Non-positive amounts are not recorded and produce `reject` for that step. Return `{\"recorded\": [...], \"results\": [...]}`.",
    ["Order matches the input", "Rejects are not recorded"],
    [
        "Walk the amounts.",
        "A positive int is appended and results get ok.",
        "Anything else appends reject and does not record the amount.",
    ],
    "A recording fake is a test double with a real method. It stores the amounts the subject tried to charge. Assertions then look at the list, not at a mock's call history. Rejected amounts stay out of that list so a bug that charges zero is visible as a reject rather than as a stored zero.",
    "O(n)",
    "O(n)",
    """
def solve(amounts):
    recorded = []
    results = []
    for amount in amounts:
        if type(amount) is int and amount > 0:
            recorded.append(amount)
            results.append("ok")
        else:
            results.append("reject")
    return {"recorded": recorded, "results": results}
""",
    [
        {"amounts": [100, 0, 50]},
        {"amounts": []},
        {"amounts": [-1]},
        {"amounts": [1, 2]},
    ],
)

add(
    "python-ex-logging-wrapper",
    "Wrapper Return",
    "medium",
    ["python", "composition"],
    "Implement `solve(amount)`. A logging wrapper forwards `charge` to an inner client and records the amount. The inner client returns `ok:{amount}` for a positive int and `reject` otherwise. The wrapper must return that same result, not None, and include the amount in `seen` only when it forwarded. Return `{\"result\": ..., \"seen\": [...]}`. Always forward, including rejects, and record every forwarded amount.",
    ["The wrapper returns the inner result", "seen contains the forwarded amount"],
    [
        "Call the inner charge.",
        "Append the amount to seen.",
        "Return the inner result unchanged.",
    ],
    "A wrapper that logs and forgets to return the inner result turns a successful charge into None. The decorator-style object has one job besides the log line: pass the return value through. Recording the amount shows the forward happened.",
    "O(1)",
    "O(1)",
    """
def solve(amount):
    class Inner:
        def charge(self, minor):
            if type(minor) is int and minor > 0:
                return f"ok:{minor}"
            return "reject"

    class Logging:
        def __init__(self, inner):
            self.inner = inner
            self.seen = []

        def charge(self, minor):
            self.seen.append(minor)
            return self.inner.charge(minor)

    wrapper = Logging(Inner())
    result = wrapper.charge(amount)
    return {"result": result, "seen": wrapper.seen}
""",
    [
        {"amount": 500},
        {"amount": 0},
        {"amount": -2},
        {"amount": 1},
    ],
)

add(
    "python-ex-has-a",
    "Has A",
    "easy",
    ["python", "composition"],
    "Implement `solve(sentences)`. Each sentence is `child is-a parent` or `whole has-a part`. Return a list of `is-a` or `has-a` in order. A sentence that matches neither returns `unknown` for that item.",
    ["Look at the verb", "Do not infer from the nouns"],
    [
        "Split on spaces. The tests use exactly three words.",
        "The middle word is the relation.",
        "Anything else is unknown.",
    ],
    "is-a is inheritance. has-a is composition. The nouns do not decide it: a Car has an Engine, and an ElectricCar is a Car. Reading the verb is the classification. Guessing from the first noun is how a design discussion gets muddy.",
    "O(n)",
    "O(n)",
    """
def solve(sentences):
    out = []
    for sentence in sentences:
        parts = sentence.split()
        if len(parts) == 3 and parts[1] in ("is-a", "has-a"):
            out.append(parts[1])
        else:
            out.append("unknown")
    return out
""",
    [
        {"sentences": ["Car has-a Engine", "ElectricCar is-a Car"]},
        {"sentences": ["nope"]},
        {"sentences": []},
        {"sentences": ["A is-a B"]},
    ],
)

add(
    "python-ex-place-order",
    "Place Order",
    "medium",
    ["python", "solid"],
    "Implement `solve(amount, duplicate)`. If `amount` is not a positive int, return `error` and do not charge. If `duplicate` is 1, return `conflict`. Otherwise return `charged:{amount}`. Checkout calls a charger and a store. Those collaborators are implied by the result: a conflict happens before the charge string is returned.",
    ["Non-positive amounts are error", "duplicate 1 is conflict"],
    [
        "Validate the amount first.",
        "Then honor the duplicate flag.",
        "Only the remaining path returns charged.",
    ],
    "One class that prices, charges, saves, and emails violates single responsibility, and it is hard to fail one step. Splitting the charge and the save makes the order of checks explicit: bad amount, then conflict, then charge. The result string is the path that ran.",
    "O(1)",
    "O(1)",
    """
def solve(amount, duplicate):
    if type(amount) is not int or amount <= 0:
        return "error"
    if duplicate:
        return "conflict"
    return f"charged:{amount}"
""",
    [
        {"amount": 500, "duplicate": 0},
        {"amount": 0, "duplicate": 0},
        {"amount": 500, "duplicate": 1},
        {"amount": -1, "duplicate": 1},
    ],
)

add(
    "python-ex-split-reasons",
    "Split Reasons",
    "easy",
    ["python", "solid"],
    "Implement `solve(duties)`. Each duty is `price` or `ship` or something else. Return `{\"pricing\": [...], \"delivery\": [...]}`. `price` goes to pricing. `ship` goes to delivery. Anything else is dropped. Order inside each list follows the input.",
    ["Unknown duties are dropped", "The two lists are independent"],
    [
        "Walk once.",
        "Append price duties to pricing and ship duties to delivery.",
        "Do not put a duty in both lists.",
    ],
    "A class that both prices and ships has two reasons to change. Partitioning the duty list is the small version of that split. Dropping unknown words keeps a typo from landing in the wrong bucket silently. It is omitted, not guessed.",
    "O(n)",
    "O(n)",
    """
def solve(duties):
    pricing = []
    delivery = []
    for duty in duties:
        if duty == "price":
            pricing.append(duty)
        elif duty == "ship":
            delivery.append(duty)
    return {"pricing": pricing, "delivery": delivery}
""",
    [
        {"duties": ["price", "ship", "price", "email"]},
        {"duties": []},
        {"duties": ["ship"]},
        {"duties": ["other"]},
    ],
)

add(
    "python-ex-subtype-ok",
    "Subtype Check",
    "medium",
    ["python", "solid"],
    "Implement `solve(base_accepts, sub_accepts)`. Each flag is 1 or 0 for a particular input. Return `substitutable` when the subclass accepts every input the base accepts, which in this two-flag model means: if the base accepts, the subclass must accept. If the base rejects, the subclass may do either. Return `break` when the base accepts and the subclass rejects.",
    ["A narrower subclass breaks substitution", "A wider subclass is allowed here"],
    [
        "The failure is base_accepts == 1 and sub_accepts == 0.",
        "Every other combination returns substitutable.",
        "Do not require the flags to be equal.",
    ],
    "Liskov substitution says a subclass must accept what callers already pass to the base. Rejecting a positive amount that the base charged is a break. Accepting an extra case the base rejected does not surprise those callers. The flag pair is that test for one input.",
    "O(1)",
    "O(1)",
    """
def solve(base_accepts, sub_accepts):
    if base_accepts and not sub_accepts:
        return "break"
    return "substitutable"
""",
    [
        {"base_accepts": 1, "sub_accepts": 1},
        {"base_accepts": 1, "sub_accepts": 0},
        {"base_accepts": 0, "sub_accepts": 1},
        {"base_accepts": 0, "sub_accepts": 0},
    ],
)

add(
    "python-ex-wire-root",
    "Wire Root",
    "easy",
    ["python", "solid"],
    "Implement `solve(concrete)`. `concrete` is a list of class names from the outside dependency to the inner one, for example a client then a checkout. Return them reversed, which is the construction order: build the inside first. An empty list returns an empty list.",
    ["Input is outside-in", "Output is inside-out construction order"],
    [
        "Reverse the list.",
        "Do not sort.",
        "The last input name is constructed first.",
    ],
    "Dependency inversion means the use case names an abstraction, and main passes a concrete object. You construct the leaf first because the outer object needs it in its constructor. Reversing the outside-in list is that order.",
    "O(n)",
    "O(n)",
    """
def solve(concrete):
    return list(reversed(concrete))
""",
    [
        {"concrete": ["Checkout", "Client"]},
        {"concrete": ["App", "Service", "Repo"]},
        {"concrete": []},
        {"concrete": ["Only"]},
    ],
)

add(
    "python-ex-build-channel",
    "Build Channel",
    "medium",
    ["python", "patterns"],
    "Implement `solve(kind, message)`. `kind` is `email` or `sms`. Return `email:message` or `sms:message`. Any other kind returns `error`. This is a factory function. The caller does not construct the classes.",
    ["Unknown kinds are error", "The message is included for known kinds"],
    [
        "Map kind to a constructor in a dict.",
        "A missing kind returns error.",
        "Call send on the new instance.",
    ],
    "A factory hides the constructors behind a kind string the edge of the system already has, such as a config value. The mapping is the only branch. Callers depend on the send method, not on the class statements.",
    "O(1)",
    "O(1)",
    """
def solve(kind, message):
    class Email:
        def send(self, text):
            return "email:" + text

    class Sms:
        def send(self, text):
            return "sms:" + text

    table = {"email": Email, "sms": Sms}
    if kind not in table:
        return "error"
    return table[kind]().send(message)
""",
    [
        {"kind": "email", "message": "hi"},
        {"kind": "sms", "message": "hi"},
        {"kind": "push", "message": "hi"},
        {"kind": "email", "message": ""},
    ],
)

add(
    "python-ex-user-factory",
    "From Row Factory",
    "easy",
    ["python", "patterns"],
    "Implement `solve(name)`. Strip the name. Return `error` if it is empty. Otherwise return `user:{name}`. Construction goes through that validating path, not through a raw constructor the caller can call with a blank.",
    ["Whitespace-only is error", "The prefix is user:"],
    [
        "Strip.",
        "Reject empty.",
        "Return the prefixed name.",
    ],
    "A factory is the supported constructor when the raw initializer would accept junk, or when you want one place that validates. Callers that bypass it are the bug. The result string is what the factory returns after a successful check.",
    "O(n)",
    "O(n)",
    """
def solve(name):
    cleaned = name.strip()
    if not cleaned:
        return "error"
    return "user:" + cleaned
""",
    [
        {"name": " Ada "},
        {"name": "  "},
        {"name": "Grace"},
        {"name": ""},
    ],
)

add(
    "python-ex-singleton-init",
    "Singleton Init",
    "medium",
    ["python", "patterns"],
    "Implement `solve(levels, guarded)`. `levels` is a list of integer levels passed to successive constructors. `guarded` is 1 when `__init__` runs only the first time the instance is created, and 0 when every constructor call runs `__init__` again on the same object. Return the level that remains. Unguarded, the last level wins. Guarded, the first level wins. An empty list returns `error`.",
    ["guarded 1 keeps the first level", "guarded 0 keeps the last level"],
    [
        "An empty list has no instance.",
        "If guarded is 1, return levels[0].",
        "Otherwise return levels[-1].",
    ],
    "A __new__ singleton that always runs __init__ will reconfigure the shared object on the second constructor call. Guarding init with a flag keeps the first configuration. That bug is why a module-level instance, created once, is easier to reason about than a hand-rolled singleton.",
    "O(1)",
    "O(1)",
    """
def solve(levels, guarded):
    if not levels:
        return "error"
    if guarded:
        return levels[0]
    return levels[-1]
""",
    [
        {"levels": [1, 9], "guarded": 1},
        {"levels": [1, 9], "guarded": 0},
        {"levels": [], "guarded": 1},
        {"levels": [4], "guarded": 0},
    ],
)

add(
    "python-ex-registry-add",
    "Registry Add",
    "medium",
    ["python", "patterns"],
    "Implement `solve(registrations, kind)`. `registrations` is a list of `[kind, builder]` pairs in order. A duplicate kind returns `error` for the whole registration and does not silently overwrite. If registration succeeds, return the builder name for `kind`, or `missing` if that kind was never registered.",
    ["The first duplicate aborts", "Builders are strings"],
    [
        "Insert into a dict only when the kind is new.",
        "On a duplicate, return error immediately.",
        "After a clean insert pass, look up kind.",
    ],
    "A factory registry that overwrites a kind hides two teams registering the same name. Rejecting the duplicate makes the clash visible at startup. The lookup after a clean registration is the normal factory path.",
    "O(n)",
    "O(n)",
    """
def solve(registrations, kind):
    table = {}
    for key, builder in registrations:
        if key in table:
            return "error"
        table[key] = builder
    return table.get(kind, "missing")
""",
    [
        {"registrations": [["email", "Email"], ["sms", "Sms"]], "kind": "sms"},
        {"registrations": [["email", "A"], ["email", "B"]], "kind": "email"},
        {"registrations": [], "kind": "email"},
        {"registrations": [["email", "Email"]], "kind": "sms"},
    ],
)

add(
    "python-ex-percent-off",
    "Percent Off",
    "easy",
    ["python", "patterns"],
    "Implement `solve(minor, percent)`. `minor` is a non-negative integer price in minor units. `percent` is an integer from 0 through 100. Return the discounted price using integer arithmetic: `minor - minor * percent // 100`. If `minor` is negative or `percent` is outside 0 through 100, return `error`.",
    ["Integer math only", "percent is inclusive of 0 and 100"],
    [
        "Validate both inputs.",
        "Compute the discount with floor division.",
        "Subtract it from minor.",
    ],
    "A percent-off strategy is one function of money. Float percents drift. Integer minor units and floor division keep the result exact and slightly in the customer's favor on the remainder, which you can document. The validation stops a 200 percent discount from producing a negative price.",
    "O(1)",
    "O(1)",
    """
def solve(minor, percent):
    if minor < 0 or percent < 0 or percent > 100:
        return "error"
    return minor - minor * percent // 100
""",
    [
        {"minor": 1000, "percent": 10},
        {"minor": 199, "percent": 10},
        {"minor": 1000, "percent": 0},
        {"minor": -1, "percent": 10},
    ],
)

add(
    "python-ex-order-listeners",
    "Order Listeners",
    "medium",
    ["python", "patterns"],
    "Implement `solve(listeners, event)`. `listeners` is a list of names. Notify a snapshot of that list with `event`. Return `[name:event, ...]` in the snapshot order. Take the snapshot before you notify, so the result length matches the input length even if a listener would have unsubscribed itself. You do not need to mutate the list. Just notify the copy.",
    ["Snapshot first", "Every current listener is notified once"],
    [
        "Copy the listener list.",
        "Build name:event for each copied name.",
        "Do not iterate the live list if you also delete from it. The copy is the point.",
    ],
    "An observer list mutated during notification skips or double-calls. Iterating a copy, or iterating a snapshot of the names, freezes the set of recipients for this event. The result is that snapshot's messages, in order.",
    "O(n)",
    "O(n)",
    """
def solve(listeners, event):
    snapshot = list(listeners)
    return [name + ":" + event for name in snapshot]
""",
    [
        {"listeners": ["audit", "mail"], "event": "placed"},
        {"listeners": [], "event": "placed"},
        {"listeners": ["audit"], "event": ""},
        {"listeners": ["a", "b", "a"], "event": "x"},
    ],
)

add(
    "python-ex-retry-send",
    "Retry Send",
    "medium",
    ["python", "patterns"],
    "Implement `solve(attempts)`. `attempts` is a list of `ok` or `conn` in the order the sender would fail. Retry only `conn`, up to 3 attempts. Return the first `ok`, or `conn` if all consumed attempts were `conn`, or `error` if a non-conn failure appears... The only failure tag is `conn`. Stop at `ok`. If you consume 3 `conn` values without an ok, return `conn`. If the list ends earlier on `conn`, return `conn`. A first `ok` returns `ok`.",
    ["Maximum 3 attempts", "ok stops the loop"],
    [
        "Look at most at the first 3 attempts.",
        "Return ok on the first ok.",
        "If you never see ok, return conn.",
    ],
    "A retry wrapper around a sender is a decorator object, not an edit of the sender. It retries one failure class. A validation error would not be in this list. The cap of 3 stops a dead host from pinning the request. The returned tag is what the caller observes.",
    "O(1)",
    "O(1)",
    """
def solve(attempts):
    for result in attempts[:3]:
        if result == "ok":
            return "ok"
    return "conn"
""",
    [
        {"attempts": ["conn", "ok"]},
        {"attempts": ["conn", "conn", "conn", "ok"]},
        {"attempts": ["ok"]},
        {"attempts": ["conn"]},
    ],
)

add(
    "python-ex-wrapper-order",
    "Stack Wrappers",
    "medium",
    ["python", "patterns"],
    "Implement `solve(names)`. `names` is wrapper names from the outside in, the first name being the first one entered on a send. Return that same order. This is the call order, not the construction order. Construction wraps from the inside out, so the last constructed wrapper is the outside and runs first. The input is already outside-in. Return a copy.",
    ["Do not reverse", "The first name runs first"],
    [
        "The problem states the input is already the call order.",
        "Return a new list of the same names.",
        "An empty stack returns an empty list.",
    ],
    "Decorators and wrapper objects both nest. The outside wrapper runs first on the way in and last on the way out. If you construct retry(logging(sender)), retry is outside and runs first. The list you return is that entry order, which the caller already arranged outside-in.",
    "O(n)",
    "O(n)",
    """
def solve(names):
    return list(names)
""",
    [
        {"names": ["retry", "log", "sender"]},
        {"names": ["sender"]},
        {"names": []},
        {"names": ["a", "b"]},
    ],
)
