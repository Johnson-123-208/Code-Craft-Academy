#!/usr/bin/env python3
"""Write distinct ml-*.json exercises and verify them with the submit harness comparison."""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "content" / "problems"


def dot(a: list[float], b: list[float]) -> float:
    return float(sum(x * y for x, y in zip(a, b)))


def mean(xs: list[float]) -> float:
    return float(sum(xs) / len(xs))


def mse(y_true: list[float], y_pred: list[float]) -> float:
    return float(sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true))


def accuracy(y_true: list[int], y_pred: list[int]) -> float:
    return float(sum(int(a == b) for a, b in zip(y_true, y_pred)) / len(y_true))


def minmax(xs: list[float]) -> list[float]:
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return [0.0 for _ in xs]
    return [(x - lo) / (hi - lo) for x in xs]


def cosine(a: list[float], b: list[float]) -> float:
    denom = math.sqrt(dot(a, a)) * math.sqrt(dot(b, b))
    return float(dot(a, b) / denom)


def sigmoid(z: float) -> float:
    if z >= 0:
        ez = math.exp(-z)
        return float(1.0 / (1.0 + ez))
    ez = math.exp(z)
    return float(ez / (1.0 + ez))


def softmax(logits: list[float]) -> list[float]:
    m = max(logits)
    exps = [math.exp(z - m) for z in logits]
    s = sum(exps)
    return [e / s for e in exps]


def bce(y_true: list[float], y_prob: list[float]) -> float:
    eps = 1e-12
    total = 0.0
    for y, p in zip(y_true, y_prob):
        p = min(max(p, eps), 1.0 - eps)
        total += -(y * math.log(p) + (1.0 - y) * math.log(1.0 - p))
    return float(total / len(y_true))


def f1_score(y_true: list[int], y_pred: list[int]) -> float:
    tp = fp = fn = 0
    for a, b in zip(y_true, y_pred):
        if a == 1 and b == 1:
            tp += 1
        elif a == 0 and b == 1:
            fp += 1
        elif a == 1 and b == 0:
            fn += 1
    if tp == 0:
        return 0.0
    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    return float(2 * prec * rec / (prec + rec))


def linreg_step(w: list[float], x: list[float], y: float, lr: float) -> list[float]:
    pred = sum(wi * xi for wi, xi in zip(w, x))
    err = pred - y
    return [wi - lr * err * xi for wi, xi in zip(w, x)]


def zscore(xs: list[float]) -> list[float]:
    mu = mean(xs)
    var = sum((x - mu) ** 2 for x in xs) / len(xs)
    sd = math.sqrt(var)
    if sd == 0.0:
        return [0.0 for _ in xs]
    return [(x - mu) / sd for x in xs]


def euclidean(a: list[float], b: list[float]) -> float:
    return float(math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))))


def gini(labels: list[int]) -> float:
    n = len(labels)
    counts = Counter(labels)
    return float(1.0 - sum((c / n) ** 2 for c in counts.values()))


def entropy(labels: list[int]) -> float:
    n = len(labels)
    counts = Counter(labels)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return float(h)


def knn_predict(
    train_x: list[list[float]],
    train_y: list[int],
    query: list[float],
    k: int,
) -> int:
    ranked = sorted(
        ((euclidean(x, query), i, train_y[i]) for i, x in enumerate(train_x)),
        key=lambda t: (t[0], t[1]),
    )
    votes = Counter(label for _, _, label in ranked[:k])
    best = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return int(best)


def kmeans_assign(points: list[list[float]], centroids: list[list[float]]) -> list[int]:
    out: list[int] = []
    for p in points:
        best_i = 0
        best_d = float("inf")
        for i, c in enumerate(centroids):
            d = euclidean(p, c)
            if d < best_d:
                best_d = d
                best_i = i
        out.append(best_i)
    return out


def hinge(y_true: list[float], scores: list[float]) -> float:
    total = 0.0
    for y, s in zip(y_true, scores):
        total += max(0.0, 1.0 - y * s)
    return float(total / len(y_true))


def attention_weights(query: list[float], keys: list[list[float]]) -> list[float]:
    scale = math.sqrt(len(query))
    logits = [dot(query, k) / scale for k in keys]
    return softmax(logits)


def rmse(y_true: list[float], y_pred: list[float]) -> float:
    return float(math.sqrt(mse(y_true, y_pred)))


FUNCS = {
    "dot": dot,
    "mse": mse,
    "accuracy": accuracy,
    "mean": mean,
    "minmax": minmax,
    "cosine": cosine,
    "sigmoid": sigmoid,
    "softmax": softmax,
    "bce": bce,
    "f1_score": f1_score,
    "linreg_step": linreg_step,
    "zscore": zscore,
    "euclidean": euclidean,
    "gini": gini,
    "entropy": entropy,
    "knn_predict": knn_predict,
    "kmeans_assign": kmeans_assign,
    "hinge": hinge,
    "attention_weights": attention_weights,
    "rmse": rmse,
}


def problem(
    *,
    title: str,
    slug: str,
    difficulty: str,
    topics: list[str],
    companies: list[str],
    statement: str,
    constraints: list[str],
    fn: str,
    starter: str,
    hints: list[str],
    approaches: list[dict],
    visible: list[dict],
    hidden: list[dict],
    editorial: str,
    reference: str,
    examples: list[dict] | None = None,
) -> dict:
    if examples is None:
        examples = []
        for case in visible:
            examples.append(
                {
                    "input": json.dumps(case["args"]),
                    "output": json.dumps(FUNCS[fn](**case["args"])),
                    "explanation": case.get("explanation", "Matches the reference on this input."),
                }
            )
    return {
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "topics": topics,
        "company_tags": companies,
        "statement": statement,
        "constraints": constraints,
        "examples": examples,
        "starter_code": starter,
        "function_name": fn,
        "hints": hints,
        "approaches": approaches,
        "visible_tests": [{k: v for k, v in c.items() if k != "explanation"} for c in visible],
        "hidden_tests": [{k: v for k, v in c.items() if k != "explanation"} for c in hidden],
        "editorial": editorial,
        "reference_solution": reference,
    }


def fill_expected(cases: list[dict], fn: str) -> list[dict]:
    out = []
    for c in cases:
        item = dict(c)
        item["expected"] = FUNCS[fn](**c["args"])
        out.append(item)
    return out


def verify(data: dict) -> None:
    fn = FUNCS[data["function_name"]]
    blob = json.loads(json.dumps(data))
    for group in ("visible_tests", "hidden_tests"):
        for case in blob[group]:
            actual = fn(**case["args"])
            ok = json.dumps(actual, sort_keys=True, default=str) == json.dumps(
                case["expected"], sort_keys=True, default=str
            )
            if not ok:
                raise SystemExit(
                    f"{data['slug']} {case['name']} mismatch\n actual={actual!r}\n expected={case['expected']!r}"
                )
    if len(data["hints"]) < 3:
        raise SystemExit(f"{data['slug']} needs 3 hints")
    if not data["approaches"] or not data["editorial"] or not data["reference_solution"]:
        raise SystemExit(f"{data['slug']} incomplete schema")
    if "{" in data["statement"] or "}" in data["statement"]:
        raise SystemExit(f"{data['slug']} statement has braces")


def build() -> list[dict]:
    specs: list[dict] = []

    def add(**kwargs):
        fn = kwargs["fn"]
        kwargs["visible"] = fill_expected(kwargs["visible"], fn)
        kwargs["hidden"] = fill_expected(kwargs["hidden"], fn)
        specs.append(problem(**kwargs))

    add(
        title="Dot Product",
        slug="ml-dot",
        difficulty="easy",
        topics=["machine-learning", "linear-algebra", "python"],
        companies=["Google", "DeepMind"],
        statement=(
            "Implement `dot(a, b)`, the dot product of two equal-length vectors. "
            "Return the sum of elementwise products as a float. "
            "This is the similarity score inside linear regression, cosine retrieval, and attention logits."
        ),
        constraints=[
            "1 <= len(a) == len(b) <= 10^5",
            "Values are finite floats",
            "Return a Python float",
        ],
        fn="dot",
        starter="def dot(a: list[float], b: list[float]) -> float:\n    pass\n",
        hints=[
            "Walk both vectors with zip.",
            "Accumulate x * y into a float sum.",
            "Do not normalize; cosine is a different function.",
        ],
        approaches=[
            {
                "name": "Single pass",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "One multiply-add per coordinate. This is the inner product BLAS calls gemv and attention both reduce to.",
            }
        ],
        visible=[
            {"name": "aligned", "args": {"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]}, "explanation": "1*4 + 2*5 + 3*6 = 32."},
            {"name": "orthogonal", "args": {"a": [1.0, 0.0], "b": [0.0, 1.0]}, "explanation": "Perpendicular vectors have dot product 0."},
        ],
        hidden=[
            {"name": "negatives", "args": {"a": [-1.0, 2.0], "b": [3.0, -4.0]}, "explanation": "Signs matter."},
            {"name": "singleton", "args": {"a": [2.5], "b": [4.0]}, "explanation": "n = 1."},
        ],
        editorial=(
            "The dot product a · b = Σᵢ aᵢ bᵢ measures signed alignment. "
            "A positive value means the vectors point into the same half-space; zero means they are orthogonal; "
            "negative means they oppose. Linear layers, least squares, and attention scores are all built on this reduction. "
            "The implementation is a single zip over coordinates. Length mismatches are out of contract here, but production code should assert shapes before the loop."
        ),
        reference="def dot(a: list[float], b: list[float]) -> float:\n    return float(sum(x * y for x, y in zip(a, b)))\n",
    )

    add(
        title="Mean Squared Error",
        slug="ml-mse",
        difficulty="easy",
        topics=["machine-learning", "metrics", "python"],
        companies=["Amazon", "Meta"],
        statement=(
            "Implement `mse(y_true, y_pred)`, the mean squared error between two equal-length sequences. "
            "Average the squared residuals. Do not take a square root; that is RMSE."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Sequences have equal length",
            "Return a Python float",
        ],
        fn="mse",
        starter="def mse(y_true: list[float], y_pred: list[float]) -> float:\n    pass\n",
        hints=[
            "Square the residual before averaging.",
            "Divide by n, not n - 1.",
            "A perfect prediction has MSE 0.",
        ],
        approaches=[
            {
                "name": "Direct average",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "MSE is the empirical risk for squared loss. The factor 1/n makes the number comparable across batch sizes.",
            }
        ],
        visible=[
            {"name": "one-miss", "args": {"y_true": [1.0, 2.0, 3.0], "y_pred": [1.0, 2.0, 4.0]}},
            {"name": "perfect", "args": {"y_true": [2.0, 2.0], "y_pred": [2.0, 2.0]}},
        ],
        hidden=[
            {"name": "signed", "args": {"y_true": [0.0, 0.0], "y_pred": [1.0, -1.0]}},
            {"name": "single", "args": {"y_true": [5.0], "y_pred": [2.0]}},
        ],
        editorial=(
            "MSE = (1/n) Σ (yᵢ − ŷᵢ)². Squaring penalizes large misses more than absolute error and gives a smooth gradient 2(ŷ − y)/n "
            "with respect to the prediction. Divide by n so a longer test set does not inflate the metric. "
            "RMSE is the square root of this value and lives in the original units of y."
        ),
        reference="def mse(y_true: list[float], y_pred: list[float]) -> float:\n    return float(sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true))\n",
    )

    add(
        title="Classification Accuracy",
        slug="ml-accuracy",
        difficulty="easy",
        topics=["machine-learning", "metrics", "python"],
        companies=["Stripe", "Meta"],
        statement=(
            "Implement `accuracy(y_true, y_pred)` for integer class labels. "
            "Return the fraction of positions where the prediction equals the label. "
            "Accuracy is the right headline metric only when classes are balanced and errors have similar cost."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Labels are integers",
            "Return a float in 0 to 1 inclusive",
        ],
        fn="accuracy",
        starter="def accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    pass\n",
        hints=[
            "Count exact matches.",
            "Divide the count by n as a float.",
            "Do not treat a nearby class as correct.",
        ],
        approaches=[
            {
                "name": "Match count",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "Accuracy is the 0-1 loss averaged and flipped. It ignores how confident the model was.",
            }
        ],
        visible=[
            {"name": "three-of-four", "args": {"y_true": [1, 0, 1, 1], "y_pred": [1, 0, 0, 1]}},
            {"name": "all-wrong", "args": {"y_true": [0, 1, 0], "y_pred": [1, 0, 1]}},
        ],
        hidden=[
            {"name": "multiclass", "args": {"y_true": [2, 0, 2, 1], "y_pred": [2, 2, 2, 1]}},
            {"name": "single", "args": {"y_true": [7], "y_pred": [7]}},
        ],
        editorial=(
            "Accuracy = (1/n) Σ 1[yᵢ = ŷᵢ]. It is easy to explain and easy to game on imbalanced data: "
            "a fraud model that always predicts legitimate can post 99 percent accuracy while catching nothing. "
            "Pair it with precision, recall, or balanced accuracy before you ship a classifier. The implementation is a single pass of equality tests."
        ),
        reference="def accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    return float(sum(int(a == b) for a, b in zip(y_true, y_pred)) / len(y_true))\n",
    )

    add(
        title="Compute Mean",
        slug="ml-mean",
        difficulty="easy",
        topics=["machine-learning", "statistics", "python"],
        companies=["Two Sigma", "Amazon"],
        statement=(
            "Implement `mean(xs)` for a non-empty list of floats. "
            "Return the arithmetic mean, sum divided by count. "
            "This is the baseline predictor for squared loss and the centering step in standardization."
        ),
        constraints=[
            "1 <= len(xs) <= 10^5",
            "Values are finite",
            "Return a Python float",
        ],
        fn="mean",
        starter="def mean(xs: list[float]) -> float:\n    pass\n",
        hints=[
            "Sum every element.",
            "Divide by the length, not by length minus one.",
            "Keep the result a float even if the sum looks integral.",
        ],
        approaches=[
            {
                "name": "One pass sum",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "The sample mean minimizes squared error among constant predictors.",
            }
        ],
        visible=[
            {"name": "one-two-three", "args": {"xs": [1.0, 2.0, 3.0]}},
            {"name": "negatives", "args": {"xs": [-2.0, 2.0]}},
        ],
        hidden=[
            {"name": "single", "args": {"xs": [4.5]}},
            {"name": "zeros", "args": {"xs": [0.0, 0.0, 0.0]}},
        ],
        editorial=(
            "The arithmetic mean μ = (1/n) Σ xᵢ is the first moment of the empirical distribution. "
            "For squared error, predicting μ on a constant-only model is optimal. "
            "Do not confuse it with the median, which is optimal for absolute error, or with the population formula that divides by n versus the unbiased variance that divides by n − 1. Mean itself always divides by n."
        ),
        reference="def mean(xs: list[float]) -> float:\n    return float(sum(xs) / len(xs))\n",
    )

    add(
        title="Min-Max Scale",
        slug="ml-minmax",
        difficulty="easy",
        topics=["machine-learning", "feature-engineering", "python"],
        companies=["Uber", "Airbnb"],
        statement=(
            "Implement `minmax(xs)`, scaling a non-empty list into the unit interval. "
            "For each x return (x − min) / (max − min). "
            "If max equals min, return a list of zeros of the same length so a constant feature does not divide by zero."
        ),
        constraints=[
            "1 <= len(xs) <= 10^5",
            "Constant columns map to zeros",
            "Return a list of floats",
        ],
        fn="minmax",
        starter="def minmax(xs: list[float]) -> list[float]:\n    pass\n",
        hints=[
            "Find min and max in one or two passes.",
            "Guard the case max == min.",
            "The original minimum maps to 0 and the maximum maps to 1 when they differ.",
        ],
        approaches=[
            {
                "name": "Affine map",
                "complexity": {"time": "O(n)", "space": "O(n)"},
                "explanation": "Min-max is an affine map onto 0..1. It is sensitive to outliers, unlike z-scores.",
            }
        ],
        visible=[
            {"name": "spread", "args": {"xs": [0.0, 5.0, 10.0]}},
            {"name": "constant", "args": {"xs": [3.0, 3.0, 3.0]}},
        ],
        hidden=[
            {"name": "reversed", "args": {"xs": [10.0, 0.0, 5.0]}},
            {"name": "negatives", "args": {"xs": [-2.0, 0.0, 2.0]}},
        ],
        editorial=(
            "Min-max scaling sends the smallest training value to 0 and the largest to 1, with linear interpolation between them. "
            "Neural nets with saturating activations often train more calmly when features share a scale. "
            "Fit min and max on the training fold only, then apply those constants to validation and test rows. "
            "A constant feature has no range; returning zeros is the safe, deterministic choice and matches a column of no information."
        ),
        reference=(
            "def minmax(xs: list[float]) -> list[float]:\n"
            "    lo, hi = min(xs), max(xs)\n"
            "    if hi == lo:\n"
            "        return [0.0 for _ in xs]\n"
            "    return [(x - lo) / (hi - lo) for x in xs]\n"
        ),
    )

    add(
        title="Cosine Similarity",
        slug="ml-cosine",
        difficulty="easy",
        topics=["machine-learning", "linear-algebra", "retrieval"],
        companies=["Spotify", "Google"],
        statement=(
            "Implement `cosine(a, b)` for two equal-length, non-zero vectors. "
            "Return the dot product divided by the product of Euclidean norms. "
            "The result lies between -1 and 1 and ignores magnitude, which is why embedding search uses it."
        ),
        constraints=[
            "Vectors are non-zero and equal length",
            "1 <= n <= 10^5",
            "Return a Python float",
        ],
        fn="cosine",
        starter="def cosine(a: list[float], b: list[float]) -> float:\n    pass\n",
        hints=[
            "Reuse the dot product for the numerator and for each squared norm.",
            "The norm is the square root of the self-dot.",
            "Identical direction yields 1 even if magnitudes differ.",
        ],
        approaches=[
            {
                "name": "Normalized dot",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "cos θ = (a · b) / (‖a‖ ‖b‖). Pre-normalized embeddings reduce this to a dot product.",
            }
        ],
        visible=[
            {"name": "unit-angle", "args": {"a": [1.0, 0.0], "b": [0.6, 0.8]}},
            {"name": "same-direction", "args": {"a": [1.0, 1.0], "b": [2.0, 2.0]}},
        ],
        hidden=[
            {"name": "opposite", "args": {"a": [1.0, 0.0], "b": [-2.0, 0.0]}},
            {"name": "orthogonal", "args": {"a": [3.0, 0.0], "b": [0.0, 4.0]}},
        ],
        editorial=(
            "Cosine similarity is the dot product of two L2-normalized vectors. "
            "It answers 'do these point the same way?' and ignores length, so a long document and a short query can still match in bag-of-words space. "
            "If either vector is the zero vector the denominator vanishes; production retrieval stacks should drop or specially handle those rows. "
            "Numerically, compute norms from the sum of squares and take one square root each."
        ),
        reference=(
            "import math\n\n"
            "def cosine(a: list[float], b: list[float]) -> float:\n"
            "    dot = sum(x * y for x, y in zip(a, b))\n"
            "    na = math.sqrt(sum(x * x for x in a))\n"
            "    nb = math.sqrt(sum(y * y for y in b))\n"
            "    return float(dot / (na * nb))\n"
        ),
    )

    add(
        title="Stable Sigmoid",
        slug="ml-sigmoid",
        difficulty="easy",
        topics=["machine-learning", "deep-learning", "python"],
        companies=["OpenAI", "Google"],
        statement=(
            "Implement `sigmoid(z)` for a real logit z. "
            "Return 1 / (1 + e^(−z)). For z greater than or equal to 0 evaluate exp(−z). "
            "For negative z evaluate exp(z) / (1 + exp(z)) so the exponential never overflows."
        ),
        constraints=[
            "z is a finite float",
            "Use the stable branch described in the statement",
            "Return a Python float in (0, 1)",
        ],
        fn="sigmoid",
        starter="def sigmoid(z: float) -> float:\n    pass\n",
        hints=[
            "sigmoid(0) is exactly 0.5.",
            "Large positive logits approach 1 and large negative logits approach 0.",
            "Never compute exp of a large positive number; flip the formula when z is negative.",
        ],
        approaches=[
            {
                "name": "Branch on sign",
                "complexity": {"time": "O(1)", "space": "O(1)"},
                "explanation": "The two algebraically equal forms keep the exp argument non-positive.",
            }
        ],
        visible=[
            {"name": "zero", "args": {"z": 0.0}},
            {"name": "positive", "args": {"z": 2.0}},
        ],
        hidden=[
            {"name": "negative", "args": {"z": -2.0}},
            {"name": "large", "args": {"z": 20.0}},
        ],
        editorial=(
            "The logistic function σ(z) = 1 / (1 + e^(−z)) maps a logit to a probability. "
            "Its derivative is σ(z) (1 − σ(z)), which is why logistic regression and sigmoid output layers train with a simple gradient. "
            "A naive exp(−z) overflows when z is a large negative number. Branching so the exponent is always ≤ 0 keeps the value finite and matches the mathematical function."
        ),
        reference=(
            "import math\n\n"
            "def sigmoid(z: float) -> float:\n"
            "    if z >= 0:\n"
            "        ez = math.exp(-z)\n"
            "        return float(1.0 / (1.0 + ez))\n"
            "    ez = math.exp(z)\n"
            "    return float(ez / (1.0 + ez))\n"
        ),
    )

    add(
        title="Softmax",
        slug="ml-softmax",
        difficulty="medium",
        topics=["machine-learning", "deep-learning", "python"],
        companies=["OpenAI", "Anthropic"],
        statement=(
            "Implement `softmax(logits)` for a non-empty list of finite logits. "
            "Subtract the max logit before exponentiating, then divide by the sum of exponentials. "
            "The outputs must be positive and sum to 1. This is the distribution a classifier or attention head predicts."
        ),
        constraints=[
            "1 <= len(logits) <= 10^4",
            "Subtract the max for stability",
            "Return a list of floats",
        ],
        fn="softmax",
        starter="def softmax(logits: list[float]) -> list[float]:\n    pass\n",
        hints=[
            "Subtract max(logits) before calling exp.",
            "Equal logits must produce a uniform distribution.",
            "Do not use a plain sum of exp on raw logits when one value is huge.",
        ],
        approaches=[
            {
                "name": "Max-shifted exp",
                "complexity": {"time": "O(n)", "space": "O(n)"},
                "explanation": "Softmax is shift-invariant. Subtracting the max keeps every exp argument ≤ 0.",
            }
        ],
        visible=[
            {"name": "equal", "args": {"logits": [1.0, 1.0, 1.0]}},
            {"name": "increasing", "args": {"logits": [1.0, 2.0, 3.0]}},
        ],
        hidden=[
            {"name": "dominant", "args": {"logits": [0.0, 0.0, 10.0]}},
            {"name": "pair", "args": {"logits": [0.0, 0.0]}},
        ],
        editorial=(
            "Softmax turns logits z into probabilities pᵢ = e^(zᵢ) / Σⱼ e^(zⱼ). "
            "Adding a constant to every logit does not change p, so subtracting the maximum logit is exact, not an approximation, and it prevents overflow. "
            "The Jacobian of softmax is diag(p) − p pᵀ, which combines with cross-entropy into the beautifully simple gradient p − y. "
            "Attention uses the same map on scaled dot products."
        ),
        reference=(
            "import math\n\n"
            "def softmax(logits: list[float]) -> list[float]:\n"
            "    m = max(logits)\n"
            "    exps = [math.exp(z - m) for z in logits]\n"
            "    s = sum(exps)\n"
            "    return [e / s for e in exps]\n"
        ),
    )

    add(
        title="Binary Cross-Entropy",
        slug="ml-bce",
        difficulty="medium",
        topics=["machine-learning", "metrics", "deep-learning"],
        companies=["Meta", "Google"],
        statement=(
            "Implement `bce(y_true, y_prob)`, the mean binary cross-entropy. "
            "Labels are 0 or 1 and probabilities are in (0, 1). "
            "Clip each probability into the closed range 1e-12 through 1 − 1e-12 before the log, then average "
            "−(y log p + (1 − y) log(1 − p)) over the batch."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Clip probabilities to [1e-12, 1 - 1e-12]",
            "Return the mean, not the sum",
        ],
        fn="bce",
        starter="def bce(y_true: list[float], y_prob: list[float]) -> float:\n    pass\n",
        hints=[
            "Clip before log so a probability of 0 does not yield −inf.",
            "A confident correct prediction contributes almost 0.",
            "Average across the batch.",
        ],
        approaches=[
            {
                "name": "Clipped mean NLL",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "BCE is the negative log likelihood of independent Bernoulli trials.",
            }
        ],
        visible=[
            {"name": "confident-correct", "args": {"y_true": [1.0, 0.0], "y_prob": [0.9, 0.1]}},
            {"name": "uncertain", "args": {"y_true": [1.0, 0.0], "y_prob": [0.5, 0.5]}},
        ],
        hidden=[
            {"name": "overconfident-wrong", "args": {"y_true": [1.0], "y_prob": [0.01]}},
            {"name": "clip-edge", "args": {"y_true": [1.0, 0.0], "y_prob": [1.0, 0.0]}},
        ],
        editorial=(
            "Binary cross-entropy is the negative log likelihood under a Bernoulli model. "
            "It punishes confident wrong answers much harder than squared error on probabilities, which is why classifiers train with log loss. "
            "Clipping keeps the log defined when a model emits an exact 0 or 1. "
            "With a sigmoid output, the gradient of BCE with respect to the logit collapses to p − y, a fact interviewers love."
        ),
        reference=(
            "import math\n\n"
            "def bce(y_true: list[float], y_prob: list[float]) -> float:\n"
            "    eps = 1e-12\n"
            "    total = 0.0\n"
            "    for y, p in zip(y_true, y_prob):\n"
            "        p = min(max(p, eps), 1.0 - eps)\n"
            "        total += -(y * math.log(p) + (1.0 - y) * math.log(1.0 - p))\n"
            "    return float(total / len(y_true))\n"
        ),
    )

    add(
        title="Binary F1 Score",
        slug="ml-f1",
        difficulty="medium",
        topics=["machine-learning", "metrics", "python"],
        companies=["Stripe", "Amazon"],
        statement=(
            "Implement `f1_score(y_true, y_pred)` for binary labels where 1 is the positive class. "
            "Compute precision and recall from true positives, false positives, and false negatives. "
            "Return the harmonic mean 2PR / (P + R). If there are no true positives, return 0.0."
        ),
        constraints=[
            "Labels are 0 or 1",
            "1 <= n <= 10^5",
            "Zero true positives yields 0.0, not an exception",
        ],
        fn="f1_score",
        starter="def f1_score(y_true: list[int], y_pred: list[int]) -> float:\n    pass\n",
        hints=[
            "Count tp, fp, and fn in one pass.",
            "Precision = tp / (tp + fp) and recall = tp / (tp + fn).",
            "If tp is 0, skip the divisions and return 0.",
        ],
        approaches=[
            {
                "name": "Confusion counts",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "F1 is the harmonic mean, so both precision and recall must be high.",
            }
        ],
        visible=[
            {"name": "mixed", "args": {"y_true": [1, 0, 1, 1], "y_pred": [1, 0, 0, 1]}},
            {"name": "no-positive-pred", "args": {"y_true": [1, 0, 1], "y_pred": [0, 0, 0]}},
        ],
        hidden=[
            {"name": "perfect", "args": {"y_true": [1, 0, 1, 0], "y_pred": [1, 0, 1, 0]}},
            {"name": "false-alarms", "args": {"y_true": [0, 0, 0], "y_pred": [1, 0, 1]}},
        ],
        editorial=(
            "Precision asks how many predicted positives were real. Recall asks how many real positives were found. "
            "F1 = 2PR / (P + R) is high only when both are high, which is why it is the default on imbalanced classification. "
            "When tp is 0, precision or recall hits a zero denominator; the conventional score is 0. "
            "This implementation is binary and treats label 1 as positive. Multiclass F1 needs an averaging policy (macro, micro, or weighted) that you should state before coding."
        ),
        reference=(
            "def f1_score(y_true: list[int], y_pred: list[int]) -> float:\n"
            "    tp = fp = fn = 0\n"
            "    for a, b in zip(y_true, y_pred):\n"
            "        if a == 1 and b == 1:\n"
            "            tp += 1\n"
            "        elif a == 0 and b == 1:\n"
            "            fp += 1\n"
            "        elif a == 1 and b == 0:\n"
            "            fn += 1\n"
            "    if tp == 0:\n"
            "        return 0.0\n"
            "    prec = tp / (tp + fp)\n"
            "    rec = tp / (tp + fn)\n"
            "    return float(2 * prec * rec / (prec + rec))\n"
        ),
    )

    add(
        title="One Linear Regression Step",
        slug="ml-linreg-step",
        difficulty="medium",
        topics=["machine-learning", "optimization", "python"],
        companies=["Jane Street", "Google"],
        statement=(
            "Implement `linreg_step(w, x, y, lr)` for one example of linear regression without a separate bias feature "
            "(put a constant 1 in x if you want a bias). "
            "Prediction is the dot product of w and x. "
            "Update each weight by subtracting lr times (prediction − y) times the matching x coordinate. "
            "Return the new weight vector. This is gradient descent on half the squared error."
        ),
        constraints=[
            "len(w) == len(x) >= 1",
            "lr is a positive float",
            "Return a new list; do not require the caller to reuse the old one",
        ],
        fn="linreg_step",
        starter="def linreg_step(w: list[float], x: list[float], y: float, lr: float) -> list[float]:\n    pass\n",
        hints=[
            "Compute the scalar error prediction minus y.",
            "The partial derivative of 0.5 (pred − y)² w.r.t. wᵢ is error * xᵢ.",
            "A zero error must leave w unchanged.",
        ],
        approaches=[
            {
                "name": "SGD on half-square loss",
                "complexity": {"time": "O(d)", "space": "O(d)"},
                "explanation": "One example, one step. Full-batch GD averages this gradient over the dataset.",
            }
        ],
        visible=[
            {"name": "moves", "args": {"w": [0.0, 0.0], "x": [1.0, 2.0], "y": 1.0, "lr": 0.1}},
            {"name": "already-fit", "args": {"w": [0.5, 0.5], "x": [2.0, 2.0], "y": 2.0, "lr": 0.5}},
        ],
        hidden=[
            {"name": "negative-target", "args": {"w": [1.0], "x": [1.0], "y": -1.0, "lr": 0.25}},
            {"name": "bias-feature", "args": {"w": [0.0, 0.0], "x": [1.0, 3.0], "y": 3.0, "lr": 0.1}},
        ],
        editorial=(
            "For a single row, loss L = 0.5 (w · x − y)² has gradient (w · x − y) x. "
            "Subtracting learning-rate times that gradient is stochastic gradient descent. "
            "The leading 0.5 is a convention so the 2 from the chain rule disappears; some texts omit it and fold the 2 into the learning rate. "
            "State which convention you use. A bias term is just a feature that is always 1, which is why this signature has no separate intercept."
        ),
        reference=(
            "def linreg_step(w: list[float], x: list[float], y: float, lr: float) -> list[float]:\n"
            "    pred = sum(wi * xi for wi, xi in zip(w, x))\n"
            "    err = pred - y\n"
            "    return [wi - lr * err * xi for wi, xi in zip(w, x)]\n"
        ),
    )

    add(
        title="Z-Score Standardization",
        slug="ml-zscore",
        difficulty="easy",
        topics=["machine-learning", "statistics", "feature-engineering"],
        companies=["Two Sigma", "Netflix"],
        statement=(
            "Implement `zscore(xs)` using the population standard deviation (divide variance by n, not n − 1). "
            "Return (x − mean) / sd for each element. If the standard deviation is 0, return zeros."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Use population std (divide by n)",
            "Constant input returns zeros",
        ],
        fn="zscore",
        starter="def zscore(xs: list[float]) -> list[float]:\n    pass\n",
        hints=[
            "Compute the mean first.",
            "Variance is the mean of squared deviations, dividing by n.",
            "A symmetric series such as -1, 0, 1 has mean 0.",
        ],
        approaches=[
            {
                "name": "Center then scale",
                "complexity": {"time": "O(n)", "space": "O(n)"},
                "explanation": "Z-scores put features on a common scale without bounding them to 0..1.",
            }
        ],
        visible=[
            {"name": "symmetric", "args": {"xs": [-1.0, 0.0, 1.0]}},
            {"name": "constant", "args": {"xs": [5.0, 5.0]}},
        ],
        hidden=[
            {"name": "shifted", "args": {"xs": [1.0, 2.0, 3.0]}},
            {"name": "single", "args": {"xs": [8.0]}},
        ],
        editorial=(
            "A z-score asks how many population standard deviations a value sits from the mean. "
            "Linear models with L2 penalties need this: a feature measured in millimeters would otherwise dominate one measured in kilometers. "
            "This problem uses the population definition (divide by n), which is what most ML scalers compute on the training column they just saw. "
            "The unbiased sample variance divides by n − 1 and is a statistics-course default, not the usual feature-scaler default. Say which one you used."
        ),
        reference=(
            "import math\n\n"
            "def zscore(xs: list[float]) -> list[float]:\n"
            "    mu = sum(xs) / len(xs)\n"
            "    var = sum((x - mu) ** 2 for x in xs) / len(xs)\n"
            "    sd = math.sqrt(var)\n"
            "    if sd == 0.0:\n"
            "        return [0.0 for _ in xs]\n"
            "    return [(x - mu) / sd for x in xs]\n"
        ),
    )

    add(
        title="Euclidean Distance",
        slug="ml-euclidean",
        difficulty="easy",
        topics=["machine-learning", "linear-algebra", "metrics"],
        companies=["Uber", "Amazon"],
        statement=(
            "Implement `euclidean(a, b)`, the L2 distance between two equal-length vectors. "
            "Return the square root of the sum of squared coordinate differences."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Equal lengths",
            "Distance is non-negative",
        ],
        fn="euclidean",
        starter="def euclidean(a: list[float], b: list[float]) -> float:\n    pass\n",
        hints=[
            "Square each difference before summing.",
            "Take one square root at the end.",
            "A vector compared with itself has distance 0.",
        ],
        approaches=[
            {
                "name": "L2 norm of the difference",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "‖a − b‖₂ is the default metric for k-NN and K-Means in continuous space.",
            }
        ],
        visible=[
            {"name": "3-4-5", "args": {"a": [0.0, 0.0], "b": [3.0, 4.0]}},
            {"name": "same", "args": {"a": [1.0, 2.0], "b": [1.0, 2.0]}},
        ],
        hidden=[
            {"name": "negatives", "args": {"a": [-1.0, -1.0], "b": [-1.0, 1.0]}},
            {"name": "1d", "args": {"a": [2.0], "b": [5.0]}},
        ],
        editorial=(
            "Euclidean distance is the L2 norm of a − b. "
            "K-Means and k-NN use it because it matches the geometry of squared error. "
            "In high dimensions all points become far apart; that is a modeling issue, not a bug in the formula. "
            "If you only need nearest neighbors, compare squared distances and skip the square root."
        ),
        reference=(
            "import math\n\n"
            "def euclidean(a: list[float], b: list[float]) -> float:\n"
            "    return float(math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))))\n"
        ),
    )

    add(
        title="Gini Impurity",
        slug="ml-gini",
        difficulty="medium",
        topics=["machine-learning", "trees", "python"],
        companies=["Microsoft", "Amazon"],
        statement=(
            "Implement `gini(labels)` for a non-empty list of integer class labels. "
            "Return 1 minus the sum of squared class proportions. "
            "A pure node, where every label is the same, has Gini impurity 0."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Labels are integers",
            "Return a Python float",
        ],
        fn="gini",
        starter="def gini(labels: list[int]) -> float:\n    pass\n",
        hints=[
            "Count label frequencies.",
            "Convert each count to a proportion by dividing by n.",
            "A 50/50 binary node has Gini 0.5.",
        ],
        approaches=[
            {
                "name": "Frequency map",
                "complexity": {"time": "O(n)", "space": "O(c)"},
                "explanation": "CART uses Gini because it is cheaper than entropy and similarly ranks splits.",
            }
        ],
        visible=[
            {"name": "pure", "args": {"labels": [1, 1, 1, 1]}},
            {"name": "balanced-binary", "args": {"labels": [0, 0, 1, 1]}},
        ],
        hidden=[
            {"name": "three-class", "args": {"labels": [0, 1, 2, 0]}},
            {"name": "skewed", "args": {"labels": [1, 1, 1, 0]}},
        ],
        editorial=(
            "Gini impurity G = 1 − Σₖ pₖ² is the probability that two labels drawn with replacement from the node disagree. "
            "CART decision trees pick the split that most reduces the weighted Gini of the children. "
            "Entropy ranks splits similarly but needs logarithms. A pure node has p = 1 for one class, so G = 0, and the tree can stop splitting there."
        ),
        reference=(
            "from collections import Counter\n\n"
            "def gini(labels: list[int]) -> float:\n"
            "    n = len(labels)\n"
            "    counts = Counter(labels)\n"
            "    return float(1.0 - sum((c / n) ** 2 for c in counts.values()))\n"
        ),
    )

    add(
        title="Shannon Entropy",
        slug="ml-entropy",
        difficulty="medium",
        topics=["machine-learning", "information-theory", "trees"],
        companies=["DeepMind", "Google"],
        statement=(
            "Implement `entropy(labels)`, the Shannon entropy in bits of the empirical label distribution. "
            "Use log base 2. Skip classes that do not appear. A pure list has entropy 0. "
            "A fair coin of two labels has entropy 1."
        ),
        constraints=[
            "1 <= n <= 10^5",
            "Use log base 2",
            "Return a Python float",
        ],
        fn="entropy",
        starter="def entropy(labels: list[int]) -> float:\n    pass\n",
        hints=[
            "Estimate pₖ as count(k) / n.",
            "Add −p log2(p) for each class that appears.",
            "Do not include a zero-count class; the limit of p log p is 0 but log(0) is undefined.",
        ],
        approaches=[
            {
                "name": "Empirical entropy",
                "complexity": {"time": "O(n)", "space": "O(c)"},
                "explanation": "ID3 and C4.5 split on information gain, which is the drop in this entropy.",
            }
        ],
        visible=[
            {"name": "pure", "args": {"labels": [0, 0, 0]}},
            {"name": "fair-coin", "args": {"labels": [0, 1, 0, 1]}},
        ],
        hidden=[
            {"name": "skewed", "args": {"labels": [1, 1, 1, 0]}},
            {"name": "four-way", "args": {"labels": [0, 1, 2, 3]}},
        ],
        editorial=(
            "Shannon entropy H = − Σ pₖ log₂ pₖ measures surprise in bits. "
            "Decision-tree information gain is the entropy of the parent minus the weighted entropy of the children. "
            "Only observed classes contribute; a missing class has probability 0 and adds nothing. "
            "Natural log gives nats instead of bits. State the base. A balanced two-class node is exactly 1 bit."
        ),
        reference=(
            "import math\n"
            "from collections import Counter\n\n"
            "def entropy(labels: list[int]) -> float:\n"
            "    n = len(labels)\n"
            "    h = 0.0\n"
            "    for c in Counter(labels).values():\n"
            "        p = c / n\n"
            "        h -= p * math.log2(p)\n"
            "    return float(h)\n"
        ),
    )

    add(
        title="k-NN Classify",
        slug="ml-knn-classify",
        difficulty="medium",
        topics=["machine-learning", "classical-ml", "python"],
        companies=["Amazon", "Microsoft"],
        statement=(
            "Implement `knn_predict(train_x, train_y, query, k)`. "
            "Distance is Euclidean. Break distance ties by the smaller training index so the result is deterministic. "
            "Among the k nearest labels, return the majority label. If votes tie, return the smaller label."
        ),
        constraints=[
            "1 <= k <= len(train_x)",
            "Every training row has the same dimension as query",
            "Labels are integers",
        ],
        fn="knn_predict",
        starter=(
            "def knn_predict(train_x: list[list[float]], train_y: list[int], query: list[float], k: int) -> int:\n"
            "    pass\n"
        ),
        hints=[
            "Pair each training row with its distance and its index.",
            "Sort by distance, then by index.",
            "Count votes in the first k rows and break label ties toward the smaller label.",
        ],
        approaches=[
            {
                "name": "Brute force",
                "complexity": {"time": "O(n d + n log n)", "space": "O(n)"},
                "explanation": "Exact k-NN scans the training set. Ball trees and HNSW approximate this when n is large.",
            }
        ],
        visible=[
            {
                "name": "obvious",
                "args": {
                    "train_x": [[0.0, 0.0], [0.1, 0.0], [5.0, 5.0]],
                    "train_y": [0, 0, 1],
                    "query": [0.0, 0.2],
                    "k": 1,
                },
            },
            {
                "name": "majority",
                "args": {
                    "train_x": [[0.0], [0.2], [0.9], [3.0]],
                    "train_y": [1, 1, 0, 0],
                    "query": [0.1],
                    "k": 3,
                },
            },
        ],
        hidden=[
            {
                "name": "label-tie",
                "args": {
                    "train_x": [[0.0], [1.0]],
                    "train_y": [5, 1],
                    "query": [0.5],
                    "k": 2,
                },
            },
            {
                "name": "index-tie",
                "args": {
                    "train_x": [[1.0, 0.0], [0.0, 1.0], [2.0, 2.0]],
                    "train_y": [3, 4, 9],
                    "query": [0.0, 0.0],
                    "k": 1,
                },
            },
        ],
        editorial=(
            "k-NN memorizes the training set and predicts by local vote. "
            "Sorting by (distance, index) makes equal distances deterministic: the earlier training row wins. "
            "Vote ties break toward the smaller label so tests do not depend on dict ordering. "
            "Choose odd k for binary problems when you want to avoid ties, scale features before measuring distance, and remember that prediction cost grows with the training set unless you add an index."
        ),
        reference=(
            "import math\n"
            "from collections import Counter\n\n"
            "def knn_predict(train_x: list[list[float]], train_y: list[int], query: list[float], k: int) -> int:\n"
            "    def dist(a: list[float]) -> float:\n"
            "        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, query)))\n"
            "    ranked = sorted(((dist(x), i, train_y[i]) for i, x in enumerate(train_x)))\n"
            "    votes = Counter(label for _, _, label in ranked[:k])\n"
            "    return int(sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0])\n"
        ),
    )

    add(
        title="K-Means Assignment",
        slug="ml-kmeans-assign",
        difficulty="medium",
        topics=["machine-learning", "clustering", "python"],
        companies=["Netflix", "Uber"],
        statement=(
            "Implement `kmeans_assign(points, centroids)`. "
            "Return the index of the nearest centroid for each point under Euclidean distance. "
            "If two centroids are equally far, choose the smaller index."
        ),
        constraints=[
            "At least one centroid",
            "Points and centroids share a dimension",
            "Ties break toward the smaller index",
        ],
        fn="kmeans_assign",
        starter=(
            "def kmeans_assign(points: list[list[float]], centroids: list[list[float]]) -> list[int]:\n"
            "    pass\n"
        ),
        hints=[
            "This is only the assignment step, not the mean update.",
            "Track the best distance and best index together.",
            "Update the winner only when the new distance is strictly smaller, so earlier centroids win ties.",
        ],
        approaches=[
            {
                "name": "Lloyd assignment",
                "complexity": {"time": "O(n k d)", "space": "O(n)"},
                "explanation": "Lloyd's algorithm alternates this assignment with a mean update.",
            }
        ],
        visible=[
            {
                "name": "two-blobs",
                "args": {
                    "points": [[0.0, 0.0], [0.2, 0.1], [5.0, 5.0]],
                    "centroids": [[0.0, 0.0], [5.0, 5.0]],
                },
            },
            {
                "name": "tie",
                "args": {
                    "points": [[0.0]],
                    "centroids": [[-1.0], [1.0]],
                },
            },
        ],
        hidden=[
            {
                "name": "one-d",
                "args": {
                    "points": [[0.0], [10.0], [3.0]],
                    "centroids": [[1.0], [9.0]],
                },
            },
            {
                "name": "three",
                "args": {
                    "points": [[1.0, 1.0]],
                    "centroids": [[0.0, 0.0], [1.0, 1.0], [8.0, 8.0]],
                },
            },
        ],
        editorial=(
            "K-Means alternates two steps. Assignment gives each point the nearest centroid. Update replaces each centroid with the mean of its points. "
            "This exercise is only assignment. Using a strict less-than when you compare distances makes an equal distance keep the earlier centroid, which is the smaller index if you scan left to right. "
            "Empty clusters are a separate problem: a later update step must reseed them or the algorithm stalls."
        ),
        reference=(
            "import math\n\n"
            "def kmeans_assign(points: list[list[float]], centroids: list[list[float]]) -> list[int]:\n"
            "    def dist(a: list[float], b: list[float]) -> float:\n"
            "        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))\n"
            "    out = []\n"
            "    for p in points:\n"
            "        best_i = 0\n"
            "        best_d = float('inf')\n"
            "        for i, c in enumerate(centroids):\n"
            "            d = dist(p, c)\n"
            "            if d < best_d:\n"
            "                best_d = d\n"
            "                best_i = i\n"
            "        out.append(best_i)\n"
            "    return out\n"
        ),
    )

    add(
        title="Mean Hinge Loss",
        slug="ml-hinge",
        difficulty="medium",
        topics=["machine-learning", "svm", "python"],
        companies=["Google", "Microsoft"],
        statement=(
            "Implement `hinge(y_true, scores)`, the mean hinge loss. "
            "Each label is −1 or +1 and each score is a real decision value. "
            "The per-example loss is max(0, 1 − y * score). Average over the batch."
        ),
        constraints=[
            "Labels are -1 or +1",
            "1 <= n <= 10^5",
            "Return the mean hinge",
        ],
        fn="hinge",
        starter="def hinge(y_true: list[float], scores: list[float]) -> float:\n    pass\n",
        hints=[
            "A correct score with margin at least 1 contributes 0.",
            "Multiply label by score before subtracting from 1.",
            "Negative labels flip the meaning of the score.",
        ],
        approaches=[
            {
                "name": "Margin loss",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "The hinge is the convex surrogate used by linear SVMs.",
            }
        ],
        visible=[
            {"name": "on-margin", "args": {"y_true": [1.0, -1.0], "scores": [1.0, -1.0]}},
            {"name": "violations", "args": {"y_true": [1.0, 1.0], "scores": [0.0, -1.0]}},
        ],
        hidden=[
            {"name": "beyond-margin", "args": {"y_true": [1.0], "scores": [3.0]}},
            {"name": "negative-label", "args": {"y_true": [-1.0, -1.0], "scores": [0.5, -2.0]}},
        ],
        editorial=(
            "Hinge loss max(0, 1 − y s) is zero once the signed score clears a margin of 1, and linear beyond that. "
            "Support vector machines minimize this loss plus an L2 penalty on the weights, which is why only points inside or on the margin become support vectors. "
            "Labels must be −1 and +1, not 0 and 1. If your dataset uses 0/1, map 0 to −1 before calling this function. "
            "The subgradient with respect to the score is −y when the margin is violated and 0 when it is satisfied."
        ),
        reference=(
            "def hinge(y_true: list[float], scores: list[float]) -> float:\n"
            "    total = 0.0\n"
            "    for y, s in zip(y_true, scores):\n"
            "        total += max(0.0, 1.0 - y * s)\n"
            "    return float(total / len(y_true))\n"
        ),
    )

    add(
        title="Scaled Dot-Product Attention Weights",
        slug="ml-attention-weights",
        difficulty="hard",
        topics=["machine-learning", "deep-learning", "transformers"],
        companies=["OpenAI", "Google", "Anthropic"],
        statement=(
            "Implement `attention_weights(query, keys)` for a single query and a list of key vectors, all of dimension d. "
            "Logits are the dot product of the query with each key, divided by sqrt(d). "
            "Return the softmax of those logits. Subtract the max logit inside softmax for stability. "
            "This is one row of scaled dot-product attention before multiplying by values."
        ),
        constraints=[
            "d >= 1 and every key has length d",
            "At least one key",
            "Weights are positive and sum to 1",
        ],
        fn="attention_weights",
        starter=(
            "def attention_weights(query: list[float], keys: list[list[float]]) -> list[float]:\n"
            "    pass\n"
        ),
        hints=[
            "Scale by sqrt(d), not by d.",
            "Softmax is shift-invariant; subtract the max logit.",
            "Identical keys produce a uniform distribution.",
        ],
        approaches=[
            {
                "name": "Scaled dots then softmax",
                "complexity": {"time": "O(n d)", "space": "O(n)"},
                "explanation": "Vaswani et al. scale by sqrt(d) so the variance of the dot product stays stable as dimension grows.",
            }
        ],
        visible=[
            {
                "name": "identical-keys",
                "args": {"query": [1.0, 0.0], "keys": [[1.0, 0.0], [1.0, 0.0]]},
            },
            {
                "name": "prefers-aligned",
                "args": {"query": [1.0, 0.0], "keys": [[1.0, 0.0], [0.0, 1.0]]},
            },
        ],
        hidden=[
            {
                "name": "three",
                "args": {
                    "query": [0.0, 1.0],
                    "keys": [[0.0, 1.0], [0.0, -1.0], [1.0, 0.0]],
                },
            },
            {
                "name": "d-one",
                "args": {"query": [2.0], "keys": [[2.0], [0.0]]},
            },
        ],
        editorial=(
            "Scaled dot-product attention computes softmax(q Kᵀ / √d) and then multiplies by V. "
            "The square-root scale keeps logits from growing like d when components are random with variance 1, which would saturate softmax. "
            "This exercise returns only the weights for one query. The full head is those weights times the value matrix. "
            "Masking, as in causal language models, is implemented by setting illegal logits to a large negative number before the softmax."
        ),
        reference=(
            "import math\n\n"
            "def attention_weights(query: list[float], keys: list[list[float]]) -> list[float]:\n"
            "    scale = math.sqrt(len(query))\n"
            "    logits = [sum(q * k for q, k in zip(query, key)) / scale for key in keys]\n"
            "    m = max(logits)\n"
            "    exps = [math.exp(z - m) for z in logits]\n"
            "    s = sum(exps)\n"
            "    return [e / s for e in exps]\n"
        ),
    )

    add(
        title="Root Mean Squared Error",
        slug="ml-rmse",
        difficulty="easy",
        topics=["machine-learning", "metrics", "python"],
        companies=["Netflix", "Amazon"],
        statement=(
            "Implement `rmse(y_true, y_pred)`. "
            "Return the square root of the mean squared error. "
            "RMSE is in the same units as the target, which makes it easier to explain than MSE."
        ),
        constraints=[
            "Equal non-empty lengths",
            "Return a non-negative float",
            "A perfect prediction has RMSE 0",
        ],
        fn="rmse",
        starter="def rmse(y_true: list[float], y_pred: list[float]) -> float:\n    pass\n",
        hints=[
            "Compute MSE first.",
            "Take the square root once.",
            "Do not average the square roots of absolute residuals; that would be a different metric.",
        ],
        approaches=[
            {
                "name": "Sqrt of MSE",
                "complexity": {"time": "O(n)", "space": "O(1)"},
                "explanation": "RMSE and MSE rank models the same way. RMSE is easier to read.",
            }
        ],
        visible=[
            {"name": "unit-miss", "args": {"y_true": [0.0, 0.0], "y_pred": [1.0, -1.0]}},
            {"name": "perfect", "args": {"y_true": [3.0, 4.0], "y_pred": [3.0, 4.0]}},
        ],
        hidden=[
            {"name": "single", "args": {"y_true": [10.0], "y_pred": [6.0]}},
            {"name": "partial", "args": {"y_true": [1.0, 2.0, 3.0], "y_pred": [1.0, 2.0, 6.0]}},
        ],
        editorial=(
            "RMSE = sqrt( (1/n) Σ (y − ŷ)² ). "
            "Because square root is monotone, the model that wins on MSE wins on RMSE, but the number is interpretable in target units: an RMSE of 2.0 on house prices in hundreds of thousands of dollars is a typical error of about 200,000 dollars. "
            "Outliers still dominate, since the square happens before the root. Use MAE when you want each residual to count linearly."
        ),
        reference=(
            "import math\n\n"
            "def rmse(y_true: list[float], y_pred: list[float]) -> float:\n"
            "    mse = sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)\n"
            "    return float(math.sqrt(mse))\n"
        ),
    )

    return specs


def main() -> None:
    items = build()
    if len(items) != 20:
        raise SystemExit(f"expected 20 problems, got {len(items)}")
    slugs = [p["slug"] for p in items]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("duplicate slugs")
    PROBLEMS.mkdir(parents=True, exist_ok=True)
    for data in items:
        verify(data)
        path = PROBLEMS / f"{data['slug']}.json"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.name}")
    print(f"ok {len(items)} problems")


if __name__ == "__main__":
    main()
