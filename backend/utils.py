import re

def clean_html_output(text: str) -> str:
    """
    Cleans Gemini output to ensure valid raw HTML.
    Removes markdown fences if present.
    """
    # Remove ```html or ``` if present
    text = re.sub(r"```html", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    return text.strip()
