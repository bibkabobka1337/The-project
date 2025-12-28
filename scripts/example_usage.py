"""
Example usage script for Code Quality Assessment Tool.

This script demonstrates how to use the analyzer programmatically.
"""

from src.analyzer import CodeAnalyzer
from src.reporter import ReportGenerator


def main():
    """Demonstrate the code quality assessment tool."""
    print("=" * 80)
    print("Code Quality Assessment Tool - Example Usage")
    print("=" * 80)
    print()

    # Initialize
    analyzer = CodeAnalyzer()
    reporter = ReportGenerator()

    # Analyze sample code
    sample_file = "data/sample_code.py"
    print(f"Analyzing: {sample_file}")
    print("-" * 80)

    results = analyzer.analyze_file(sample_file)

    if "error" in results:
        print(f"Error: {results['error']}")
        return

    # Display results
    print(f"Overall Score: {results['overall_score']}/100")
    print(f"PEP 8 Score: {results['pep8_score']*100:.1f}%")
    print(f"Average Complexity: {results['complexity']['average']:.2f}")
    print(f"Docstring Coverage: {results['docstring_coverage']['coverage']*100:.1f}%")
    print(f"Code Duplication: {results['duplication']['duplication_ratio']*100:.1f}%")
    print()

    # Generate and display report
    print("Full Report:")
    print("-" * 80)
    report = reporter.generate_text_report(results)
    print(report)

    # Generate summary
    print("\nSummary:")
    print("-" * 80)
    summary = reporter.generate_summary(results)
    print(f"Grade: {summary['grade']}")
    print(f"Score: {summary['score']}/100")
    print(f"Timestamp: {summary['timestamp']}")


if __name__ == "__main__":
    main()

