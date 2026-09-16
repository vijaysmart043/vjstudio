"""
Broadcast Studio Dark UI Theme and CSS stylesheet definition.
"""

# Color Palette Definitions
COLOR_CANVAS = "#0E1014"
COLOR_SURFACE_DARK = "#15181F"
COLOR_SURFACE_CARD = "#1D212A"
COLOR_SURFACE_CARD_HOVER = "#242A35"
COLOR_BORDER = "#2B3240"
COLOR_BORDER_LIGHT = "#384152"

# Broadcast Status Colors
COLOR_PROGRAM_LIVE = "#FF2E4D"       # Neon Red Tally
COLOR_PREVIEW_CUE = "#00E676"        # Neon Green Tally
COLOR_TRANSITION_ACCENT = "#FFB300"  # Amber Transition / Warning
COLOR_PRIMARY_ACCENT = "#00A8FF"     # Electric Blue Focus
COLOR_TEXT_PRIMARY = "#F3F5F7"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_TEXT_DISABLED = "#556070"

# Professional Broadcast QSS Stylesheet
DARK_BROADCAST_STYLESHEET = f"""
/* Global Reset & Base Typography */
QWidget {{
    background-color: {COLOR_CANVAS};
    color: {COLOR_TEXT_PRIMARY};
    font-family: 'Segoe UI', -apple-system, Roboto, Helvetica, Arial, sans-serif;
    font-size: 12px;
    font-weight: 400;
}}

/* Top Menu Bar */
QMenuBar {{
    background-color: {COLOR_SURFACE_DARK};
    border-bottom: 1px solid {COLOR_BORDER};
    padding: 2px 6px;
    font-weight: 500;
}}

QMenuBar::item {{
    background: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background-color: {COLOR_SURFACE_CARD};
    color: {COLOR_PRIMARY_ACCENT};
}}

QMenu {{
    background-color: {COLOR_SURFACE_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 6px 0px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 3px;
}}

QMenu::item:selected {{
    background-color: {COLOR_PRIMARY_ACCENT};
    color: #FFFFFF;
}}

QMenu::separator {{
    height: 1px;
    background: {COLOR_BORDER};
    margin: 4px 10px;
}}

/* Panels and Cards */
QFrame#Panel {{
    background-color: {COLOR_SURFACE_DARK};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
}}

QFrame#Card {{
    background-color: {COLOR_SURFACE_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
}}

/* Section Headers */
QLabel#SectionTitle {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    color: {COLOR_TEXT_MUTED};
    text-transform: uppercase;
    padding-bottom: 2px;
}}

/* Buttons */
QPushButton {{
    background-color: {COLOR_SURFACE_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 600;
    min-height: 24px;
}}

QPushButton:hover {{
    background-color: {COLOR_SURFACE_CARD_HOVER};
    border-color: {COLOR_BORDER_LIGHT};
}}

QPushButton:pressed {{
    background-color: {COLOR_SURFACE_DARK};
}}

/* CUT Action Button */
QPushButton#CutButton {{
    background-color: #241416;
    border: 1px solid #781726;
    color: #FFA3AF;
    font-size: 13px;
    font-weight: 800;
}}

QPushButton#CutButton:hover {{
    background-color: {COLOR_PROGRAM_LIVE};
    color: #FFFFFF;
    border-color: #FF7084;
}}

/* FADE & DISSOLVE Buttons */
QPushButton#TransitionButton {{
    background-color: #1A1F2B;
    border: 1px solid #2B3D63;
    color: #8AC2FF;
    font-size: 12px;
    font-weight: 700;
}}

QPushButton#TransitionButton:hover {{
    background-color: {COLOR_PRIMARY_ACCENT};
    color: #FFFFFF;
}}

/* Scroll Bars */
QScrollBar:vertical {{
    background: {COLOR_SURFACE_DARK};
    width: 8px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLOR_TEXT_MUTED};
}}

/* Sliders (Audio Fader & T-Bar) */
QSlider::groove:horizontal {{
    height: 6px;
    background: {COLOR_SURFACE_DARK};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {COLOR_PRIMARY_ACCENT};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    width: 14px;
    margin-top: -4px;
    margin-bottom: -4px;
    border-radius: 7px;
}}

QSlider::groove:vertical {{
    width: 6px;
    background: {COLOR_SURFACE_DARK};
    border-radius: 3px;
}}

QSlider::sub-page:vertical {{
    background: {COLOR_PRIMARY_ACCENT};
    border-radius: 3px;
}}

QSlider::handle:vertical {{
    background: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    height: 14px;
    margin-left: -4px;
    margin-right: -4px;
    border-radius: 7px;
}}

/* Text inputs & combo boxes */
QLineEdit, QSpinBox, QComboBox {{
    background-color: {COLOR_SURFACE_DARK};
    border: 1px solid {COLOR_BORDER};
    border-radius: 4px;
    padding: 5px 8px;
    color: {COLOR_TEXT_PRIMARY};
}}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {COLOR_PRIMARY_ACCENT};
}}

/* Dialog styling */
QDialog {{
    background-color: {COLOR_CANVAS};
}}

QTabWidget::pane {{
    border: 1px solid {COLOR_BORDER};
    background: {COLOR_SURFACE_DARK};
    border-radius: 6px;
}}

QTabBar::tab {{
    background: {COLOR_CANVAS};
    border: 1px solid {COLOR_BORDER};
    border-bottom: none;
    padding: 8px 16px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background: {COLOR_SURFACE_DARK};
    border-color: {COLOR_PRIMARY_ACCENT};
    color: {COLOR_PRIMARY_ACCENT};
}}
"""
