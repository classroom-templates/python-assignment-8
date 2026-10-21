# Assignment 8 — Reflection

Answer each question clearly, specifically, and in your own words.

Your responses must demonstrate **depth of thought and actual engagement with your project**.

Short, vague, or generic answers will not receive full credit.

Whenever possible, refer to specific files, functions, data, test results, or behavior from your own completed program.

Each question is worth **2 points**, for a total of **10 points**.

---

## 1. External Representation and Internal Representation

The supplied inventory file contains records such as:

```text
1077,Monitor Arm,59.95,9
```

Inside your program, that line becomes:

```python
(1077, "Monitor Arm", 59.95, 9)
```

Explain the difference between these two representations.

Your answer must explain:

- why the file contents are initially text;
- why the product ID, price, and quantity must be converted;
- why the tuple representation is more useful for the program; and
- what `read_inventory()` is doing conceptually when it performs this conversion.

---

## 2. Preserving Original Order

Your program creates a copy before sorting:

```python
sorted_records = records.copy()
```

Explain why this is necessary.

Your answer must discuss:

- the fact that `selection_sort_by_id()` sorts in place;
- what would happen if you sorted `records` directly;
- why the report needs both original file order and sorted order; and
- how this example relates to mutability and copying.

Refer to the behavior of your own completed program.

---

## 3. Linear Search vs. Binary Search

Your program searches for the same product ID twice:

- once using Linear Search on the original records; and
- once using Binary Search on the sorted records.

Explain why Linear Search can operate correctly on the original unsorted records while Binary Search cannot.

Your answer must explain:

- how Linear Search examines the data;
- why Binary Search depends on ordering;
- why the records must be sorted by **product ID** specifically; and
- why sorting the records by another field, such as price or product name, would not satisfy the Binary Search precondition when searching by product ID.

---

## 4. Algorithmic Efficiency and Engineering Tradeoffs

For this assignment:

```text
Linear Search      O(n)
Selection Sort     O(n²)
Binary Search      O(log n)
```

Explain what these classifications mean at the introductory level.

Then consider this question:

> If a program had unsorted data and needed to perform only one search, would sorting the entire collection solely so that it could use Binary Search necessarily be a good engineering decision?

Explain why or why not.

Your answer should distinguish between:

- the cost of searching;
- the cost of preparing the data by sorting; and
- a situation in which sorting once and then using Binary Search repeatedly could make more sense.

Do not answer only by repeating the Big O labels.

---

## 5. Selection Sort vs. Insertion Sort

You learned both Selection Sort and Insertion Sort, but this assignment requires Selection Sort.

Explain how the two algorithms differ conceptually.

Your answer must describe:

- how Selection Sort builds the sorted region;
- how Insertion Sort builds the sorted region;
- the major difference in how values are moved;
- why both are classified as O(n²) in the general introductory analysis used in this course; and
- one situation in which Insertion Sort may perform less work than Selection Sort.

You are not being asked to implement Insertion Sort in this assignment.

The purpose of this question is to demonstrate that you understand both algorithms and can compare their behavior.
