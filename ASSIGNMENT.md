# Assignment 8 — Inventory Data Processor

## Description

**Read this entire assignment before you begin, and pay special attention to testing with `test.py`.**

In this assignment, you will build a multifile inventory-processing program that combines the major topics from the most recent unit:

- file input and output;
- structured text records;
- parsing and type conversion;
- lists and tuples;
- linear search;
- Selection Sort;
- binary search;
- copying mutable collections;
- modular program design; and
- local program testing.

The program will read inventory records from a supplied text file, convert those records into an in-memory collection, search the original data, create and sort a copy of the collection, search the sorted data, and write a formatted report to a new output file.

The overall data flow is:

```text
inventory.txt
      ↓
read and parse
      ↓
list of inventory records
      ↓
linear search on original data
      ↓
copy the collection
      ↓
Selection Sort copy by product ID
      ↓
binary search sorted copy by product ID
      ↓
write inventory_report.txt
```

This assignment is designed to reinforce how several individual programming concepts work together inside one coherent application.

---

## Learning Objectives

By completing this assignment, you should be able to:

- read structured records from a text file;
- explain the difference between external file representation and internal program representation;
- parse text fields and convert them to appropriate Python data types;
- represent related data using tuples stored in a list;
- implement Linear Search without using `break`;
- implement Selection Sort using explicit nested loops;
- explain and use in-place sorting;
- preserve original list order by sorting a copy;
- implement iterative Binary Search;
- explain why Binary Search requires sorted data;
- explain why the sort key and search key must agree;
- write formatted results to a new text file;
- preserve the supplied source file;
- use multiple modules with clear responsibilities;
- use supplied local tests throughout development;
- maintain meaningful incremental Git history; and
- use generative AI while retaining responsibility for understanding and verification.

---

## Background

Before beginning this assignment, complete and review:

- **File I/O Part I** lecture and notes;
- **File I/O Part II** lecture and notes;
- **Searching** lecture and notes;
- **Sorting** lecture and notes;
- **Modularity and Multifile Programs Part I and II** lecture and notes;
- the course [Best Practices for Procedural Programming](https://katrompas.accprofessors.com/best-practice-procedural-programming);
- the course [Commenting Guidelines](https://katrompas.accprofessors.com/commenting);
- the [.gitignore Guidelines](https://katrompas.accprofessors.com/gitignore-guidelines);
- the [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines); and
- the course [Commit Guidelines](https://katrompas.accprofessors.com/committing).

This assignment assumes that you already understand:

- functions and function contracts;
- `main()` as the application driver;
- imports and module namespaces;
- lists and tuples;
- mutability and copying;
- loops and nested loops;
- algorithmic efficiency using Big O;
- and the course rule of no more than one `return` statement per function.

---

# Starter Repository

Your starter repository contains:

```text
ASSIGNMENT.md
ESSAY.md
README.md
.gitignore
main.py
algorithms.py
inventory_io.py
inventory.txt
test.py
```

Do not rename these files.

Do not modify:

```text
inventory.txt
test.py
```

The starter source files provide:

- the required module architecture;
- required function names and parameter lists;
- comments identifying major responsibilities;
- incomplete function implementations; and
- incomplete documentation that you must finish according to course standards.

---

# Part I — Required Inventory Data

The supplied file:

```text
inventory.txt
```

contains:

```text
1042,Keyboard,79.99,12
1007,Mouse,24.50,31
1098,Webcam,89.50,6
1015,USB Hub,54.95,17
1077,Monitor Arm,59.95,9
1024,Desk Lamp,29.50,18
1112,Laptop Dock,129.95,8
1056,Office Chair,199.99,5
```

Each line represents one inventory record in this format:

```text
product_id,product_name,price,quantity
```

For example:

```text
1077,Monitor Arm,59.95,9
```

must become this Python tuple:

```python
(1077, "Monitor Arm", 59.95, 9)
```

with these types:

```text
int, str, float, int
```

The input file is guaranteed to contain valid records in the required format.

You are **not** required to validate malformed records in this assignment.

Do not modify `inventory.txt`.

---

# Part II — Project Architecture

The program uses three Python source modules:

```text
main.py
    application driver and orchestration

inventory_io.py
    file reading, parsing, and report writing

algorithms.py
    searching and sorting algorithms
```

The intended dependency structure is:

```text
main.py
   |
   +----> inventory_io.py
   |
   +----> algorithms.py
```

`main.py` is the application driver.

Supporting modules must not start the application when imported.

---

# Part III — `inventory_io.py`

This module owns the program's file input and output behavior.

It contains two required functions.

---

## `read_inventory(filename)`

Required interface:

```python
read_inventory(filename)
```

This function must:

- open the supplied file for reading;
- read the file line by line;
- remove the line ending;
- split each record using the comma delimiter;
- convert the product ID to `int`;
- keep the product name as `str`;
- convert the price to `float`;
- convert the quantity to `int`;
- create a tuple in this form:

  ```python
  (product_id, product_name, price, quantity)
  ```

- append each tuple to a list;
- return the completed list;
- contain no more than one `return` statement; and
- not print anything.

Use the normal course file pattern:

```python
with open(filename, "r") as file:
```

The function must work with alternate valid inventory files, not only the supplied `inventory.txt`.

Do not hardcode the required records.

---

## `write_report(...)`

Required interface:

```python
write_report(
    filename,
    original_records,
    sorted_records,
    target_id,
    linear_index,
    binary_index,
)
```

This function must:

- open the supplied output filename using write mode;
- create or replace the report file;
- use the supplied arguments rather than recalculating searches or sorting;
- display information about the Linear Search result;
- display information about the Binary Search result;
- display all records in original file order;
- display all records sorted by product ID;
- format prices with exactly two digits after the decimal point;
- return no calculated result;
- contain no more than one `return` statement; and
- not modify either supplied collection.

The function should use:

```python
with open(filename, "w") as file:
```

The output file is a generated report, so overwriting the previous report is the correct behavior.

---

# Part IV — `algorithms.py`

This module contains the required searching and sorting algorithms.

Do not replace these algorithms with Python built-ins.

---

## `linear_search_by_id(records, target_id)`

Required interface:

```python
linear_search_by_id(records, target_id)
```

This function must:

- search the collection by product ID;
- return the matching list index;
- return `-1` when the target does not exist;
- use an explicit `while` loop;
- stop when either:
  - the target is found; or
  - there are no more records to inspect;
- contain no more than one `return` statement;
- not modify the collection; and
- not print anything.

Use the course-style continuation logic discussed in the Searching lecture.

Do not use:

- `break`;
- `continue`;
- `list.index()`;
- `in` as a substitute for the required algorithm; or
- another built-in searching technique.

---

## `selection_sort_by_id(records)`

Required interface:

```python
selection_sort_by_id(records)
```

This function must:

- implement Selection Sort;
- sort the supplied list **in place**;
- sort records in ascending order by product ID;
- use nested explicit `for` loops;
- maintain the position of the smallest remaining record;
- perform the required swap after each outer pass;
- return no new collection;
- contain no more than one `return` statement; and
- not print anything.

Do not use:

```python
sorted(...)
```

or:

```python
list.sort()
```

The purpose of this function is to implement and understand the Selection Sort algorithm.

---

## `binary_search_by_id(records, target_id)`

Required interface:

```python
binary_search_by_id(records, target_id)
```

This function must:

- search by product ID;
- assume the supplied records are already sorted in ascending order by product ID;
- implement iterative Binary Search using:
  - `low`;
  - `high`;
  - `middle`;
- return the matching list index;
- return `-1` when the target does not exist;
- use a `while` loop;
- contain no more than one `return` statement;
- not modify the collection; and
- not print anything.

Do not use:

- recursion;
- `break`;
- `continue`;
- built-in search substitutes; or
- sorting inside the search function.

### Important Precondition

Binary Search only works correctly when the collection is sorted by the same key being searched.

For this assignment:

```text
sort key   = product ID
search key = product ID
```

---

# Part V — `main.py`

`main.py` is the application driver.

Use:

```python
target_id = 1077
```

Do not change the final search target.

Complete `main()` so that it performs these operations in this order:

1. read `inventory.txt`;
2. perform Linear Search on the original records;
3. create a copy of the original record list;
4. Selection Sort the copied list by product ID;
5. perform Binary Search on the sorted copy;
6. write the complete report to:

   ```text
   inventory_report.txt
   ```

7. display this confirmation message:

   ```text
   Report written to inventory_report.txt.
   ```

The program should use the required module namespaces:

```python
inventory_io.function_name(...)
algorithms.function_name(...)
```

Do not move file-I/O or algorithm implementations into `main.py`.

The standard run guard is required:

```python
if __name__ == "__main__":
    main()
```

---

# Part VI — Preserve the Original Order

Selection Sort modifies its list argument.

The original inventory data must remain in its original file order for the report.

Therefore, before sorting, create a copy:

```python
sorted_records = records.copy()
```

Then sort:

```python
algorithms.selection_sort_by_id(sorted_records)
```

Do not sort the original `records` list.

After sorting:

```text
records
```

must still represent the original file order, while:

```text
sorted_records
```

must represent ascending product-ID order.

---

# Part VII — Required Program Behavior

Running:

```bash
python main.py
```

must display:

```text
Report written to inventory_report.txt.
```

The program must also create:

```text
inventory_report.txt
```

with this content **exactly** as shown:

```text
Inventory Search and Sort Report

Records Loaded: 8
Search Target: 1077

Linear Search
Original index: 4
Product: Monitor Arm
Price: $59.95
Quantity: 9

Binary Search
Sorted index: 5
Product: Monitor Arm
Price: $59.95
Quantity: 9

Original File Order
1042 | Keyboard | $79.99 | 12
1007 | Mouse | $24.50 | 31
1098 | Webcam | $89.50 | 6
1015 | USB Hub | $54.95 | 17
1077 | Monitor Arm | $59.95 | 9
1024 | Desk Lamp | $29.50 | 18
1112 | Laptop Dock | $129.95 | 8
1056 | Office Chair | $199.99 | 5

Sorted by Product ID
1007 | Mouse | $24.50 | 31
1015 | USB Hub | $54.95 | 17
1024 | Desk Lamp | $29.50 | 18
1042 | Keyboard | $79.99 | 12
1056 | Office Chair | $199.99 | 5
1077 | Monitor Arm | $59.95 | 9
1098 | Webcam | $89.50 | 6
1112 | Laptop Dock | $129.95 | 8
```

Do not hardcode the report contents.

The report must be produced from the data read from the file and the results calculated by the program.

---

# Part VIII — Supplied Tests

The repository contains:

```text
test.py
```

Do not modify it.

Run:

```bash
python test.py
```

or:

```bash
python3 test.py
```

depending on your system.

The supplied test module verifies:

- required project files;
- required function names and signatures;
- safe module imports;
- the standard run guard;
- inventory parsing and field types;
- Linear Search behavior;
- required Linear Search loop structure;
- Selection Sort behavior;
- in-place sorting;
- preservation of inventory records;
- nested Selection Sort structure;
- prohibition of `sort()` and `sorted()`;
- preservation of original order when sorting a copy;
- Binary Search behavior;
- required Binary Search loop structure;
- the single-return rule;
- report-file contents; and
- complete application behavior.

Your final program should report:

```text
15/15 tests passed
```

Passing all supplied tests is necessary, but it does not represent the complete assignment grade.

The tests do not evaluate every requirement, including:

- documentation quality;
- README quality;
- ESSAY responses;
- Git history;
- code clarity; and
- your understanding of the submitted work.

There is **no Classroom 50 autograding** for this assignment.

### Run the supplied tests locally throughout development.

---

# Part IX — Programming Standards and Constraints

The normal course standards apply.

In particular:

- each source file must contain the required file header documentation;
- every function must contain a course-standard function docstring;
- each function may contain no more than one `return` statement;
- computational functions return rather than print;
- supporting modules must not unexpectedly execute application behavior when imported;
- dependencies should be explicit;
- avoid global program state;
- preserve the supplied input file;
- keep `main.py` as the application driver;
- and use the supplied module architecture.

Do not use:

- `while True`;
- `break`;
- `continue`;
- recursion;
- classes;
- lambda expressions;
- comprehensions as substitutes for the required searching or sorting algorithms;
- `list.index()` as a search substitute;
- `sorted()` as a sorting substitute;
- `list.sort()` as a sorting substitute;
- additional third-party libraries; or
- additional user-defined functions unless specifically approved.

---

# Part X — Documentation Requirements

Complete all source-file and function documentation according to the course Commenting Guidelines.

Function docstrings must begin with a short description and then use the course-standard fields:

```python
"""
Short description of what the function does.

:param: ...
:raises: ...
:return: ...
:note: ...
"""
```

Use wording appropriate to the actual function.

Do not copy generic descriptions that do not explain the function's real contract.

Remove all instructional comments that tell you to complete documentation before submitting.

---

# Part XI — Git and Development Process

Develop incrementally.

Do not complete the entire project and then make one final program commit.

Your repository must contain **at least ten meaningful program-development commits**.

Ten is the minimum, not the target.

Natural milestones may include:

- completing inventory-file parsing;
- implementing Linear Search;
- testing Linear Search;
- implementing Selection Sort;
- testing and correcting Selection Sort;
- preserving original order using a copy;
- implementing Binary Search;
- testing Binary Search;
- implementing report output;
- integrating modules through the driver;
- correcting a real test failure; or
- another coherent program improvement.

Changes only to:

```text
README.md
ESSAY.md
```

do not count toward the required program-development commits.

Do not manufacture meaningless commits merely to reach the minimum.

Test before committing.

Push regularly.

---

# Part XII — Generative AI

Use of generative AI is required.

You may use AI as a:

- tutor;
- programming partner;
- algorithm explanation tool;
- debugging assistant;
- design critic;
- testing assistant; or
- documentation assistant.

You may show AI the complete assignment and supplied `test.py`.

You remain responsible for:

- understanding every line of submitted code;
- preserving the required algorithms rather than replacing them with built-ins;
- recognizing when AI suggests code outside the assignment requirements;
- interpreting test failures;
- verifying file behavior;
- verifying search and sort correctness;
- making final implementation decisions; and
- explaining your work in `ESSAY.md`.

AI may suggest:

- `break`;
- `list.index()`;
- `sorted()`;
- `list.sort()`;
- recursive Binary Search;
- lambda expressions;
- built-in CSV parsing; or
- other valid techniques that violate this assignment's learning requirements.

Follow the assignment contract.

---

# Part XIII — `README.md`

Complete the supplied README according to the course [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines).

Your README should accurately describe:

- what the program does;
- the role of each source module;
- the supplied input file;
- the generated output file;
- how to run the program;
- how to run the supplied tests; and
- any other information required by the course README standard.

---

# Part XIV — `ESSAY.md`

Complete all five supplied reflection questions.

Your answers must refer to your actual implementation and demonstrate substantive reasoning.

Short, generic responses will not receive full credit.

---

# Final Review and Submission

Before submitting:

### 1. Run the complete program

```bash
python main.py
```

Verify that the console displays:

```text
Report written to inventory_report.txt.
```

### 2. Inspect the generated report

Open:

```text
inventory_report.txt
```

and verify the required content and ordering.

### 3. Verify the source file

Confirm that:

```text
inventory.txt
```

has not been modified.

### 4. Run the supplied tests

```bash
python test.py
```

Verify:

```text
15/15 tests passed
```

### 5. Check Git status

```bash
git status
```

Your working tree should be clean.

### 6. Review development history

```bash
git log --oneline
```

Verify that your history shows meaningful incremental development and contains at least **ten** qualifying program-development commits.

### 7. Review the repository

Confirm that the repository contains:

```text
ASSIGNMENT.md
ESSAY.md
README.md
.gitignore
main.py
algorithms.py
inventory_io.py
inventory.txt
test.py
```

The generated:

```text
inventory_report.txt
```

may also be present in your completed repository if required by your instructor.

### 8. Review documentation

Verify that:

- all instructional documentation comments have been removed;
- every function uses the course-standard docstring format;
- the README is complete;
- the ESSAY is complete; and
- temporary debugging code has been removed.

### 9. Submit through Blackboard

Submit the normal HTTPS URL of the completed GitHub repository in Blackboard.
