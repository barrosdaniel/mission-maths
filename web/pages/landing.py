"""Landing page — the first screen a visitor sees.

A minimal placeholder that establishes the Mission Maths theme.
No auth or logic yet; exists so there is something visible in the browser.
"""
from nicegui import ui


def create() -> None:
    """Register the landing page route with NiceGUI."""

    @ui.page("/")
    def landing() -> None:
        ui.query("body").style("margin: 0; background: #0a0e1a;")

        with ui.column().classes("items-center justify-center min-h-screen w-full gap-6"):
            # Mission badge
            ui.label("🚀").style("font-size: 4rem;")

            # Title
            ui.label("Mission Maths").style(
                "font-size: 2.5rem; font-weight: 700; color: #e8f4fd; letter-spacing: 0.05em;"
            )

            # Tagline
            ui.label("Train your mind. Reach the stars.").style(
                "font-size: 1.1rem; color: #7eb8d4; letter-spacing: 0.1em;"
            )

            ui.separator().style("width: 200px; border-color: #1e3a5f; margin: 0.5rem 0;")

            # Fleet Academy rank teaser
            ui.label("Fleet Academy — Trainee Astronaut Programme").style(
                "font-size: 0.85rem; color: #4a7a9b; text-transform: uppercase; letter-spacing: 0.15em;"
            )

            # CTA button (placeholder — no auth yet)
            ui.button(
                "Begin Your Mission",
                on_click=lambda: ui.notify("Coming soon — strap in, astronaut! 🛸"),
            ).props("unelevated rounded").style(
                "background: #1565c0; color: white; font-size: 1rem; "
                "padding: 0.75rem 2.5rem; margin-top: 1rem; letter-spacing: 0.05em;"
            )

            # Build note
            ui.label("Alpha build — mission systems loading…").style(
                "font-size: 0.75rem; color: #2a4a6b; margin-top: 2rem;"
            )
