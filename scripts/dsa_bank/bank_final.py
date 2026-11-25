"""Bits, math, heaps, greedy, and a few more classics."""

from __future__ import annotations

import heapq
from collections import Counter

from lib import cases, define


@define(
    slug="single-number",
    title="Single Number",
    difficulty="easy",
    topics=["bit-manipulation"],
    statement="Every element appears twice except one. Return the one that appears once. Use linear time and constant extra memory.",
    constraints=["1 <= nums.length <= 3 * 10^4", "Every element but one appears twice"],
    signature="from typing import List\n\ndef single_number(nums: List[int]) -> int:",
    function_name="single_number",
    hints=[
        "XOR is its own inverse: x XOR x is 0, and x XOR 0 is x.",
        "XOR is commutative, so pairs cancel regardless of order.",
        "Fold XOR across the array. The leftover bits are the single number.",
    ],
    approaches=[
        ("Hash set", "O(n)", "O(n)", "Add and remove. The last remaining value is the answer."),
        ("XOR fold", "O(n)", "O(1)", "Pairs cancel."),
    ],
    editorial=(
        "Start from 0 and XOR every value. Each duplicated number returns the accumulator to the state it had before that pair. "
        "The unique number is XOR-ed once and remains."
    ),
    companies=["Amazon", "Adobe", "Apple", "Bloomberg"],
)
def single_number(nums: list[int]) -> int:
    acc = 0
    for value in nums:
        acc ^= value
    return acc


def _oracle_single_number(nums: list[int]) -> int:
    counts = Counter(nums)
    return next(value for value, count in counts.items() if count == 1)


cases(
    "single-number",
    _oracle_single_number,
    [
        ("classic", {"nums": [2, 2, 1]}, True, "1 appears once."),
        ("middle", {"nums": [4, 1, 2, 1, 2]}, True, "4 appears once."),
        ("single", {"nums": [7]}, False, None),
        ("negative", {"nums": [-1, -1, 3]}, False, None),
        ("zero", {"nums": [0, 1, 0]}, False, None),
    ],
)


@define(
    slug="counting-bits",
    title="Counting Bits",
    difficulty="easy",
    topics=["bit-manipulation", "dynamic-programming"],
    statement="Return an array `ans` of length n + 1 where ans[i] is the number of 1-bits in the binary representation of i.",
    constraints=["0 <= n <= 10^5"],
    signature="from typing import List\n\ndef count_bits(n: int) -> List[int]:",
    function_name="count_bits",
    hints=[
        "ans[i] = ans[i >> 1] + (i & 1). The shift drops the last bit and the mask reads it.",
        "i & (i - 1) clears the lowest set bit, so ans[i] = ans[i & (i - 1)] + 1 for i > 0.",
        "Either recurrence fills the array in one pass.",
    ],
    approaches=[
        ("Built-in popcount per integer", "O(n log n)", "O(1)", "Count bits independently."),
        ("DP from the parent number", "O(n)", "O(1) extra", "Each integer reuses a smaller answer."),
    ],
    editorial=(
        "Right-shifting i produces a number whose popcount is already known, because it is smaller than i. "
        "Add one when i is odd. ans[0] is 0. The loop from 1 to n is therefore a linear DP."
    ),
    companies=["Amazon", "Google", "Apple", "Microsoft"],
)
def count_bits(n: int) -> list[int]:
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans


def _oracle_count_bits(n: int) -> list[int]:
    return [bin(i).count("1") for i in range(n + 1)]


cases(
    "counting-bits",
    _oracle_count_bits,
    [
        ("two", {"n": 2}, True, "[0, 1, 1]."),
        ("five", {"n": 5}, True, "Popcounts through 5."),
        ("zero", {"n": 0}, False, None),
        ("one", {"n": 1}, False, None),
        ("eight", {"n": 8}, False, None),
    ],
)


@define(
    slug="number-of-1-bits",
    title="Number of 1 Bits",
    difficulty="easy",
    topics=["bit-manipulation"],
    statement="Return the number of 1 bits in the binary representation of the non-negative integer `n`. This is the Hamming weight.",
    constraints=["0 <= n <= 2^31 - 1"],
    signature="def hamming_weight(n: int) -> int:",
    function_name="hamming_weight",
    hints=[
        "n & (n - 1) clears the lowest set bit.",
        "Repeat until n is 0 and count the operations.",
        "The loop runs once per set bit, not once per bit position.",
    ],
    approaches=[
        ("Shift and test", "O(word size)", "O(1)", "Test the low bit and shift."),
        ("Kernighan", "O(number of set bits)", "O(1)", "Clear the lowest set bit each iteration."),
    ],
    editorial=(
        "Subtracting one flips every bit up to and including the lowest 1. "
        "AND-ing with the original number clears that 1 and leaves the higher bits unchanged. "
        "Counting those clears is the popcount."
    ),
    companies=["Amazon", "Apple", "Microsoft", "Adobe"],
)
def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def _oracle_hamming_weight(n: int) -> int:
    return bin(n).count("1")


cases(
    "number-of-1-bits",
    _oracle_hamming_weight,
    [
        ("eleven", {"n": 11}, True, "1011 has three 1 bits."),
        ("zero", {"n": 0}, True, "No set bits."),
        ("one", {"n": 1}, False, None),
        ("power", {"n": 128}, False, None),
        ("dense", {"n": 127}, False, None),
    ],
)


@define(
    slug="power-of-two",
    title="Power of Two",
    difficulty="easy",
    topics=["bit-manipulation"],
    statement="Return true when `n` is a power of two. 1 is 2^0 and counts. Non-positive numbers do not.",
    constraints=["-2^31 <= n <= 2^31 - 1"],
    signature="def is_power_of_two(n: int) -> bool:",
    function_name="is_power_of_two",
    hints=[
        "A power of two has exactly one bit set.",
        "For n > 0, n & (n - 1) is 0 exactly then.",
        "n > 0 is required because zero and negatives are not powers of two.",
    ],
    approaches=[
        ("Loop dividing by 2", "O(log n)", "O(1)", "Reject odd numbers other than 1."),
        ("Bit test", "O(1)", "O(1)", "One set bit."),
    ],
    editorial=(
        "Powers of two are 1, 2, 4, 8, and so on. In binary each is a single 1 followed by zeros. "
        "Clearing the lowest set bit of such a number produces 0. Any other positive number still has a bit left."
    ),
    companies=["Amazon", "Google", "Adobe", "Apple"],
)
def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def _oracle_is_power_of_two(n: int) -> bool:
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


cases(
    "power-of-two",
    _oracle_is_power_of_two,
    [
        ("sixteen", {"n": 16}, True, "2^4."),
        ("three", {"n": 3}, True, "Not a power of two."),
        ("one", {"n": 1}, False, None),
        ("zero", {"n": 0}, False, None),
        ("negative", {"n": -16}, False, None),
    ],
)


@define(
    slug="reverse-bits",
    title="Reverse Bits",
    difficulty="easy",
    topics=["bit-manipulation"],
    statement="Reverse the 32 bits of the non-negative integer `n` and return the result as an integer. Bits beyond the low 32 are zero in the input.",
    constraints=["0 <= n < 2^32"],
    signature="def reverse_bits(n: int) -> int:",
    function_name="reverse_bits",
    hints=[
        "Build the answer by taking the low bit of n and appending it to the high side of the result.",
        "Do this exactly 32 times, even when n becomes zero, so leading zeros become trailing zeros of the reverse.",
        "result = (result << 1) | (n & 1), then n >>= 1.",
    ],
    approaches=[
        ("String reverse of a 32-bit format", "O(1)", "O(1)", "The word size is fixed."),
        ("Bit by bit", "O(1)", "O(1)", "32 shifts."),
    ],
    editorial=(
        "A 32-iteration loop treats the word width as part of the contract. "
        "Each iteration moves one input bit into the result's next low position after shifting the bits already collected. "
        "Stopping early would drop the reversed leading zeros."
    ),
    companies=["Amazon", "Apple", "Microsoft", "Adobe"],
)
def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def _oracle_reverse_bits(n: int) -> int:
    bits = f"{n:032b}"
    return int(bits[::-1], 2)


cases(
    "reverse-bits",
    _oracle_reverse_bits,
    [
        ("example", {"n": 43261596}, True, "The 32-bit reverse is 964176192."),
        ("zero", {"n": 0}, True, "Still zero."),
        ("one", {"n": 1}, False, None),
        ("high", {"n": 1 << 31}, False, None),
        ("all", {"n": (1 << 32) - 1}, False, None),
    ],
)


@define(
    slug="bitwise-and-of-numbers-range",
    title="Bitwise AND of Numbers Range",
    difficulty="medium",
    topics=["bit-manipulation"],
    statement="Return the bitwise AND of every integer in the inclusive range [left, right].",
    constraints=["0 <= left <= right <= 2^31 - 1"],
    signature="def range_bitwise_and(left: int, right: int) -> int:",
    function_name="range_bitwise_and",
    hints=[
        "A bit that flips anywhere inside the range becomes 0 in the AND.",
        "The common binary prefix of left and right is exactly the bits that stay constant.",
        "Shift both numbers right until they are equal, counting the shifts, then shift the common prefix back.",
    ],
    approaches=[
        ("Loop the range", "O(right - left)", "O(1)", "Too slow when the range is a billion wide."),
        ("Common prefix", "O(log right)", "O(1)", "Shift until left equals right."),
    ],
    editorial=(
        "While left and right differ, their low bits are not shared by the whole range, so clear them by shifting both right. "
        "When they meet, that value is the common prefix. Shift it left by the number of cleared bits. "
        "If left equals right at the start, the range is a single number and the answer is that number."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def range_bitwise_and(left: int, right: int) -> int:
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift


def _oracle_range_bitwise_and(left: int, right: int) -> int:
    acc = left
    for value in range(left + 1, right + 1):
        acc &= value
        if acc == 0:
            break
    return acc


cases(
    "bitwise-and-of-numbers-range",
    _oracle_range_bitwise_and,
    [
        ("classic", {"left": 5, "right": 7}, True, "5 & 6 & 7 = 4."),
        ("zero", {"left": 0, "right": 0}, True, "A single zero."),
        ("wide", {"left": 1, "right": 15}, False, None),
        ("equal", {"left": 9, "right": 9}, False, None),
        ("span", {"left": 12, "right": 15}, False, None),
    ],
)


@define(
    slug="count-primes",
    title="Count Primes",
    difficulty="medium",
    topics=["math", "sieve"],
    statement="Return the number of prime numbers strictly less than `n`.",
    constraints=["0 <= n <= 5 * 10^6"],
    signature="def count_primes(n: int) -> int:",
    function_name="count_primes",
    hints=[
        "Trial division of every integer is correct and too slow for large n.",
        "The sieve of Eratosthenes marks multiples of each prime.",
        "Start marking at p * p, and only consider odd primes after handling 2. The simple sieve that starts at 2 * p is enough to learn.",
    ],
    approaches=[
        ("Trial division", "O(n sqrt n)", "O(1)", "Test each candidate."),
        ("Sieve of Eratosthenes", "O(n log log n)", "O(n)", "A boolean array of composites."),
    ],
    editorial=(
        "Create a boolean array is_prime of length n, initially true, with 0 and 1 false. "
        "For each p from 2 while p * p < n, if p is still prime, mark p*p, p*p+p, ... as composite. "
        "The answer is the number of true entries. Multiples below p*p were marked by smaller primes."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def count_primes(n: int) -> int:
    if n < 2:
        return 0
    prime = [True] * n
    prime[0] = prime[1] = False
    p = 2
    while p * p < n:
        if prime[p]:
            for multiple in range(p * p, n, p):
                prime[multiple] = False
        p += 1
    return sum(prime)


def _oracle_count_primes(n: int) -> int:
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True

    return sum(is_prime(x) for x in range(n))


cases(
    "count-primes",
    _oracle_count_primes,
    [
        ("ten", {"n": 10}, True, "2, 3, 5, 7. Four primes."),
        ("zero", {"n": 0}, True, "No primes below 0."),
        ("two", {"n": 2}, False, None),
        ("one", {"n": 1}, False, None),
        ("twenty", {"n": 20}, False, None),
    ],
)


@define(
    slug="factorial-trailing-zeroes",
    title="Factorial Trailing Zeroes",
    difficulty="medium",
    topics=["math"],
    statement="Return the number of trailing zeroes in n!. Do not compute n!.",
    constraints=["0 <= n <= 10^4"],
    signature="def trailing_zeroes(n: int) -> int:",
    function_name="trailing_zeroes",
    hints=[
        "A trailing zero is a factor of 10, which is 2 * 5.",
        "Factorials contain more twos than fives, so the number of fives is the answer.",
        "Count floor(n/5) + floor(n/25) + floor(n/125) + ... because multiples of 25 contribute extra fives.",
    ],
    approaches=[
        ("Compute n!", "O(n) big integers", "O(n)", "Possible in Python and the wrong lesson."),
        ("Count factors of 5", "O(log n)", "O(1)", "The closed counting argument."),
    ],
    editorial=(
        "Every pair of a factor 2 and a factor 5 makes a trailing zero, and the fives are rarer. "
        "floor(n/5) counts multiples of 5, but 25 contributes two fives and was only counted once, so add floor(n/25), then floor(n/125), and so on. "
        "The loop divides n by 5 until it becomes zero."
    ),
    companies=["Amazon", "Bloomberg", "Microsoft", "Adobe"],
)
def trailing_zeroes(n: int) -> int:
    zeros = 0
    while n:
        n //= 5
        zeros += n
    return zeros


def _oracle_trailing_zeroes(n: int) -> int:
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    zeros = 0
    while fact and fact % 10 == 0:
        fact //= 10
        zeros += 1
    return zeros


cases(
    "factorial-trailing-zeroes",
    _oracle_trailing_zeroes,
    [
        ("three", {"n": 3}, True, "6 has no trailing zero."),
        ("five", {"n": 5}, True, "120 has one trailing zero."),
        ("zero", {"n": 0}, False, None),
        ("twenty-five", {"n": 25}, False, None),
        ("ten", {"n": 10}, False, None),
    ],
)


@define(
    slug="reverse-integer",
    title="Reverse Integer",
    difficulty="medium",
    topics=["math"],
    statement="Reverse the digits of a 32-bit signed integer. If the reversed value overflows the signed 32-bit range, return 0. The sign stays in front.",
    constraints=["-2^31 <= x <= 2^31 - 1"],
    signature="def reverse_integer(x: int) -> int:",
    function_name="reverse_integer",
    hints=[
        "Pop digits with modulo 10 and build the reverse by multiplying by 10.",
        "Python integers do not overflow. Compare the result with [-2^31, 2^31 - 1] at the end.",
        "Negative inputs: either reverse the absolute value and restore the sign, or let Python's modulo behavior be handled explicitly so the digit math stays non-negative.",
    ],
    approaches=[
        ("String reverse", "O(digits)", "O(digits)", "Strip the sign, reverse, parse, and range-check."),
        ("Arithmetic", "O(digits)", "O(1)", "No string allocation."),
    ],
    editorial=(
        "Take the sign, reverse the absolute value by repeated divmod, and reapply the sign. "
        "If the result is outside the signed 32-bit range, return 0. "
        "The problem is about overflow discipline more than about digits."
    ),
    companies=["Amazon", "Apple", "Bloomberg", "Adobe"],
)
def reverse_integer(x: int) -> int:
    sign = -1 if x < 0 else 1
    value = abs(x)
    rev = 0
    while value:
        value, digit = divmod(value, 10)
        rev = rev * 10 + digit
    rev *= sign
    if rev < -(2**31) or rev > 2**31 - 1:
        return 0
    return rev


def _oracle_reverse_integer(x: int) -> int:
    sign = "-" if x < 0 else ""
    digits = str(abs(x))[::-1].lstrip("0") or "0"
    rev = int(sign + digits)
    if rev < -(2**31) or rev > 2**31 - 1:
        return 0
    return rev


cases(
    "reverse-integer",
    _oracle_reverse_integer,
    [
        ("positive", {"x": 123}, True, "321."),
        ("negative", {"x": -123}, True, "-321."),
        ("trailing-zero", {"x": 120}, False, None),
        ("zero", {"x": 0}, False, None),
        ("overflow", {"x": 1534236469}, False, None),
    ],
)


@define(
    slug="palindrome-number",
    title="Palindrome Number",
    difficulty="easy",
    topics=["math"],
    statement="Return true when the integer `x` reads the same forward and backward. Negative numbers are not palindromes.",
    constraints=["-2^31 <= x <= 2^31 - 1"],
    signature="def is_palindrome_number(x: int) -> bool:",
    function_name="is_palindrome_number",
    hints=[
        "A negative number has a sign and is not a palindrome.",
        "Reverse the digits and compare. Overflow does not matter if you compare the full reverse.",
        "You can reverse only half the digits and compare the two halves to avoid building a number larger than the input.",
    ],
    approaches=[
        ("String compare", "O(digits)", "O(digits)", "Compare the decimal representation with its reverse."),
        ("Half reverse", "O(digits)", "O(1)", "Stop when the reversed half catches the remaining half."),
    ],
    editorial=(
        "Reject negatives. Reverse the decimal digits of the absolute value and compare. "
        "The half-reverse version stops when the reversed suffix has as many digits as the remaining prefix, and handles an odd middle digit by dividing the reverse by 10."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def is_palindrome_number(x: int) -> bool:
    if x < 0:
        return False
    original = x
    rev = 0
    while x:
        x, digit = divmod(x, 10)
        rev = rev * 10 + digit
    return rev == original


def _oracle_is_palindrome_number(x: int) -> bool:
    text = str(x)
    return text == text[::-1]


cases(
    "palindrome-number",
    _oracle_is_palindrome_number,
    [
        ("yes", {"x": 121}, True, "121 reversed is 121."),
        ("negative", {"x": -121}, True, "The sign breaks the palindrome."),
        ("ten", {"x": 10}, False, None),
        ("zero", {"x": 0}, False, None),
        ("odd", {"x": 12321}, False, None),
    ],
)


@define(
    slug="plus-one",
    title="Plus One",
    difficulty="easy",
    topics=["arrays", "math"],
    statement="`digits` represents a non-negative integer, most significant digit first, with no leading zeros except the number 0. Return the digits of that integer plus one.",
    constraints=["1 <= digits.length <= 100", "0 <= digits[i] <= 9"],
    signature="from typing import List\n\ndef plus_one(digits: List[int]) -> List[int]:",
    function_name="plus_one",
    hints=[
        "Add one to the last digit. If it is less than 10, you are done.",
        "A 9 becomes 0 and the carry moves left.",
        "If the carry survives the first digit, the result is 1 followed by zeros.",
    ],
    approaches=[
        ("Convert to an integer", "O(n)", "O(n)", "Easy in Python, and it hides the carry."),
        ("In-place carry", "O(n)", "O(1) extra", "One walk from the end."),
    ],
    editorial=(
        "Walk from the least significant digit. A digit below 9 increments and returns. "
        "A 9 becomes 0 and the walk continues. "
        "If every digit was 9, insert a leading 1."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def plus_one(digits: list[int]) -> list[int]:
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits


def _oracle_plus_one(digits: list[int]) -> list[int]:
    value = int("".join(map(str, digits))) + 1
    return [int(ch) for ch in str(value)]


cases(
    "plus-one",
    _oracle_plus_one,
    [
        ("simple", {"digits": [1, 2, 3]}, True, "124."),
        ("nines", {"digits": [9, 9]}, True, "100."),
        ("zero", {"digits": [0]}, False, None),
        ("nine", {"digits": [9]}, False, None),
        ("mid", {"digits": [1, 9, 9]}, False, None),
    ],
)


@define(
    slug="add-binary",
    title="Add Binary",
    difficulty="easy",
    topics=["math", "bit-manipulation", "strings"],
    statement="Given two binary strings `a` and `b`, return their sum as a binary string. Neither input has leading zeros except the number 0.",
    constraints=["1 <= a.length, b.length <= 10^4", "a and b consist of '0' and '1'"],
    signature="def add_binary(a: str, b: str) -> str:",
    function_name="add_binary",
    hints=[
        "Add from the right, the same way you add decimals, with a carry of 0 or 1.",
        "The digit is (bit_a + bit_b + carry) mod 2. The next carry is the sum divided by 2.",
        "Continue while either string or the carry remains. A final carry becomes a leading 1.",
    ],
    approaches=[
        ("Convert to int", "O(n)", "O(n)", "Python accepts arbitrary binary integers."),
        ("Digit walk", "O(n)", "O(1) extra", "The interview version that does not hide the carry."),
    ],
    editorial=(
        "Align the strings at the right. While either index is in range or the carry is 1, add the available bits and the carry. "
        "Prepend the new bit so the string is built most-significant digit last, or append and reverse at the end. "
        "The result has no leading zero unless the sum is zero."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def add_binary(a: str, b: str) -> str:
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out: list[str] = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += a[i] == "1"
            i -= 1
        if j >= 0:
            total += b[j] == "1"
            j -= 1
        out.append(str(total % 2))
        carry = total // 2
    return "".join(reversed(out))


def _oracle_add_binary(a: str, b: str) -> str:
    return bin(int(a, 2) + int(b, 2))[2:]


cases(
    "add-binary",
    _oracle_add_binary,
    [
        ("classic", {"a": "11", "b": "1"}, True, "3 + 1 = 4, which is 100."),
        ("zero", {"a": "0", "b": "0"}, True, "0."),
        ("carry", {"a": "111", "b": "1"}, False, None),
        ("uneven", {"a": "1010", "b": "1011"}, False, None),
        ("one", {"a": "1", "b": "0"}, False, None),
    ],
)


@define(
    slug="kth-largest-element-in-an-array",
    title="Kth Largest Element in an Array",
    difficulty="medium",
    topics=["heaps", "quickselect", "sorting"],
    statement="Return the kth largest element in `nums`. It is the kth element in sorted order, not the kth distinct element.",
    constraints=["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef find_kth_largest(nums: List[int], k: int) -> int:",
    function_name="find_kth_largest",
    hints=[
        "Sorting and indexing at n - k is correct and costs n log n.",
        "A min-heap of size k keeps the k largest elements. The root is the kth largest.",
        "Quickselect finds the element at index n - k in expected linear time by partitioning like quicksort and recurring into one side.",
    ],
    approaches=[
        ("Sort", "O(n log n)", "O(n)", "Return the element at index n - k after sorting ascending."),
        ("Heap of size k", "O(n log k)", "O(k)", "Push every element and pop when the heap exceeds k."),
        ("Quickselect", "O(n) average", "O(1)", "Partition until the pivot lands on n - k."),
    ],
    editorial=(
        "The heap solution is the one to reach for when k is small and the stream might be online. "
        "Maintain a min-heap. After processing the array its size is k and its smallest element is the kth largest in the whole array. "
        "Quickselect is faster on average but has a quadratic worst case unless the pivot is chosen carefully."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def find_kth_largest(nums: list[int], k: int) -> int:
    heap: list[int] = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def _oracle_find_kth_largest(nums: list[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]


cases(
    "kth-largest-element-in-an-array",
    _oracle_find_kth_largest,
    [
        ("classic", {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, True, "The second largest is 5."),
        ("dups", {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}, True, "Duplicates count separately. The 4th largest is 4."),
        ("one", {"nums": [1], "k": 1}, False, None),
        ("last", {"nums": [7, 1, 2], "k": 3}, False, None),
        ("neg", {"nums": [-1, -2, 0], "k": 1}, False, None),
    ],
)


@define(
    slug="last-stone-weight",
    title="Last Stone Weight",
    difficulty="easy",
    topics=["heaps"],
    statement=(
        "You smash the two heaviest stones. If they differ, the difference is a new stone. If they are equal, both disappear. "
        "Return the weight of the last stone, or 0 if none remain."
    ),
    constraints=["1 <= stones.length <= 30", "1 <= stones[i] <= 1000"],
    signature="from typing import List\n\ndef last_stone_weight(stones: List[int]) -> int:",
    function_name="last_stone_weight",
    hints=[
        "A max-heap gives the two heaviest stones in logarithmic time.",
        "Python's heapq is a min-heap. Store negative weights.",
        "Push the positive difference back when the stones differ.",
    ],
    approaches=[
        ("Sort every smash", "O(n^2 log n)", "O(1)", "Fine at n = 30."),
        ("Max-heap", "O(n log n)", "O(n)", "Each stone is pushed a small number of times."),
    ],
    editorial=(
        "Negate the weights and heapify. While at least two stones remain, pop two, and if they differ push the negation of the difference. "
        "The last remaining negated weight, or zero, is the answer."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def last_stone_weight(stones: list[int]) -> int:
    heap = [-stone for stone in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0


def _oracle_last_stone_weight(stones: list[int]) -> int:
    stones = sorted(stones)
    while len(stones) > 1:
        first = stones.pop()
        second = stones.pop()
        if first != second:
            diff = first - second
            lo, hi = 0, len(stones)
            while lo < hi:
                mid = (lo + hi) // 2
                if stones[mid] < diff:
                    lo = mid + 1
                else:
                    hi = mid
            stones.insert(lo, diff)
    return stones[0] if stones else 0


cases(
    "last-stone-weight",
    _oracle_last_stone_weight,
    [
        ("classic", {"stones": [2, 7, 4, 1, 8, 1]}, True, "The last stone weighs 1."),
        ("equal", {"stones": [2, 2]}, True, "Both stones disappear."),
        ("one", {"stones": [5]}, False, None),
        ("three", {"stones": [3, 7, 2]}, False, None),
        ("chain", {"stones": [1, 3, 5]}, False, None),
    ],
)


@define(
    slug="k-closest-points-to-origin",
    title="K Closest Points to Origin",
    difficulty="medium",
    topics=["heaps", "sorting"],
    statement="Return the `k` points closest to the origin, measured by Euclidean distance. Sort the result by distance, then by x, then by y. Distance ties are broken by that sort.",
    constraints=["1 <= k <= points.length <= 10^4", "-10^4 <= x, y <= 10^4"],
    signature="from typing import List\n\ndef k_closest(points: List[List[int]], k: int) -> List[List[int]]:",
    function_name="k_closest",
    hints=[
        "Comparing squared distances avoids square roots and preserves order.",
        "A max-heap of size k keeps the closest points. The heap key is the squared distance.",
        "Sorting all points by squared distance is the simple O(n log n) answer.",
    ],
    approaches=[
        ("Sort", "O(n log n)", "O(n)", "Take the first k after sorting by distance."),
        ("Heap of size k", "O(n log k)", "O(k)", "A max-heap evicts the farthest of the current k."),
    ],
    editorial=(
        "Squared distance x*x + y*y is enough because the square function is increasing on non-negative numbers. "
        "Sort by that key and return the first k points, with a deterministic tie break. "
        "Quickselect on the distance would be expected linear and is the follow-up."
    ),
    companies=["Amazon", "Facebook", "Uber", "Adobe"],
)
def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    ranked = sorted(points, key=lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1]))
    return ranked[:k]


def _oracle_k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    return sorted(points, key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))[:k]


cases(
    "k-closest-points-to-origin",
    _oracle_k_closest,
    [
        ("classic", {"points": [[1, 3], [-2, 2]], "k": 1}, True, "[-2, 2] is closer."),
        ("two", {"points": [[3, 3], [5, -1], [-2, 4]], "k": 2}, True, "The two closest points."),
        ("all", {"points": [[0, 1], [1, 0]], "k": 2}, False, None),
        ("tie", {"points": [[1, 1], [-1, 1], [1, -1]], "k": 2}, False, None),
        ("origin", {"points": [[0, 0], [1, 1]], "k": 1}, False, None),
    ],
)


@define(
    slug="task-scheduler",
    title="Task Scheduler",
    difficulty="medium",
    topics=["greedy", "heaps"],
    statement=(
        "Tasks are uppercase letters. The same task must be separated by at least `n` intervals. "
        "An interval is one task or one idle. Return the minimum intervals required to finish every task. Order of different tasks is free."
    ),
    constraints=["1 <= tasks.length <= 10^4", "0 <= n <= 100"],
    signature="from typing import List\n\ndef least_interval(tasks: List[str], n: int) -> int:",
    function_name="least_interval",
    hints=[
        "The most frequent task determines the number of gaps.",
        "If the max frequency is f and m tasks share that frequency, the frame is (f - 1) * (n + 1) + m.",
        "If there are enough other tasks to fill the gaps, the answer is just the number of tasks. Take the max of the frame and len(tasks).",
    ],
    approaches=[
        ("Simulate with a heap and a cooldown queue", "O(time * alphabet)", "O(alphabet)", "The literal schedule."),
        ("Frequency formula", "O(n)", "O(1)", "The frame argument above. Here n is the cooldown, and the scan is linear in the task list."),
    ],
    editorial=(
        "Place the most frequent tasks first, leaving n idle slots between copies. "
        "Other tasks fill those slots. If several tasks share the maximum frequency, they occupy the last column of the frame together. "
        "Extra tasks beyond the frame just lengthen the schedule to the task count, because cooldown is already satisfied."
    ),
    companies=["Amazon", "Facebook", "Google", "Microsoft"],
)
def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    most = max(counts.values())
    tied = sum(count == most for count in counts.values())
    return max(len(tasks), (most - 1) * (n + 1) + tied)


def _oracle_least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    time = 0
    while counts:
        used = []
        for task, _ in counts.most_common(n + 1):
            used.append(task)
        for task in used:
            counts[task] -= 1
            if counts[task] == 0:
                del counts[task]
        time += n + 1 if counts else len(used)
    return time


cases(
    "task-scheduler",
    _oracle_least_interval,
    [
        ("classic", {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 2}, True, "The schedule length is 8."),
        ("no-idle", {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 0}, True, "No cooldown, so the length is the task count."),
        ("one", {"tasks": ["A"], "n": 2}, False, None),
        ("idle", {"tasks": ["A", "A", "A"], "n": 2}, False, None),
        ("mixed", {"tasks": ["A", "A", "B", "C"], "n": 1}, False, None),
    ],
)


@define(
    slug="ugly-number-ii",
    title="Ugly Number II",
    difficulty="medium",
    topics=["heaps", "dynamic-programming", "math"],
    statement="An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Return the nth ugly number. 1 is the first.",
    constraints=["1 <= n <= 1690"],
    signature="def nth_ugly_number(n: int) -> int:",
    function_name="nth_ugly_number",
    hints=[
        "Every ugly number except 1 is an earlier ugly number multiplied by 2, 3, or 5.",
        "Three pointers remember the next index to multiply by each factor.",
        "Take the minimum of the three candidates, append it once, and advance every pointer that produced it so duplicates are skipped.",
    ],
    approaches=[
        ("Min-heap with a set", "O(n log n)", "O(n)", "Push 2x, 3x, and 5x and skip values already seen."),
        ("Three pointers", "O(n)", "O(n)", "The DP formulation."),
    ],
    editorial=(
        "ugly[0] = 1. Maintain i2, i3, and i5. "
        "The next ugly number is the min of ugly[i2]*2, ugly[i3]*3, and ugly[i5]*5. "
        "Advance each pointer whose product equals that minimum. Advancing all matches is what collapses 6 = 2*3 = 3*2 into one entry."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def nth_ugly_number(n: int) -> int:
    ugly = [1]
    i2 = i3 = i5 = 0
    while len(ugly) < n:
        nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)
        ugly.append(nxt)
        if nxt == ugly[i2] * 2:
            i2 += 1
        if nxt == ugly[i3] * 3:
            i3 += 1
        if nxt == ugly[i5] * 5:
            i5 += 1
    return ugly[-1]


def _oracle_nth_ugly_number(n: int) -> int:
    heap = [1]
    seen = {1}
    value = 1
    for _ in range(n):
        value = heapq.heappop(heap)
        for factor in (2, 3, 5):
            nxt = value * factor
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, nxt)
    return value


cases(
    "ugly-number-ii",
    _oracle_nth_ugly_number,
    [
        ("ten", {"n": 10}, True, "The 10th ugly number is 12."),
        ("one", {"n": 1}, True, "1 is ugly."),
        ("two", {"n": 2}, False, None),
        ("seven", {"n": 7}, False, None),
        ("fifteen", {"n": 15}, False, None),
    ],
)


@define(
    slug="candy",
    title="Candy",
    difficulty="hard",
    topics=["greedy"],
    statement=(
        "Children stand in a line with ratings. Each child gets at least one candy. "
        "A child with a strictly higher rating than a neighbor must get more candies than that neighbor. Return the minimum total candies."
    ),
    constraints=["1 <= ratings.length <= 2 * 10^4", "0 <= ratings[i] <= 2 * 10^4"],
    signature="from typing import List\n\ndef candy(ratings: List[int]) -> int:",
    function_name="candy",
    hints=[
        "One pass left to right enforces the left neighbor. One pass right to left enforces the right neighbor.",
        "Initialize every child to 1.",
        "When a child is higher than the neighbor you are comparing, set their candies to at least that neighbor's candies plus one. Use max so the other pass is not undone.",
    ],
    approaches=[
        ("Search the assignment", "exponential", "O(n)", "Not viable."),
        ("Two passes", "O(n)", "O(n)", "Left constraints, then right constraints."),
    ],
    editorial=(
        "The left-to-right pass makes every ascending pair legal from the left. "
        "The right-to-left pass does the same for descending pairs and keeps the larger requirement. "
        "The sum is minimal because each child receives exactly the candies forced by the longer of the two chains."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


def _oracle_candy(ratings: list[int]) -> int:
    n = len(ratings)
    left = [1] * n
    right = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            left[i] = left[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            right[i] = right[i + 1] + 1
    return sum(max(a, b) for a, b in zip(left, right))


cases(
    "candy",
    _oracle_candy,
    [
        ("classic", {"ratings": [1, 0, 2]}, True, "The distribution 2, 1, 2 sums to 5."),
        ("peak", {"ratings": [1, 2, 2]}, True, "Equal neighbors can both receive 1. The total is 4."),
        ("one", {"ratings": [5]}, False, None),
        ("down", {"ratings": [3, 2, 1]}, False, None),
        ("valley", {"ratings": [1, 3, 2, 2, 1]}, False, None),
    ],
)


@define(
    slug="lemonade-change",
    title="Lemonade Change",
    difficulty="easy",
    topics=["greedy"],
    statement=(
        "Lemonade costs 5. Customers pay with bills of 5, 10, or 20, in the given order. "
        "You start with no cash. Return true when you can give the correct change to every customer."
    ),
    constraints=["1 <= bills.length <= 10^5", "bills[i] is 5, 10, or 20"],
    signature="from typing import List\n\ndef lemonade_change(bills: List[int]) -> bool:",
    function_name="lemonade_change",
    hints=[
        "A 5 needs no change and becomes a bill you can use later.",
        "A 10 needs one 5.",
        "A 20 prefers a 10 plus a 5, because a 10 is less useful later than three 5s. If you have no 10, use three 5s.",
    ],
    approaches=[
        ("Simulate every bill combination", "exponential", "O(n)", "Unnecessary. The greedy choice is forced."),
        ("Count fives and tens", "O(n)", "O(1)", "Twenties never help as change."),
    ],
    editorial=(
        "Only 5s and 10s are useful change. "
        "Spend a 10 before three 5s on a 20, because a later 10-bill customer can only be served by a 5. "
        "If a required bill is missing, return false immediately."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def lemonade_change(bills: list[int]) -> bool:
    five = ten = 0
    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if five == 0:
                return False
            five -= 1
            ten += 1
        else:
            if ten and five:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True


def _oracle_lemonade_change(bills: list[int]) -> bool:
    wallet = Counter()
    for bill in bills:
        wallet[bill] += 1
        change = bill - 5
        for coin in (10, 5):
            while change >= coin and wallet[coin]:
                wallet[coin] -= 1
                change -= coin
        if change:
            return False
    return True


cases(
    "lemonade-change",
    _oracle_lemonade_change,
    [
        ("yes", {"bills": [5, 5, 5, 10, 20]}, True, "The 20 is paid with a 10 and a 5."),
        ("no", {"bills": [5, 5, 10, 10, 20]}, True, "The last customer cannot be given change."),
        ("only-fives", {"bills": [5, 5, 5]}, False, None),
        ("twenty-first", {"bills": [20]}, False, None),
        ("tens", {"bills": [5, 10, 5, 10]}, False, None),
    ],
)


@define(
    slug="assign-cookies",
    title="Assign Cookies",
    difficulty="easy",
    topics=["greedy", "two-pointers"],
    statement=(
        "`g[i]` is the minimum cookie size child i accepts. `s[j]` is the size of cookie j. "
        "Each child gets at most one cookie. Return the maximum number of content children."
    ),
    constraints=["1 <= g.length, s.length <= 3 * 10^4", "1 <= g[i], s[j] <= 2^31 - 1"],
    signature="from typing import List\n\ndef find_content_children(g: List[int], s: List[int]) -> int:",
    function_name="find_content_children",
    hints=[
        "Sort both arrays.",
        "Give the smallest cookie that satisfies the smallest remaining child.",
        "If the cookie is too small, discard it. If it fits, move to the next child.",
    ],
    approaches=[
        ("Try every assignment", "exponential", "O(n)", "Not needed."),
        ("Two pointers after sorting", "O(n log n)", "O(1)", "The greedy match."),
    ],
    editorial=(
        "Sorting both sides makes the greedy choice local. "
        "A cookie that cannot satisfy the smallest child cannot satisfy any later child, so it is discarded. "
        "A cookie that can satisfy the child is assigned immediately, because saving it cannot help a smaller child and a larger child can still use a larger cookie."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def find_content_children(g: list[int], s: list[int]) -> int:
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child


def _oracle_find_content_children(g: list[int], s: list[int]) -> int:
    children = sorted(g)
    cookies = sorted(s)
    i = j = 0
    while i < len(children) and j < len(cookies):
        if cookies[j] >= children[i]:
            i += 1
        j += 1
    return i


cases(
    "assign-cookies",
    _oracle_find_content_children,
    [
        ("classic", {"g": [1, 2, 3], "s": [1, 1]}, True, "One child is content."),
        ("two", {"g": [1, 2], "s": [1, 2, 3]}, True, "Both children are content."),
        ("none", {"g": [5], "s": [1]}, False, None),
        ("empty-cookies", {"g": [1], "s": []}, False, None),
        ("exact", {"g": [2, 2], "s": [2, 2]}, False, None),
    ],
)


@define(
    slug="boats-to-save-people",
    title="Boats to Save People",
    difficulty="medium",
    topics=["greedy", "two-pointers"],
    statement=(
        "People have weights. Each boat carries at most two people and at most `limit` total weight. "
        "Every person weighs at most limit. Return the minimum number of boats."
    ),
    constraints=["1 <= people.length <= 5 * 10^4", "1 <= people[i] <= limit <= 3 * 10^4"],
    signature="from typing import List\n\ndef num_rescue_boats(people: List[int], limit: int) -> int:",
    function_name="num_rescue_boats",
    hints=[
        "Sort the people.",
        "The heaviest person must take a boat. Pair them with the lightest person if the sum fits.",
        "Otherwise the heaviest person goes alone. Each decision uses one boat.",
    ],
    approaches=[
        ("Search pairings", "exponential", "O(n)", "Unnecessary."),
        ("Two pointers", "O(n log n)", "O(1)", "Sort, then pair from the ends."),
    ],
    editorial=(
        "After sorting, the heaviest remaining person is the constraint. "
        "If the lightest person can join them, do it, because that light person cannot help any heavier remaining person more than they help this one. "
        "If not, the heavy person is alone. Move the pointers and count a boat either way."
    ),
    companies=["Amazon", "Google", "Uber", "Adobe"],
)
def num_rescue_boats(people: list[int], limit: int) -> int:
    people.sort()
    left, right = 0, len(people) - 1
    boats = 0
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1
        right -= 1
        boats += 1
    return boats


def _oracle_num_rescue_boats(people: list[int], limit: int) -> int:
    ordered = sorted(people)
    i, j = 0, len(ordered) - 1
    boats = 0
    while i <= j:
        if ordered[i] + ordered[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return boats


cases(
    "boats-to-save-people",
    _oracle_num_rescue_boats,
    [
        ("classic", {"people": [1, 2], "limit": 3}, True, "One boat carries both."),
        ("two", {"people": [3, 2, 2, 1], "limit": 3}, True, "Three boats."),
        ("alone", {"people": [3, 5, 3, 4], "limit": 5}, False, None),
        ("one", {"people": [2], "limit": 3}, False, None),
        ("pairs", {"people": [1, 1, 1, 1], "limit": 2}, False, None),
    ],
)


@define(
    slug="partition-labels",
    title="Partition Labels",
    difficulty="medium",
    topics=["greedy", "strings", "hashing"],
    statement=(
        "Partition `s` into as many parts as possible so each letter appears in at most one part. "
        "Return a list of the part sizes, in order."
    ),
    constraints=["1 <= s.length <= 500", "s consists of lowercase English letters"],
    signature="from typing import List\n\ndef partition_labels(s: str) -> List[int]:",
    function_name="partition_labels",
    hints=[
        "Record the last index of every character.",
        "Extend the current part's end to the last index of every character you see inside it.",
        "When the scan index reaches that end, the part is closed. Record its length and start a new one.",
    ],
    approaches=[
        ("Re-scan for each cut", "O(n^2)", "O(1)", "Find the farthest last occurrence repeatedly."),
        ("Last-index greedy", "O(n)", "O(1)", "The alphabet is constant."),
    ],
    editorial=(
        "A part that contains a character must extend at least through that character's last occurrence. "
        "Taking the max last-index inside the current window is the earliest legal cut. "
        "Cutting there is safe and maximal, so the greedy cuts produce the required partition."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    out: list[int] = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            out.append(end - start + 1)
            start = i + 1
    return out


def _oracle_partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    sizes = []
    i = 0
    while i < len(s):
        end = last[s[i]]
        j = i
        while j < end:
            end = max(end, last[s[j]])
            j += 1
        sizes.append(end - i + 1)
        i = end + 1
    return sizes


cases(
    "partition-labels",
    _oracle_partition_labels,
    [
        ("classic", {"s": "ababcbacadefegdehijhklij"}, True, "The sizes are 9, 7, 8."),
        ("one", {"s": "eccbbbbdec"}, True, "The whole string is one part."),
        ("single", {"s": "a"}, False, None),
        ("all-different", {"s": "abc"}, False, None),
        ("pairs", {"s": "aabbcc"}, False, None),
    ],
)


@define(
    slug="h-index",
    title="H-Index",
    difficulty="medium",
    topics=["sorting", "binary-search"],
    statement=(
        "A researcher has h-index h when h of their papers have at least h citations each, and the other papers have at most h citations each. "
        "`citations[i]` is the citation count of paper i. Return the researcher's h-index."
    ),
    constraints=["1 <= citations.length <= 5000", "0 <= citations[i] <= 1000"],
    signature="from typing import List\n\ndef h_index(citations: List[int]) -> int:",
    function_name="h_index",
    hints=[
        "Sort descending. The h-index is the largest h such that the h-th paper has at least h citations.",
        "If citations is sorted descending, paper i (1-based) supports h = i when citations[i - 1] >= i.",
        "A counting bucket of size n + 1 also computes it in linear time, because any count above n is equivalent to n.",
    ],
    approaches=[
        ("Sort", "O(n log n)", "O(n)", "Scan the sorted citation list."),
        ("Counting sort", "O(n)", "O(n)", "Bucket citation counts clipped at n."),
    ],
    editorial=(
        "After sorting descending, walk i from 1. While the i-th paper has at least i citations, h can be i. "
        "Stop at the first paper that does not. "
        "That h is maximal because a larger value would require the next paper to have even more citations."
    ),
    companies=["Google", "Amazon", "Bloomberg", "Microsoft"],
)
def h_index(citations: list[int]) -> int:
    ordered = sorted(citations, reverse=True)
    h = 0
    for i, count in enumerate(ordered, 1):
        if count >= i:
            h = i
        else:
            break
    return h


def _oracle_h_index(citations: list[int]) -> int:
    n = len(citations)
    for h in range(n, -1, -1):
        if sum(count >= h for count in citations) >= h:
            return h
    return 0


cases(
    "h-index",
    _oracle_h_index,
    [
        ("classic", {"citations": [3, 0, 6, 1, 5]}, True, "The h-index is 3."),
        ("one", {"citations": [1, 3, 1]}, True, "The h-index is 1."),
        ("zero", {"citations": [0]}, False, None),
        ("all", {"citations": [10, 10, 10]}, False, None),
        ("single", {"citations": [100]}, False, None),
    ],
)


@define(
    slug="find-the-index-of-the-first-occurrence",
    title="Find the Index of the First Occurrence in a String",
    difficulty="easy",
    topics=["strings", "kmp"],
    statement="Return the first index of needle in haystack, or -1 if needle is not a substring. Implement the search yourself. The Knuth-Morris-Pratt prefix table is the linear solution.",
    constraints=["1 <= haystack.length, needle.length <= 10^4"],
    signature="def str_str(haystack: str, needle: str) -> int:",
    function_name="str_str",
    hints=[
        "The naive double loop compares needle at every alignment.",
        "KMP builds a longest-prefix-that-is-suffix table for needle.",
        "On a mismatch, the table says how far the pattern can shift without re-reading the text.",
    ],
    approaches=[
        ("Naive search", "O(n * m)", "O(1)", "Try every alignment."),
        ("KMP", "O(n + m)", "O(m)", "The prefix table plus one scan of the text."),
    ],
    editorial=(
        "Build lps where lps[i] is the longest proper prefix of needle[:i+1] that is also a suffix. "
        "Scan the haystack with a pattern index. On a match, advance both. On a mismatch, jump the pattern index to lps[pattern index - 1], or move the text index if the pattern index is already 0. "
        "When the pattern index reaches the needle length, the match started at text index minus that length."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def str_str(haystack: str, needle: str) -> int:
    if needle == "":
        return 0
    lps = [0] * len(needle)
    length = 0
    i = 1
    while i < len(needle):
        if needle[i] == needle[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    i = j = 0
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == len(needle):
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def _oracle_str_str(haystack: str, needle: str) -> int:
    return haystack.find(needle)


cases(
    "find-the-index-of-the-first-occurrence",
    _oracle_str_str,
    [
        ("sad", {"haystack": "sadbutsad", "needle": "sad"}, True, "The first match is at index 0."),
        ("miss", {"haystack": "leetcode", "needle": "leeto"}, True, "No match."),
        ("middle", {"haystack": "hello", "needle": "ll"}, False, None),
        ("repeat", {"haystack": "aaaaa", "needle": "bba"}, False, None),
        ("overlap", {"haystack": "aaa", "needle": "aa"}, False, None),
    ],
)


@define(
    slug="repeated-substring-pattern",
    title="Repeated Substring Pattern",
    difficulty="easy",
    topics=["strings", "kmp"],
    statement="Return true when `s` can be built by concatenating a nonempty substring with itself at least twice.",
    constraints=["1 <= s.length <= 10^4"],
    signature="def repeated_substring_pattern(s: str) -> bool:",
    function_name="repeated_substring_pattern",
    hints=[
        "If s is made of a repeated block, then s appears in (s + s) before the last character and after the first.",
        "Search for s inside (s + s)[1:-1].",
        "The KMP prefix table gives the same fact: if n % (n - lps[n - 1]) == 0 and lps[n - 1] is nonzero, the string repeats.",
    ],
    approaches=[
        ("Try every divisor", "O(n sqrt n)", "O(n)", "A period must divide the length."),
        ("Concatenation trick or KMP", "O(n)", "O(n)", "One string search."),
    ],
    editorial=(
        "Let t = s + s. If s is periodic, a second copy starts at the period inside t, so s is found strictly inside t, not only at the two ends. "
        "Conversely, a match inside t[1:-1] means a rotation of s equals s, which is exactly a repeated block. "
        "haystack.find on the sliced concatenation is the short proof. The KMP border is the interview follow-up."
    ),
    companies=["Amazon", "Adobe", "Google", "Microsoft"],
)
def repeated_substring_pattern(s: str) -> bool:
    return s in (s + s)[1:-1]


def _oracle_repeated_substring_pattern(s: str) -> bool:
    n = len(s)
    for size in range(1, n // 2 + 1):
        if n % size == 0 and s[:size] * (n // size) == s:
            return True
    return False


cases(
    "repeated-substring-pattern",
    _oracle_repeated_substring_pattern,
    [
        ("yes", {"s": "abab"}, True, "ab repeated twice."),
        ("no", {"s": "aba"}, True, "No repeated block."),
        ("triple", {"s": "abcabcabc"}, False, None),
        ("single", {"s": "a"}, False, None),
        ("aa", {"s": "aa"}, False, None),
    ],
)


@define(
    slug="valid-palindrome-ii",
    title="Valid Palindrome II",
    difficulty="easy",
    topics=["strings", "two-pointers"],
    statement="Return true when `s` is a palindrome, or becomes a palindrome after deleting at most one character.",
    constraints=["1 <= s.length <= 10^5", "s is lowercase"],
    signature="def valid_palindrome(s: str) -> bool:",
    function_name="valid_palindrome",
    hints=[
        "Two pointers find the first mismatch.",
        "At the mismatch you may skip the left character or the right character, but not both in different places.",
        "Check whether either remaining slice is a strict palindrome.",
    ],
    approaches=[
        ("Delete each character", "O(n^2)", "O(n)", "Try every deletion."),
        ("One mismatch branch", "O(n)", "O(1)", "Two candidate skips."),
    ],
    editorial=(
        "Walk inward. While the characters match, continue. "
        "On a mismatch, the answer is true when s[left+1:right+1] is a palindrome or s[left:right] is a palindrome. "
        "A second mismatch inside either check fails that branch. You do not get a second deletion."
    ),
    companies=["Facebook", "Amazon", "Microsoft", "Adobe"],
)
def valid_palindrome(s: str) -> bool:
    def is_pal(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True


def _oracle_valid_palindrome(s: str) -> bool:
    if s == s[::-1]:
        return True
    for i in range(len(s)):
        t = s[:i] + s[i + 1 :]
        if t == t[::-1]:
            return True
    return False


cases(
    "valid-palindrome-ii",
    _oracle_valid_palindrome,
    [
        ("aba", {"s": "aba"}, True, "Already a palindrome."),
        ("abca", {"s": "abca"}, True, "Delete b or c."),
        ("abc", {"s": "abc"}, False, None),
        ("single", {"s": "a"}, False, None),
        ("almost", {"s": "abcca"}, False, None),
    ],
)


@define(
    slug="count-inversions",
    title="Count Inversions",
    difficulty="hard",
    topics=["divide-and-conquer", "sorting"],
    statement="Return the number of pairs (i, j) with i < j and nums[i] > nums[j]. An inversion is a pair that is out of sorted order.",
    constraints=["1 <= nums.length <= 5000 for these tests", "-10^9 <= nums[i] <= 10^9"],
    signature="from typing import List\n\ndef count_inversions(nums: List[int]) -> int:",
    function_name="count_inversions",
    hints=[
        "A double loop counts pairs and is quadratic.",
        "Merge sort counts them while merging. When the right half contributes a value first, it is smaller than every remaining left value.",
        "Add the number of remaining left values at that moment.",
    ],
    approaches=[
        ("All pairs", "O(n^2)", "O(1)", "The definition."),
        ("Modified merge sort", "O(n log n)", "O(n)", "Inversions are split across the two halves plus the merge."),
    ],
    editorial=(
        "Inversions are of three kinds: inside the left half, inside the right half, and across the midpoint. "
        "The recursive calls count the first two. During the merge, every time a right value is taken before leftover left values, it forms an inversion with each of them. "
        "Sum those counts. The sorted merge is what makes the leftover left values a contiguous suffix."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def count_inversions(nums: list[int]) -> int:
    temp = nums[:]
    def sort_count(left: int, right: int) -> int:
        if right - left <= 1:
            return 0
        mid = (left + right) // 2
        inversions = sort_count(left, mid) + sort_count(mid, right)
        merged = []
        i, j = left, mid
        while i < mid and j < right:
            if temp[i] <= temp[j]:
                merged.append(temp[i])
                i += 1
            else:
                merged.append(temp[j])
                inversions += mid - i
                j += 1
        merged.extend(temp[i:mid])
        merged.extend(temp[j:right])
        temp[left:right] = merged
        return inversions

    return sort_count(0, len(temp))


def _oracle_count_inversions(nums: list[int]) -> int:
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                count += 1
    return count


cases(
    "count-inversions",
    _oracle_count_inversions,
    [
        ("classic", {"nums": [2, 4, 1, 3, 5]}, True, "Three inversions: (2, 1), (4, 1), (4, 3)."),
        ("sorted", {"nums": [1, 2, 3]}, True, "No inversions."),
        ("reversed", {"nums": [3, 2, 1]}, False, None),
        ("dups", {"nums": [1, 3, 2, 3, 1]}, False, None),
        ("one", {"nums": [5]}, False, None),
    ],
)


@define(
    slug="min-cost-climbing-stairs",
    title="Min Cost Climbing Stairs",
    difficulty="easy",
    topics=["dynamic-programming"],
    statement="You pay cost[i] to step on stair i, then you may climb one or two stairs. You may start at stair 0 or stair 1. Return the minimum cost to reach the top, which is just past the last stair.",
    constraints=["2 <= cost.length <= 1000", "0 <= cost[i] <= 999"],
    signature="from typing import List\n\ndef min_cost_climbing_stairs(cost: List[int]) -> int:",
    function_name="min_cost_climbing_stairs",
    hints=[
        "The top is an imaginary stair after the last index, and stepping on it is free.",
        "The cost to reach i is cost[i] plus the cheaper of reaching i from i - 1 or i - 2, for real stairs.",
        "The answer is the cheaper of the last two stairs, because from either you can step to the top.",
    ],
    approaches=[
        ("Recursion", "O(2^n)", "O(n)", "Two choices."),
        ("Rolling DP", "O(n)", "O(1)", "Two previous costs."),
    ],
    editorial=(
        "Let dp[i] be the minimum cost to reach stair i and pay for it. "
        "dp[i] = cost[i] + min(dp[i - 1], dp[i - 2]), with the starts dp[0] = cost[0] and dp[1] = cost[1]. "
        "The top is reached from n - 1 or n - 2 without an extra payment, so return the min of those two."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def min_cost_climbing_stairs(cost: list[int]) -> int:
    a, b = cost[0], cost[1]
    for value in cost[2:]:
        a, b = b, value + min(a, b)
    return min(a, b)


def _oracle_min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)

    def best(i: int) -> int:
        if i >= n:
            return 0
        return cost[i] + min(best(i + 1), best(i + 2))

    return min(best(0), best(1))


cases(
    "min-cost-climbing-stairs",
    _oracle_min_cost_climbing_stairs,
    [
        ("classic", {"cost": [10, 15, 20]}, True, "Pay 15."),
        ("longer", {"cost": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}, True, "The minimum cost is 6."),
        ("two", {"cost": [1, 2]}, False, None),
        ("flat", {"cost": [5, 5, 5]}, False, None),
        ("zeros", {"cost": [0, 0, 0, 0]}, False, None),
    ],
)


@define(
    slug="search-a-2d-matrix",
    title="Search a 2D Matrix",
    difficulty="medium",
    topics=["binary-search", "matrix"],
    statement=(
        "Each row of the matrix is sorted, and the first element of each row is greater than the last element of the previous row. "
        "Return true when `target` is present."
    ),
    constraints=["1 <= m, n <= 100", "-10^4 <= values, target <= 10^4"],
    signature="from typing import List\n\ndef search_matrix(matrix: List[List[int]], target: int) -> bool:",
    function_name="search_matrix",
    hints=[
        "The matrix is a sorted array written in rows.",
        "Binary search the index range 0 .. m*n - 1.",
        "Index k lives at row k // n and column k % n.",
    ],
    approaches=[
        ("Binary search each row", "O(m log n)", "O(1)", "Find the row, then search it."),
        ("One binary search", "O(log (m*n))", "O(1)", "Treat the matrix as a flat sorted array."),
    ],
    editorial=(
        "Map a flat index to a cell and run an ordinary binary search. "
        "The row-start condition is what makes the flat sequence sorted, so the usual halving argument applies. "
        "A staircase search from the top-right is the algorithm for the different problem where each row and each column is sorted but rows do not continue each other."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Facebook"],
)
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def _oracle_search_matrix(matrix: list[list[int]], target: int) -> bool:
    return any(target in row for row in matrix)


cases(
    "search-a-2d-matrix",
    _oracle_search_matrix,
    [
        ("hit", {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 3}, True, "3 is in the first row."),
        ("miss", {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 13}, True, "13 is absent."),
        ("corner", {"matrix": [[1]], "target": 1}, False, None),
        ("last", {"matrix": [[1, 2], [3, 4]], "target": 4}, False, None),
        ("none", {"matrix": [[1, 2], [3, 4]], "target": 5}, False, None),
    ],
)


@define(
    slug="find-peak-element",
    title="Find Peak Element",
    difficulty="medium",
    topics=["binary-search"],
    statement=(
        "A peak is an element strictly greater than its neighbors. The ends have one neighbor, and the array is treated as bordered by negative infinity. "
        "`nums` may contain several peaks. Return the index of any peak."
    ),
    constraints=["1 <= nums.length <= 1000", "neighbors are never equal"],
    signature="from typing import List\n\ndef find_peak_element(nums: List[int]) -> int:",
    function_name="find_peak_element",
    hints=[
        "A linear scan finds a peak by walking uphill.",
        "Binary search also works. If nums[mid] < nums[mid + 1], a peak exists on the right, because the slope is rising and the border is negative infinity.",
        "Otherwise a peak exists at mid or on the left.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1)", "Return the first descent, or the last index."),
        ("Binary search on the slope", "O(log n)", "O(1)", "Follow the rising side."),
    ],
    editorial=(
        "The negative-infinity borders guarantee a peak. "
        "On a rising slope, the peak cannot be to the left of the higher neighbor, so discard the left half including mid. "
        "On a falling slope, mid itself may be the peak, so keep it by setting hi = mid. The loop ends on a peak index."
    ),
    companies=["Google", "Amazon", "Microsoft", "Adobe"],
)
def find_peak_element(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _oracle_find_peak_element(nums: list[int]) -> int:
    # Return the same peak the binary search returns, verified to be a peak.
    index = find_peak_element(nums)
    left = nums[index - 1] if index else float("-inf")
    right = nums[index + 1] if index + 1 < len(nums) else float("-inf")
    if not (nums[index] > left and nums[index] > right):
        raise AssertionError("not a peak")
    return index


cases(
    "find-peak-element",
    _oracle_find_peak_element,
    [
        ("classic", {"nums": [1, 2, 3, 1]}, True, "Index 2 is a peak."),
        ("two", {"nums": [1, 2, 1, 3, 5, 6, 4]}, True, "Either peak is acceptable. The binary search picks one."),
        ("single", {"nums": [1]}, False, None),
        ("rising", {"nums": [1, 2, 3]}, False, None),
        ("falling", {"nums": [3, 2, 1]}, False, None),
    ],
)


@define(
    slug="majority-element-ii",
    title="Majority Element II",
    difficulty="medium",
    topics=["arrays", "boyer-moore"],
    statement="Return every element that appears more than n / 3 times, sorted. There are at most two such elements.",
    constraints=["1 <= nums.length <= 5 * 10^4"],
    signature="from typing import List\n\ndef majority_element_ii(nums: List[int]) -> List[int]:",
    function_name="majority_element_ii",
    hints=[
        "A hash map is the direct count.",
        "Boyer-Moore generalizes to two candidates, because more than two values cannot each exceed n / 3.",
        "A second pass verifies the candidates. The vote can name a value that does not actually qualify.",
    ],
    approaches=[
        ("Count", "O(n)", "O(n)", "Filter values whose count exceeds n / 3."),
        ("Two-candidate voting", "O(n)", "O(1)", "Pair cancellations, then verify."),
    ],
    editorial=(
        "Keep two candidates and two counts. A match increments. An empty slot takes the value. Otherwise both counts decrement, which cancels one of each. "
        "After the vote, count the candidates for real and keep those above n / 3. "
        "Sort the result."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def majority_element_ii(nums: list[int]) -> list[int]:
    cand1 = cand2 = None
    count1 = count2 = 0
    for value in nums:
        if value == cand1:
            count1 += 1
        elif value == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = value, 1
        elif count2 == 0:
            cand2, count2 = value, 1
        else:
            count1 -= 1
            count2 -= 1
    threshold = len(nums) // 3
    return sorted(value for value in (cand1, cand2) if value is not None and nums.count(value) > threshold)


def _oracle_majority_element_ii(nums: list[int]) -> list[int]:
    threshold = len(nums) // 3
    return sorted(value for value, count in Counter(nums).items() if count > threshold)


cases(
    "majority-element-ii",
    _oracle_majority_element_ii,
    [
        ("two", {"nums": [3, 2, 3]}, True, "3 appears more than n/3 times."),
        ("both", {"nums": [1, 1, 1, 3, 3, 2, 2, 2]}, True, "1 and 2 both qualify."),
        ("none", {"nums": [1, 2, 3]}, False, None),
        ("one", {"nums": [1]}, False, None),
        ("all", {"nums": [2, 2, 2, 2]}, False, None),
    ],
)


@define(
    slug="rotate-array",
    title="Rotate Array",
    difficulty="medium",
    topics=["arrays"],
    statement="Rotate `nums` to the right by `k` steps and return the rotated array. k may be larger than the length.",
    constraints=["1 <= nums.length <= 10^5", "0 <= k <= 10^5"],
    signature="from typing import List\n\ndef rotate(nums: List[int], k: int) -> List[int]:",
    function_name="rotate",
    hints=[
        "k modulo n is the effective rotation.",
        "The last k elements become the new prefix.",
        "Three reversals do it in place: reverse the whole array, reverse the first k, reverse the rest.",
    ],
    approaches=[
        ("Extra array", "O(n)", "O(n)", "Write each element to (i + k) mod n."),
        ("Three reversals", "O(n)", "O(1)", "In-place, no extra buffer beyond a few indices."),
    ],
    editorial=(
        "Reduce k modulo n. Reverse the entire array, then reverse the first k elements, then reverse the suffix. "
        "The first reversal puts the old suffix at the front in reverse. The next two reversals restore order inside each piece."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def rotate(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    k %= n
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
    return nums


def _oracle_rotate(nums: list[int], k: int) -> list[int]:
    if not nums:
        return []
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else list(nums)


cases(
    "rotate-array",
    _oracle_rotate,
    [
        ("classic", {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}, True, "The array becomes 5, 6, 7, 1, 2, 3, 4."),
        ("wrap", {"nums": [-1, -100, 3, 99], "k": 2}, True, "Two steps."),
        ("zero", {"nums": [1, 2], "k": 0}, False, None),
        ("full", {"nums": [1, 2, 3], "k": 3}, False, None),
        ("over", {"nums": [1, 2], "k": 5}, False, None),
    ],
)


@define(
    slug="increasing-triplet-subsequence",
    title="Increasing Triplet Subsequence",
    difficulty="medium",
    topics=["arrays", "greedy"],
    statement="Return true when there exist indices i < j < k with nums[i] < nums[j] < nums[k].",
    constraints=["1 <= nums.length <= 5 * 10^5", "-2^31 <= nums[i] <= 2^31 - 1"],
    signature="from typing import List\n\ndef increasing_triplet(nums: List[int]) -> bool:",
    function_name="increasing_triplet",
    hints=[
        "Track the smallest value so far and the smallest value that has a smaller predecessor.",
        "Call them first and second, both starting at infinity.",
        "If a value is bigger than second, it completes a triplet. If it is smaller than first, it becomes the new first. Otherwise, if it is between them, it becomes the new second.",
    ],
    approaches=[
        ("Triple loop or LIS length", "O(n^2) or O(n log n)", "O(n)", "Stop when the LIS reaches length 3."),
        ("Two candidates", "O(n)", "O(1)", "The greedy pair above."),
    ],
    editorial=(
        "first is the smallest start seen. second is the smallest middle that already has a valid start somewhere before it, not necessarily first as it stands now. "
        "Updating first to a later smaller value does not invalidate second, because second's original start is still to its left. "
        "A value above second therefore has both a middle and a start before it."
    ),
    companies=["Amazon", "Facebook", "Google", "Adobe"],
)
def increasing_triplet(nums: list[int]) -> bool:
    first = second = float("inf")
    for value in nums:
        if value <= first:
            first = value
        elif value <= second:
            second = value
        else:
            return True
    return False


def _oracle_increasing_triplet(nums: list[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] <= nums[i]:
                continue
            for k in range(j + 1, len(nums)):
                if nums[k] > nums[j]:
                    return True
    return False


cases(
    "increasing-triplet-subsequence",
    _oracle_increasing_triplet,
    [
        ("yes", {"nums": [1, 2, 3, 4, 5]}, True, "Any increasing triple works."),
        ("no", {"nums": [5, 4, 3, 2, 1]}, True, "The array is decreasing."),
        ("reset", {"nums": [2, 1, 5, 0, 4, 6]}, False, None),
        ("short", {"nums": [1, 2]}, False, None),
        ("equal", {"nums": [1, 1, 1, 1]}, False, None),
    ],
)


@define(
    slug="n-queens-ii",
    title="N-Queens II",
    difficulty="hard",
    topics=["backtracking"],
    statement="Return the number of distinct ways to place `n` queens on an n by n chessboard so that no two queens attack each other.",
    constraints=["1 <= n <= 9"],
    signature="def total_n_queens(n: int) -> int:",
    function_name="total_n_queens",
    hints=[
        "Place one queen per row.",
        "A column, a diagonal, and an anti-diagonal can each hold at most one queen.",
        "Diagonals share r - c. Anti-diagonals share r + c. Sets of occupied columns and diagonals prune the search.",
    ],
    approaches=[
        ("Permutations of columns", "O(n!)", "O(n)", "A permutation avoids column clashes. Filter the diagonals."),
        ("Backtracking with three sets", "O(n!)", "O(n)", "Prune before the permutation is complete."),
    ],
    editorial=(
        "The row-by-row search tries each column that is free in the column set, the (r - c) set, and the (r + c) set. "
        "Add the column and both diagonals, recurse to the next row, and remove them. "
        "A completed row count of n is one solution. The known sequence starts 1, 0, 0, 2, 10, 4, 40, 92 for n from 1."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def total_n_queens(n: int) -> int:
    cols: set[int] = set()
    diag: set[int] = set()
    anti: set[int] = set()

    def dfs(row: int) -> int:
        if row == n:
            return 1
        total = 0
        for col in range(n):
            if col in cols or row - col in diag or row + col in anti:
                continue
            cols.add(col)
            diag.add(row - col)
            anti.add(row + col)
            total += dfs(row + 1)
            cols.remove(col)
            diag.remove(row - col)
            anti.remove(row + col)
        return total

    return dfs(0)


def _oracle_total_n_queens(n: int) -> int:
    def ok(cols: tuple[int, ...]) -> bool:
        return len({r - c for r, c in enumerate(cols)}) == n and len({r + c for r, c in enumerate(cols)}) == n

    from itertools import permutations

    return sum(ok(cols) for cols in permutations(range(n)))


cases(
    "n-queens-ii",
    _oracle_total_n_queens,
    [
        ("four", {"n": 4}, True, "Two solutions."),
        ("one", {"n": 1}, True, "One solution."),
        ("two", {"n": 2}, False, None),
        ("three", {"n": 3}, False, None),
        ("five", {"n": 5}, False, None),
    ],
)


@define(
    slug="letter-case-permutation",
    title="Letter Case Permutation",
    difficulty="medium",
    topics=["backtracking", "bit-manipulation"],
    statement="Given a string of letters and digits, return every string obtained by changing the case of any letters. Digits stay fixed. Sort the result.",
    constraints=["1 <= s.length <= 12", "s consists of letters and digits"],
    signature="from typing import List\n\ndef letter_case_permutation(s: str) -> List[str]:",
    function_name="letter_case_permutation",
    hints=[
        "Each letter has two choices. Digits have one.",
        "A DFS that branches only on letters builds every string.",
        "There are 2^(number of letters) results.",
    ],
    approaches=[
        ("Iterative product", "O(2^k * n)", "O(2^k * n)", "Start from the empty prefix and extend."),
        ("Backtracking", "O(2^k * n)", "O(n)", "The same product, depth-first."),
    ],
    editorial=(
        "Walk the string. A digit is appended as itself. A letter branches into its lower and upper forms. "
        "At the end of the string, record the path. "
        "Sorting makes the list deterministic."
    ),
    companies=["Amazon", "Adobe", "Microsoft", "Apple"],
)
def letter_case_permutation(s: str) -> list[str]:
    out: list[str] = []
    path: list[str] = []

    def dfs(i: int) -> None:
        if i == len(s):
            out.append("".join(path))
            return
        ch = s[i]
        if ch.isdigit():
            path.append(ch)
            dfs(i + 1)
            path.pop()
        else:
            for variant in (ch.lower(), ch.upper()):
                path.append(variant)
                dfs(i + 1)
                path.pop()

    dfs(0)
    return sorted(out)


def _oracle_letter_case_permutation(s: str) -> list[str]:
    out = [""]
    for ch in s:
        if ch.isdigit():
            out = [item + ch for item in out]
        else:
            out = [item + variant for item in out for variant in (ch.lower(), ch.upper())]
    return sorted(set(out))


cases(
    "letter-case-permutation",
    _oracle_letter_case_permutation,
    [
        ("classic", {"s": "a1b2"}, True, "Four strings."),
        ("digits", {"s": "123"}, True, "Only one string."),
        ("one", {"s": "a"}, False, None),
        ("three", {"s": "ab"}, False, None),
        ("mixed", {"s": "3z4"}, False, None),
    ],
)


@define(
    slug="restore-ip-addresses",
    title="Restore IP Addresses",
    difficulty="medium",
    topics=["backtracking", "strings"],
    statement=(
        "A valid IP address is four integers separated by dots. Each integer is 0..255 and has no leading zero. "
        "Return every possible valid IP address that can be formed by inserting three dots into `s`. Sort the result."
    ),
    constraints=["1 <= s.length <= 20", "s consists of digits"],
    signature="from typing import List\n\ndef restore_ip_addresses(s: str) -> List[str]:",
    function_name="restore_ip_addresses",
    hints=[
        "Choose a segment of length 1, 2, or 3.",
        "Reject a segment with a leading zero, unless the segment is exactly '0'. Reject a segment whose integer value exceeds 255.",
        "Stop after four segments. The last segment must consume the rest of the string.",
    ],
    approaches=[
        ("Four nested loops", "O(1) because the string is short", "O(1)", "The lengths are at most 3."),
        ("Backtracking", "O(3^4)", "O(1)", "The same search written recursively."),
    ],
    editorial=(
        "The recursion carries the start index and the segments chosen so far. "
        "It tries each legal next segment and, when four segments consume the string, joins them with dots. "
        "Leading-zero rejection is a string check, not an integer check, because int('00') is 0."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def restore_ip_addresses(s: str) -> list[str]:
    out: list[str] = []

    def dfs(i: int, parts: list[str]) -> None:
        if len(parts) == 4:
            if i == len(s):
                out.append(".".join(parts))
            return
        for length in range(1, 4):
            if i + length > len(s):
                break
            piece = s[i : i + length]
            if (len(piece) > 1 and piece[0] == "0") or int(piece) > 255:
                continue
            parts.append(piece)
            dfs(i + length, parts)
            parts.pop()

    dfs(0, [])
    return sorted(out)


def _oracle_restore_ip_addresses(s: str) -> list[str]:
    out = []
    n = len(s)
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                d = n - a - b - c
                if not 1 <= d <= 3:
                    continue
                parts = [s[:a], s[a : a + b], s[a + b : a + b + c], s[a + b + c :]]
                if all((len(p) == 1 or p[0] != "0") and int(p) <= 255 for p in parts):
                    out.append(".".join(parts))
    return sorted(out)


cases(
    "restore-ip-addresses",
    _oracle_restore_ip_addresses,
    [
        ("classic", {"s": "25525511135"}, True, "Two valid addresses."),
        ("zeros", {"s": "0000"}, True, "Only 0.0.0.0."),
        ("short", {"s": "111"}, False, None),
        ("leading", {"s": "010010"}, False, None),
        ("one", {"s": "101023"}, False, None),
    ],
)


@define(
    slug="combination-sum-iii",
    title="Combination Sum III",
    difficulty="medium",
    topics=["backtracking"],
    statement="Find every combination of `k` distinct integers from 1..9 that sum to `n`. Sort each combination and sort the list.",
    constraints=["2 <= k <= 9", "1 <= n <= 60"],
    signature="from typing import List\n\ndef combination_sum3(k: int, n: int) -> List[List[int]]:",
    function_name="combination_sum3",
    hints=[
        "This is combinations of a fixed size with a sum constraint.",
        "Choose numbers in increasing order so each combination is generated once.",
        "Prune when the remaining sum is negative or the remaining count cannot be filled.",
    ],
    approaches=[
        ("Enumerate combinations", "O(C(9, k))", "O(k)", "Filter by sum."),
        ("Backtracking", "O(C(9, k))", "O(k)", "The same search with early exits."),
    ],
    editorial=(
        "Start from 1 and append a number larger than the previous one. "
        "Decrease the remaining sum and the remaining count. "
        "Record the path when both hit zero. Skip a branch whose next number already exceeds the remainder."
    ),
    companies=["Amazon", "Adobe", "Google", "Microsoft"],
)
def combination_sum3(k: int, n: int) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if len(path) == k:
            if remain == 0:
                out.append(path[:])
            return
        for value in range(start, 10):
            if value > remain:
                break
            path.append(value)
            dfs(value + 1, remain - value)
            path.pop()

    dfs(1, n)
    return out


def _oracle_combination_sum3(k: int, n: int) -> list[list[int]]:
    from itertools import combinations

    return [list(comb) for comb in combinations(range(1, 10), k) if sum(comb) == n]


cases(
    "combination-sum-iii",
    _oracle_combination_sum3,
    [
        ("classic", {"k": 3, "n": 7}, True, "Only 1, 2, 4."),
        ("two", {"k": 3, "n": 9}, True, "Three combinations."),
        ("none", {"k": 4, "n": 1}, False, None),
        ("nine", {"k": 2, "n": 18}, False, None),
        ("one-way", {"k": 9, "n": 45}, False, None),
    ],
)


@define(
    slug="merge-k-sorted-lists",
    title="Merge K Sorted Lists",
    difficulty="hard",
    topics=["heaps", "linked-lists", "divide-and-conquer"],
    statement="Merge `lists`, a list of sorted integer arrays, into one sorted array. Empty lists are allowed.",
    constraints=["0 <= k <= 10^4", "0 <= list length <= 500", "-10^4 <= values <= 10^4"],
    signature="from typing import List\n\ndef merge_k_lists(lists: List[List[int]]) -> List[int]:",
    function_name="merge_k_lists",
    hints=[
        "Concatenating and sorting is correct and ignores the sorted inputs.",
        "A min-heap of size k stores the current head of each list. Pop the smallest and push that list's next value.",
        "Divide and conquer merges the lists like merge sort, pairing them until one list remains.",
    ],
    approaches=[
        ("Concat and sort", "O(N log N)", "O(N)", "N is the total number of elements."),
        ("Heap", "O(N log k)", "O(k)", "Each element is pushed and popped once."),
    ],
    editorial=(
        "Push (value, list index, element index) for every nonempty list. "
        "Pop the smallest triple, append the value, and if that list has another element, push it. "
        "The list index breaks ties so the heap never compares two equal values by falling through to a later incomparable object. Here the element index is an int, so the triple stays ordered."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def merge_k_lists(lists: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []
    for i, row in enumerate(lists):
        if row:
            heap.append((row[0], i, 0))
    heapq.heapify(heap)
    out: list[int] = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


def _oracle_merge_k_lists(lists: list[list[int]]) -> list[int]:
    merged: list[int] = []
    for row in lists:
        merged.extend(row)
    return sorted(merged)


cases(
    "merge-k-sorted-lists",
    _oracle_merge_k_lists,
    [
        ("classic", {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]}, True, "The merged list is sorted."),
        ("empty", {"lists": []}, True, "Nothing to merge."),
        ("blanks", {"lists": [[], [1]]}, False, None),
        ("one", {"lists": [[1, 2, 3]]}, False, None),
        ("neg", {"lists": [[-2, 0], [-1], []]}, False, None),
    ],
)


@define(
    slug="josephus",
    title="Josephus Problem",
    difficulty="medium",
    topics=["math", "queues"],
    statement=(
        "There are `n` people numbered 1..n in a circle. Counting starts at 1. Every `k`-th remaining person is eliminated until one remains. "
        "Return the number of the survivor. k is at least 1."
    ),
    constraints=["1 <= n <= 5000", "1 <= k <= n"],
    signature="def josephus(n: int, k: int) -> int:",
    function_name="josephus",
    hints=[
        "A queue or a circular list simulates the count.",
        "Move k - 1 people from the front to the back, then eliminate the front.",
        "The 0-based recurrence is f(1) = 0 and f(n) = (f(n - 1) + k) mod n. Add 1 to convert to 1-based numbering.",
    ],
    approaches=[
        ("Simulation", "O(n * k)", "O(n)", "A deque of the living people."),
        ("Recurrence", "O(n)", "O(1)", "The classic modular formula."),
    ],
    editorial=(
        "The 0-based survivor after eliminating every k-th person satisfies f(n) = (f(n - 1) + k) mod n, with f(1) = 0. "
        "The formula shifts the previous survivor by k positions because one person was removed and the count continues at the next person. "
        "This problem numbers people from 1, so return f(n) + 1."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def josephus(n: int, k: int) -> int:
    survivor = 0
    for size in range(2, n + 1):
        survivor = (survivor + k) % size
    return survivor + 1


def _oracle_josephus(n: int, k: int) -> int:
    from collections import deque

    circle = deque(range(1, n + 1))
    while len(circle) > 1:
        circle.rotate(1 - k)
        circle.popleft()
    return circle[0]


cases(
    "josephus",
    _oracle_josephus,
    [
        ("classic", {"n": 5, "k": 2}, True, "The survivor is 3."),
        ("one", {"n": 1, "k": 1}, True, "The only person survives."),
        ("all", {"n": 7, "k": 3}, False, None),
        ("k-one", {"n": 4, "k": 1}, False, None),
        ("six", {"n": 6, "k": 5}, False, None),
    ],
)


@define(
    slug="excel-sheet-column-number",
    title="Excel Sheet Column Number",
    difficulty="easy",
    topics=["math", "strings"],
    statement="Convert an Excel column title to its number. A is 1, Z is 26, AA is 27, and so on. The title is a base-26 numeral with digits A..Z.",
    constraints=["1 <= columnTitle.length <= 7", "The title is uppercase"],
    signature="def title_to_number(column_title: str) -> int:",
    function_name="title_to_number",
    hints=[
        "This is base 26, but the digits are 1..26 rather than 0..25.",
        "Fold from the left: result = result * 26 + (char - 'A' + 1).",
        "There is no zero digit, which is why AA is 27 and not 26 * 26.",
    ],
    approaches=[
        ("Horner fold", "O(length)", "O(1)", "One multiply-add per character."),
        ("Powers from the right", "O(length)", "O(1)", "The same polynomial written explicitly."),
    ],
    editorial=(
        "Each new character shifts the value accumulated so far by one digit and adds the new digit. "
        "The digit of a letter is its alphabet position, starting at 1. "
        "That off-by-one from ordinary base conversion is the whole trick."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Facebook"],
)
def title_to_number(column_title: str) -> int:
    result = 0
    for ch in column_title:
        result = result * 26 + (ord(ch) - ord("A") + 1)
    return result


def _oracle_title_to_number(column_title: str) -> int:
    result = 0
    for i, ch in enumerate(reversed(column_title)):
        result += (ord(ch) - ord("A") + 1) * (26**i)
    return result


cases(
    "excel-sheet-column-number",
    _oracle_title_to_number,
    [
        ("A", {"column_title": "A"}, True, "1."),
        ("AB", {"column_title": "AB"}, True, "28."),
        ("ZY", {"column_title": "ZY"}, False, None),
        ("AA", {"column_title": "AA"}, False, None),
        ("FXSHRXW", {"column_title": "FXSHRXW"}, False, None),
    ],
)
