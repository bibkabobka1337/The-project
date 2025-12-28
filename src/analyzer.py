"""
Code Quality Analyzer

Analyzes Python code quality based on multiple metrics:
- PEP 8 compliance
- Cyclomatic complexity
- Docstring presence
- Code duplication
"""

import ast
import os
from typing import Dict, List
from collections import defaultdict


class CodeAnalyzer:
    """Analyzes Python code quality using various metrics."""

    def __init__(self):
        """Initialize the analyzer."""
        self.complexity_threshold = 10
        self.duplication_threshold = 0.3

    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze a single Python file.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            Dictionary with analysis results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"error": f"Syntax error: {str(e)}"}

        results = {
            "file_path": file_path,
            "pep8_score": self._check_pep8(code),
            "complexity": self._calculate_complexity(tree),
            "docstring_coverage": self._check_docstrings(tree),
            "duplication": self._check_duplication(code),
            "line_count": len(code.splitlines()),
            "function_count": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            "class_count": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
        }

        results["overall_score"] = self._calculate_overall_score(results)
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _check_pep8(self, code: str) -> float:
        """
        Check PEP 8 compliance (simplified version).

        Args:
            code: Source code as string

        Returns:
            PEP 8 compliance score (0-1)
        """
        lines = code.splitlines()
        if not lines:
            return 0.0

        violations = 0
        total_checks = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check line length (max 79 for code, 72 for comments)
            if stripped and not stripped.startswith("#"):
                total_checks += 1
                if len(line) > 79:
                    violations += 1

            # Check for trailing whitespace
            if line and line[-1] in [" ", "\t"]:
                violations += 1
                total_checks += 1

            # Check for multiple statements on one line
            if ";" in stripped and not stripped.startswith("#"):
                violations += 1
                total_checks += 1

        if total_checks == 0:
            return 1.0

        return max(0.0, 1.0 - (violations / total_checks))

    def _calculate_complexity(self, tree: ast.AST) -> Dict:
        """
        Calculate cyclomatic complexity for functions.

        Args:
            tree: AST tree of the code

        Returns:
            Dictionary with complexity metrics
        """
        complexities = []
        function_complexities = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = 1  # Base complexity

                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                    elif isinstance(child, ast.ExceptHandler):
                        complexity += 1

                complexities.append(complexity)
                function_complexities[node.name] = complexity

        if not complexities:
            return {
                "average": 0,
                "max": 0,
                "functions": {},
                "high_complexity_count": 0,
            }

        return {
            "average": sum(complexities) / len(complexities),
            "max": max(complexities),
            "functions": function_complexities,
            "high_complexity_count": sum(1 for c in complexities if c > self.complexity_threshold),
        }

    def _check_docstrings(self, tree: ast.AST) -> Dict:
        """
        Check docstring coverage.

        Args:
            tree: AST tree of the code

        Returns:
            Dictionary with docstring metrics
        """
        functions = []
        classes = []
        modules_with_docstring = ast.get_docstring(tree) is not None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
            elif isinstance(node, ast.ClassDef):
                classes.append(node)

        functions_with_docstring = sum(
            1 for f in functions if ast.get_docstring(f) is not None
        )
        classes_with_docstring = sum(
            1 for c in classes if ast.get_docstring(c) is not None
        )

        total_items = len(functions) + len(classes)
        items_with_docstring = functions_with_docstring + classes_with_docstring

        coverage = items_with_docstring / total_items if total_items > 0 else 1.0

        return {
            "coverage": coverage,
            "functions_total": len(functions),
            "functions_with_docstring": functions_with_docstring,
            "classes_total": len(classes),
            "classes_with_docstring": classes_with_docstring,
            "module_has_docstring": modules_with_docstring,
        }

    def _check_duplication(self, code: str) -> Dict:
        """
        Check for code duplication (simplified version).

        Args:
            code: Source code as string

        Returns:
            Dictionary with duplication metrics
        """
        lines = [line.strip() for line in code.splitlines() if line.strip() and not line.strip().startswith("#")]

        if len(lines) < 4:
            return {"duplication_ratio": 0.0, "duplicate_blocks": []}

        # Check for duplicate sequences of 3+ lines
        duplicate_blocks = []
        seen_sequences = defaultdict(list)

        for i in range(len(lines) - 2):
            sequence = tuple(lines[i : i + 3])
            seen_sequences[sequence].append(i)

        for sequence, positions in seen_sequences.items():
            if len(positions) > 1:
                duplicate_blocks.append({
                    "sequence": list(sequence),
                    "occurrences": len(positions),
                    "positions": positions,
                })

        total_lines = len(lines)
        duplicate_lines = sum(
            len(block["sequence"]) * (block["occurrences"] - 1)
            for block in duplicate_blocks
        )

        duplication_ratio = duplicate_lines / total_lines if total_lines > 0 else 0.0

        return {
            "duplication_ratio": duplication_ratio,
            "duplicate_blocks": duplicate_blocks[:5],  # Limit to first 5
        }

    def _calculate_overall_score(self, results: Dict) -> float:
        """
        Calculate overall quality score.

        Args:
            results: Analysis results dictionary

        Returns:
            Overall score (0-100)
        """
        if "error" in results:
            return 0.0

        # Weighted scoring
        pep8_weight = 0.3
        complexity_weight = 0.3
        docstring_weight = 0.2
        duplication_weight = 0.2

        pep8_score = results["pep8_score"] * 100

        # Complexity score (inverse - lower is better)
        avg_complexity = results["complexity"]["average"]
        complexity_score = max(0, 100 - (avg_complexity * 5)) if avg_complexity > 0 else 100

        # Docstring score
        docstring_score = results["docstring_coverage"]["coverage"] * 100

        # Duplication score (inverse - lower is better)
        duplication_ratio = results["duplication"]["duplication_ratio"]
        duplication_score = max(0, 100 - (duplication_ratio * 100))

        overall = (
            pep8_score * pep8_weight
            + complexity_score * complexity_weight
            + docstring_score * docstring_weight
            + duplication_score * duplication_weight
        )

        return round(overall, 2)

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """
        Generate recommendations based on analysis.

        Args:
            results: Analysis results dictionary

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if results["pep8_score"] < 0.8:
            recommendations.append("Improve PEP 8 compliance: check line lengths and formatting")

        if results["complexity"]["average"] > 7:
            recommendations.append(
                f"Reduce cyclomatic complexity (average: {results['complexity']['average']:.1f})"
            )

        if results["complexity"]["high_complexity_count"] > 0:
            recommendations.append(
                f"Refactor {results['complexity']['high_complexity_count']} function(s) with high complexity"
            )

        if results["docstring_coverage"]["coverage"] < 0.7:
            recommendations.append(
                f"Add docstrings to functions and classes (current coverage: {results['docstring_coverage']['coverage']*100:.1f}%)"
            )

        if results["duplication"]["duplication_ratio"] > 0.2:
            recommendations.append(
                f"Reduce code duplication (current ratio: {results['duplication']['duplication_ratio']*100:.1f}%)"
            )

        if not recommendations:
            recommendations.append("Code quality is good! Keep up the good work.")

        return recommendations

    def analyze_directory(self, directory: str) -> Dict:
        """
        Analyze all Python files in a directory.

        Args:
            directory: Path to directory containing Python files

        Returns:
            Dictionary with aggregated results
        """
        if not os.path.isdir(directory):
            return {"error": f"Directory not found: {directory}"}

        python_files = []
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["__pycache__", "venv", "env"]]

            for file in files:
                if file.endswith(".py") and not file.startswith("."):
                    python_files.append(os.path.join(root, file))

        if not python_files:
            return {"error": "No Python files found in directory"}

        file_results = []
        for file_path in python_files:
            result = self.analyze_file(file_path)
            if "error" not in result:
                file_results.append(result)

        if not file_results:
            return {"error": "No valid Python files could be analyzed"}

        # Aggregate results
        total_score = sum(r["overall_score"] for r in file_results)
        avg_score = total_score / len(file_results)

        return {
            "directory": directory,
            "files_analyzed": len(file_results),
            "average_score": round(avg_score, 2),
            "file_results": file_results,
        }

