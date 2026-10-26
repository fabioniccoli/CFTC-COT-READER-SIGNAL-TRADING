import flet as ft
import urllib.request
import csv
import io

def main(page: ft.Page):
    try:
        page.title = "CFTC COT Analyzer"
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20

        # Usiamo stringhe semplici per i colori per evitare qualsiasi errore di versione di Flet
        title_text = ft.Text("CFTC COT Analyzer", size=24, weight=ft.FontWeight.BOLD, color="white")
        status_text = ft.Text("Stato: Pronto", size=14, color="green")
        progress_ring = ft.ProgressRing(visible=False, width=24, height=24)
        
        results_column = ft.Column(spacing=8)

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
                        results_column.controls.append(
                            ft.Text(str(row[0]), size=12, font_family="monospace", color="white70")
                        )
                        count += 1
                        if count > 25:
                            break

                status_text.value = "Analisi completata con successo!"
            except Exception as ex:
                status_text.value = f"Errore rete/parsing: {ex}"
            
            progress_ring.visible = False
            page.update()

        analyze_btn = ft.ElevatedButton(
            "Avvia Analisi", 
            on_click=run_analysis, 
            bgcolor="blue",
            color="white"
        )

        # Aggiungiamo tutto alla pagina
        page.add(
            title_text,
            ft.Divider(height=20, color="white24"),
            status_text,
            ft.Container(height=10),
            ft.Row([analyze_btn, progress_ring], alignment=ft.MainAxisAlignment.START, spacing=15),
            ft.Divider(height=20, color="white24"),
            results_column
        )

    except Exception as initialization_error:
        # Se qualcosa fallisce all'avvio, lo stampiamo a schermo in rosso vivo!
        page.clean()
        page.add(
            ft.Text("ERRORE CRITICO DI AVVIO:", size=18, color="red", weight=ft.FontWeight.BOLD),
            ft.Text(str(initialization_error), size=14, color="white")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
