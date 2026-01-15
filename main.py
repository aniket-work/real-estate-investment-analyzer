"""
AI-Powered Real Estate Investment Analyzer
Main orchestration script
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich import box
import time
import json

from models.property import Property
from data.mock_properties import get_sample_properties
from agents.market_analyzer import MarketAnalyzer
from agents.property_evaluator import PropertyEvaluator
from agents.financial_calculator import FinancialCalculator
from agents.decision_engine import DecisionEngine


console = Console()


def print_header():
    """Prints application header"""
    header = Panel(
        "[bold cyan]AI-Powered Real Estate Investment Analyzer[/bold cyan]\n"
        "[dim]Multi-Agent System for Property Investment Analysis[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    )
    console.print(header)
    console.print()


def analyze_property(property: Property, agents: dict) -> dict:
    """Analyzes a single property using all agents"""
    
    console.print(f"\n[bold yellow]Analyzing Property: {property.property_id}[/bold yellow]")
    console.print(f"[dim]{property.address}, {property.city}, {property.state}[/dim]\n")
    
    results = {}
    
    # Market Analysis
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Running Market Analysis...", total=None)
        time.sleep(0.8)  # Simulate processing
        market_analysis = agents["market"].analyze_market(property)
        results["market"] = market_analysis
        progress.update(task, completed=True)
    
    console.print(f"  ✓ Location Score: [green]{market_analysis.location_score}/100[/green]")
    console.print(f"  ✓ Market Heat: [yellow]{market_analysis.market_heat}[/yellow]")
    console.print(f"  ✓ Appreciation Rate: [green]{market_analysis.appreciation_rate}%/year[/green]\n")
    
    # Property Evaluation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Evaluating Property Condition...", total=None)
        time.sleep(0.8)
        property_eval = agents["evaluator"].evaluate_property(property)
        results["evaluation"] = property_eval
        progress.update(task, completed=True)
    
    console.print(f"  ✓ Condition Score: [green]{property_eval.condition_score}/100[/green]")
    console.print(f"  ✓ Value Rating: [yellow]{property_eval.value_rating}[/yellow]")
    console.print(f"  ✓ Price/SqFt: [cyan]${property_eval.price_per_sqft}[/cyan] "
                 f"(Market Avg: ${property_eval.market_avg_price_per_sqft})\n")
    
    # Financial Analysis
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Calculating Financial Metrics...", total=None)
        time.sleep(0.8)
        financial_metrics = agents["financial"].calculate_metrics(
            property, market_analysis.appreciation_rate
        )
        results["financial"] = financial_metrics
        progress.update(task, completed=True)
    
    console.print(f"  ✓ Cap Rate: [green]{financial_metrics.cap_rate}%[/green]")
    console.print(f"  ✓ Monthly Cash Flow: [green]${financial_metrics.monthly_cash_flow}[/green]")
    console.print(f"  ✓ 5-Year ROI: [green]{financial_metrics.roi_5_year}%[/green]\n")
    
    # Decision Engine
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Generating Investment Recommendation...", total=None)
        time.sleep(0.8)
        decision = agents["decision"].make_decision(
            property, market_analysis, property_eval, financial_metrics
        )
        results["decision"] = decision
        progress.update(task, completed=True)
    
    console.print(f"  ✓ Investment Grade: [bold green]{decision.investment_grade}[/bold green]")
    console.print(f"  ✓ Overall Score: [green]{decision.overall_score}/100[/green]")
    console.print(f"  ✓ Recommendation: [bold yellow]{decision.recommendation}[/bold yellow]\n")
    
    return results


def display_summary_table(all_results: list):
    """Displays ASCII summary table of all properties"""
    
    console.print("\n" + "="*80)
    console.print("[bold cyan]INVESTMENT ANALYSIS SUMMARY[/bold cyan]".center(80))
    console.print("="*80 + "\n")
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Property ID", style="cyan", width=12)
    table.add_column("City", style="white", width=12)
    table.add_column("Price", justify="right", style="yellow", width=12)
    table.add_column("Grade", justify="center", style="bold green", width=8)
    table.add_column("Score", justify="right", style="green", width=8)
    table.add_column("Cap Rate", justify="right", style="cyan", width=10)
    table.add_column("Cash Flow", justify="right", style="green", width=12)
    table.add_column("Recommendation", style="bold yellow", width=15)
    
    # Sort by overall score (descending)
    sorted_results = sorted(all_results, 
                           key=lambda x: x["decision"].overall_score, 
                           reverse=True)
    
    for result in sorted_results:
        prop = result["property"]
        decision = result["decision"]
        financial = result["financial"]
        
        # Color code recommendation
        rec_style = "bold green" if "Buy" in decision.recommendation else "yellow"
        
        table.add_row(
            prop.property_id,
            prop.city,
            f"${prop.price:,}",
            decision.investment_grade,
            f"{decision.overall_score}",
            f"{financial.cap_rate}%",
            f"${financial.monthly_cash_flow}",
            f"[{rec_style}]{decision.recommendation}[/{rec_style}]"
        )
    
    console.print(table)
    console.print()


def display_detailed_report(result: dict):
    """Displays detailed report for top property"""
    
    decision = result["decision"]
    prop = result["property"]
    financial = result["financial"]
    market = result["market"]
    
    console.print("\n" + "="*80)
    console.print(f"[bold cyan]TOP INVESTMENT OPPORTUNITY: {prop.property_id}[/bold cyan]".center(90))
    console.print("="*80 + "\n")
    
    # Property Details
    details_table = Table(show_header=False, box=box.SIMPLE)
    details_table.add_column("Field", style="cyan bold", width=25)
    details_table.add_column("Value", style="white", width=50)
    
    details_table.add_row("Address", f"{prop.address}")
    details_table.add_row("Location", f"{prop.city}, {prop.state}")
    details_table.add_row("Property Type", prop.property_type)
    details_table.add_row("Price", f"${prop.price:,}")
    details_table.add_row("Size", f"{prop.bedrooms} bed / {prop.bathrooms} bath / {prop.sqft} sqft")
    details_table.add_row("Year Built", str(prop.year_built))
    
    console.print(Panel(details_table, title="[bold]Property Details[/bold]", border_style="cyan"))
    
    # Investment Metrics
    metrics_table = Table(show_header=False, box=box.SIMPLE)
    metrics_table.add_column("Metric", style="cyan bold", width=25)
    metrics_table.add_column("Value", style="green", width=50)
    
    metrics_table.add_row("Investment Grade", f"[bold]{decision.investment_grade}[/bold]")
    metrics_table.add_row("Overall Score", f"{decision.overall_score}/100")
    metrics_table.add_row("Confidence", f"{decision.confidence}%")
    metrics_table.add_row("Risk Level", decision.risk_level)
    metrics_table.add_row("Cap Rate", f"{financial.cap_rate}%")
    metrics_table.add_row("Monthly Cash Flow", f"${financial.monthly_cash_flow}")
    metrics_table.add_row("5-Year ROI", f"{financial.roi_5_year}%")
    metrics_table.add_row("Break-Even", f"{financial.break_even_months} months")
    
    console.print(Panel(metrics_table, title="[bold]Investment Metrics[/bold]", border_style="green"))
    
    # Strengths & Concerns
    console.print("\n[bold green]Key Strengths:[/bold green]")
    for strength in decision.key_strengths:
        console.print(f"  ✓ {strength}")
    
    console.print("\n[bold yellow]Key Concerns:[/bold yellow]")
    for concern in decision.key_concerns:
        console.print(f"  ⚠ {concern}")
    
    console.print(f"\n[bold cyan]Recommendation:[/bold cyan] [bold yellow]{decision.recommendation}[/bold yellow]")
    console.print(f"[dim]{decision.rationale}[/dim]\n")


def save_results(all_results: list):
    """Saves analysis results to JSON file"""
    
    output_file = "analysis_results.json"
    
    # Convert results to serializable format
    serializable_results = []
    for result in all_results:
        serializable_results.append({
            "property_id": result["property"].property_id,
            "address": result["property"].address,
            "city": result["property"].city,
            "price": result["property"].price,
            "investment_grade": result["decision"].investment_grade,
            "overall_score": result["decision"].overall_score,
            "recommendation": result["decision"].recommendation,
            "cap_rate": result["financial"].cap_rate,
            "monthly_cash_flow": result["financial"].monthly_cash_flow,
            "roi_5_year": result["financial"].roi_5_year
        })
    
    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    console.print(f"[dim]Results saved to {output_file}[/dim]\n")


def main():
    """Main execution function"""
    
    print_header()
    
    # Initialize agents
    console.print("[bold]Initializing AI Agents...[/bold]")
    agents = {
        "market": MarketAnalyzer(),
        "evaluator": PropertyEvaluator(),
        "financial": FinancialCalculator(),
        "decision": DecisionEngine()
    }
    console.print("[green]✓ All agents initialized successfully[/green]\n")
    
    # Load properties
    properties = get_sample_properties()
    console.print(f"[bold]Loaded {len(properties)} properties for analysis[/bold]\n")
    
    # Analyze all properties
    all_results = []
    for prop in properties:
        result = analyze_property(prop, agents)
        result["property"] = prop  # Store property reference
        all_results.append(result)
        time.sleep(0.5)
    
    # Display summary
    display_summary_table(all_results)
    
    # Display detailed report for top property
    top_property = max(all_results, key=lambda x: x["decision"].overall_score)
    display_detailed_report(top_property)
    
    # Save results
    save_results(all_results)
    
    console.print("[bold green]Analysis Complete![/bold green]\n")


if __name__ == "__main__":
    main()
