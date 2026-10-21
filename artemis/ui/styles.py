"""Stylesheet for the translucent look."""

STYLE = """
#bar {
    background: rgba(18, 18, 26, 175);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
QToolButton { background: transparent; border: none; border-radius: 8px; }
QToolButton:hover { background: rgba(255, 255, 255, 40); }
QToolButton:disabled { background: transparent; }
#close:hover { background: rgba(220, 60, 60, 210); }
QLineEdit {
    background: rgba(255, 255, 255, 38); color: white; border: none;
    border-radius: 15px; padding: 5px 14px; font-size: 13px;
    selection-background-color: rgba(120, 140, 255, 180);
}
QLineEdit:focus { background: rgba(255, 255, 255, 62); }
QMenu { background: rgba(28, 28, 38, 245); color: white; border-radius: 8px; padding: 4px; }
QMenu::item { padding: 6px 18px; border-radius: 6px; }
QMenu::item:selected { background: rgba(255, 255, 255, 45); }
QDialog { background: #1c1c26; color: white; }
QDialog QLabel, QDialog QCheckBox { color: white; }
QDialog QPushButton { background: rgba(255, 255, 255, 30); color: white; border: none;
                      border-radius: 6px; padding: 6px 14px; }
QDialog QPushButton:hover { background: rgba(255, 255, 255, 55); }
QDialog QLineEdit, QDialog QDoubleSpinBox { background: rgba(255, 255, 255, 25);
                      border-radius: 6px; padding: 4px 8px; color: white; }
"""
