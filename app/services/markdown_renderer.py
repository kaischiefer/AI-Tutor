import bleach
import markdown


ALLOWED_TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "p",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "blockquote",
    "pre",
    "code",
    "hr",
    "br",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
]

ALLOWED_ATTRIBUTES: dict[str, list[str]] = {}


def render_markdown(content: str) -> str:
    raw_html = markdown.markdown(
        content,
        extensions=[
            "fenced_code",
            "tables",
        ],
    )

    return bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )