import os
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from google.genai import types

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def analyze_webpage(
    working_directory: str,
    url: str,
    analysis_type: str = "full",
    include_html: bool = False,
):
    """
    Analyze a webpage using BeautifulSoup.

    Args:
        working_directory: Working directory (not used in this function but kept for consistency)
        url: The URL of the webpage to analyze
        analysis_type: Type of analysis to perform ('full', 'structure', 'content', 'links', 'forms', 'images')
        include_html: Whether to include the raw HTML structure in the output

    Returns:
        A detailed analysis of the webpage structure and content
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        result = {
            "url": url,
            "status_code": response.status_code,
            "title": soup.title.string if soup.title else "No title",
            "encoding": response.encoding,
            "length": len(response.content),
        }

        if analysis_type in ["full", "structure"]:
            result["meta_tags"] = _extract_meta_tags(soup)
            result["headings"] = _extract_headings(soup)
            result["html_structure"] = (
                _extract_structure(soup) if include_html else None
            )

        if analysis_type in ["full", "content"]:
            result["text_content"] = _extract_text_content(soup)
            result["body_structure"] = _extract_body_structure(soup)

        if analysis_type in ["full", "links"]:
            result["links"] = _extract_links(soup, url)

        if analysis_type in ["full", "images"]:
            result["images"] = _extract_images(soup, url)

        if analysis_type in ["full", "forms"]:
            result["forms"] = _extract_forms(soup)

        result["stylesheets"] = _extract_stylesheets(soup, url)
        result["scripts"] = _extract_scripts(soup, url)

        return _format_result(result, analysis_type)

    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error analyzing webpage: {str(e)}"


def _extract_meta_tags(soup):
    """Extract meta tags from the webpage."""
    meta_tags = {}

    for meta in soup.find_all("meta"):
        if meta.get("name"):
            meta_tags[meta.get("name")] = meta.get("content", "")
        elif meta.get("property"):
            meta_tags[meta.get("property")] = meta.get("content", "")

    return meta_tags


def _extract_headings(soup):
    """Extract all heading tags and their text."""
    headings = {}

    for level in range(1, 7):
        h_tags = soup.find_all(f"h{level}")
        if h_tags:
            headings[f"h{level}"] = [tag.get_text(strip=True) for tag in h_tags]

    return headings


def _extract_structure(soup):
    """Extract the basic HTML structure."""
    structure = {
        "doctype": str(soup.contents[0])
        if soup.contents and len(soup.contents) > 0
        else None,
        "html_tag": str(soup.find("html")) if soup.find("html") else None,
        "head_tag": str(soup.find("head")) if soup.find("head") else None,
    }
    return structure


def _extract_text_content(soup):
    """Extract text content from the webpage."""
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator=" ", strip=True)

    paragraphs = soup.find_all("p")
    paragraph_texts = [p.get_text(strip=True) for p in paragraphs]

    return {
        "full_text": text,
        "word_count": len(text.split()),
        "paragraph_count": len(paragraphs),
        "sample_paragraphs": paragraph_texts[:5],
    }


def _extract_body_structure(soup):
    """Extract the structure of the body element."""
    body = soup.find("body")
    if not body:
        return {"error": "No body tag found"}

    structure = {
        "main_elements": [],
        "container_divs": [],
        "navigation": [],
        "footer": None,
    }

    for tag in body.find_all(["nav", "header", "main", "footer", "aside", "section"]):
        if tag.name in ["nav", "header", "footer"]:
            structure[tag.name + "s"].append(tag.get_text(strip=True)[:100])
        else:
            structure["main_elements"].append(
                {
                    "tag": tag.name,
                    "id": tag.get("id", ""),
                    "class": " ".join(tag.get("class", [])),
                    "text_preview": tag.get_text(strip=True)[:100],
                }
            )

    return structure


def _extract_links(soup, base_url):
    """Extract all links from the webpage."""
    links = []

    for link in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, link["href"])

        links.append(
            {
                "text": link.get_text(strip=True),
                "url": absolute_url,
                "type": _categorize_link(absolute_url, base_url),
            }
        )

    return {
        "total_count": len(links),
        "external_links": [l for l in links if l["type"] == "external"],
        "internal_links": [l for l in links if l["type"] == "internal"],
        "sample_links": links[:20],
    }


def _categorize_link(url, base_url):
    """Categorize a link as internal, external, or anchor."""
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)

    if url.startswith("#"):
        return "anchor"
    elif parsed_url.netloc == parsed_base.netloc:
        return "internal"
    else:
        return "external"


def _extract_images(soup, base_url):
    """Extract all images from the webpage."""
    images = []

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            absolute_url = urljoin(base_url, src)

            images.append(
                {
                    "src": absolute_url,
                    "alt": img.get("alt", ""),
                    "width": img.get("width", ""),
                    "height": img.get("height", ""),
                }
            )

    return {
        "total_count": len(images),
        "images": images[:20],
    }


def _extract_forms(soup):
    """Extract all forms from the webpage."""
    forms = []

    for form in soup.find_all("form"):
        inputs = []
        for input_tag in form.find_all(["input", "textarea", "select"]):
            inputs.append(
                {
                    "type": input_tag.get("type", input_tag.name),
                    "name": input_tag.get("name", ""),
                    "id": input_tag.get("id", ""),
                }
            )

        forms.append(
            {
                "action": form.get("action", ""),
                "method": form.get("method", "GET"),
                "inputs": inputs,
            }
        )

    return forms


def _extract_stylesheets(soup, base_url):
    """Extract all stylesheet links."""
    stylesheets = []

    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if href:
            absolute_url = urljoin(base_url, href)
            stylesheets.append(absolute_url)

    return stylesheets


def _extract_scripts(soup, base_url):
    """Extract all script sources."""
    scripts = []

    for script in soup.find_all("script"):
        src = script.get("src", "")
        if src:
            absolute_url = urljoin(base_url, src)
            scripts.append(absolute_url)

    return scripts


def _format_result(result, analysis_type):
    """Format the analysis result for display."""
    output = []

    output.append("=" * 80)
    output.append("WEBPAGE ANALYSIS")
    output.append("=" * 80)
    output.append(f"\nURL: {result['url']}")
    output.append(f"Title: {result['title']}")
    output.append(f"Status: {result['status_code']}")
    output.append(f"Content Length: {result['length']} bytes")

    if "meta_tags" in result:
        output.append("\n" + "-" * 80)
        output.append("META TAGS")
        output.append("-" * 80)
        for key, value in result["meta_tags"].items():
            output.append(f"{key}: {value}")

    if "headings" in result:
        output.append("\n" + "-" * 80)
        output.append("HEADINGS STRUCTURE")
        output.append("-" * 80)
        for level, headings in result["headings"].items():
            output.append(f"{level.upper()}: {len(headings)} headings")
            for heading in headings[:5]:
                output.append(f"  - {heading}")
            if len(headings) > 5:
                output.append(f"  ... and {len(headings) - 5} more")

    if "text_content" in result:
        output.append("\n" + "-" * 80)
        output.append("TEXT CONTENT")
        output.append("-" * 80)
        output.append(f"Word Count: {result['text_content']['word_count']}")
        output.append(f"Paragraph Count: {result['text_content']['paragraph_count']}")
        output.append("\nSample Paragraphs:")
        for para in result["text_content"]["sample_paragraphs"]:
            output.append(f"  {para[:150]}...")

    if "links" in result:
        output.append("\n" + "-" * 80)
        output.append("LINKS")
        output.append("-" * 80)
        output.append(f"Total Links: {result['links']['total_count']}")
        output.append(f"Internal: {len(result['links']['internal_links'])}")
        output.append(f"External: {len(result['links']['external_links'])}")
        output.append("\nSample Links:")
        for link in result["links"]["sample_links"][:10]:
            output.append(
                f"  [{link['type'].upper()}] {link['text'][:50]}... -> {link['url'][:60]}..."
            )

    if "images" in result:
        output.append("\n" + "-" * 80)
        output.append("IMAGES")
        output.append("-" * 80)
        output.append(f"Total Images: {result['images']['total_count']}")
        output.append("\nSample Images:")
        for img in result["images"]["images"][:10]:
            alt = img["alt"] if img["alt"] else "No alt text"
            output.append(f"  Alt: {alt[:50]}... -> {img['src'][:60]}...")

    if "forms" in result:
        output.append("\n" + "-" * 80)
        output.append("FORMS")
        output.append("-" * 80)
        output.append(f"Total Forms: {len(result['forms'])}")
        for form in result["forms"]:
            output.append(f"  Action: {form['action']}")
            output.append(f"  Method: {form['method']}")
            output.append(f"  Inputs: {len(form['inputs'])}")

    if "stylesheets" in result:
        output.append("\n" + "-" * 80)
        output.append("STYLESHEETS")
        output.append("-" * 80)
        for css in result["stylesheets"]:
            output.append(f"  {css}")

    if "scripts" in result:
        output.append("\n" + "-" * 80)
        output.append("SCRIPTS")
        output.append("-" * 80)
        for script in result["scripts"]:
            output.append(f"  {script}")

    if result.get("html_structure") and any(result["html_structure"].values()):
        output.append("\n" + "-" * 80)
        output.append("HTML STRUCTURE (for replication)")
        output.append("-" * 80)

        if result["html_structure"].get("doctype"):
            output.append("\nDOCTYPE:")
            output.append(result["html_structure"]["doctype"])

        if result["html_structure"].get("html_tag"):
            output.append("\nHTML Tag:")
            output.append(result["html_structure"]["html_tag"])

        if result["html_structure"].get("head_tag"):
            output.append("\nHEAD Tag:")
            output.append(result["html_structure"]["head_tag"])

    output.append("\n" + "=" * 80)

    return "\n".join(output)


schema_analyze_webpage = types.FunctionDeclaration(
    name="analyze_webpage",
    description="Analyze a webpage using BeautifulSoup. Provides comprehensive analysis including structure, content, links, images, and forms. Useful for understanding webpage layout and replicating web designs.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "url": types.Schema(
                type=types.Type.STRING,
                description="The URL of the webpage to analyze (e.g., 'https://example.com')",
            ),
            "analysis_type": types.Schema(
                type=types.Type.STRING,
                description="Type of analysis to perform. Options: 'full' (default, comprehensive analysis), 'structure' (HTML structure and meta tags), 'content' (text content and body structure), 'links' (all links and categorization), 'forms' (form elements), 'images' (image elements)",
                enum=["full", "structure", "content", "links", "forms", "images"],
            ),
            "include_html": types.Schema(
                type=types.Type.BOOLEAN,
                description="Whether to include raw HTML structure in the output for replication purposes (default: False)",
            ),
        },
        required=["url"],
    ),
)
