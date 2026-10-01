import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    """
    Scrape readable text from a webpage.

    Args:
        url: Webpage URL to scrape.

    Returns:
        Cleaned webpage text.
    """

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/154.0.0.0 Safari/537.36"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary webpage elements
        for element in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
                "noscript"
            ]
        ):
            element.decompose()

        # Extract readable text
        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Clean excessive whitespace
        text = " ".join(text.split())

        # Limit text size before sending to the LLM
        max_length = 15000

        if len(text) > max_length:
            text = text[:max_length]

        return text

    except requests.exceptions.Timeout:
        return "Error: The webpage took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"Error: Could not access the webpage. {str(e)}"

    except Exception as e:
        return f"Error while scraping webpage: {str(e)}"