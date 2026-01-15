"""
Generate Mermaid.js diagrams and convert to PNG images
"""
import base64
import requests
from pathlib import Path


def generate_diagrams():
    """Generates all required Mermaid diagrams as PNG images"""
    
    # Create images directory
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    diagrams = {
        "title_diagram": """
graph TB
    subgraph Input["📊 Property Data Input"]
        P1[Property Details]
        P2[Market Data]
        P3[Financial Info]
    end
    
    subgraph Agents["🤖 AI Agent System"]
        A1[Market Analyzer<br/>Location & Trends]
        A2[Property Evaluator<br/>Condition & Value]
        A3[Financial Calculator<br/>ROI & Cash Flow]
        A4[Decision Engine<br/>Final Recommendation]
    end
    
    subgraph Output["📈 Investment Analysis"]
        O1[Investment Grade A+ to D]
        O2[Risk Assessment]
        O3[Buy/Hold/Pass Decision]
    end
    
    P1 --> A1
    P2 --> A1
    P1 --> A2
    P3 --> A3
    P1 --> A3
    
    A1 --> A4
    A2 --> A4
    A3 --> A4
    
    A4 --> O1
    A4 --> O2
    A4 --> O3
    
    style A1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style A2 fill:#2196F3,stroke:#1565C0,color:#fff
    style A3 fill:#FF9800,stroke:#E65100,color:#fff
    style A4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style O1 fill:#FFD700,stroke:#FFA000,color:#000
    style O2 fill:#FFD700,stroke:#FFA000,color:#000
    style O3 fill:#FFD700,stroke:#FFA000,color:#000
""",
        
        "architecture_diagram": """
graph LR
    subgraph DataLayer["Data Layer"]
        Props[Property Database<br/>5 Sample Properties]
        Market[Market Data<br/>City Statistics]
    end
    
    subgraph AgentLayer["Agent Layer"]
        MA[Market Analyzer]
        PE[Property Evaluator]
        FC[Financial Calculator]
    end
    
    subgraph DecisionLayer["Decision Layer"]
        DE[Decision Engine<br/>Weighted Scoring]
        Rank[Property Ranking]
    end
    
    subgraph OutputLayer["Output Layer"]
        Report[Detailed Report]
        JSON[JSON Export]
        CLI[Rich CLI Display]
    end
    
    Props --> MA
    Market --> MA
    Props --> PE
    Props --> FC
    Market --> FC
    
    MA --> DE
    PE --> DE
    FC --> DE
    
    DE --> Rank
    Rank --> Report
    Rank --> JSON
    Rank --> CLI
    
    style MA fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PE fill:#2196F3,stroke:#1565C0,color:#fff
    style FC fill:#FF9800,stroke:#E65100,color:#fff
    style DE fill:#9C27B0,stroke:#6A1B9A,color:#fff
""",
        
        "sequence_diagram": """
sequenceDiagram
    participant User
    participant Main
    participant MA as Market Analyzer
    participant PE as Property Evaluator
    participant FC as Financial Calculator
    participant DE as Decision Engine
    
    User->>Main: Run Analysis
    Main->>Main: Load 5 Properties
    
    loop For Each Property
        Main->>MA: Analyze Market(property)
        MA-->>Main: MarketAnalysis
        
        Main->>PE: Evaluate Property(property)
        PE-->>Main: PropertyEvaluation
        
        Main->>FC: Calculate Metrics(property, appreciation)
        FC-->>Main: FinancialMetrics
        
        Main->>DE: Make Decision(all analyses)
        DE-->>Main: InvestmentRecommendation
    end
    
    Main->>Main: Rank Properties by Score
    Main->>User: Display Summary Table
    Main->>User: Show Top Property Details
    Main->>Main: Export to JSON
""",
        
        "flow_diagram": """
flowchart TD
    Start([Start Analysis]) --> Load[Load Property Data]
    Load --> Init[Initialize 4 AI Agents]
    
    Init --> Loop{More Properties?}
    Loop -->|Yes| Market[Market Analyzer<br/>Location Score 0-100]
    
    Market --> Property[Property Evaluator<br/>Condition & Value]
    Property --> Financial[Financial Calculator<br/>Cap Rate, ROI, Cash Flow]
    
    Financial --> Decision[Decision Engine<br/>Weighted Scoring]
    
    Decision --> Grade{Calculate Grade}
    Grade -->|Score ≥ 90| GradeA[Grade: A+]
    Grade -->|Score 85-89| GradeA2[Grade: A]
    Grade -->|Score 80-84| GradeA3[Grade: A-]
    Grade -->|Score 75-79| GradeB[Grade: B+]
    Grade -->|Score 70-74| GradeB2[Grade: B]
    Grade -->|Score < 70| GradeC[Grade: C or below]
    
    GradeA --> Store[Store Results]
    GradeA2 --> Store
    GradeA3 --> Store
    GradeB --> Store
    GradeB2 --> Store
    GradeC --> Store
    
    Store --> Loop
    
    Loop -->|No| Rank[Rank by Overall Score]
    Rank --> Display[Display Summary Table]
    Display --> Report[Generate Detailed Report]
    Report --> Export[Export JSON]
    Export --> End([Analysis Complete])
    
    style Market fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Property fill:#2196F3,stroke:#1565C0,color:#fff
    style Financial fill:#FF9800,stroke:#E65100,color:#fff
    style Decision fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style GradeA fill:#FFD700,stroke:#FFA000,color:#000
"""
    }
    
    print("Generating Mermaid diagrams...")
    
    for name, mermaid_code in diagrams.items():
        try:
            # Encode Mermaid code to base64
            encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
            
            # Use mermaid.ink service to convert to PNG
            url = f"https://mermaid.ink/img/{encoded}"
            
            print(f"  Fetching {name}.png...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save PNG file
            output_path = images_dir / f"{name}.png"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✓ Created {output_path}")
            
        except Exception as e:
            print(f"  ✗ Error generating {name}: {e}")
    
    print("\nDiagram generation complete!")


if __name__ == "__main__":
    generate_diagrams()
