"""Monotonic stacks and expression evaluation."""

from emit import emit

MONO = r'''
## Why this matters

A stack remembers unfinished work in the order you must finish it. Parentheses, undo, depth-first search, and function calls are all stacks. The monotonic variant is the interview workhorse for "the next greater element" and its cousins: daily temperatures, stock spans, the largest rectangle in a histogram, and the sliding-window maximum when the window is a deque. The naive answer scans backward from every index and is quadratic. The stack keeps only the candidates that are still possible, and each index is pushed once and popped once. That is the aggregate argument from the amortization lesson, applied to a shape you can draw.

## Intuition

Imagine people standing in a line, each holding a height. Someone new arrives who is taller than the people at the back. Those shorter people will never be the "next taller person" for anyone still waiting, because the newcomer stands closer and is at least as tall. They can leave, and as they leave you can tell each of them that the newcomer is their answer. The people who remain are in decreasing order of height, closest at the top. That decreasing order is the monotonic invariant. A deque does the same job from both ends when a window also expires old indexes.

## Core concept in depth

A plain stack is last-in first-out. Push, pop, and peek are constant time if the stack is a dynamic array or a linked list of nodes. A queue is first-in first-out. A ring buffer or a deque gives constant-time operations at both ends. Implementing a queue with two stacks is the amortized exercise from the foundations module: push to the inbox, and pour into the outbox only when the outbox is empty. Each element moves at most once.

Valid parentheses uses a plain stack of opening characters. An opening character pushes. A closing character pops and must match. The stack must be empty at the end. A mismatch or a pop from empty is a failure. Min Stack keeps a second stack of the minimum at every height. On push, the new minimum is the smaller of the value and the current minimum. On pop, both stacks pop. Top and getMin are then peeks. The parallel stack is simpler than storing pairs, and it is the same information.

A next-greater-element stack stores indexes, not only values, because the answer is often a distance or a later index. Walk left to right. While the stack is not empty and the value at the top index is strictly less than the current value, pop it and record the current index as its next greater element. Then push the current index. Indexes still on the stack at the end have no next greater element. The invariant: values at the stacked indexes are strictly decreasing from bottom to top, and each is waiting for a greater element to its right. Popping a smaller top preserves the invariant. Daily temperatures is this algorithm with the distance `current - popped` as the stored answer. The circular next greater element runs the same loop on a conceptual double array, or it runs twice, and it only assigns an answer that is still unset so a later wrap does not overwrite a nearer neighbor.

Stock span is the same pops with a running width. Pop while the top price is less than or equal to today's price, and add that day's span to today's span. Push today's price together with its span. Equal prices must be popped for the span definition, which counts previous days that were less than or equal. Next-greater usually uses a strict comparison. Read the inequality from the statement. Getting it backwards is a one-character bug with a wrong example.

Largest rectangle in a histogram treats each bar as the shortest bar of some rectangle. The width is the distance between the nearest strictly shorter bar on the left and the nearest strictly shorter bar on the right. A monotonic increasing stack of indexes computes both boundaries. When a bar is shorter than the top, the top's right boundary is the current index, and its left boundary is the new top after the pop, or the start of the array if the stack empties. Sentinel bars of height 0 at both ends remove the edge cases. The area is height times width. The maximum over all popped bars is the answer. Each index is pushed and popped once, so the algorithm is linear after you accept the sentinels.

Remove k digits uses a stack that wants the smallest number in order. While the top is greater than the next digit and you still have deletions left, pop. Digits only leave if a smaller digit soon to the right can take their place, and the stack stays non-decreasing. Strip leading zeros at the end. If deletions remain, they come off the tail, which is the largest remaining place values. This is a monotonic stack whose answer is the stack itself, not a side array of "next greater."

The sliding-window maximum is a monotonic deque of indexes, decreasing in value. Pop the back while it is smaller than the new value. Pop the front while it has left the window. The front is the maximum. It was derived in the window lesson. Here the point is that the deque is a double-ended monotonic stack. The aggregate argument is identical.

## Diagram and dry run

```mermaid
flowchart TD
    A[Next index i] --> B{Stack top strictly smaller than the value at i?}
    B -->|Yes| C[Pop the top. Its next greater index is i]
    C --> B
    B -->|No| D[Push i. The stack stays decreasing]
```

Next greater element to the right, on 2, 1, 2, 4, 3. Answers are indexed values. Unfilled answers stay -1.

| i | Value | Stack of indexes after the step | Newly solved |
| --- | --- | --- | --- |
| 0 | 2 | 0 | none |
| 1 | 1 | 0, 1 | none. 1 is smaller, so 2 is still waiting |
| 2 | 2 | 0, 2 | index 1 solved by value 2. Index 0 is not strictly smaller than 2? Wait, 2 is not strictly less than 2, so index 0 stays |
| 3 | 4 | 3 | indexes 0 and 2 solved by 4 |
| 4 | 3 | 3, 4 | none |

Correct the third row carefully. Values 2, 1, 2. The stack after index 1 is 0 then 1, values 2 then 1. Index 2 holds 2, which is greater than the top value 1, so pop index 1. The new top value is 2, which is not strictly less than 2, so stop. Push index 2. Solved: index 1. Then index 3 holds 4, which pops both remaining indexes. The answers, as next greater values, are 4, 2, 4, and none, and none. Distances for daily temperatures would be 3, 1, 1, and zeros.

Largest rectangle on heights 2, 1, 5, 6, 2, 3 is the standard example whose best area is 10, the rectangle of height 5 and 6 extended only as far as the bars that stay at least 5. Walk it with sentinels when you practice. The area 10 comes from the bar of height 5, spanning the 5 and the 6, or equivalently from those two bars. Do the arithmetic on paper rather than memorizing 10.

## Runnable Python

The next-greater loop is the template. The recursive version is unnatural, because the stack is already an explicit recursion. A recursive depth-first search of a parenthesis string is included instead, so you see a stack as a call stack. The iterative matcher is the one to ship.

```python
def next_greater(nums: list[int]) -> list[int]:
    answer = [-1] * len(nums)
    stack: list[int] = []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            answer[stack.pop()] = value
        stack.append(i)
    return answer


def valid_parens(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
```

`next_greater` on 2, 1, 2, 4, 3 returns 4, 2, 4, -1, -1. `valid_parens` returns true on a string of three matched pairs and false on an opener followed by the wrong closer. The map from closing character to opening character is the whole matching rule. In speech, say "each closer must pop its own opener."

## Complexity and trade-offs

| Problem | Naive | Stack or deque | Extra space |
| --- | --- | --- | --- |
| Next greater element | Theta(n squared) | Theta(n), each index once | Theta(n) |
| Daily temperatures | Theta(n squared) | Theta(n) | Theta(n) |
| Stock span | Theta(n squared) | Theta(n) | Theta(n) |
| Largest rectangle | Theta(n squared) | Theta(n) | Theta(n) |
| Window maximum | Theta(n k) | Theta(n) amortized | Theta(k) |
| Valid parentheses | scans | Theta(n) | Theta(n) |
| Min stack operations | linear getMin if you scan | Theta(1) per call | Theta(n) |

A segment tree can also answer range-maximum queries inside a window in log time, which is worse than the deque by a log and more code. Use the deque. A heap does not delete an arbitrary expired index cheaply. Mention that dead end if you almost reach for one.

## Tricks, tips, and patterns

Store indexes when the answer is a distance or a later lookup. Choose the inequality from the statement: strictly greater, or greater-or-equal. Sentinels of a neutral height simplify the histogram. For digits, the stack is the answer and the monotonic direction is "increasing, so the number is small." Pop only while budget remains. For parentheses, the empty stack is a failure on a closer, and a non-empty stack at the end is a failure too. For the circular array, iterate twice and write an answer only if it is still empty. The second pass must not push indexes past the original length if that would duplicate work. Pushing only while the index is in the first copy, and only looking during both copies, is a clean variant.

## Common mistakes and edge cases

Using a non-strict comparison for next greater, so equal elements pop each other and the "next" is not greater. Using a strict comparison for stock span, so equal prices do not extend the span. Forgetting that the histogram width is right - left - 1 when both boundaries are exclusive. Off-by-one there is the entire bug. An empty histogram. A single bar. All bars equal, where the width is the whole array. A decreasing histogram, where every bar waits until the right sentinel. Leading zeros in remove-k-digits, including the case that every digit is removed and the answer is a single zero rather than an empty string. A min stack that forgets to push the previous minimum when the new value is larger. Parentheses with nothing but closers.

## Interview notes

Draw the decreasing stack and pop one example before you code. Say "each index is pushed once and popped once, so this is linear." For the histogram, state the exclusive boundaries and the width formula, then use sentinels. If you are unsure of the formula, compute one bar by hand from the nearest shorter neighbors and check the formula against that bar. For parentheses, test the empty string, a single pair, a mismatch, and an extra opener. Mention the two-stack queue only if the conversation is about implementing a queue. It is not the monotonic pattern.

## Practice problems

1. [Daily Temperatures](/practice/daily-temperatures) and [Next Greater Element I](/practice/next-greater-element-i).
2. [Next Greater Element II](/practice/next-greater-element-ii) — the circular version.
3. [Online Stock Span](/practice/online-stock-span).
4. [Largest Rectangle in Histogram](/practice/largest-rectangle-in-histogram).
5. [Sliding Window Maximum](/practice/sliding-window-maximum).
6. [Remove K Digits](/practice/remove-k-digits).
7. [Valid Parentheses](/practice/valid-parentheses) and [Min Stack](/practice/min-stack).

## Summary and cheat sheet

- A monotonic stack stores candidates that are still possible, in sorted order.
- Next greater: pop smaller tops, then push. Each index once. Linear.
- Distances and spans are arithmetic on the popped index. Match the inequality to the statement.
- Histogram: the bar is the shortest of a rectangle whose sides are the nearest shorter bars. Width is the gap between exclusive boundaries. Sentinels help.
- Remove k digits keeps an increasing stack and spends deletions on larger tops.
- A deque is a monotonic stack with expiration at the front.
- Parentheses and min stacks are ordinary stacks, not monotonic ones. Do not force the pattern.

## Further reading

- [Wikipedia — Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))
- [Wikipedia — Double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue)
- [CP-Algorithms, stack applications are spread across; the histogram problem is a standard linear stack scan](https://cp-algorithms.com/)
'''

EXPR = r'''
## Why this matters

Expression evaluation is the stack's original job. Compilers turn infix into postfix, then evaluate postfix with a value stack. Interview variants strip the compiler down: reverse Polish notation, a calculator with plus and minus and parentheses, a calculator with multiplication and division, and a decoder that repeats a bracketed substring. The bugs are precedence and the moment you flush a number. A recursive descent parser is the other legal implementation. You should be able to write the stack version and explain the recursive one as "the call stack holds the parenthesis frames."

## Intuition

Infix is how people write `3 + 4 * 2`. The multiplication happens before the addition even though it is written later. Postfix, or reverse Polish notation, writes `3 4 2 * +`. Operators come after their operands, so a left-to-right scan with a stack is enough: numbers push, and an operator pops two numbers, applies, and pushes the result. Parentheses in infix are a way to force order. A stack of operators, with a precedence rule, either applies an operator now or saves it until a higher-precedence neighbor is finished. That saving is the shunting yard.

## Core concept in depth

Reverse Polish notation. Split the tokens. If the token is a number, push it. If it is an operator, pop the right operand, then the left, apply the operator, and push the result. Subtraction and division are not commutative, so the pop order matters. At the end the stack holds one value. The algorithm is linear in the number of tokens and uses stack space proportional to the depth of the expression. It assumes the expression is valid, which interview prompts usually guarantee.

Basic calculator with plus, minus, and parentheses. Ignore spaces. Keep a running result, the number currently being parsed, and a sign that is about to apply to that number. A digit extends the number by ten times the old number plus the digit. An operator flushes `sign * number` into the result, clears the number, and stores the new sign. An opening parenthesis pushes the current result and the current sign, then resets the result and the sign, because the inside of the parentheses is a fresh expression. A closing parenthesis flushes the number, multiplies the inner result by the saved sign, and adds the saved outer result. After the string, flush the last number. Unary minus at the start, or after an opening parenthesis, is a flush of zero plus a negative sign, so the same code handles it if you treat the sign as pending rather than as a binary operator that demands two numbers already present.

Calculator II adds multiplication and division, and usually has no parentheses. One style keeps the last flushed term. Plus and minus push a signed number onto a stack of terms. Multiplication and division pop the last term, combine it with the new number, and push the combination, so precedence is applied immediately. The answer is the sum of the terms. Another style is full shunting yard: two stacks, or an output queue and an operator stack, with precedence of times and divide above plus and minus, and left associativity. Left associativity means an operator on the stack with greater or equal precedence is applied before the new operator is pushed. Equal precedence must be applied, not saved, or `8 / 4 / 2` becomes 4 instead of 1.

Shunting yard in full. Numbers go to the output. An operator pops operators of higher or equal precedence, then pushes. An opening parenthesis pushes. A closing parenthesis pops until the opening parenthesis, and discards the parenthesis. At the end, pop the remaining operators. Then evaluate the postfix. This is the algorithm to describe if the interviewer asks how a calculator really parses. The specialized loops above are what you code when the operator set is small.

Decode string reads `k[abc]` as the substring abc repeated k times. A stack of pairs, the string built so far and the repeat count, handles nesting. Digits accumulate into k. An opening bracket pushes the current string and the current k, then clears both. Characters append to the current string. A closing bracket pops the previous string and the count, and sets the current string to previous plus current repeated count times. Nested brackets work because the stack holds the outer frame while the inner frame runs. This is the same parenthesis frame as the calculator, with a string instead of an integer result.

Score of parentheses is a smaller cousin. A stack of scores starts with 0. An opening parenthesis pushes 0. A closing parenthesis pops the inner score. If it is 0, the pair was empty and worth 1. Otherwise the pair is worth twice the inner score. Add that value onto the new top, which sums adjacent groups. The final top is the score. The recursive reading is the specification: `()` is 1, concatenation adds, and a wrapper doubles.

Recursive descent is the recursive form of these parsers. A function `parse_expression` reads terms separated by plus and minus. A function `parse_term` reads factors separated by times and divide. A function `parse_factor` reads a number or a parenthesized expression, and a parenthesized expression calls `parse_expression`. The call stack is the parenthesis stack. This style extends more cleanly to a real language. The explicit stack is easier to debug in a 30-minute slot. Know which one you are writing.

## Diagram and dry run

```mermaid
flowchart TD
    A[Next character] --> B{Kind}
    B -->|Digit| C[Accumulate into the current number]
    B -->|Plus or minus| D[Flush the pending signed number. Store the new sign]
    B -->|Open paren| E[Push result and sign. Start a fresh result]
    B -->|Close paren| F[Flush, multiply by the saved sign, add the saved result]
    C --> A
    D --> A
    E --> A
    F --> A
```

Evaluate `1 + (4 - 2)`.

| Character | Number | Sign | Result | Stack | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | +1 | 0 | empty | building a number |
| + | 0 | +1 | 1 | empty | flushed +1 |
| ( | 0 | +1 | 0 | 1, then +1 | saved the outer frame |
| 4 | 4 | +1 | 0 | saved | building |
| - | 0 | -1 | 4 | saved | flushed +4 |
| 2 | 2 | -1 | 4 | saved | building |
| ) | 0 | -1 | 2 | empty | inner result 4 + (-1)*2 = 2, times saved sign +1, plus saved result 1, equals 3 |

The value is 3. The same expression in postfix is `1 4 2 - +`. The value stack goes 1, then 1 4, then 1 4 2, then 1 2, then 3.

## Runnable Python

The postfix evaluator is the shortest correct calculator. The recursive descent alongside it handles infix plus and minus and parentheses, which is the recursive form of the stack calculator. Both assume a valid expression. The descent uses an index in a list so the recursive calls can advance it.

```python
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    for token in tokens:
        if token not in {"+", "-", "*", "/"}:
            stack.append(int(token))
            continue
        right = stack.pop()
        left = stack.pop()
        if token == "+":
            stack.append(left + right)
        elif token == "-":
            stack.append(left - right)
        elif token == "*":
            stack.append(left * right)
        else:
            stack.append(int(left / right))
    return stack[-1]


def eval_infix(s: str) -> int:
    tokens = [ch for ch in s if ch != " "]
    i = 0

    def parse() -> int:
        nonlocal i
        result = 0
        sign = 1
        while i < len(tokens):
            ch = tokens[i]
            if ch.isdigit():
                number = 0
                while i < len(tokens) and tokens[i].isdigit():
                    number = number * 10 + int(tokens[i])
                    i += 1
                result += sign * number
                continue
            if ch == "+":
                sign = 1
            elif ch == "-":
                sign = -1
            elif ch == "(":
                i += 1
                result += sign * parse()
                sign = 1
                continue
            elif ch == ")":
                i += 1
                return result
            i += 1
        return result

    return parse()
```

`eval_rpn` on the tokens 1, 4, 2, -, + returns 3. Integer division toward zero matches the usual calculator-II contract. Python's floor division would make `-3 / 2` equal -2, so the conversion through `int(left / right)` is deliberate. `eval_infix("1+(4-2)")` returns 3. Extend `parse` with a term function if multiplication arrives.

## Complexity and trade-offs

| Parser | Time | Extra space | Operators it likes |
| --- | --- | --- | --- |
| Postfix stack | Theta(n) | Theta(n) | Any, once the input is postfix |
| Infix plus and minus with parentheses | Theta(n) | Theta(depth) | The specialized result-and-sign stack |
| Terms for times and divide | Theta(n) | Theta(n) terms, or Theta(depth) | Precedence without a full grammar |
| Shunting yard | Theta(n) | Theta(n) | Arbitrary precedence and associativity |
| Recursive descent | Theta(n) | Theta(depth) call stack | A grammar you can write as functions |

Shunting yard is more code and more general. The specialized calculator is less code and easier to get wrong at the flush points. Pick the specialized loop for plus and minus, and the term-stack for times and divide. Describe shunting yard if the operator set is not fixed. Recursive descent wins when the grammar grows nested structures that are not only parentheses, such as the decode-string brackets with a number in front.

## Tricks, tips, and patterns

Flush at operators, at closing parentheses, and at the end. Forgetting the final flush drops the last number. Parse multi-digit numbers in an inner loop, not one digit at a time as separate numbers. Pop right before left. Decide the division rounding before you code, and test a negative numerator. For decode-string, the stack frame is the previous text plus the repeat count, and the current text starts empty after an opening bracket. For score of parentheses, an empty inner frame is the unit score 1, not 0, and a non-empty frame doubles. Left associativity means equal precedence applies the stacked operator first.

## Common mistakes and edge cases

Popping left before right, so subtraction flips. Floor division on negatives. A final number that is never flushed. Treating a space as a token. Unary minus coded as binary minus with a missing left operand. `8/4/2` associated to the right. A decode count of 10 parsed as 1 and 0 because the digit loop stopped early. Nested decode strings that append to the outer string too soon. An empty parenthesis pair in the score problem counted as 0. Stack underflow on an invalid expression. If the prompt guarantees validity, you still guard pops in your head so a bug does not become an exception you cannot explain. The empty expression is 0 if it can occur. A single number is itself.

## Interview notes

Start from postfix if you need a warm-up, then add precedence. Say when a number is flushed. Dry-run `1+(4-2)` or `3+4*2` depending on the operator set, and write the stack column. Mention integer-division rounding. If parentheses nest deeply, say the stack height is the depth. Offer recursive descent as the same frames in the call stack. For decode-string, dry-run a nested example `3[a2[c]]` which becomes `accaccacc`. That one example catches a frame bug.

## Practice problems

1. [Evaluate Reverse Polish Notation](/practice/evaluate-reverse-polish-notation).
2. [Basic Calculator](/practice/basic-calculator) — plus, minus, parentheses.
3. [Basic Calculator II](/practice/basic-calculator-ii) — times and divide, no parentheses.
4. [Decode String](/practice/decode-string).
5. [Score of Parentheses](/practice/score-of-parentheses).
6. [Exclusive Time of Functions](/practice/exclusive-time-of-functions) — a stack of call frames, the same idea on a log.

## Summary and cheat sheet

- Postfix: numbers push, operators pop right then left, push the result.
- Infix plus and minus: pending sign, flush on the next operator, parenthesis frames on a stack.
- Times and divide: combine with the last term immediately, or use precedence in shunting yard.
- Equal precedence is left-associative: apply the stacked operator.
- Division of negatives truncates toward zero in the usual problem. Do not use floor division blindly.
- Decode string and parenthesis scores are the same frames with a different payload.
- Recursive descent stores those frames in the call stack.

## Further reading

- [Wikipedia — Reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
- [Wikipedia — Shunting yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)
- [Wikipedia — Recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser)
'''

emit(
    "05-stacks-queues",
    "01-monotonic-stacks.mdx",
    title="Stacks, Queues, and Monotonic Candidates",
    slug="monotonic-stacks",
    summary="Plain stacks, the decreasing-candidate invariant, histograms, and the aggregate linear bound.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["linked-list-patterns"],
    tags=["stacks", "monotonic-stack", "queues"],
    order=1,
    body=MONO,
)
emit(
    "05-stacks-queues",
    "02-expression-evaluation.mdx",
    title="Expression Evaluation",
    slug="expression-evaluation",
    summary="Postfix stacks, infix precedence, parentheses as frames, and recursive descent.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["monotonic-stacks"],
    tags=["stacks", "parsing", "expressions"],
    order=2,
    body=EXPR,
)
