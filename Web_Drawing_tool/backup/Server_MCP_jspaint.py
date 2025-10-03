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
from playwright.async_api import async_playwright, Error as PlaywrightError

# Playwright (async) for driving jspaint.app (cross-platform, works on macOS)
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# Globals to hold the browser/page similar to paint_app in the original code
_jspaint_browser: Browser | None = None
_jspaint_context: BrowserContext | None = None
_jspaint_page: Page | None = None
_jspaint_lock = asyncio.Lock()

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


# # Replaced Windows/MSPaint-specific tools with cross-platform jspaint.app implementations using Playwright.
# # These keep the same @mcp.tool async signatures and return shapes as your original code.

# #
# @mcp.tool()
# async def open_paint(headless: bool = False) -> dict:
#     """Open JS Paint (jspaint.app) in a browser page and keep it ready for drawing.
#     If Playwright's browser executable is missing, attempt to install Chromium automatically.
#     """
#     global _jspaint_browser, _jspaint_context, _jspaint_page
#     print("CALLED: open_paint() -> dict:")
#     try:
#         async with _jspaint_lock:
#             if _jspaint_page is not None:
#                 return {
#                     "content": [
#                         TextContent(
#                             type="text",
#                             text="JS Paint is already open and ready."
#                         )
#                     ]
#                 }

#             # Helper to attempt launch; separated so we can retry after install
#             async def try_launch():
#                 playwright = await async_playwright().__aenter__()
#                 browser = await playwright.chromium.launch(headless=headless)
#                 context = await browser.new_context()
#                 page = await context.new_page()
#                 await page.goto("https://jspaint.app/")
#                 await page.wait_for_selector("canvas", timeout=10000)
#                 return playwright, browser, context, page

#             try:
#                 playwright, browser, context, page = await try_launch()
#             except PlaywrightError as e:
#                 err_text = str(e)
#                 # detect missing executable error (best-effort match)
#                 if "Executable doesn't exist" in err_text or "Could not find Chromium" in err_text or "install" in err_text:
#                     # Attempt to auto-install chromium using the playwright CLI
#                     try:
#                         # Use the same Python interpreter to run the playwright install command
#                         python_exe = shutil.which("python") or shutil.which("python3") or sys.executable
#                         if not python_exe:
#                             raise RuntimeError("Cannot find python executable to run playwright install.")
#                         # run CLI to install chromium
#                         install_cmd = [python_exe, "-m", "playwright", "install", "chromium"]
#                         subprocess.run(install_cmd, check=True)
#                         # After install, retry launching
#                         playwright, browser, context, page = await try_launch()
#                     except subprocess.CalledProcessError as ie:
#                         return {
#                             "content": [
#                                 TextContent(
#                                     type="text",
#                                     text=f"Error opening JS Paint: Playwright browser install failed: {ie}"
#                                 )
#                             ]
#                         }
#                     except Exception as ie:
#                         return {
#                             "content": [
#                                 TextContent(
#                                     type="text",
#                                     text=f"Error opening JS Paint while attempting install: {ie}"
#                                 )
#                             ]
#                         }
#                 else:
#                     # some other playwright error
#                     return {
#                         "content": [
#                             TextContent(
#                                 type="text",
#                                 text=f"Error opening JS Paint: {err_text}"
#                             )
#                         ]
#                     }

#             # store globals for later use
#             _jspaint_browser = browser
#             _jspaint_context = context
#             _jspaint_page = page

#             # Small delay to let UI settle
#             await asyncio.sleep(0.2)

#             return {
#                 "content": [
#                     TextContent(
#                         type="text",
#                         text="JS Paint opened successfully and ready."
#                     )
#                 ]
#             }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error opening JS Paint: {str(e)}"
#                 )
#             ]
#         }

# # New helper tool to close the browser and cleanup
# @mcp.tool()
# async def close_paint() -> dict:
#     """Close the JS Paint browser/context if open."""
#     global _jspaint_browser, _jspaint_context, _jspaint_page
#     print("CALLED: close_paint() -> dict:")
#     try:
#         async with _jspaint_lock:
#             if _jspaint_page is None:
#                 return {"content":[TextContent(type="text", text="JS Paint is not open.")]}
#             try:
#                 await _jspaint_context.close()
#             except Exception:
#                 pass
#             try:
#                 await _jspaint_browser.close()
#             except Exception:
#                 pass
#             _jspaint_page = None
#             _jspaint_context = None
#             _jspaint_browser = None
#             return {"content":[TextContent(type="text", text="JS Paint closed.")]}
#     except Exception as e:
#         return {"content":[TextContent(type="text", text=f"Error closing JS Paint: {e}")]}

# @mcp.tool()
# async def draw_rectangle_and_text(text: str) -> dict:
#     """Draw a rectangle and add text in JS Paint using hard-coded tool coordinates."""
#     global _jspaint_page
#     print("CALLED: draw_rectangle_and_text(text: str) -> dict:")
#     try:
#         if not _jspaint_page:
#             return {
#                 "content": [
#                     TextContent(
#                         type="text",
#                         text="Paint is not open. Please call open_paint first."
#                     )
#                 ]
#             }

#         page = _jspaint_page

#         # --- Step 0: sanity find canvas and bounds (we need canvas offsets for drawing/text coords) ---
#         canvas = await page.query_selector("canvas")
#         if not canvas:
#             return {"content":[TextContent(type="text", text="Canvas element not found on JS Paint page.")]}
#         box = await canvas.bounding_box()
#         if not box:
#             return {"content":[TextContent(type="text", text="Unable to determine canvas bounds.")]}
#         canvas_left, canvas_top = box["x"], box["y"]
#         canvas_width, canvas_height = box["width"], box["height"]

#         # --- Step 1: click Rectangle tool by viewport coordinates (hard-coded) ---
#         # These coordinates are viewport coordinates (relative to the visible browser window).
#         rect_tool_x, rect_tool_y = 40, 315
#         await page.mouse.click(rect_tool_x, rect_tool_y)
#         await asyncio.sleep(0.18)  # let UI react

#         # --- Step 2: draw rectangle using canvas-relative hard-coded coords ---
#         start_x, start_y = canvas_left + 110, canvas_top + 210
#         end_x, end_y     = canvas_left + 510, canvas_top + 310

#         # Validate coords are inside the canvas
#         if not (0 <= start_x - canvas_left < canvas_width and 0 <= end_x - canvas_left <= canvas_width and
#                 0 <= start_y - canvas_top < canvas_height and 0 <= end_y - canvas_top <= canvas_height):
#             return {
#                 "content": [
#                     TextContent(
#                         type="text",
#                         text=f"Rectangle coordinates outside canvas bounds: canvas size ({int(canvas_width)}x{int(canvas_height)})"
#                     )
#                 ]
#             }

#         await page.mouse.move(start_x, start_y)
#         await page.mouse.down()
#         await page.mouse.move(end_x, end_y, steps=10)
#         await page.mouse.up()
#         await asyncio.sleep(0.25)

#         # --- Step 3: click Text tool by viewport coordinates (hard-coded) ---
#         text_tool_x, text_tool_y = 60, 250
#         await page.mouse.click(text_tool_x, text_tool_y)
#         await asyncio.sleep(0.18)

#         # --- Step 4: click canvas to start typing (hard-coded canvas-relative) ---
#         text_x, text_y = canvas_left + 160, canvas_top + 210
#         if not (0 <= text_x - canvas_left <= canvas_width and 0 <= text_y - canvas_top <= canvas_height):
#             return {
#                 "content": [
#                     TextContent(type="text", text="Text start coordinates outside canvas bounds.")
#                 ]
#             }
#         await page.mouse.click(text_x, text_y)
#         await asyncio.sleep(0.12)

#         # --- Step 5: type the text and exit text mode by clicking outside (hard-coded) ---
#         await page.keyboard.type(text)
#         await asyncio.sleep(0.12)
#         exit_x, exit_y = canvas_left + 510, canvas_top + 310
#         await page.mouse.click(exit_x, exit_y)
#         await asyncio.sleep(0.12)

#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Rectangle drawn and text '{text}' added successfully"
#                 )
#             ]
#         }

#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error: {str(e)}"
#                 )
#             ]
#         }

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
