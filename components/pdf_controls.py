import flet as ft
from typing import List
from utils.pdf_operations import (
    compress_pdf,
    extract_pages,
    merge_pdfs,
    delete_pages,
    split_pdf,
    parse_page_ranges,
)

class PDFToolkitApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PDF Toolkit"
        self.page.window_width = 600
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.build_ui()

    def build_ui(self):
        """Build the main menu UI"""
        self.main_menu = ft.Column(
            controls=[
                ft.Text("PDF Toolkit", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ElevatedButton("Extract Pages", on_click=self.show_extract_form),
                ft.ElevatedButton("Merge PDFs", on_click=self.show_merge_form),
                ft.ElevatedButton("Split PDF", on_click=self.show_split_form),
                ft.ElevatedButton("Delete Pages", on_click=self.show_delete_form),
                ft.ElevatedButton("Compress PDF", on_click=self.show_compress_form),
                ft.ElevatedButton("Exit", on_click=lambda _: self.page.window_destroy()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page.add(self.main_menu)

    def show_snack(self, text: str):
        """Show a snackbar message"""
        self.page.snack_bar = ft.SnackBar(ft.Text(text), duration=3000)
        self.page.snack_bar.open = True
        self.page.update()

    def return_to_menu(self):
        """Return to the main menu"""
        self.page.clean()
        self.build_ui()

    def show_extract_form(self, e):
        """Show form for extracting pages"""
        input_pdf_field = ft.TextField(label="Input PDF Path", width=500)
        output_pdf_field = ft.TextField(label="Output PDF Path", width=500)
        page_ranges_field = ft.TextField(label="Page Ranges (e.g., 1-5,8-10)", width=500)
        submit_button = ft.ElevatedButton(
            "Extract",
            on_click=lambda _: self.handle_extract(
                input_pdf_field.value, output_pdf_field.value, page_ranges_field.value
            ),
        )
        back_button = ft.ElevatedButton("Back to Menu", on_click=lambda _: self.return_to_menu())
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Extract Pages", size=20, weight=ft.FontWeight.BOLD),
                    input_pdf_field,
                    output_pdf_field,
                    page_ranges_field,
                    submit_button,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def handle_extract(self, input_pdf: str, output_pdf: str, page_ranges: str):
        try:
            extract_pages(input_pdf, output_pdf, parse_page_ranges(page_ranges))
            self.show_snack("Pages extracted successfully!")
        except Exception as ex:
            self.show_snack(f"Error: {ex}")

    def show_merge_form(self, e):
        """Show form for merging PDFs"""
        input_files_field = ft.TextField(label="Input PDF Files (comma-separated)", width=500)
        output_pdf_field = ft.TextField(label="Output PDF Path", width=500)
        submit_button = ft.ElevatedButton(
            "Merge",
            on_click=lambda _: self.handle_merge(
                input_files_field.value.split(","), output_pdf_field.value
            ),
        )
        back_button = ft.ElevatedButton("Back to Menu", on_click=lambda _: self.return_to_menu())
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Merge PDFs", size=20, weight=ft.FontWeight.BOLD),
                    input_files_field,
                    output_pdf_field,
                    submit_button,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def handle_merge(self, input_files: List[str], output_pdf: str):
        try:
            merge_pdfs(input_files, output_pdf)
            self.show_snack("Files merged successfully!")
        except Exception as ex:
            self.show_snack(f"Error: {ex}")

    def show_split_form(self, e):
        """Show form for splitting PDF"""
        input_pdf_field = ft.TextField(label="Input PDF Path", width=500)
        pages_per_part_field = ft.TextField(label="Pages Per Part", width=500)
        submit_button = ft.ElevatedButton(
            "Split",
            on_click=lambda _: self.handle_split(input_pdf_field.value, int(pages_per_part_field.value)),
        )
        back_button = ft.ElevatedButton("Back to Menu", on_click=lambda _: self.return_to_menu())
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Split PDF", size=20, weight=ft.FontWeight.BOLD),
                    input_pdf_field,
                    pages_per_part_field,
                    submit_button,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def handle_split(self, input_pdf: str, pages_per_part: int):
        try:
            split_pdf(input_pdf, pages_per_part)
            self.show_snack("PDF split successfully!")
        except Exception as ex:
            self.show_snack(f"Error: {ex}")

    def show_delete_form(self, e):
        """Show form for deleting pages"""
        input_pdf_field = ft.TextField(label="Input PDF Path", width=500)
        output_pdf_field = ft.TextField(label="Output PDF Path", width=500)
        page_ranges_field = ft.TextField(label="Page Ranges to Delete (e.g., 1-5,8-10)", width=500)
        submit_button = ft.ElevatedButton(
            "Delete",
            on_click=lambda _: self.handle_delete(
                input_pdf_field.value, output_pdf_field.value, page_ranges_field.value
            ),
        )
        back_button = ft.ElevatedButton("Back to Menu", on_click=lambda _: self.return_to_menu())
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Delete Pages", size=20, weight=ft.FontWeight.BOLD),
                    input_pdf_field,
                    output_pdf_field,
                    page_ranges_field,
                    submit_button,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def handle_delete(self, input_pdf: str, output_pdf: str, page_ranges: str):
        try:
            delete_pages(input_pdf, output_pdf, parse_page_ranges(page_ranges))
            self.show_snack("Pages deleted successfully!")
        except Exception as ex:
            self.show_snack(f"Error: {ex}")

    def show_compress_form(self, e):
        """Show form for compressing PDF"""
        input_pdf_field = ft.TextField(label="Input PDF Path", width=500)
        output_pdf_field = ft.TextField(label="Output PDF Path", width=500)
        compression_level_field = ft.TextField(label="Compression Level (1-5)", width=500)
        submit_button = ft.ElevatedButton(
            "Compress",
            on_click=lambda _: self.handle_compress(
                input_pdf_field.value, output_pdf_field.value, int(compression_level_field.value)
            ),
        )
        back_button = ft.ElevatedButton("Back to Menu", on_click=lambda _: self.return_to_menu())
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Compress PDF", size=20, weight=ft.FontWeight.BOLD),
                    input_pdf_field,
                    output_pdf_field,
                    compression_level_field,
                    submit_button,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def handle_compress(self, input_pdf: str, output_pdf: str, power: int):
        try:
            compress_pdf(input_pdf, output_pdf, power)
            self.show_snack("PDF compressed successfully!")
        except Exception as ex:
            self.show_snack(f"Error: {ex}")
