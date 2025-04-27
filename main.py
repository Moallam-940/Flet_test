import flet as ft
import sys
import os

# إضافة المسار الأساسي للمشروع إلى قائمة المسارات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components.pdf_controls import PDFToolkitApp

def main(page: ft.Page):
    app = PDFToolkitApp(page)

ft.app(target=main)
