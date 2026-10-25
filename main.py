import flet as ft

def main(page: ft.Page):
    page.title = "Test Minimale"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # Aggiungiamo subito un elemento visivo elementare
    page.add(
        ft.Column(
            [
                ft.Text("FUNZIONA!", size=30, color="green", weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Cliccami", on_click=lambda e: print("Cliccato!"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
