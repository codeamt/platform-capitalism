from fasthtml.common import Html, Head, Body, Div, Link, Script

class Layout:
    def __init__(self, title="Platform Simulation"):
        self.title = title

    def wrap(self, content, active_path="/"):
        return Html(
            Head(
                Link(rel="stylesheet", href="/static/css/main.css"),
                Script(src="https://unpkg.com/htmx.org@1.9.2"),
                Script(src="https://cdn.tailwindcss.com")
            ),
            Body(
                Div(
                    Div(f"Active Page: {active_path}", cls="text-sm text-gray-500"),
                    content,
                    cls="max-w-7xl mx-auto p-6 space-y-4"
                )
            )
        )