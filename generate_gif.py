"""
Generate animated GIF with terminal + simple UI
Following 2026-01-14 guidelines: Terminal (MANDATORY) + Simple UI (not complex graphs)
"""
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pathlib import Path
import time


# Terminal color scheme
BG_COLOR = '#1E1E1E'
TEXT_COLOR = '#D4D4D4'
PROMPT_COLOR = '#4EC9B0'
OUTPUT_COLOR = '#CE9178'
SUCCESS_COLOR = '#4CAF50'
HEADER_COLOR = '#569CD6'
CURSOR_COLOR = '#FFFFFF'


def create_terminal_frame(width=1200, height=800, text_lines=None, cursor_pos=None):
    """Creates a single terminal frame"""
    
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 16)
        font_large = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 18)
    except:
        font = ImageFont.load_default()
        font_large = font
    
    y_offset = 30
    line_height = 25
    
    # Draw terminal header
    draw.text((20, y_offset), "real-estate-analyzer", font=font_large, fill=HEADER_COLOR)
    y_offset += 40
    
    # Draw text lines
    if text_lines:
        for line, color in text_lines:
            draw.text((20, y_offset), line, font=font, fill=color)
            y_offset += line_height
    
    # Draw cursor if specified
    if cursor_pos:
        cursor_x, cursor_y = cursor_pos
        draw.rectangle([cursor_x, cursor_y, cursor_x + 10, cursor_y + 20], fill=CURSOR_COLOR)
    
    return img


def create_typing_frames(command, num_frames=15):
    """Creates frames showing typing effect"""
    
    frames = []
    
    for i in range(num_frames + 1):
        chars_to_show = int((i / num_frames) * len(command))
        partial_command = command[:chars_to_show]
        
        text_lines = [
            ("$ " + partial_command, PROMPT_COLOR)
        ]
        
        # Add cursor at end of text
        cursor_x = 20 + len("$ " + partial_command) * 10
        cursor_y = 70
        
        frame = create_terminal_frame(text_lines=text_lines, cursor_pos=(cursor_x, cursor_y))
        frames.append(frame)
    
    return frames


def create_execution_frames():
    """Creates frames showing command execution"""
    
    frames = []
    
    # Frame 1: Command entered
    text_lines = [
        ("$ python main.py", PROMPT_COLOR),
        ("", TEXT_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    # Frame 2: Initializing
    text_lines = [
        ("$ python main.py", PROMPT_COLOR),
        ("", TEXT_COLOR),
        ("Initializing AI Agents...", OUTPUT_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    # Frame 3: Agents initialized
    text_lines = [
        ("$ python main.py", PROMPT_COLOR),
        ("", TEXT_COLOR),
        ("Initializing AI Agents...", OUTPUT_COLOR),
        ("✓ All agents initialized successfully", SUCCESS_COLOR),
        ("", TEXT_COLOR),
        ("Loaded 5 properties for analysis", OUTPUT_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    # Frame 4: Analyzing first property
    text_lines = [
        ("$ python main.py", PROMPT_COLOR),
        ("", TEXT_COLOR),
        ("Initializing AI Agents...", OUTPUT_COLOR),
        ("✓ All agents initialized successfully", SUCCESS_COLOR),
        ("", TEXT_COLOR),
        ("Loaded 5 properties for analysis", OUTPUT_COLOR),
        ("", TEXT_COLOR),
        ("Analyzing Property: PROP-001", HEADER_COLOR),
        ("1234 Maple Street, Austin, TX", TEXT_COLOR),
        ("", TEXT_COLOR),
        ("  ✓ Location Score: 85.0/100", SUCCESS_COLOR),
        ("  ✓ Market Heat: Hot", OUTPUT_COLOR),
        ("  ✓ Appreciation Rate: 8.5%/year", SUCCESS_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    # Frame 5: Financial metrics
    text_lines = [
        ("$ python main.py", PROMPT_COLOR),
        ("", TEXT_COLOR),
        ("Analyzing Property: PROP-001", HEADER_COLOR),
        ("1234 Maple Street, Austin, TX", TEXT_COLOR),
        ("", TEXT_COLOR),
        ("  ✓ Location Score: 85.0/100", SUCCESS_COLOR),
        ("  ✓ Condition Score: 82.5/100", SUCCESS_COLOR),
        ("  ✓ Cap Rate: 6.8%", SUCCESS_COLOR),
        ("  ✓ Monthly Cash Flow: $200", SUCCESS_COLOR),
        ("  ✓ 5-Year ROI: 95.2%", SUCCESS_COLOR),
        ("  ✓ Investment Grade: B+", HEADER_COLOR),
        ("  ✓ Recommendation: Buy", SUCCESS_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    # Frame 6: Processing more properties
    text_lines = [
        ("Analyzing Property: PROP-002", HEADER_COLOR),
        ("567 Ocean View Blvd, San Diego, CA", TEXT_COLOR),
        ("  ✓ Investment Grade: B-", HEADER_COLOR),
        ("", TEXT_COLOR),
        ("Analyzing Property: PROP-003", HEADER_COLOR),
        ("890 Industrial Ave, Phoenix, AZ", TEXT_COLOR),
        ("  ✓ Investment Grade: A-", HEADER_COLOR),
        ("", TEXT_COLOR),
        ("Analyzing Property: PROP-004", HEADER_COLOR),
        ("2345 Downtown Plaza, Nashville, TN", TEXT_COLOR),
        ("  ✓ Investment Grade: A+", HEADER_COLOR)
    ]
    frames.append(create_terminal_frame(text_lines=text_lines))
    
    return frames


def create_ascii_table_frame():
    """Creates frame with ASCII summary table"""
    
    text_lines = [
        ("=" * 80, TEXT_COLOR),
        ("            INVESTMENT ANALYSIS SUMMARY", HEADER_COLOR),
        ("=" * 80, TEXT_COLOR),
        ("", TEXT_COLOR),
        ("Property ID  City        Price      Grade  Score  Cap Rate  Cash Flow  Recommendation", TEXT_COLOR),
        ("───────────────────────────────────────────────────────────────────────────────────────", TEXT_COLOR),
        ("PROP-004     Nashville   $550,000   A+     92.3   9.2%      $800       Strong Buy", SUCCESS_COLOR),
        ("PROP-003     Phoenix     $320,000   A-     87.8   8.5%      $400       Strong Buy", SUCCESS_COLOR),
        ("PROP-001     Austin      $425,000   B+     78.5   6.8%      $200       Buy", OUTPUT_COLOR),
        ("PROP-005     Charlotte   $380,000   B      75.2   7.1%      $200       Buy", OUTPUT_COLOR),
        ("PROP-002     San Diego   $785,000   B-     68.4   4.2%      -$400      Pass", TEXT_COLOR),
        ("", TEXT_COLOR),
        ("Analysis Complete! Results saved to analysis_results.json", SUCCESS_COLOR)
    ]
    
    return create_terminal_frame(text_lines=text_lines)


def create_simple_ui_frame():
    """Creates simple UI showing top property details (NOT complex graphs)"""
    
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        font_header = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_text = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_value = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        font_title = ImageFont.load_default()
        font_header = font_title
        font_text = font_title
        font_value = font_title
    
    # Header
    draw.rectangle([0, 0, width, 80], fill='#2196F3')
    draw.text((width//2, 40), "TOP INVESTMENT OPPORTUNITY", font=font_title, fill='white', anchor='mm')
    
    # Property card
    card_y = 120
    draw.rectangle([50, card_y, width-50, card_y+180], fill='white', outline='#CCCCCC', width=2)
    
    # Property details
    y = card_y + 30
    draw.text((70, y), "PROP-004: 2345 Downtown Plaza, Nashville, TN", font=font_header, fill='#333333')
    y += 40
    draw.text((70, y), "3 bed / 3 bath / 1,650 sqft / Multi-Family", font=font_text, fill='#666666')
    y += 35
    draw.text((70, y), "Price: $550,000", font=font_text, fill='#666666')
    y += 35
    draw.text((70, y), "Estimated Rent: $3,800/month", font=font_text, fill='#666666')
    
    # Investment grade badge
    badge_x = width - 200
    badge_y = card_y + 60
    draw.ellipse([badge_x, badge_y, badge_x+120, badge_y+120], fill='#4CAF50', outline='#2E7D32', width=3)
    draw.text((badge_x+60, badge_y+60), "A+", font=font_title, fill='white', anchor='mm')
    
    # Metrics grid
    metrics_y = card_y + 220
    draw.rectangle([50, metrics_y, width-50, metrics_y+280], fill='white', outline='#CCCCCC', width=2)
    
    draw.text((width//2, metrics_y+20), "KEY INVESTMENT METRICS", font=font_header, fill='#2196F3', anchor='mm')
    
    # Metrics in grid
    metrics = [
        ("Overall Score", "92.3/100", "#4CAF50"),
        ("Cap Rate", "9.2%", "#4CAF50"),
        ("Monthly Cash Flow", "$800", "#4CAF50"),
        ("5-Year ROI", "112.4%", "#4CAF50"),
        ("Risk Level", "Low", "#4CAF50"),
        ("Recommendation", "Strong Buy", "#4CAF50")
    ]
    
    grid_y = metrics_y + 70
    col_width = (width - 100) // 2
    
    for i, (label, value, color) in enumerate(metrics):
        row = i // 2
        col = i % 2
        x = 70 + col * col_width
        y = grid_y + row * 60
        
        draw.text((x, y), label, font=font_text, fill='#666666')
        draw.text((x, y+25), value, font=font_value, fill=color)
    
    # Footer
    draw.rectangle([0, height-60, width, height], fill='#37474F')
    draw.text((width//2, height-30), "AI-Powered Real Estate Investment Analyzer", 
             font=font_text, fill='white', anchor='mm')
    
    return img


def generate_gif():
    """Generates the complete animated GIF"""
    
    print("Generating animated GIF (Terminal + Simple UI)...")
    
    all_frames = []
    
    # Part 1: MANDATORY Terminal Animation
    print("  Creating typing effect frames...")
    typing_frames = create_typing_frames("python main.py")
    all_frames.extend(typing_frames)
    
    print("  Creating execution frames...")
    execution_frames = create_execution_frames()
    all_frames.extend(execution_frames)
    
    print("  Creating ASCII table frame...")
    table_frame = create_ascii_table_frame()
    all_frames.extend([table_frame] * 5)  # Hold for 5 frames
    
    # Part 2: Simple UI (NOT complex graphs - following 2026-01-14 guidelines)
    print("  Creating simple UI frame...")
    ui_frame = create_simple_ui_frame()
    all_frames.extend([ui_frame] * 5)  # Hold for 5 frames
    
    # Convert all frames to palette mode for compatibility
    print("  Converting frames to palette mode...")
    palette_frames = []
    for frame in all_frames:
        palette_frame = frame.convert('P', palette=Image.ADAPTIVE, colors=256)
        palette_frames.append(palette_frame)
    
    # Save as GIF
    output_path = Path("images/title-animation.gif")
    output_path.parent.mkdir(exist_ok=True)
    
    print("  Saving GIF...")
    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=200,  # 200ms per frame
        loop=0
    )
    
    print(f"✓ Created {output_path}")
    print(f"  Total frames: {len(palette_frames)}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    generate_gif()
