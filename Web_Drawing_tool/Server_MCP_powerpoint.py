# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import time
import asyncio
import subprocess
import shutil
import os
import subprocess
from pdb import set_trace

# instantiate an MCP server client
mcp = FastMCP("Calculator")


# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# --- open_powerpoint: launch PowerPoint ---
@mcp.tool()
async def open_powerpoint(headless: bool = False) -> dict:
    """Open / bring Microsoft PowerPoint to front on macOS."""
    print("CALLED: open_paint() -> dict:")
    try:
        # Try to open PowerPoint app (non-blocking)
        def _open():
            # Prefer explicit app open; if MS PowerPoint not installed, fallback to 'open' generic
            if shutil.which("open"):
                subprocess.run(["open", "-a", "Microsoft PowerPoint"], check=False)
            else:
                raise RuntimeError("macOS 'open' command not found.")
        await asyncio.to_thread(_open)
        await asyncio.sleep(0.25)
        return {"content":[TextContent(type="text", text="Microsoft PowerPoint launched (or brought to front).")]}

    except Exception as e:
        return {"content":[TextContent(type="text", text=f"Error opening PowerPoint: {e}")]}


# --- draw_rectangle_and_text: AppleScript driven live GUI edits ---
@mcp.tool()
async def draw_rectangle_and_text(text: str) -> dict:
    """
    Draw rectangle and insert text into it in the active PowerPoint window using AppleScript.
    Hard-coded design coordinates (pixels): rectangle (110,210) -> (710,510),
    text start (260,310), exit (610,410). Pixels are converted to points via 0.75 factor.
    """
    print("CALLED: draw_rectangle_and_text(text: str) -> dict:")
    try:
        # Convert pixels -> points (PowerPoint uses points). Assumption: 96 px per inch -> 72 points/inch.
        def px_to_points(px: float) -> float:
            return px * 0.75

        # design pixels (your requested values)
        left_px = 110
        top_px = 210
        right_px = 710
        bottom_px = 510
        # width/height (pixels)
        width_px = right_px - left_px  # 600
        height_px = bottom_px - top_px  # 300

        # Convert to points (rounded to 1 decimal)
        left_pt = round(px_to_points(left_px), 1)
        top_pt = round(px_to_points(top_px), 1)
        width_pt = round(px_to_points(width_px), 1)
        height_pt = round(px_to_points(height_px), 1)

        # Escape user text for AppleScript string literal
        esc_text = str(text).replace("\\", "\\\\").replace('"', '\\"')

        applescript = f'''
tell application "Microsoft PowerPoint"
    activate
    delay 0.12
    -- if no presentation open, create one
    if (count of presentations) = 0 then
        make new presentation
        delay 0.1
    end if
    set pres to active presentation
    -- ensure at least one slide
    if (count of slides of pres) = 0 then
        make new slide at end of pres with properties {{layout:slide layout blank}}
        delay 0.05
    end if
    set theSlide to slide 1 of pres

    -- create rectangle (using points). left/top/width/height are in points.
    set theShape to make new shape at end of theSlide with properties {{auto shape type:autoshape rectangle, left position:{left_pt}, top:{top_pt}, height:{height_pt}, width:{width_pt}}}

    -- put text into the shape
    set content of text range of text frame of theShape to "{esc_text}"

    -- attempt to center paragraph alignment (best-effort)
    try
        set alignment of paragraph format of paragraph 1 of text range of text frame of theShape to paragraph align center
    end try

    -- bring slide to front (select the shape)
    select theShape

end tell
'''
        # Execute AppleScript via osascript in a thread so we don't block the loop
        def _run_applescript(script_str: str):
            # call osascript with script given via stdin for multi-line safety
            proc = subprocess.run(["/usr/bin/osascript", "-"], input=script_str.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return proc

        proc = await asyncio.to_thread(_run_applescript, applescript)

        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="ignore")
            stdout = proc.stdout.decode("utf-8", errors="ignore")
            return {"content": [TextContent(type="text", text=f"AppleScript failed (code {proc.returncode}). stderr: {stderr} stdout: {stdout}")]}

        await asyncio.sleep(2)
        return {"content":[TextContent(type="text", text=f"Rectangle drawn and text '{text}' added in PowerPoint (live).")]}

    except Exception as e:
        return {"content":[TextContent(type="text", text=f"Error: {e}")]}

# --- close_powerpoint: optionally quit PowerPoint ---
@mcp.tool()
async def close_powerpoint() -> dict:
    """Quit Microsoft PowerPoint (optional)."""
    print("CALLED: close_paint() -> dict:")
    try:
        def _quit():
            subprocess.run(["/usr/bin/osascript", "-e", 'tell application "Microsoft PowerPoint" to quit'], check=False)
        await asyncio.to_thread(_quit)
        await asyncio.sleep(0.12)
        return {"content":[TextContent(type="text", text="Requested PowerPoint to quit (if it was running).")]}
    except Exception as e:
        return {"content":[TextContent(type="text", text=f"Error quitting PowerPoint: {e}")]}

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE SERVER AT AMAZING LOCATION")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
