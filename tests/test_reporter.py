"""Tests for ReportGenerator class."""

import pytest
import tempfile
import os
from src.reporter import ReportGenerator


class TestReportGenerator:
    """Test cases for ReportGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.reporter = ReportGenerator()

    def test_generate_text_report_single_file(self):
        """Test text report generation for single file."""
        results = {
            "file_path": "test.py",
            "overall_score": 85.5,
            "pep8_score": 0.9,
            "complexity": {
                "average": 4.5,
                "max": 8,
                "functions": {"func1": 3, "func2": 8},
                "high_complexity_count": 1,
            },
            "docstring_coverage": {
                "coverage": 0.8,
                "functions_total": 2,
                "functions_with_docstring": 2,
                "classes_total": 1,
                "classes_with_docstring": 0,
                "module_has_docstring": True,
            },
            "duplication": {"duplication_ratio": 0.1},
            "line_count": 50,
            "function_count": 2,
            "class_count": 1,
            "recommendations": ["Add docstrings", "Reduce complexity"],
        }

        report = self.reporter.generate_text_report(results)
        assert "CODE QUALITY ASSESSMENT REPORT" in report
        assert "test.py" in report
        assert "85.5" in report
        assert "RECOMMENDATIONS" in report

    def test_generate_text_report_directory(self):
        """Test text report generation for directory."""
        results = {
            "directory": "/path/to/code",
            "files_analyzed": 3,
            "average_score": 75.0,
            "file_results": [
                {"file_path": "file1.py", "overall_score": 80},
                {"file_path": "file2.py", "overall_score": 70},
            ],
        }

        report = self.reporter.generate_text_report(results)
        assert "Directory:" in report
        assert "3" in report
        assert "75.0" in report

    def test_generate_json_report(self):
        """Test JSON report generation."""
        results = {"file_path": "test.py", "overall_score": 85.5}

        report = self.reporter.generate_json_report(results)
        assert isinstance(report, str)
        assert "test.py" in report
        assert "85.5" in report

    def test_generate_summary_single_file(self):
        """Test summary generation for single file."""
        results = {
            "file_path": "test.py",
            "overall_score": 85.5,
        }

        summary = self.reporter.generate_summary(results)
        assert "file" in summary
        assert "score" in summary
        assert "grade" in summary
        assert summary["score"] == 85.5

    def test_generate_summary_directory(self):
        """Test summary generation for directory."""
        results = {
            "directory": "/path/to/code",
            "files_analyzed": 3,
            "average_score": 75.0,
        }

        summary = self.reporter.generate_summary(results)
        assert "directory" in summary
        assert "average_score" in summary
        assert "average_grade" in summary

    def test_score_to_grade(self):
        """Test score to grade conversion."""
        assert "A" in self.reporter._score_to_grade(95)
        assert "B" in self.reporter._score_to_grade(85)
        assert "C" in self.reporter._score_to_grade(75)
        assert "D" in self.reporter._score_to_grade(65)
        assert "F" in self.reporter._score_to_grade(50)

    def test_save_report_text(self):
        """Test saving text report to file."""
        results = {
            "file_path": "test.py",
            "overall_score": 85.5,
            "pep8_score": 0.9,
            "complexity": {"average": 4.5, "max": 8, "functions": {}, "high_complexity_count": 0},
            "docstring_coverage": {"coverage": 0.8},
            "duplication": {"duplication_ratio": 0.1},
            "line_count": 50,
            "function_count": 2,
            "class_count": 1,
            "recommendations": [],
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            success = self.reporter.save_report(results, temp_path, "text")
            assert success
            assert os.path.exists(temp_path)

            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "CODE QUALITY ASSESSMENT REPORT" in content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_save_report_json(self):
        """Test saving JSON report to file."""
        results = {"file_path": "test.py", "overall_score": 85.5}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            success = self.reporter.save_report(results, temp_path, "json")
            assert success
            assert os.path.exists(temp_path)

            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "test.py" in content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

