from fasthtml.common import Div, A, Nav, Script, Button

def nav_bar(current_path="/"):
    """Navigation bar for the application."""
    return Nav(
        Div(
            # Logo/Title
            Div(
                A(
                    "🏛️ Platform Capitalism",
                    href="/",
                    cls="text-lg sm:text-xl font-bold text-gray-100 hover:text-white"
                ),
                cls="flex-1"
            ),
            
            # Mobile menu button
            Button(
                "☰",
                cls="md:hidden px-3 py-2 text-gray-300 hover:text-white text-2xl",
                onclick="document.getElementById('mobile-nav').classList.toggle('hidden')"
            ),
            
            # Desktop Navigation Links
            Div(
                A(
                    "🏠 Dashboard",
                    href="/",
                    cls=f"px-3 py-2 rounded-lg font-medium transition text-sm {'bg-blue-600 text-white' if current_path == '/' else 'text-gray-300 hover:bg-gray-700'}"
                ),
                A(
                    "⚙️ Governance Lab",
                    href="/governance-lab",
                    cls=f"px-3 py-2 rounded-lg font-medium transition text-sm {'bg-blue-600 text-white' if current_path == '/governance-lab' else 'text-gray-300 hover:bg-gray-700'}"
                ),
                A(
                    "📊 Export CSV",
                    href="/export/csv",
                    cls="px-3 py-2 rounded-lg font-medium text-gray-300 hover:bg-gray-700 transition text-sm"
                ),
                cls="hidden md:flex gap-2"
            ),
            
            cls="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4 flex items-center justify-between"
        ),
        # Mobile Navigation Menu (hidden by default)
        Div(
            A(
                "🏠 Dashboard",
                href="/",
                cls=f"block px-4 py-3 font-medium transition {'bg-blue-600 text-white' if current_path == '/' else 'text-gray-300 hover:bg-gray-700'}"
            ),
            A(
                "⚙️ Governance Lab",
                href="/governance-lab",
                cls=f"block px-4 py-3 font-medium transition {'bg-blue-600 text-white' if current_path == '/governance-lab' else 'text-gray-300 hover:bg-gray-700'}"
            ),
            A(
                "📊 Export CSV",
                href="/export/csv",
                cls="block px-4 py-3 font-medium text-gray-300 hover:bg-gray-700 transition"
            ),
            id="mobile-nav",
            cls="md:hidden hidden bg-gray-800 border-t border-gray-700"
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