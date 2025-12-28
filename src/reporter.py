"""
Report Generator

Generates reports from code analysis results.
"""

import json
from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generates various types of reports from analysis results."""

    def __init__(self):
        """Initialize the report generator."""
        pass

    def generate_text_report(self, results: Dict) -> str:
        """
        Generate a plain text report.

        Args:
            results: Analysis results dictionary

        Returns:
            Formatted text report
        """
        if "error" in results:
            return f"Error: {results['error']}\n"

        report = []
        report.append("=" * 80)
        report.append("CODE QUALITY ASSESSMENT REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if "file_path" in results:
            # Single file report
            report.append(f"File: {results['file_path']}\n")
            report.append(f"Overall Score: {results['overall_score']}/100\n")
            report.append("-" * 80)
            report.append("METRICS:")
            report.append(f"  PEP 8 Compliance: {results['pep8_score']*100:.1f}%")
            report.append(f"  Average Complexity: {results['complexity']['average']:.2f}")
            report.append(f"  Max Complexity: {results['complexity']['max']}")
            report.append(f"  Docstring Coverage: {results['docstring_coverage']['coverage']*100:.1f}%")
            report.append(f"  Code Duplication: {results['duplication']['duplication_ratio']*100:.1f}%")
            report.append(f"  Lines of Code: {results['line_count']}")
            report.append(f"  Functions: {results['function_count']}")
            report.append(f"  Classes: {results['class_count']}\n")

            if results['complexity']['functions']:
                report.append("FUNCTION COMPLEXITY:")
                for func_name, complexity in sorted(
                    results['complexity']['functions'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]:
                    report.append(f"  {func_name}: {complexity}")

            report.append("\nRECOMMENDATIONS:")
            for rec in results['recommendations']:
                report.append(f"  • {rec}")

        elif "directory" in results:
            # Directory report
            report.append(f"Directory: {results['directory']}\n")
            report.append(f"Files Analyzed: {results['files_analyzed']}")
            report.append(f"Average Score: {results['average_score']}/100\n")
            report.append("-" * 80)
            report.append("FILE RESULTS:\n")

            for file_result in sorted(
                results['file_results'],
                key=lambda x: x['overall_score']
            ):
                report.append(f"  {file_result['file_path']}: {file_result['overall_score']}/100")

        report.append("\n" + "=" * 80)

        return "\n".join(report)

    def generate_json_report(self, results: Dict) -> str:
        """
        Generate a JSON report.

        Args:
            results: Analysis results dictionary

        Returns:
            JSON string
        """
        return json.dumps(results, indent=2, ensure_ascii=False)

    def generate_summary(self, results: Dict) -> Dict:
        """
        Generate a summary of results.

        Args:
            results: Analysis results dictionary

        Returns:
            Summary dictionary
        """
        if "error" in results:
            return {"error": results["error"]}

        if "file_path" in results:
            return {
                "file": results["file_path"],
                "score": results["overall_score"],
                "grade": self._score_to_grade(results["overall_score"]),
                "timestamp": datetime.now().isoformat(),
            }
        elif "directory" in results:
            return {
                "directory": results["directory"],
                "files_analyzed": results["files_analyzed"],
                "average_score": results["average_score"],
                "average_grade": self._score_to_grade(results["average_score"]),
                "timestamp": datetime.now().isoformat(),
            }

        return {"error": "Unknown results format"}

    def _score_to_grade(self, score: float) -> str:
        """
        Convert numeric score to letter grade.

        Args:
            score: Numeric score (0-100)

        Returns:
            Letter grade
        """
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Satisfactory)"
        elif score >= 60:
            return "D (Needs Improvement)"
        else:
            return "F (Poor)"

    def save_report(self, results: Dict, output_path: str, format: str = "text") -> bool:
        """
        Save report to file.

        Args:
            results: Analysis results dictionary
            output_path: Path to save the report
            format: Report format ('text' or 'json')

        Returns:
            True if successful, False otherwise
        """
        try:
            if format == "json":
                content = self.generate_json_report(results)
            else:
                content = self.generate_text_report(results)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False

