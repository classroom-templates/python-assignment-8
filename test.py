#!/usr/bin/env python3

"""Assignment 8 — Supplied Tests

This instructor-supplied module provides local tests for Assignment 8 and also
serves as an example of a separate testing module.

Run this test module from the project directory with:

    python test.py

or, on systems where Python 3 is named explicitly:

    python3 test.py

These tests are part of the Assignment 8 contract.

You are allowed and encouraged to read this file. The tests show you what
interfaces, behaviors, and selected structural requirements your program is
expected to satisfy.

DO NOT MODIFY THIS FILE.

This file is also intended to serve as an example of a properly structured test
module at your current level of understanding.

Notice several design ideas in this file:

- testing code is kept separate from the program being tested;
- application modules are imported and tested independently;
- alternate data is used so hardcoded answers do not pass;
- temporary files allow file input/output to be tested safely;
- structural requirements can be inspected with Python's `ast` module;
- mutation and preservation of data can both be checked;
- complete-program behavior can be verified without changing the application.

You are not expected to reproduce all of these techniques from memory yet.
The purpose is to continue recognizing how tests can verify both behavior and
selected design requirements.

Passing all supplied tests is necessary, but it is not the same as earning a
perfect assignment grade. The tests do not evaluate every course requirement,
including documentation quality, README quality, ESSAY responses, Git history,
or your understanding of the submitted work.

Use the tests throughout development:

    complete a small capability
    run test.py
    read the results
    reason about any failure
    correct your program
    test again

The goal is not merely to make every line say PASS.

The goal is to understand why it passes."""

import ast
import importlib
import io
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "main.py",
    "algorithms.py",
    "inventory_io.py",
    "inventory.txt",
]

REQUIRED_FUNCTIONS = {
    "algorithms": {
        "linear_search_by_id": ["records", "target_id"],
        "selection_sort_by_id": ["records"],
        "binary_search_by_id": ["records", "target_id"],
    },
    "inventory_io": {
        "read_inventory": ["filename"],
        "write_report": [
            "filename",
            "original_records",
            "sorted_records",
            "target_id",
            "linear_index",
            "binary_index",
        ],
    },
    "main": {
        "main": [],
    },
}


def normalize_output(text):
    """
        Normalize line endings and trailing whitespace for reliable text comparison.

        :param: text - Output or file-content string to normalize.
        :raises: none
        :return: Normalized string.
        :note: Used to make comparisons consistent across operating systems.
        """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    result = "\n".join(
        line.rstrip() for line in text.strip().splitlines()
    )

    return result


def load_tree(filename):
    """
        Read and parse one Python source file for structural testing.

        :param: filename - Python source filename located in the project directory.
        :raises: AssertionError if the file is missing or contains a syntax error.
        :return: Tuple containing the source text and parsed abstract syntax tree.
        :note: none
        """
    path = PROJECT_DIR / filename

    if not path.exists():
        raise AssertionError(f"{filename} was not found.")

    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise AssertionError(
            f"{filename} has a syntax error on line "
            f"{exc.lineno}: {exc.msg}"
        ) from exc

    return source, tree


def get_function_nodes(tree):
    """
        Collect the top-level function definitions from a parsed Python module.

        :param: tree - Parsed Python abstract syntax tree.
        :raises: none
        :return: Dictionary mapping function names to their AST nodes.
        :note: Only top-level function definitions are collected.
        """
    functions = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = node

    return functions


def import_module_safely(module_name):
    """
        Import a project module while capturing unexpected output during import.

        :param: module_name - Importable project-module name without the .py suffix.
        :raises: AssertionError if the module cannot be imported.
        :return: Tuple containing the imported module and captured standard output.
        :note: none
        """
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))

    if module_name in sys.modules:
        del sys.modules[module_name]

    captured = io.StringIO()

    try:
        with redirect_stdout(captured):
            module = importlib.import_module(module_name)
    except Exception as exc:
        raise AssertionError(
            f"{module_name}.py could not be imported: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    return module, captured.getvalue()


def count_returns(function_node):
    """
        Count the return statements contained in one function.

        :param: function_node - AST node representing a function definition.
        :raises: none
        :return: Integer number of return statements found.
        :note: Used to verify the course single-return rule.
        """
    count = 0

    for node in ast.walk(function_node):
        if isinstance(node, ast.Return):
            count += 1

    return count


def contains_loop(function_node, loop_type=None):
    """
        Determine whether a function contains the requested explicit loop type.

        :param: function_node - AST function node; loop_type - "for", "while", or None.
        :raises: none
        :return: True if the requested loop is present; otherwise False.
        :note: When loop_type is None, either a for or while loop is accepted.
        """
    result = False

    for node in ast.walk(function_node):
        if loop_type == "for":
            matches = isinstance(node, ast.For)
        elif loop_type == "while":
            matches = isinstance(node, ast.While)
        else:
            matches = isinstance(node, (ast.For, ast.While))

        if matches:
            result = True

    return result


def contains_break_or_continue(function_node):
    """
        Determine whether a function contains break or continue statements.

        :param: function_node - AST node representing a function definition.
        :raises: none
        :return: True if break or continue appears; otherwise False.
        :note: Used to enforce the course loop-control standard.
        """
    result = False

    for node in ast.walk(function_node):
        if isinstance(node, (ast.Break, ast.Continue)):
            result = True

    return result


def called_simple_names(function_node):
    """
        Collect simple function names called directly inside a function.

        :param: function_node - AST node representing a function definition.
        :raises: none
        :return: Set of directly called simple function names.
        :note: Attribute-style calls such as object.method() are not included.
        """
    calls = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)

    return calls


def has_standard_run_guard(tree):
    """
        Check whether a module contains the standard course run guard.

        :param: tree - Parsed abstract syntax tree for main.py.
        :raises: none
        :return: True if the standard run guard calls main(); otherwise False.
        :note: The expected form is if __name__ == "__main__": main().
        """
    result = False

    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test

            correct_test = (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            )

            if correct_test and len(node.body) == 1:
                statement = node.body[0]

                correct_call = (
                    isinstance(statement, ast.Expr)
                    and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name)
                    and statement.value.func.id == "main"
                    and not statement.value.args
                    and not statement.value.keywords
                )

                if correct_call:
                    result = True

    return result


def write_temp_inventory(directory, text):
    """
        Create an alternate inventory file for isolated file-I/O testing.

        :param: directory - Directory for the file; text - contents to write.
        :raises: OSError if the file cannot be written.
        :return: Path to the created temporary inventory file.
        :note: Creates inventory_alt.txt inside the supplied directory.
        """
    path = Path(directory) / "inventory_alt.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_01_required_files():
    """
        Verify that all required Assignment 8 project files exist.

        :param: none
        :raises: AssertionError if a required project file is missing.
        :return: None
        :note: none
        """
    for filename in REQUIRED_FILES:
        assert (PROJECT_DIR / filename).exists(), (
            f"Missing required file: {filename}"
        )


def test_02_required_functions_and_signatures():
    """
        Verify required functions and their exact parameter lists.

        :param: none
        :raises: AssertionError if a required function or signature is incorrect.
        :return: None
        :note: none
        """
    for module_name, functions in REQUIRED_FUNCTIONS.items():
        _, tree = load_tree(f"{module_name}.py")
        nodes = get_function_nodes(tree)

        for name, expected_parameters in functions.items():
            assert name in nodes, (
                f"Missing required function: "
                f"{module_name}.{name}()"
            )

            actual_parameters = [
                argument.arg
                for argument in nodes[name].args.args
            ]

            assert actual_parameters == expected_parameters, (
                f"{module_name}.{name}() must use parameters "
                f"({', '.join(expected_parameters)})."
            )

            assert nodes[name].args.vararg is None, (
                f"{module_name}.{name}() must not use *args."
            )

            assert nodes[name].args.kwarg is None, (
                f"{module_name}.{name}() must not use **kwargs."
            )


def test_03_run_guard_and_safe_imports():
    """
        Verify the standard run guard and confirm project modules import safely.

        :param: none
        :raises: AssertionError if the run guard is incorrect or an import produces output.
        :return: None
        :note: none
        """
    _, main_tree = load_tree("main.py")

    assert has_standard_run_guard(main_tree), (
        'Expected the standard run guard in main.py:\n'
        'if __name__ == "__main__":\n'
        '    main()'
    )

    for module_name in [
        "algorithms",
        "inventory_io",
        "main",
    ]:
        _, import_output = import_module_safely(module_name)

        assert normalize_output(import_output) == "", (
            f"Importing {module_name}.py produced output. "
            "The application should not run when imported."
        )


def test_04_read_inventory_parses_records_and_types():
    """
        Verify that read_inventory() parses alternate data into the required records.

        :param: none
        :raises: AssertionError if parsed values or field types are incorrect.
        :return: None
        :note: Uses a temporary alternate input file so hardcoded answers do not pass.
        """
    inventory_io, _ = import_module_safely("inventory_io")

    with tempfile.TemporaryDirectory() as temp_dir:
        path = write_temp_inventory(
            temp_dir,
            "3003,Camera,125.50,4\n"
            "1001,Cable,9.99,27\n"
            "2002,Stand,42.00,8\n"
        )

        records = inventory_io.read_inventory(path)

    expected = [
        (3003, "Camera", 125.50, 4),
        (1001, "Cable", 9.99, 27),
        (2002, "Stand", 42.00, 8),
    ]

    assert records == expected, (
        "read_inventory() did not parse the alternate file correctly."
    )

    assert isinstance(records, list)

    for record in records:
        assert isinstance(record, tuple)
        assert len(record) == 4
        assert isinstance(record[0], int)
        assert isinstance(record[1], str)
        assert isinstance(record[2], float)
        assert isinstance(record[3], int)


def test_05_linear_search_behavior():
    """
        Verify linear search for targets in several positions and for an absent ID.

        :param: none
        :raises: AssertionError if linear search returns an incorrect index.
        :return: None
        :note: Tests first, middle, last, and absent product IDs.
        """
    algorithms, _ = import_module_safely("algorithms")

    records = [
        (30, "C", 3.0, 3),
        (10, "A", 1.0, 1),
        (40, "D", 4.0, 4),
        (20, "B", 2.0, 2),
    ]

    assert algorithms.linear_search_by_id(records, 30) == 0
    assert algorithms.linear_search_by_id(records, 40) == 2
    assert algorithms.linear_search_by_id(records, 20) == 3
    assert algorithms.linear_search_by_id(records, 999) == -1


def test_06_linear_search_required_structure():
    """
        Verify that linear search uses the required while-loop structure.

        :param: none
        :raises: AssertionError if the function lacks the required while loop or uses break/continue.
        :return: None
        :note: none
        """
    _, tree = load_tree("algorithms.py")
    node = get_function_nodes(tree)["linear_search_by_id"]

    assert contains_loop(node, "while"), (
        "linear_search_by_id() must use the required while-loop form."
    )

    assert not contains_break_or_continue(node), (
        "linear_search_by_id() must not use break or continue."
    )


def test_07_selection_sort_behavior():
    """
        Verify Selection Sort with ordinary, sorted, and reverse-sorted records.

        :param: none
        :raises: AssertionError if the records are not sorted correctly by product ID.
        :return: None
        :note: none
        """
    algorithms, _ = import_module_safely("algorithms")

    ordinary = [
        (30, "C", 3.0, 3),
        (10, "A", 1.0, 1),
        (40, "D", 4.0, 4),
        (20, "B", 2.0, 2),
    ]
    algorithms.selection_sort_by_id(ordinary)
    assert [record[0] for record in ordinary] == [10, 20, 30, 40]

    already_sorted = [
        (10, "A", 1.0, 1),
        (20, "B", 2.0, 2),
        (30, "C", 3.0, 3),
    ]
    algorithms.selection_sort_by_id(already_sorted)
    assert [record[0] for record in already_sorted] == [10, 20, 30]

    reverse_sorted = [
        (30, "C", 3.0, 3),
        (20, "B", 2.0, 2),
        (10, "A", 1.0, 1),
    ]
    algorithms.selection_sort_by_id(reverse_sorted)
    assert [record[0] for record in reverse_sorted] == [10, 20, 30]


def test_08_selection_sort_in_place_and_preserves_records():
    """
        Verify that Selection Sort mutates the supplied list without losing records.

        :param: none
        :raises: AssertionError if the function returns a new collection, loses records, or fails to mutate in place.
        :return: None
        :note: Sorting may change order but must not change collection membership.
        """
    algorithms, _ = import_module_safely("algorithms")

    records = [
        (30, "C", 3.0, 3),
        (10, "A", 1.0, 1),
        (20, "B", 2.0, 2),
    ]
    original_id = id(records)
    original_members = sorted(records)

    result = algorithms.selection_sort_by_id(records)

    assert id(records) == original_id, (
        "selection_sort_by_id() must sort the supplied list in place."
    )

    assert result is None, (
        "selection_sort_by_id() should not return a new collection."
    )

    assert sorted(records) == original_members, (
        "Sorting must not add, remove, or alter inventory records."
    )


def test_09_selection_sort_required_structure():
    """
        Verify the required nested-loop Selection Sort implementation.

        :param: none
        :raises: AssertionError if nested loops are missing or prohibited sorting/control-flow features are used.
        :return: None
        :note: Prohibits sorted(), list.sort(), break, and continue.
        """
    source, tree = load_tree("algorithms.py")
    node = get_function_nodes(tree)["selection_sort_by_id"]

    assert contains_loop(node, "for"), (
        "selection_sort_by_id() must use explicit for loops."
    )

    # Require at least two for-loop nodes in the function.
    for_count = sum(
        1 for item in ast.walk(node)
        if isinstance(item, ast.For)
    )

    assert for_count >= 2, (
        "selection_sort_by_id() must use the nested-loop "
        "Selection Sort algorithm."
    )

    calls = called_simple_names(node)

    assert "sorted" not in calls, (
        "Do not use sorted() in selection_sort_by_id()."
    )

    # Attribute-style .sort() calls.
    for item in ast.walk(node):
        if isinstance(item, ast.Call):
            if isinstance(item.func, ast.Attribute):
                assert item.func.attr != "sort", (
                    "Do not use list.sort() in selection_sort_by_id()."
                )

    assert not contains_break_or_continue(node), (
        "selection_sort_by_id() must not use break or continue."
    )


def test_10_original_order_can_be_preserved_with_copy():
    """
        Verify that sorting a copied list preserves the original record order.

        :param: none
        :raises: AssertionError if the original list changes or the copied list is sorted incorrectly.
        :return: None
        :note: Reinforces copying and in-place mutation.
        """
    algorithms, _ = import_module_safely("algorithms")

    records = [
        (30, "C", 3.0, 3),
        (10, "A", 1.0, 1),
        (20, "B", 2.0, 2),
    ]

    original_snapshot = records.copy()
    sorted_records = records.copy()

    algorithms.selection_sort_by_id(sorted_records)

    assert records == original_snapshot, (
        "The original records should remain unchanged when a copy is sorted."
    )

    assert [record[0] for record in sorted_records] == [10, 20, 30]


def test_11_binary_search_behavior():
    """
        Verify binary search for first, middle, last, and absent product IDs.

        :param: none
        :raises: AssertionError if binary search returns an incorrect index.
        :return: None
        :note: The supplied records are already sorted by product ID.
        """
    algorithms, _ = import_module_safely("algorithms")

    records = [
        (10, "A", 1.0, 1),
        (20, "B", 2.0, 2),
        (30, "C", 3.0, 3),
        (40, "D", 4.0, 4),
        (50, "E", 5.0, 5),
    ]

    assert algorithms.binary_search_by_id(records, 10) == 0
    assert algorithms.binary_search_by_id(records, 30) == 2
    assert algorithms.binary_search_by_id(records, 50) == 4
    assert algorithms.binary_search_by_id(records, 35) == -1


def test_12_binary_search_required_structure():
    """
        Verify that binary search uses the required iterative while-loop design.

        :param: none
        :raises: AssertionError if iterative logic is missing, break/continue is used, or the function sorts internally.
        :return: None
        :note: none
        """
    _, tree = load_tree("algorithms.py")
    node = get_function_nodes(tree)["binary_search_by_id"]

    assert contains_loop(node, "while"), (
        "binary_search_by_id() must use an iterative while loop."
    )

    assert not contains_break_or_continue(node), (
        "binary_search_by_id() must not use break or continue."
    )

    calls = called_simple_names(node)

    assert "sorted" not in calls, (
        "binary_search_by_id() must search the supplied sorted data, "
        "not sort it internally."
    )


def test_13_single_return_rule():
    """
        Verify that required functions contain no more than one return statement.

        :param: none
        :raises: AssertionError if any required function violates the single-return rule.
        :return: None
        :note: none
        """
    for module_name, functions in REQUIRED_FUNCTIONS.items():
        _, tree = load_tree(f"{module_name}.py")
        nodes = get_function_nodes(tree)

        for name in functions:
            count = count_returns(nodes[name])

            assert count <= 1, (
                f"{module_name}.{name}() contains "
                f"{count} return statements."
            )


def test_14_write_report_contents():
    """
        Verify that write_report() creates the required report from alternate data.

        :param: none
        :raises: AssertionError if report contents or return behavior are incorrect.
        :return: None
        :note: Uses a temporary output file.
        """
    inventory_io, _ = import_module_safely("inventory_io")

    original_records = [
        (30, "Camera", 125.50, 4),
        (10, "Cable", 9.99, 27),
        (20, "Stand", 42.00, 8),
    ]

    sorted_records = [
        (10, "Cable", 9.99, 27),
        (20, "Stand", 42.00, 8),
        (30, "Camera", 125.50, 4),
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir) / "report.txt"

        result = inventory_io.write_report(
            report_path,
            original_records,
            sorted_records,
            20,
            2,
            1,
        )

        contents = report_path.read_text(encoding="utf-8")

    expected = """Inventory Search and Sort Report

Records Loaded: 3
Search Target: 20

Linear Search
Original index: 2
Product: Stand
Price: $42.00
Quantity: 8

Binary Search
Sorted index: 1
Product: Stand
Price: $42.00
Quantity: 8

Original File Order
30 | Camera | $125.50 | 4
10 | Cable | $9.99 | 27
20 | Stand | $42.00 | 8

Sorted by Product ID
10 | Cable | $9.99 | 27
20 | Stand | $42.00 | 8
30 | Camera | $125.50 | 4"""

    assert normalize_output(contents) == normalize_output(expected), (
        "write_report() did not produce the required report contents."
    )

    assert result is None, (
        "write_report() should write the file rather than return data."
    )


def test_15_complete_program_behavior():
    """
        Verify the complete application from execution through report creation.

        :param: none
        :raises: AssertionError if the program fails, report output is incorrect, or inventory.txt is modified.
        :return: None
        :note: Verifies the console confirmation and generated report file.
        """
    inventory_path = PROJECT_DIR / "inventory.txt"
    original_inventory = inventory_path.read_text(encoding="utf-8")
    report_path = PROJECT_DIR / "inventory_report.txt"

    if report_path.exists():
        report_path.unlink()

    completed = subprocess.run(
        [sys.executable, "main.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0, (
        "main.py did not complete normally.\n"
        f"{completed.stderr}"
    )

    output = normalize_output(completed.stdout)

    assert output == "Report written to inventory_report.txt.", (
        "main.py should display exactly:\n"
        "Report written to inventory_report.txt."
    )

    assert report_path.exists(), (
        "main.py did not create inventory_report.txt."
    )

    contents = report_path.read_text(encoding="utf-8")

    required_lines = [
        "Records Loaded: 8",
        "Search Target: 1077",
        "Original index: 4",
        "Sorted index: 5",
        "Product: Monitor Arm",
        "1007 | Mouse | $24.50 | 31",
        "1112 | Laptop Dock | $129.95 | 8",
    ]

    for text in required_lines:
        assert text in contents, (
            f"inventory_report.txt is missing expected content: {text}"
        )

    assert inventory_path.read_text(encoding="utf-8") == original_inventory, (
        "main.py must not modify inventory.txt."
    )


TESTS = [
    ("Required project files",
     test_01_required_files),
    ("Required functions and signatures",
     test_02_required_functions_and_signatures),
    ("Run guard and safe imports",
     test_03_run_guard_and_safe_imports),
    ("Inventory parsing and field types",
     test_04_read_inventory_parses_records_and_types),
    ("Linear search behavior",
     test_05_linear_search_behavior),
    ("Linear search required structure",
     test_06_linear_search_required_structure),
    ("Selection Sort behavior",
     test_07_selection_sort_behavior),
    ("Selection Sort mutates in place and preserves records",
     test_08_selection_sort_in_place_and_preserves_records),
    ("Selection Sort required structure",
     test_09_selection_sort_required_structure),
    ("Original order preserved when sorting a copy",
     test_10_original_order_can_be_preserved_with_copy),
    ("Binary search behavior",
     test_11_binary_search_behavior),
    ("Binary search required structure",
     test_12_binary_search_required_structure),
    ("Single-return rule",
     test_13_single_return_rule),
    ("Report-file contents",
     test_14_write_report_contents),
    ("Complete application behavior",
     test_15_complete_program_behavior),
]


def main():
    """
        Run all supplied Assignment 8 tests and display the results.

        :param: none
        :raises: none
        :return: Integer status code 0 after the test run completes.
        :note: none
        """
    print("Assignment 8 Tests")
    print()

    passed = 0

    for number, (name, test_function) in enumerate(
        TESTS,
        start=1,
    ):
        try:
            test_function()
            status = "PASS"
            passed += 1
            detail = ""
        except AssertionError as exc:
            status = "FAIL"
            detail = str(exc)
        except Exception as exc:
            status = "FAIL"
            detail = (
                f"{type(exc).__name__}: {exc}"
            )

        print(
            f"{number:02d}. "
            f"{name:<54} "
            f"{status}"
        )

        if detail:
            for line in detail.splitlines():
                print(f"    {line}")

    print()
    print(f"{passed}/{len(TESTS)} tests passed")

    if passed == len(TESTS):
        print("All supplied tests passed.")
    else:
        print(
            "Review the failed tests and continue developing."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
