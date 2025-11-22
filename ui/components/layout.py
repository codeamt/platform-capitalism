from fasthtml.common import Div, A, Nav, Script

def nav_bar(current_path="/"):
    """Navigation bar for the application."""
    return Nav(
        Div(
            # Logo/Title
            Div(
                A(
                    "🏛️ Platform Capitalism",
                    href="/",
                    cls="text-xl font-bold text-gray-100 hover:text-white"
                ),
                cls="flex-1"
            ),
            
            # Navigation Links
            Div(
                A(
                    "🏠 Dashboard",
                    href="/",
                    cls=f"px-4 py-2 rounded-lg font-medium transition {'bg-blue-600 text-white' if current_path == '/' else 'text-gray-300 hover:bg-gray-700'}"
                ),
                A(
                    "⚙️ Governance Lab",
                    href="/governance-lab",
                    cls=f"px-4 py-2 rounded-lg font-medium transition {'bg-blue-600 text-white' if current_path == '/governance-lab' else 'text-gray-300 hover:bg-gray-700'}"
                ),
                A(
                    "📊 Export Data",
                    href="/export/json",
                    cls="px-4 py-2 rounded-lg font-medium text-gray-300 hover:bg-gray-700 transition"
                ),
                cls="flex gap-2"
            ),
            
            cls="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"
        ),
        cls="bg-gray-900 border-b border-gray-700 sticky top-0 z-50 shadow-lg"
    )

def page_layout(content, current_path="/"):
    """Wrap page content with navigation and consistent styling.
    
    Args:
        content: The page content (typically from a Page function)
        current_path: Current route path for navigation highlighting
    
    Returns:
        Div containing nav + content + scripts
    """
    return Div(
        nav_bar(current_path),
        content,
        # Chart.js for future visualizations (time-series, comparisons, etc.)
        Script(src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"),
        cls="min-h-screen bg-gray-950"
    )