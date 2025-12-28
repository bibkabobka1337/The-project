"""Tests for CodeAnalyzer class."""

import pytest
import os
import tempfile
from src.analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Test cases for CodeAnalyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()

    def test_analyze_file_not_found(self):
        """Test analysis of non-existent file."""
        result = self.analyzer.analyze_file("nonexistent.py")
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_analyze_simple_file(self):
        """Test analysis of a simple Python file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('''"""
Simple test module.
"""

def hello(name):
    """Say hello to someone."""
    return f"Hello, {name}!"

class TestClass:
    """A test class."""
    
    def method(self):
        """A method."""
        return "test"
''')
            temp_path = f.name

        try:
            result = self.analyzer.analyze_file(temp_path)
            assert "error" not in result
            assert "overall_score" in result
            assert result["overall_score"] >= 0
            assert result["overall_score"] <= 100
            assert "pep8_score" in result
            assert "complexity" in result
            assert "docstring_coverage" in result
        finally:
            os.unlink(temp_path)

    def test_analyze_file_with_syntax_error(self):
        """Test analysis of file with syntax error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def invalid syntax here")
            temp_path = f.name

        try:
            result = self.analyzer.analyze_file(temp_path)
            assert "error" in result
            assert "syntax" in result["error"].lower()
        finally:
            os.unlink(temp_path)

    def test_pep8_check(self):
        """Test PEP 8 checking."""
        good_code = "def test():\n    return True\n"
        bad_code = "def test():\n    return True" + " " * 50 + "\n"

        score_good = self.analyzer._check_pep8(good_code)
        score_bad = self.analyzer._check_pep8(bad_code)

        assert 0 <= score_good <= 1
        assert 0 <= score_bad <= 1
        assert score_good >= score_bad

    def test_complexity_calculation(self):
        """Test cyclomatic complexity calculation."""
        import ast

        simple_code = "def simple():\n    return 1\n"
        complex_code = """def complex_func(x):
    if x > 0:
        if x > 10:
            for i in range(x):
                if i % 2 == 0:
                    return i
    return 0
"""

        simple_tree = ast.parse(simple_code)
        complex_tree = ast.parse(complex_code)

        simple_result = self.analyzer._calculate_complexity(simple_tree)
        complex_result = self.analyzer._calculate_complexity(complex_tree)

        assert simple_result["average"] < complex_result["average"]
        assert simple_result["max"] < complex_result["max"]

    def test_docstring_coverage(self):
        """Test docstring coverage calculation."""
        import ast

        code_with_docstrings = '''"""
Module docstring.
"""

def func1():
    """Function docstring."""
    pass

class Class1:
    """Class docstring."""
    pass
'''

        code_without_docstrings = """
def func1():
    pass

class Class1:
    pass
"""

        tree_with = ast.parse(code_with_docstrings)
        tree_without = ast.parse(code_without_docstrings)

        result_with = self.analyzer._check_docstrings(tree_with)
        result_without = self.analyzer._check_docstrings(tree_without)

        assert result_with["coverage"] > result_without["coverage"]

    def test_duplication_detection(self):
        """Test code duplication detection."""
        code_with_duplication = """
def func1():
    x = 1
    y = 2
    z = 3
    return x + y + z

def func2():
    x = 1
    y = 2
    z = 3
    return x * y * z
"""

        code_without_duplication = """
def func1():
    return 1

def func2():
    return 2
"""

        result_with = self.analyzer._check_duplication(code_with_duplication)
        result_without = self.analyzer._check_duplication(code_without_duplication)

        assert result_with["duplication_ratio"] > result_without["duplication_ratio"]

    def test_overall_score_calculation(self):
        """Test overall score calculation."""
        results = {
            "pep8_score": 0.9,
            "complexity": {"average": 3.0},
            "docstring_coverage": {"coverage": 0.8},
            "duplication": {"duplication_ratio": 0.1},
        }

        score = self.analyzer._calculate_overall_score(results)
        assert 0 <= score <= 100

    def test_recommendations_generation(self):
        """Test recommendations generation."""
        good_results = {
            "pep8_score": 0.95,
            "complexity": {"average": 3.0, "high_complexity_count": 0},
            "docstring_coverage": {"coverage": 0.9},
            "duplication": {"duplication_ratio": 0.05},
        }

        bad_results = {
            "pep8_score": 0.5,
            "complexity": {"average": 15.0, "high_complexity_count": 3},
            "docstring_coverage": {"coverage": 0.2},
            "duplication": {"duplication_ratio": 0.5},
        }

        good_recs = self.analyzer._generate_recommendations(good_results)
        bad_recs = self.analyzer._generate_recommendations(bad_results)

        assert len(good_recs) > 0
        assert len(bad_recs) > len(good_recs)

