"""
Generate hyper-realistic animated GIF with terminal + simple UI
Strictly following 2026-01-14 guidelines: 
- Terminal Component is MANDATORY
- Hyper-Realistic Terminal Animation (Typing, Cursor, ASCII Table)
- 'P' mode with Image.ADAPTIVE palette
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Terminal color scheme (VS Code style)
BG_COLOR = '#1E1E1E'
TEXT_COLOR = '#D4D4D4'
PROMPT_COLOR = '#4EC9B0'
OUTPUT_COLOR = '#CE9178'
SUCCESS_COLOR = '#4CAF50'
HEADER_COLOR = '#569CD6'
CURSOR_COLOR = '#FFFFFF'
ERROR_COLOR = '#F44336'

# Font loading
def get_fonts():
    try:
        # Try different paths for Mac fonts
        mono_font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 18)
        mono_font_bold = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 20)
        sans_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
        sans_font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except:
        try:
            mono_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 18)
            mono_font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 20)
            sans_font = ImageFont.load_default()
            sans_font_bold = sans_font
        except:
            mono_font = ImageFont.load_default()
            mono_font_bold = mono_font
            sans_font = mono_font
            sans_font_bold = mono_font
    return mono_font, mono_font_bold, sans_font, sans_font_bold

MONO, MONO_BOLD, SANS, SANS_BOLD = get_fonts()

def create_terminal_base(width=1200, height=800):
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw terminal header/title bar
    draw.rectangle([0, 0, width, 40], fill='#333333')
    
    # Window controls (Mac style)
    draw.ellipse([15, 12, 27, 24], fill='#FF5F56') # Red
    draw.ellipse([35, 12, 47, 24], fill='#FFBD2E') # Yellow
    draw.ellipse([55, 12, 67, 24], fill='#27C93F') # Green
    
    draw.text((width//2, 20), "bash — 1200x800", font=MONO, fill='#CCCCCC', anchor='mm')
    
    return img, draw

def draw_text_lines(draw, lines, start_y=60):
    y = start_y
    line_height = 28
    for line, color in lines:
        draw.text((20, y), line, font=MONO, fill=color)
        y += line_height
    return y

def generate_gif():
    print("Generating Hyper-Realistic Animated GIF...")
    
    width, height = 1200, 800
    frames = []
    durations = []
    
    # --- PART 1: Terminal Animation ---
    
    # 1. Initial Prompt & Blink (4 frames)
    for i in range(4):
        img, draw = create_terminal_base(width, height)
        lines = [("$ ", PROMPT_COLOR)]
        draw_text_lines(draw, lines)
        if i % 2 == 0: # Cursor on
            draw.rectangle([45, 62, 57, 85], fill=CURSOR_COLOR)
        frames.append(img)
        durations.append(400) # 400ms for blink
        
    # 2. Typing '$ python main.py'
    command = "python main.py"
    current_cmd = ""
    for char in command:
        current_cmd += char
        img, draw = create_terminal_base(width, height)
        lines = [("$ " + current_cmd, PROMPT_COLOR)]
        draw_text_lines(draw, lines)
        # Always show cursor while typing
        cursor_x = 20 + (len("$ ") + len(current_cmd)) * 11
        draw.rectangle([cursor_x, 62, cursor_x + 12, 85], fill=CURSOR_COLOR)
        frames.append(img)
        durations.append(100) # 100ms per char
        
    # 3. Enter key pause (2 frames)
    for i in range(2):
        img, draw = create_terminal_base(width, height)
        lines = [("$ " + command, PROMPT_COLOR)]
        draw_text_lines(draw, lines)
        if i % 2 == 0:
            cursor_x = 20 + (len("$ ") + len(command)) * 11
            draw.rectangle([cursor_x, 62, cursor_x + 12, 85], fill=CURSOR_COLOR)
        frames.append(img)
        durations.append(300)

    # 4. Successive Output Logs (Dynamic Scrolling)
    logs = [
        ("Initializing AI Real Estate Analysis Engine...", OUTPUT_COLOR),
        ("✓ Knowledge Base: Austin, TX market data loaded", SUCCESS_COLOR),
        ("✓ Agents: MarketAnalyzer, ConditionEvaluator, FinancialAgent active", SUCCESS_COLOR),
        ("Scanning local property listings...", TEXT_COLOR),
        ("Processing ID: PROP-001 [20%]", TEXT_COLOR),
        ("Processing ID: PROP-002 [40%]", TEXT_COLOR),
        ("Processing ID: PROP-003 [60%]", TEXT_COLOR),
        ("Processing ID: PROP-004 [80%]", TEXT_COLOR),
        ("Processing ID: PROP-005 [100%]", TEXT_COLOR),
        ("✓ Analysis complete. Ranking opportunities...", SUCCESS_COLOR),
        ("", TEXT_COLOR),
    ]
    
    current_lines = [("$ " + command, PROMPT_COLOR)]
    for log_line, color in logs:
        current_lines.append((log_line, color))
        img, draw = create_terminal_base(width, height)
        draw_text_lines(draw, current_lines)
        frames.append(img)
        durations.append(150) # Faster scrolling

    # 5. ASCII Table Reveal
    table_lines = [
        ("┌──────────┬───────────┬────────────┬───────┬───────┬────────────┐", TEXT_COLOR),
        ("│ ID       │ City      │ Price      │ Grade │ ROI % │ Status     │", HEADER_COLOR),
        ("├──────────┼───────────┼────────────┼───────┼───────┼────────────┤", TEXT_COLOR),
        ("│ PROP-004 │ Nashville │ $550,000   │  A+   │ 112%  │ Strong Buy │", SUCCESS_COLOR),
        ("│ PROP-003 │ Phoenix   │ $320,000   │  A-   │  88%  │ Strong Buy │", SUCCESS_COLOR),
        ("│ PROP-001 │ Austin    │ $425,000   │  B+   │  72%  │ Buy        │", OUTPUT_COLOR),
        ("│ PROP-005 │ Charlotte │ $380,000   │  B    │  65%  │ Buy        │", OUTPUT_COLOR),
        ("│ PROP-002 │ San Diego │ $785,000   │  B-   │  15%  │ Pass       │", ERROR_COLOR),
        ("└──────────┴───────────┴────────────┴───────┴───────┴────────────┘", TEXT_COLOR),
        ("", TEXT_COLOR),
        ("Generating detailed visual report...", SUCCESS_COLOR)
    ]
    
    current_lines.extend(table_lines)
    img, draw = create_terminal_base(width, height)
    draw_text_lines(draw, current_lines)
    # Final hold on table
    frames.append(img)
    durations.append(2500) # Hold for 2.5 seconds

    # --- PART 2: UI Dashboard Transition ---
    
    # 6. UI Dashboard (The "impressive" part)
    ui_bg = '#F0F2F5'
    ui_header = '#1877F2'
    
    img = Image.new('RGB', (width, height), ui_bg)
    draw = ImageDraw.Draw(img)
    
    # UI Header
    draw.rectangle([0, 0, width, 80], fill=ui_header)
    draw.text((40, 40), "AI INVESTMENT ANALYZER", font=SANS_BOLD, fill='white', anchor='lm')
    draw.text((width-40, 40), "BETA v2.4", font=SANS, fill='white', anchor='rm')
    
    # Top Card
    draw.rectangle([40, 100, width-40, 300], fill='white', outline='#DDDDDD', width=2)
    draw.text((70, 140), "MOST PROMISING OPPORTUNITY", font=SANS, fill='#666666')
    draw.text((70, 185), "PROP-004: 2345 Downtown Plaza, Nashville, TN", font=SANS_BOLD, fill='#1C1E21')
    draw.text((70, 230), "$550,000 • 3B/3B • Multi-Family", font=SANS, fill='#666666')
    
    # Badge
    draw.ellipse([width-220, 130, width-80, 270], fill='#4CAF50')
    draw.text((width-150, 200), "A+", font=SANS_BOLD, fill='white', anchor='mm')
    
    # Metrics Grid
    metrics = [
        ("Cap Rate", "9.2%"), ("Monthly Cash Flow", "$800"),
        ("Location Score", "94/100"), ("Market Heat", "Hot"),
        ("5-Yr ROI", "112.4%"), ("Risk Assessment", "Low")
    ]
    
    for i, (label, val) in enumerate(metrics):
        col = i % 2
        row = i // 2
        x = 40 + col * (width//2 - 40)
        y = 330 + row * 120
        draw.rectangle([x, y, x + (width//2 - 60), y + 100], fill='white', outline='#DDDDDD', width=2)
        draw.text((x+30, y+30), label, font=SANS, fill='#666666')
        draw.text((x+30, y+70), val, font=SANS_BOLD, fill='#1877F2')
    
    # Recommendation Footer
    draw.rectangle([40, 700, width-40, 780], fill='#E7F3FF')
    draw.text((width//2, 740), "RECOMMENDATION: PROCEED WITH IMMEDIATE DUE DILIGENCE", 
              font=SANS_BOLD, fill='#1877F2', anchor='mm')
    
    frames.append(img)
    durations.append(4000) # Hold UI for 4 seconds

    # --- SAVE GIF WITH GLOBAL PALETTE ---
    print(f"Quantizing {len(frames)} frames to global palette...")
    
    # Create a dummy image to capture all colors
    combined = Image.new('RGB', (width, height * len(frames)))
    for i, f in enumerate(frames):
        combined.paste(f, (0, i * height))
    
    # Generate global palette
    global_palette_img = combined.quantize(colors=256, method=Image.MAXCOVERAGE)
    
    palette_frames = []
    for f in frames:
        # Quantize to the global palette
        pf = f.quantize(palette=global_palette_img)
        palette_frames.append(pf)
        
    output_path = Path("images/title-animation.gif")
    output_path.parent.mkdir(exist_ok=True)
    
    print(f"Saving GIF to {output_path}...")
    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    
    print(f"✓ GIF Created Successfully! ({output_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_gif()
