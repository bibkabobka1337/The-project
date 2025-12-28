"""
Main entry point for Code Quality Assessment Tool.

Usage:
    python -m src.main <file_or_directory> [--output OUTPUT] [--format FORMAT]
"""

import argparse
import sys
import os

from src.analyzer import CodeAnalyzer
from src.reporter import ReportGenerator


def main():
    """Main function to run the code quality assessment tool."""
    parser = argparse.ArgumentParser(
        description="Code Quality Assessment Tool - Analyze Python code quality"
    )
    parser.add_argument(
        "target",
        type=str,
        help="Path to Python file or directory to analyze",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path for report (default: print to stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Report format (default: text)",
    )

    args = parser.parse_args()

    # Check if target exists
    if not os.path.exists(args.target):
        print(f"Error: Path '{args.target}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Initialize analyzer and reporter
    analyzer = CodeAnalyzer()
    reporter = ReportGenerator()

    # Analyze
    print(f"Analyzing: {args.target}...", file=sys.stderr)

    if os.path.isfile(args.target):
        results = analyzer.analyze_file(args.target)
    elif os.path.isdir(args.target):
        results = analyzer.analyze_directory(args.target)
    else:
        print(f"Error: '{args.target}' is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)

    # Check for errors
    if "error" in results:
        print(f"Error: {results['error']}", file=sys.stderr)
        sys.exit(1)

    # Generate and output report
    if args.format == "json":
        report = reporter.generate_json_report(results)
    else:
        report = reporter.generate_text_report(results)

    if args.output:
        success = reporter.save_report(results, args.output, args.format)
        if success:
            print(f"Report saved to: {args.output}", file=sys.stderr)
        else:
            print(f"Error saving report to: {args.output}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)

    # Print summary
    summary = reporter.generate_summary(results)
    if "error" not in summary:
        print(f"\nSummary: {summary['grade']} ({summary.get('score', summary.get('average_score', 'N/A'))}/100)", file=sys.stderr)


if __name__ == "__main__":
    main()

