import flet as ft
import requests
import csv
import io

def main(page: ft.Page):
    page.title = "CFTC COT Analyzer"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 15

    status_text = ft.Text("Pronto per l'analisi", size=14, color="white70")
    progress_ring = ft.ProgressRing(visible=False, width=20, height=20)
    results_column = ft.Column(spacing=5)

    def run_analysis(e):
        status_text.value = "Scaricamento dati in corso..."
        progress_ring.visible = True
        results_column.controls.clear()
        page.update()

        try:
            url_current = "https://www.cftc.gov/dea/newcot/deafut.txt"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(url_current, headers=headers, timeout=15)
            response.raise_for_status()

            f = io.StringIO(response.text)
            reader = csv.reader(f)
            rows = list(reader)

            # Test rapido di visualizzazione prime righe
            count = 0
            for row in rows:
                if row and len(row) > 0:
                    results_column.controls.append(ft.Text(str(row[0]), size=11, font_family="monospace"))
                    count += 1
                    if count > 20:  # limitiamo per non intasare subito
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
    
    page.add(
        ft.Text("CFTC COT Analyzer", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        status_text,
        ft.Row([analyze_btn, progress_ring], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        results_column
    )

if __name__ == "__main__":
    ft.app(target=main)
