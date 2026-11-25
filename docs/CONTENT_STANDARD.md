# Content Standard (15–20 LPA bar)

Every lesson MDX must meet this bar before the course is considered “done.”

## Required sections (all)

1. Why this matters  
2. Intuition  
3. Core concept in depth (real definitions, not slogans)  
4. Diagram (Mermaid) + dry-run table  
5. Runnable Python (or CLI/architecture walkthrough for pure infra topics)  
6. Complexity / trade-off analysis  
7. Tricks, tips, patterns  
8. Common mistakes and edge cases  
9. Interview notes  
10. Practice problems (linked)  
11. Summary / cheat sheet  
12. Further reading (real URLs)

## Length

- Concept / algorithm / design lessons: **1,200–3,000+ words**  
- Case studies: **1,500–3,500 words**  
- Reject thin surveys under ~1,000 words unless the topic is genuinely trivial setup

## MDX safety

- No unescaped `{` `}` outside fenced code blocks  
- Prefer Unicode math: O(n), Θ, ℝ  

## Problems

- Distinct interview problems (not numbered clones of the same prompt)  
- Full schema: statement, examples, constraints, starter, hints×3, approaches, visible+hidden tests, editorial, reference_solution  

## Course ownership

| Course | Dedicated agent focus |
| --- | --- |
| Python | `content/python/` + `python-ex-*.json` |
| DSA | `content/dsa/` + unique DSA problems |
| System Design | `content/system-design/` |
| Cloud/DevOps | expand `content/cloud-devops/` to depth |
| AI/ML | `content/ai-ml/` + `ml-*.json` |
