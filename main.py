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

        title_text = ft.Text("CFTC COT Analyzer", size=24, weight=ft.FontWeight.BOLD, color="white")
        status_text = ft.Text("Stato: Pronto per l'analisi", size=14, color="green")
        progress_ring = ft.ProgressRing(visible=False, width=24, height=24)
        
        results_column = ft.Column(spacing=6)

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

                # Categorie e parole chiave ufficiali dello script originale
                categories = {
                    "Valute": [
                        "SWISS FRANC", "U.S. DOLLAR INDEX", "MEXICAN PESO", 
                        "NZ DOLLAR", "CANADIAN DOLLAR", "BRAZILIAN REAL", "SOUTH AFRICAN RAND",
                        "BRITISH POUND", "JAPANESE YEN", "EURO FX", "AUSTRALIAN DOLLAR"
                    ],
                    "Grains": [
                        "CORN", "SOYBEANS", "SOYBEAN OIL", "SOYBEAN MEAL", 
                        "WHEAT-SRW", "WHEAT-HRW", "WHEAT-SPRING", "ROUGH RICE", "CANOLA"
                    ],
                    "Metalli": [
                        "GOLD", "SILVER", "COPPER", "PALLADIUM", "PLATINUM", "ALUMINUM"
                    ],
                    "Softs": [
                        "COCOA", "COTTON", "COFFEE", "SUGAR", "ORANGE JUICE", "LUMBER"
                    ],
                    "Energia": [
                        "CRUDE OIL", "GASOLINE", "HEATING OIL", "ULSD", "NATURAL GAS"
                    ],
                    "Indici": [
                        "S&P 500", "NASDAQ-100", "DOW JONES", "RUSSELL 2000", "VIX"
                    ]
                }

                all_results = []
                market_data = {}

                for category_name, keywords in categories.items():
                    all_results.append(f"\n--- {category_name} ---")
                    
                    for kw in keywords:
                        for row in rows:
                            if not row or len(row) < 15:
                                continue
                            market_name = str(row[0]).strip()
                            
                            if kw.upper() in market_name.upper():
                                try:
                                    # Lettura colonne esatte report CFTC Legacy
                                    open_interest = float(row[7]) if row[7].strip() and float(row[7]) > 0 else 1
                                    non_comm_long = float(row[8]) if row[8].strip() else 0
                                    non_comm_short = float(row[9]) if row[9].strip() else 0
                                    
                                    change_long = float(row[11]) if row[11].strip() else 0
                                    change_short = float(row[12]) if row[12].strip() else 0
                                    
                                    pct_long = (non_comm_long / open_interest) * 100
                                    pct_short = (non_comm_short / open_interest) * 100
                                    
                                    line = (
                                        f"{market_name[:22]:<22} | "
                                        f"L:{pct_long:4.1f}% | S:{pct_short:4.1f}%"
                                    )
                                    all_results.append(line)
                                    
                                    clean_key = kw.upper()
                                    market_data[clean_key] = {
                                        "name": market_name,
                                        "pct_long": pct_long,
                                        "pct_short": pct_short,
                                        "strength_score": (pct_long - pct_short) + ((change_long - change_short) / open_interest * 100)
                                    }
                                    break
                                except Exception:
                                    pass

                # Analisi e segnali strategici sulle valute
                signals = []
                currencies = {
                    "EURO FX": "EUR", "BRITISH POUND": "GBP", "JAPANESE YEN": "JPY",
                    "AUSTRALIAN DOLLAR": "AUD", "NZ DOLLAR": "NZD", "CANADIAN DOLLAR": "CAD",
                    "SWISS FRANC": "CHF", "U.S. DOLLAR INDEX": "USD"
                }
                
                cur_strength = {}
                for cur_key, cur_code in currencies.items():
                    if cur_key in market_data:
                        cur_strength[cur_code] = market_data[cur_key]["strength_score"]

                sorted_curs = sorted(cur_strength.items(), key=lambda x: x[1], reverse=True)
                signals.append("\n--- Segnali Strategici Valute ---")
                if len(sorted_curs) >= 2:
                    signals.append(f"Top Setup: {sorted_curs[0][0]} (Forza) vs {sorted_curs[-1][0]} (Debolezza)")

                # Inserimento dei risultati formattati nella UI
                for item in all_results:
                    if item.startswith("\n---"):
                        results_column.controls.append(ft.Text(item, weight=ft.FontWeight.BOLD, color="yellow"))
                    else:
                        results_column.controls.append(ft.Text(item, font_family="monospace", size=11, color="white"))
                
                for sig in signals:
                    results_column.controls.append(ft.Text(sig, size=12, color="amber"))

                status_text.value = "Analisi completata con successo!"
            except Exception as ex:
                status_text.value = f"Errore elaborazione: {ex}"
            
            progress_ring.visible = False
            page.update()

        analyze_btn = ft.ElevatedButton(
            "Avvia Analisi", 
            on_click=run_analysis, 
            bgcolor="blue",
            color="white"
        )

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
        page.clean()
        page.add(
            ft.Text("ERRORE CRITICO:", size=18, color="red"),
            ft.Text(str(initialization_error), size=14, color="white")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
