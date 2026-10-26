import flet as ft
import urllib.request
import csv
import io

def main(page: ft.Page):
    page.title = "CFTC COT Analyzer"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    status_text = ft.Text("Pronto per l'analisi", size=14, color="green")
    progress_ring = ft.ProgressRing(visible=False, width=20, height=20)
    
    # Usiamo una ListView o una Column interna scrollabile per i risultati
    results_column = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)

    def run_analysis(e):
        status_text.value = "Scaricamento dati in corso..."
        progress_ring.visible = True
        results_column.controls.clear()
        page.update()

        try:
            url_current = "https://www.cftc.gov/dea/newcot/deafut.txt"
            req = urllib.request.Request(
                url_current, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                html_content = response.read().decode('utf-8', errors='ignore')

            f = io.StringIO(html_content)
            reader = csv.reader(f)
            rows = list(reader)

            count = 0
            for row in rows:
                if row and len(row) > 0:
                    results_column.controls.append(ft.Text(str(row[0]), size=11, font_family="monospace", color="white"))
                    count += 1
                    if count > 30:
                        break

            status_text.value = "Analisi completata con successo!"
        except Exception as ex:
            status_text.value = f"Errore: {ex}"
        
        progress_ring.visible = False
        page.update()

    analyze_btn = ft.ElevatedButton(
        "Avvia Analisi", 
        on_click=run_analysis, 
        icon=ft.icons.PLAY_ARROW
    )
    
    # STRUTTURA DEL TEST MINIMALE: Colonna principale con expand=True
    page.add(
        ft.Column(
            [
                ft.Text("CFTC COT Analyzer", size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(),
                status_text,
                ft.Row([analyze_btn, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                results_column
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
