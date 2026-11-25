"""Monotonic stacks, expression evaluation, and interval problems."""

from __future__ import annotations

from lib import cases, define


@define(
    slug="valid-parentheses",
    title="Valid Parentheses",
    difficulty="easy",
    topics=["stacks", "strings"],
    statement="Return true when every bracket in `s` is closed by the same type and in the correct order. `s` contains only the characters ()[]{}.",
    constraints=["1 <= s.length <= 10^4"],
    signature="def is_valid(s: str) -> bool:",
    function_name="is_valid",
    hints=[
        "A closing bracket is legal only when it matches the nearest still-open bracket.",
        "A stack stores that nearest opener.",
        "The string is valid when the stack ends empty and no closer arrived too early.",
    ],
    approaches=[
        ("Replace pairs repeatedly", "O(n^2)", "O(n)", "Delete () [] and the brace pair until nothing changes."),
        ("Stack of openers", "O(n)", "O(n)", "Push openers, pop on a matching closer."),
    ],
    editorial=(
        "Scan left to right. Push opening brackets. On a closing bracket, the stack must be nonempty and its top must be the matching opener. "
        "Any other situation is invalid. After the scan the stack must be empty, otherwise some opener was never closed."
    ),
    companies=["Amazon", "Microsoft", "Google", "Bloomberg"],
)
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack


def _oracle_is_valid(s: str) -> bool:
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            stack.append(pairs[ch])
        elif not stack or stack.pop() != ch:
            return False
    return not stack


cases(
    "valid-parentheses",
    _oracle_is_valid,
    [
        ("yes", {"s": "()[]{}"}, True, "Three independent pairs."),
        ("nested", {"s": "([{}])"}, True, "Each closer matches the latest opener."),
        ("wrong", {"s": "(]"}, False, None),
        ("early", {"s": ")("}, False, None),
        ("open", {"s": "((("}, False, None),
    ],
)


@define(
    slug="daily-temperatures",
    title="Daily Temperatures",
    difficulty="medium",
    topics=["stacks", "monotonic-stack"],
    statement=(
        "Given daily temperatures, return an array `answer` where `answer[i]` is the number of days you have to wait after day i "
        "to see a strictly warmer temperature. If no future day is warmer, use 0."
    ),
    constraints=["1 <= temperatures.length <= 10^5", "30 <= temperatures[i] <= 100"],
    signature="from typing import List\n\ndef daily_temperatures(temperatures: List[int]) -> List[int]:",
    function_name="daily_temperatures",
    hints=[
        "For each day, the naive scan looks forward until a warmer day.",
        "A decreasing stack of indices remembers days still waiting for a warmer future.",
        "When today is warmer than the stack top, that top's answer is today minus its index. Pop until the stack is decreasing again.",
    ],
    approaches=[
        ("Scan forward", "O(n^2)", "O(1)", "For each day, walk the suffix."),
        ("Monotonic decreasing stack", "O(n)", "O(n)", "Each index is pushed and popped at most once."),
    ],
    editorial=(
        "The stack stores indices whose temperatures are waiting for a resolution, in decreasing temperature order. "
        "A new warmer day resolves every colder day on top. The wait is the index difference. "
        "Days left on the stack at the end keep the default answer 0."
    ),
    companies=["Amazon", "Bloomberg", "Facebook", "Microsoft"],
)
def daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def _oracle_daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = []
    for i, temp in enumerate(temperatures):
        wait = 0
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > temp:
                wait = j - i
                break
        answer.append(wait)
    return answer


cases(
    "daily-temperatures",
    _oracle_daily_temperatures,
    [
        ("classic", {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}, True, "The waits are 1, 1, 4, 2, 1, 1, 0, 0."),
        ("increasing", {"temperatures": [30, 40, 50, 60]}, True, "Each day waits exactly one day."),
        ("decreasing", {"temperatures": [90, 80, 70]}, False, None),
        ("single", {"temperatures": [50]}, False, None),
        ("tie", {"temperatures": [70, 70, 71]}, False, None),
    ],
)


@define(
    slug="next-greater-element-i",
    title="Next Greater Element I",
    difficulty="easy",
    topics=["stacks", "monotonic-stack", "hashing"],
    statement=(
        "`nums1` is a subset of `nums2`. For each value in nums1, find the next greater element in nums2 to its right. "
        "If none exists, use -1. Return the answers in the order of nums1."
    ),
    constraints=["1 <= nums1.length <= nums2.length <= 1000", "All values are unique"],
    signature="from typing import List\n\ndef next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:",
    function_name="next_greater_element",
    hints=[
        "Compute the next greater element for every index of nums2 first.",
        "A decreasing stack resolves next-greater as soon as a larger value arrives.",
        "Store the result in a map from value to next greater, then read it for nums1.",
    ],
    approaches=[
        ("Scan nums2 for each query", "O(n * m)", "O(1)", "Find the value, then scan right."),
        ("Monotonic stack plus map", "O(n + m)", "O(n)", "One pass over nums2 answers every value."),
    ],
    editorial=(
        "Walk nums2 with a decreasing stack of values. When nums2[i] is larger than the top, it is the next greater element of every popped value. "
        "Unpopped values map to -1. Query the map for each element of nums1."
    ),
    companies=["Amazon", "Bloomberg", "Google", "Adobe"],
)
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    nxt: dict[int, int] = {}
    stack: list[int] = []
    for value in nums2:
        while stack and stack[-1] < value:
            nxt[stack.pop()] = value
        stack.append(value)
    return [nxt.get(value, -1) for value in nums1]


def _oracle_next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    out = []
    for value in nums1:
        i = nums2.index(value)
        found = -1
        for later in nums2[i + 1 :]:
            if later > value:
                found = later
                break
        out.append(found)
    return out


cases(
    "next-greater-element-i",
    _oracle_next_greater_element,
    [
        ("classic", {"nums1": [4, 1, 2], "nums2": [1, 3, 4, 2]}, True, "None of 4, 1's next is 3, and 2 has none. Wait: 4 has none, 1 maps to 3, 2 has none."),
        ("all", {"nums1": [2, 4], "nums2": [2, 1, 3, 4]}, True, "2 maps to 3 and 4 maps to -1."),
        ("single", {"nums1": [1], "nums2": [1]}, False, None),
        ("increasing", {"nums1": [1, 2], "nums2": [1, 2, 3]}, False, None),
        ("decreasing", {"nums1": [3, 2], "nums2": [3, 2, 1]}, False, None),
    ],
)


@define(
    slug="next-greater-element-ii",
    title="Next Greater Element II",
    difficulty="medium",
    topics=["stacks", "monotonic-stack"],
    statement="The array `nums` is circular. For each index, return the next greater element searching to the right with wraparound, or -1 if none exists.",
    constraints=["1 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
    signature="from typing import List\n\ndef next_greater_elements(nums: List[int]) -> List[int]:",
    function_name="next_greater_elements",
    hints=[
        "A circular array can be scanned as if it were concatenated with itself, without actually copying it.",
        "Walk indices modulo n, for 2n steps, and only write an answer the first time an index is resolved.",
        "The stack still stores indices in decreasing value order.",
    ],
    approaches=[
        ("Scan the circle", "O(n^2)", "O(1)", "From each index walk at most n - 1 steps."),
        ("Monotonic stack over two passes", "O(n)", "O(n)", "Index i and i + n share the same value."),
    ],
    editorial=(
        "Iterate i from 0 to 2n - 1 and let j = i mod n. Pop indices whose values are smaller than nums[j] and assign nums[j] as their answer. "
        "Push j only during the first pass, so each index is stored once. "
        "The second pass exists only to let earlier indices see values that sit to their left in the circle."
    ),
    companies=["Amazon", "Google", "ByteDance", "Adobe"],
)
def next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [-1] * n
    stack: list[int] = []
    for i in range(2 * n):
        value = nums[i % n]
        while stack and nums[stack[-1]] < value:
            answer[stack.pop()] = value
        if i < n:
            stack.append(i)
    return answer


def _oracle_next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)
    out = []
    for i in range(n):
        found = -1
        for step in range(1, n):
            if nums[(i + step) % n] > nums[i]:
                found = nums[(i + step) % n]
                break
        out.append(found)
    return out


cases(
    "next-greater-element-ii",
    _oracle_next_greater_elements,
    [
        ("classic", {"nums": [1, 2, 1]}, True, "Answers are 2, -1, 2."),
        ("increasing", {"nums": [1, 2, 3]}, True, "Only wraparound can help 1 and 2. 3 has no greater value."),
        ("single", {"nums": [5]}, False, None),
        ("dup-max", {"nums": [5, 4, 5]}, False, None),
        ("decreasing", {"nums": [3, 2, 1]}, False, None),
    ],
)


@define(
    slug="largest-rectangle-in-histogram",
    title="Largest Rectangle in Histogram",
    difficulty="hard",
    topics=["stacks", "monotonic-stack"],
    statement="Given bar heights, return the area of the largest rectangle that can be formed inside the histogram. Each bar has width 1.",
    constraints=["1 <= heights.length <= 10^5", "0 <= heights[i] <= 10^4"],
    signature="from typing import List\n\ndef largest_rectangle_area(heights: List[int]) -> int:",
    function_name="largest_rectangle_area",
    hints=[
        "For each bar, the best rectangle that uses it as the shortest bar extends left and right until a shorter bar.",
        "A nearest-smaller index on each side gives that width.",
        "A monotonic increasing stack computes both nearest smaller indices as bars are popped.",
    ],
    approaches=[
        ("Expand each bar", "O(n^2)", "O(1)", "Walk left and right while the height stays at least heights[i]."),
        ("Monotonic stack", "O(n)", "O(n)", "Pop a bar when a shorter bar arrives. The new bar is its right bound and the new top is its left bound."),
    ],
    editorial=(
        "Append a sentinel 0 so every bar is eventually popped. The stack stores increasing heights. "
        "When bar i is shorter than the top, the top bar cannot extend to i. Its right bound is i and its left bound is the new stack top. "
        "Width is right - left - 1. Area is height times width. The maximum area is the answer."
    ),
    companies=["Amazon", "Google", "Microsoft", "Facebook"],
)
def largest_rectangle_area(heights: list[int]) -> int:
    stack = [-1]
    best = 0
    extended = heights + [0]
    for i, height in enumerate(extended):
        while stack[-1] != -1 and extended[stack[-1]] > height:
            h = extended[stack.pop()]
            width = i - stack[-1] - 1
            best = max(best, h * width)
        stack.append(i)
    return best


def _oracle_largest_rectangle_area(heights: list[int]) -> int:
    best = 0
    for i, height in enumerate(heights):
        if height == 0:
            continue
        left = i
        while left > 0 and heights[left - 1] >= height:
            left -= 1
        right = i
        while right + 1 < len(heights) and heights[right + 1] >= height:
            right += 1
        best = max(best, height * (right - left + 1))
    return best


cases(
    "largest-rectangle-in-histogram",
    _oracle_largest_rectangle_area,
    [
        ("classic", {"heights": [2, 1, 5, 6, 2, 3]}, True, "The rectangle of height 5 and width 2 has area 10."),
        ("flat", {"heights": [2, 4]}, True, "The best area is 4."),
        ("single", {"heights": [6]}, False, None),
        ("zeros", {"heights": [0, 1, 0]}, False, None),
        ("increasing", {"heights": [1, 2, 3, 4]}, False, None),
    ],
)


@define(
    slug="evaluate-reverse-polish-notation",
    title="Evaluate Reverse Polish Notation",
    difficulty="medium",
    topics=["stacks", "expression-evaluation"],
    statement=(
        "Evaluate the arithmetic expression in Reverse Polish Notation. "
        "Tokens are integers or the operators +, -, *, and /. Division truncates toward zero. Return the integer result."
    ),
    constraints=["1 <= tokens.length <= 10^4", "The expression is valid"],
    signature="from typing import List\n\ndef eval_rpn(tokens: List[str]) -> int:",
    function_name="eval_rpn",
    hints=[
        "A number is pushed. An operator pops two numbers, applies itself, and pushes the result.",
        "The right operand is the first value popped.",
        "Python's int() truncation toward zero differs from floor division for negatives. Use integer division that truncates toward zero.",
    ],
    approaches=[
        ("Recursive descent on a reversed token list", "O(n)", "O(n)", "Possible, but the stack is the natural machine for RPN."),
        ("Explicit stack", "O(n)", "O(n)", "One pass, one stack."),
    ],
    editorial=(
        "RPN is the postfix form a stack machine evaluates directly. "
        "Pop b, pop a, push a op b. For division, truncating toward zero is int(a / b) in Python 3, not a // b, because floor division goes away from zero for negatives."
    ),
    companies=["Amazon", "Google", "LinkedIn", "Microsoft"],
)
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[-1]


def _oracle_eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    for token in tokens:
        if token in ops:
            right = stack.pop()
            left = stack.pop()
            stack.append(ops[token](left, right))
        else:
            stack.append(int(token))
    return stack[0]


cases(
    "evaluate-reverse-polish-notation",
    _oracle_eval_rpn,
    [
        ("classic", {"tokens": ["2", "1", "+", "3", "*"]}, True, "(2 + 1) * 3 = 9."),
        ("division", {"tokens": ["4", "13", "5", "/", "+"]}, True, "4 + (13 / 5) = 6."),
        ("negative", {"tokens": ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]}, False, None),
        ("single", {"tokens": ["42"]}, False, None),
        ("subtract", {"tokens": ["3", "4", "-"]}, False, None),
    ],
)


@define(
    slug="basic-calculator-ii",
    title="Basic Calculator II",
    difficulty="medium",
    topics=["stacks", "expression-evaluation"],
    statement=(
        "Evaluate an expression string containing non-negative integers, the operators +, -, *, /, and spaces. "
        "Division truncates toward zero. Operator precedence applies: * and / bind tighter than + and -."
    ),
    constraints=["1 <= s.length <= 10^5", "The expression is valid", "The answer fits in a 32-bit signed integer"],
    signature="def calculate(s: str) -> int:",
    function_name="calculate",
    hints=[
        "You can delay + and - by pushing signed numbers, and apply * and / immediately to the stack top.",
        "Keep the previous operator. When a number ends, apply that operator.",
        "A trailing sentinel operator forces the last number to be applied.",
    ],
    approaches=[
        ("Two stacks with precedence", "O(n)", "O(n)", "The general shunting-yard method."),
        ("One stack and last operator", "O(n)", "O(n)", "Enough when the only precedence split is times/divide versus plus/minus."),
    ],
    editorial=(
        "Scan the string and accumulate the current number. When an operator is seen, the previous operator decides what to do with that number. "
        "Plus pushes the number, minus pushes its negation, and times or divide combine it with the stack top using truncation toward zero. "
        "The answer is the sum of the stack. Processing a final '+' after the loop flushes the last number."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Uber"],
)
def calculate(s: str) -> int:
    stack: list[int] = []
    num = 0
    op = "+"
    for i, ch in enumerate(s + "+"):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in "+-*/" or i == len(s):
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))
            op = ch
            num = 0
    return sum(stack)


def _oracle_calculate(s: str) -> int:
    tokens: list[str] = []
    num = ""
    for ch in s:
        if ch == " ":
            continue
        if ch.isdigit():
            num += ch
        else:
            if num:
                tokens.append(num)
                num = ""
            tokens.append(ch)
    if num:
        tokens.append(num)
    # Shunting into values with immediate * /
    values: list[int] = []
    pending = "+"
    for token in tokens + ["+"]:
        if token in "+-*/":
            values.append(0)  # placeholder replaced below? handle differently
    values = []
    current = 0
    last = "+"
    raw = s.replace(" ", "") + "+"
    i = 0
    while i < len(raw):
        if raw[i].isdigit():
            j = i
            while j < len(raw) and raw[j].isdigit():
                j += 1
            current = int(raw[i:j])
            i = j
        else:
            if last == "+":
                values.append(current)
            elif last == "-":
                values.append(-current)
            elif last == "*":
                values.append(values.pop() * current)
            else:
                values.append(int(values.pop() / current))
            last = raw[i]
            current = 0
            i += 1
    return sum(values)


cases(
    "basic-calculator-ii",
    _oracle_calculate,
    [
        ("plus-times", {"s": "3+2*2"}, True, "Multiplication happens before addition: 7."),
        ("divide", {"s": " 3/2 "}, True, "Truncation toward zero yields 1."),
        ("mixed", {"s": " 3+5 / 2 "}, False, None),
        ("chain", {"s": "14-3/2"}, False, None),
        ("only", {"s": "42"}, False, None),
    ],
)


@define(
    slug="decode-string",
    title="Decode String",
    difficulty="medium",
    topics=["stacks", "strings"],
    statement=(
        "Decode an encoded string. `k[encoded]` means the encoded substring inside the brackets is repeated k times. "
        "Inputs are valid and nesting is allowed. Digits are not zero and do not have leading zeros."
    ),
    constraints=["1 <= s.length <= 30 for these tests", "The decoded length is small"],
    signature="def decode_string(s: str) -> str:",
    function_name="decode_string",
    hints=[
        "When you see '[', you must remember both the current string and the repeat count that applies to the upcoming substring.",
        "A stack of (previous_string, repeat) pairs handles nesting.",
        "On ']', pop, repeat the current buffer, and append it to the previous string.",
    ],
    approaches=[
        ("Recursion with an index", "O(n)", "O(n)", "A helper consumes one substring and returns the new index."),
        ("Explicit stack", "O(n)", "O(n)", "Same state as the call stack, stored manually."),
    ],
    editorial=(
        "Maintain the string built at the current nesting level and the number currently being parsed. "
        "An opening bracket pushes both and resets them. A closing bracket pops and concatenates previous + current * repeat. "
        "Digits extend the number, and letters extend the current string."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []
    current = ""
    number = 0
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch == "[":
            stack.append((current, number))
            current = ""
            number = 0
        elif ch == "]":
            prev, repeat = stack.pop()
            current = prev + current * repeat
        else:
            current += ch
    return current


def _oracle_decode_string(s: str) -> str:
    def parse(i: int) -> tuple[str, int]:
        current = ""
        number = 0
        while i < len(s):
            ch = s[i]
            if ch.isdigit():
                number = number * 10 + int(ch)
                i += 1
            elif ch == "[":
                inner, i = parse(i + 1)
                current += inner * number
                number = 0
            elif ch == "]":
                return current, i + 1
            else:
                current += ch
                i += 1
        return current, i

    text, _ = parse(0)
    return text


cases(
    "decode-string",
    _oracle_decode_string,
    [
        ("simple", {"s": "3[a]2[bc]"}, True, "The decoding is aaabcbc."),
        ("nested", {"s": "3[a2[c]]"}, True, "The decoding is accaccacc."),
        ("plain", {"s": "abc"}, False, None),
        ("mixed", {"s": "2[ab3[c]]"}, False, None),
        ("ten", {"s": "10[a]"}, False, None),
    ],
)


@define(
    slug="asteroid-collision",
    title="Asteroid Collision",
    difficulty="medium",
    topics=["stacks"],
    statement=(
        "Each asteroid is an integer. Sign is direction, right is positive, and magnitude is size. "
        "Asteroids move at the same speed. When two collide, the smaller explodes. Equal magnitudes both explode. "
        "Asteroids moving in the same direction never meet. Return the state after all collisions."
    ),
    constraints=["2 <= asteroids.length <= 10^4", "-1000 <= asteroids[i] <= 1000", "asteroids[i] != 0"],
    signature="from typing import List\n\ndef asteroid_collision(asteroids: List[int]) -> List[int]:",
    function_name="asteroid_collision",
    hints=[
        "A collision happens only when a right-moving asteroid is already on the stack and the new one moves left.",
        "The stack top is the candidate that the new left-mover hits.",
        "If the new asteroid is larger, pop the top and keep comparing. If it is equal, pop and discard the new one.",
    ],
    approaches=[
        ("Simulation with a list", "O(n^2)", "O(n)", "Rescan after every explosion."),
        ("Stack of survivors", "O(n)", "O(n)", "Each asteroid is pushed and popped at most once."),
    ],
    editorial=(
        "Stable asteroids are those that will never meet a later opposite asteroid already resolved. "
        "Push right-movers freely. A left-mover destroys smaller right-movers on top, dies against a larger one, or mutually destroys an equal one. "
        "A left-mover that clears the stack, or meets another left-mover, survives."
    ),
    companies=["Amazon", "Facebook", "Uber", "Google"],
)
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for rock in asteroids:
        alive = True
        while alive and rock < 0 and stack and stack[-1] > 0:
            if stack[-1] < -rock:
                stack.pop()
            elif stack[-1] == -rock:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(rock)
    return stack


def _oracle_asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for rock in asteroids:
        stack.append(rock)
        while len(stack) >= 2 and stack[-2] > 0 and stack[-1] < 0:
            right, left = stack[-2], stack[-1]
            if abs(right) == abs(left):
                stack.pop()
                stack.pop()
            elif abs(right) > abs(left):
                stack.pop()
            else:
                left_rock = stack.pop()
                stack.pop()
                stack.append(left_rock)
    return stack


cases(
    "asteroid-collision",
    _oracle_asteroid_collision,
    [
        ("classic", {"asteroids": [5, 10, -5]}, True, "10 destroys -5. The state is 5, 10."),
        ("equal", {"asteroids": [8, -8]}, True, "Both explode."),
        ("left-first", {"asteroids": [-2, -1, 1, -2]}, False, None),
        ("chain", {"asteroids": [10, 2, -5]}, False, None),
        ("same-way", {"asteroids": [-2, -1, 1, 2]}, False, None),
    ],
)


@define(
    slug="remove-k-digits",
    title="Remove K Digits",
    difficulty="medium",
    topics=["stacks", "monotonic-stack", "greedy"],
    statement=(
        "Remove `k` digits from the non-negative integer string `num` so the remaining number is as small as possible. "
        "Return it as a string without leading zeros, or '0' if every digit is removed."
    ),
    constraints=["1 <= num.length <= 10^5", "0 <= k <= num.length", "num has no leading zeros except the number 0"],
    signature="def remove_kdigits(num: str, k: int) -> str:",
    function_name="remove_kdigits",
    hints=[
        "A decreasing digit sequence is already small. An ascent is a place where deleting the previous larger digit helps.",
        "Keep a stack of chosen digits. While the new digit is smaller than the top and deletions remain, pop.",
        "If deletions remain, they come off the tail. Then strip leading zeros.",
    ],
    approaches=[
        ("Try every deletion subset", "O(C(n, k) * n)", "O(n)", "Only for tiny n."),
        ("Monotonic increasing stack", "O(n)", "O(n)", "Each digit is pushed and popped at most once."),
    ],
    editorial=(
        "The greedy choice is to delete a left digit that is larger than the digit immediately after it. "
        "The stack enforces that by popping while the top is greater than the incoming digit and k remains. "
        "After the scan, delete any leftover budget from the end, which handles a nondecreasing number such as 12345. Strip zeros and return '0' for an empty result."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def remove_kdigits(num: str, k: int) -> str:
    stack: list[str] = []
    for digit in num:
        while k and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k:
        stack = stack[:-k]
    result = "".join(stack).lstrip("0")
    return result or "0"


def _oracle_remove_kdigits(num: str, k: int) -> str:
    from itertools import combinations

    if k == len(num):
        return "0"
    best = None
    for keep in combinations(range(len(num)), len(num) - k):
        candidate = "".join(num[i] for i in keep).lstrip("0") or "0"
        if best is None or (len(candidate), candidate) < (len(best), best):
            best = candidate
    return best or "0"


cases(
    "remove-k-digits",
    _oracle_remove_kdigits,
    [
        ("classic", {"num": "1432219", "k": 3}, True, "Removing 4, 3, and 2 leaves 1219."),
        ("zeros", {"num": "10200", "k": 1}, True, "Removing 1 leaves 200, written as 200."),
        ("all", {"num": "10", "k": 2}, False, None),
        ("increasing", {"num": "1234", "k": 2}, False, None),
        ("same", {"num": "1111", "k": 2}, False, None),
    ],
)


@define(
    slug="simplify-path",
    title="Simplify Path",
    difficulty="medium",
    topics=["stacks", "strings"],
    statement=(
        "Convert an absolute Unix path to its canonical form. "
        "'.' means the current directory, '..' means the parent, and multiple slashes are one separator. The result starts with a single slash."
    ),
    constraints=["1 <= path.length <= 3000", "path is an absolute path"],
    signature="def simplify_path(path: str) -> str:",
    function_name="simplify_path",
    hints=[
        "Split on '/'. Empty tokens come from repeated slashes and are ignored.",
        "'.' is ignored. '..' pops a directory if the stack is not empty. You cannot go above the root.",
        "Join the stack with slashes and prefix the root slash.",
    ],
    approaches=[
        ("String replace", "O(n^2)", "O(n)", "Fragile around repeated slashes and dot segments."),
        ("Stack of directory names", "O(n)", "O(n)", "One token decides push, pop, or skip."),
    ],
    editorial=(
        "The stack is the sequence of real directories still on the path. "
        "Tokens that are empty or '.' do not change it. '..' pops when possible. Every other token is a directory name and is pushed. "
        "The canonical path is '/' joined with the stack, or '/' when the stack is empty."
    ),
    companies=["Facebook", "Amazon", "Microsoft", "Bloomberg"],
)
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for token in path.split("/"):
        if token in {"", "."}:
            continue
        if token == "..":
            if stack:
                stack.pop()
        else:
            stack.append(token)
    return "/" + "/".join(stack)


def _oracle_simplify_path(path: str) -> str:
    parts: list[str] = []
    i = 0
    while i < len(path):
        while i < len(path) and path[i] == "/":
            i += 1
        j = i
        while j < len(path) and path[j] != "/":
            j += 1
        token = path[i:j]
        i = j
        if token in {"", "."}:
            continue
        if token == "..":
            if parts:
                parts.pop()
        else:
            parts.append(token)
    return "/" + "/".join(parts)


cases(
    "simplify-path",
    _oracle_simplify_path,
    [
        ("classic", {"path": "/home/"}, True, "The canonical path is /home."),
        ("parent", {"path": "/../"}, True, "The root has no parent."),
        ("dots", {"path": "/home//foo/"}, False, None),
        ("up", {"path": "/a/./b/../../c/"}, False, None),
        ("file", {"path": "/a/../../b/../c//.//"}, False, None),
    ],
)


@define(
    slug="merge-intervals",
    title="Merge Intervals",
    difficulty="medium",
    topics=["intervals", "sorting"],
    statement="Merge all overlapping intervals and return an array of the non-overlapping intervals that cover them. Touching endpoints overlap. Sort the result by start time.",
    constraints=["1 <= intervals.length <= 10^4", "0 <= start <= end <= 10^4"],
    signature="from typing import List\n\ndef merge(intervals: List[List[int]]) -> List[List[int]]:",
    function_name="merge",
    hints=[
        "Sorting by start time makes overlaps local. The next interval can only overlap the last merged one.",
        "If the next start is at most the last end, extend the last end to the maximum of the two ends.",
        "Otherwise append a new interval.",
    ],
    approaches=[
        ("Compare all pairs", "O(n^2)", "O(n)", "Repeatedly merge any overlapping pair."),
        ("Sort and sweep", "O(n log n)", "O(n)", "One pass after sorting."),
    ],
    editorial=(
        "Sort by start. The merged list's last interval is the only one that can still grow. "
        "An interval that starts after that end is disjoint and becomes a new group. "
        "An interval that starts earlier or at the end extends the group. The sort is the expensive step."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def merge(intervals: list[list[int]]) -> list[list[int]]:
    ordered = sorted(intervals)
    out = [ordered[0][:]]
    for start, end in ordered[1:]:
        if start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


def _oracle_merge(intervals: list[list[int]]) -> list[list[int]]:
    ordered = sorted(intervals)
    changed = True
    while changed:
        changed = False
        nxt: list[list[int]] = []
        for start, end in ordered:
            if nxt and start <= nxt[-1][1]:
                nxt[-1][1] = max(nxt[-1][1], end)
                changed = True
            else:
                nxt.append([start, end])
        ordered = nxt
    return ordered


cases(
    "merge-intervals",
    _oracle_merge,
    [
        ("classic", {"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]}, True, "[1, 3] and [2, 6] become [1, 6]."),
        ("touch", {"intervals": [[1, 4], [4, 5]]}, True, "Touching endpoints merge into [1, 5]."),
        ("contained", {"intervals": [[1, 10], [2, 3], [4, 5]]}, False, None),
        ("disjoint", {"intervals": [[1, 2], [4, 5]]}, False, None),
        ("unsorted", {"intervals": [[5, 6], [1, 3], [2, 4]]}, False, None),
    ],
)


@define(
    slug="insert-interval",
    title="Insert Interval",
    difficulty="medium",
    topics=["intervals"],
    statement=(
        "`intervals` is a sorted list of non-overlapping intervals. Insert `new_interval` and merge whatever overlaps it. "
        "Return the sorted result."
    ),
    constraints=["0 <= intervals.length <= 10^4", "intervals are sorted by start and do not overlap"],
    signature="from typing import List\n\ndef insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:",
    function_name="insert",
    hints=[
        "Copy every interval that ends before the new one starts.",
        "Merge every interval that overlaps the new one by expanding its start and end.",
        "Then append the merged interval and copy the rest unchanged.",
    ],
    approaches=[
        ("Append and run merge-intervals", "O(n log n)", "O(n)", "Ignores the fact that the input is already sorted."),
        ("Linear insertion", "O(n)", "O(n)", "Three phases: before, overlap, after."),
    ],
    editorial=(
        "Because the input is sorted and disjoint, overlap is a single contiguous run. "
        "Skip the prefix that ends before new_interval starts. Fold the overlapping run into one interval. Append the untouched suffix. "
        "No full sort is required."
    ),
    companies=["Google", "Amazon", "Facebook", "LinkedIn"],
)
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    i = 0
    start, end = new_interval
    while i < len(intervals) and intervals[i][1] < start:
        out.append(intervals[i])
        i += 1
    while i < len(intervals) and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    out.extend(intervals[i:])
    return out


def _oracle_insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    return merge(intervals + [new_interval])


cases(
    "insert-interval",
    _oracle_insert,
    [
        ("overlap", {"intervals": [[1, 3], [6, 9]], "new_interval": [2, 5]}, True, "The new interval merges with [1, 3]."),
        ("middle", {"intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], "new_interval": [4, 8]}, True, "Several intervals collapse."),
        ("empty", {"intervals": [], "new_interval": [5, 7]}, False, None),
        ("front", {"intervals": [[3, 4], [6, 7]], "new_interval": [1, 2]}, False, None),
        ("cover", {"intervals": [[1, 5]], "new_interval": [0, 6]}, False, None),
    ],
)


@define(
    slug="non-overlapping-intervals",
    title="Non-overlapping Intervals",
    difficulty="medium",
    topics=["intervals", "greedy"],
    statement="Return the minimum number of intervals to remove so the rest do not overlap. Touching endpoints do not count as overlap.",
    constraints=["1 <= intervals.length <= 10^5", "-5 * 10^4 <= start < end <= 5 * 10^4"],
    signature="from typing import List\n\ndef erase_overlap_intervals(intervals: List[List[int]]) -> int:",
    function_name="erase_overlap_intervals",
    hints=[
        "Sorting by end time makes the greedy choice obvious: keep the interval that frees the timeline soonest.",
        "If the next interval starts before the last kept end, it overlaps and must be removed.",
        "Otherwise keep it and move the end forward.",
    ],
    approaches=[
        ("Sort by start and dynamic programming", "O(n^2)", "O(n)", "Longest non-overlapping subset, then removals are n minus that length."),
        ("Greedy by earliest end", "O(n log n)", "O(1)", "One pass after sorting by end."),
    ],
    editorial=(
        "The minimum deletions equal n minus the size of the largest compatible subset. "
        "Activity selection proves that sorting by finish time and taking every interval that starts at or after the last finish is optimal. "
        "Count the intervals you skip. Endpoints that merely touch are compatible, so the comparison is strict: start < last_end means overlap."
    ),
    companies=["Amazon", "Google", "Microsoft", "ByteDance"],
)
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    ordered = sorted(intervals, key=lambda item: item[1])
    removed = 0
    end = ordered[0][1]
    for start, finish in ordered[1:]:
        if start < end:
            removed += 1
        else:
            end = finish
    return removed


def _oracle_erase_overlap_intervals(intervals: list[list[int]]) -> int:
    ordered = sorted(intervals, key=lambda item: item[1])
    kept = 0
    end = None
    for start, finish in ordered:
        if end is None or start >= end:
            kept += 1
            end = finish
    return len(intervals) - kept


cases(
    "non-overlapping-intervals",
    _oracle_erase_overlap_intervals,
    [
        ("classic", {"intervals": [[1, 2], [2, 3], [3, 4], [1, 3]]}, True, "Remove [1, 3]. Touching intervals stay."),
        ("chain", {"intervals": [[1, 2], [1, 2], [1, 2]]}, True, "Keep one copy and remove two."),
        ("none", {"intervals": [[1, 2], [2, 3]]}, False, None),
        ("nested", {"intervals": [[1, 10], [2, 3], [3, 4]]}, False, None),
        ("single", {"intervals": [[1, 5]]}, False, None),
    ],
)


@define(
    slug="meeting-rooms",
    title="Meeting Rooms",
    difficulty="easy",
    topics=["intervals", "sorting"],
    statement="Given meeting intervals, return true when a person can attend every meeting. Meetings that touch at an endpoint do not conflict.",
    constraints=["0 <= intervals.length <= 10^4", "0 <= start <= end <= 10^6"],
    signature="from typing import List\n\ndef can_attend_meetings(intervals: List[List[int]]) -> bool:",
    function_name="can_attend_meetings",
    hints=[
        "Sort by start time.",
        "A conflict is a meeting that starts before the previous meeting ends.",
        "One linear check after the sort is enough.",
    ],
    approaches=[
        ("All pairs", "O(n^2)", "O(1)", "Test every pair for overlap."),
        ("Sort and adjacent check", "O(n log n)", "O(1)", "Only neighbors in start order can be the first conflict."),
    ],
    editorial=(
        "If any two meetings overlap, the one with the earlier start overlaps the next one after sorting. "
        "So it is enough to compare each meeting with its predecessor. A start equal to the previous end is allowed."
    ),
    companies=["Facebook", "Amazon", "Google", "Uber"],
)
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals)
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:
            return False
    return True


def _oracle_can_attend_meetings(intervals: list[list[int]]) -> bool:
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            a, b = intervals[i], intervals[j]
            if a[0] < b[1] and b[0] < a[1]:
                return False
    return True


cases(
    "meeting-rooms",
    _oracle_can_attend_meetings,
    [
        ("no", {"intervals": [[0, 30], [5, 10], [15, 20]]}, True, "The long meeting covers the other two."),
        ("yes", {"intervals": [[7, 10], [2, 4]]}, True, "The meetings are disjoint."),
        ("touch", {"intervals": [[1, 2], [2, 3]]}, False, None),
        ("empty", {"intervals": []}, False, None),
        ("one", {"intervals": [[1, 5]]}, False, None),
    ],
)


@define(
    slug="meeting-rooms-ii",
    title="Meeting Rooms II",
    difficulty="medium",
    topics=["intervals", "heaps"],
    statement="Return the minimum number of conference rooms required so that all the meetings can be scheduled. Touching endpoints can share a room.",
    constraints=["1 <= intervals.length <= 10^4", "0 <= start < end <= 10^6"],
    signature="from typing import List\n\ndef min_meeting_rooms(intervals: List[List[int]]) -> int:",
    function_name="min_meeting_rooms",
    hints=[
        "Sort starts and ends separately.",
        "A start before the earliest end needs a new room. A start at or after that end frees a room.",
        "The maximum number of rooms in use during the sweep is the answer.",
    ],
    approaches=[
        ("Min-heap of end times", "O(n log n)", "O(n)", "The heap size is the number of rooms currently busy."),
        ("Two-pointer sweep", "O(n log n)", "O(n)", "Sort starts and ends, then walk the starts."),
    ],
    editorial=(
        "Chronological order is the whole problem. Separate the start events from the end events. "
        "If the next start happens strictly before the next end, a new room opens. Otherwise a room frees first and is reused. "
        "The peak of the running count is the minimum number of rooms."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    starts = sorted(item[0] for item in intervals)
    ends = sorted(item[1] for item in intervals)
    rooms = best = end_i = 0
    for start in starts:
        if start < ends[end_i]:
            rooms += 1
            best = max(best, rooms)
        else:
            end_i += 1
    return best


def _oracle_min_meeting_rooms(intervals: list[list[int]]) -> int:
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort(key=lambda item: (item[0], item[1]))
    rooms = best = 0
    for _, delta in events:
        rooms += delta
        best = max(best, rooms)
    return best


cases(
    "meeting-rooms-ii",
    _oracle_min_meeting_rooms,
    [
        ("two", {"intervals": [[0, 30], [5, 10], [15, 20]]}, True, "The long meeting forces a second room."),
        ("one", {"intervals": [[7, 10], [2, 4]]}, True, "One room is reused."),
        ("touch", {"intervals": [[1, 2], [2, 3]]}, False, None),
        ("same", {"intervals": [[1, 5], [1, 5], [1, 5]]}, False, None),
        ("chain", {"intervals": [[1, 4], [2, 5], [6, 8]]}, False, None),
    ],
)


@define(
    slug="minimum-number-of-arrows-to-burst-balloons",
    title="Minimum Number of Arrows to Burst Balloons",
    difficulty="medium",
    topics=["intervals", "greedy"],
    statement=(
        "Balloons are horizontal intervals. An arrow shot at x bursts every balloon whose interval contains x. "
        "Return the minimum number of arrows required. Endpoints are inclusive."
    ),
    constraints=["1 <= points.length <= 10^5", "-2^31 <= start <= end <= 2^31 - 1"],
    signature="from typing import List\n\ndef find_min_arrow_shots(points: List[List[int]]) -> int:",
    function_name="find_min_arrow_shots",
    hints=[
        "Sort by end coordinate. The first balloon to finish must be burst by then.",
        "Shoot at its end. Every later balloon that starts at or before that x is burst for free.",
        "The next balloon that starts after x needs a new arrow. This is activity selection in disguise.",
    ],
    approaches=[
        ("Sort by start and merge overlaps", "O(n log n)", "O(n)", "The number of merged groups is not the answer when one arrow can cross a chain that does not share one common point."),
        ("Greedy earliest end", "O(n log n)", "O(1)", "Each arrow is placed at the current group's earliest end."),
    ],
    editorial=(
        "Sorting by finish time and shooting at that finish bursts the current balloon and every balloon that overlaps that point. "
        "A balloon that starts after the shot is the start of a new group. "
        "The number of groups is the number of arrows. Inclusive endpoints mean a balloon that starts exactly at the shot is burst."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def find_min_arrow_shots(points: list[list[int]]) -> int:
    ordered = sorted(points, key=lambda item: item[1])
    arrows = 1
    end = ordered[0][1]
    for start, finish in ordered[1:]:
        if start > end:
            arrows += 1
            end = finish
    return arrows


def _oracle_find_min_arrow_shots(points: list[list[int]]) -> int:
    ordered = sorted(points, key=lambda item: (item[1], item[0]))
    arrows = 0
    i = 0
    while i < len(ordered):
        arrows += 1
        shot = ordered[i][1]
        i += 1
        while i < len(ordered) and ordered[i][0] <= shot:
            i += 1
    return arrows


cases(
    "minimum-number-of-arrows-to-burst-balloons",
    _oracle_find_min_arrow_shots,
    [
        ("classic", {"points": [[10, 16], [2, 8], [1, 6], [7, 12]]}, True, "Two arrows are enough."),
        ("overlap-point", {"points": [[1, 2], [2, 3], [3, 4], [4, 5]]}, True, "Touching endpoints share an arrow, so two arrows burst four balloons."),
        ("one", {"points": [[1, 2]]}, False, None),
        ("same", {"points": [[1, 5], [2, 4], [3, 6]]}, False, None),
        ("disjoint", {"points": [[1, 2], [4, 5], [8, 9]]}, False, None),
    ],
)
