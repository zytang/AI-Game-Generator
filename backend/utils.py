import re

def clean_html_output(text: str) -> str:
    """
    Cleans Gemini output to ensure valid raw HTML.
    Removes markdown fences if present.
    """
    # Remove ```html or ``` if present
    text = re.sub(r"```html", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    
    # Trim whitespace
    text = text.strip()

    # Basic repair: Ensure critical tags are closed if they were opened
    # This is a fallback for truncation
    if "<html" in text.lower() and "</html>" not in text.lower():
        print("!!! CRITICAL ERROR: Game generation was TRUNCATED by the model.")
        print("!!! The generated file will likely be broken.")
        
        # Patching defensively so the page at least loads an error message
        if "</script>" not in text.lower() and "<script" in text.lower():
            text += "\n// [TRUNCATED BY AI]\n</script>"
        text += "\n<div style='position:fixed;bottom:0;left:0;width:100%;background:red;color:white;text-align:center;z-index:9999;padding:10px;'>Warning: This game was truncated during generation and may not work.</div>"
        text += "\n</body></html>"

    return text
