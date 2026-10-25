import flet as ft
import requests
import csv
import io

TRANSLATIONS = {
    "it": {
        "title": "CFTC COT Analyzer",
        "ready": "Pronto per l'analisi",
        "downloading": "Scaricamento dati in corso...",
        "success": "Analisi completata con successo!",
        "error": "Errore",
        "btn_text": "Avvia Analisi",
        "cat_valute": "Valute",
        "cat_grains": "Grains",
        "cat_metalli": "Metalli",
        "cat_softs": "Softs",
        "cat_energies": "Energia",
        "cat_indici": "Indici",
        "currency_section": "--- Analisi Valute ---",
        "top_setup": "Top Setup: {cur1} vs {cur2}",
        "strat_signals": "Segnali Strategici:"
    }
}

def main(page: ft.Page):
    # Usiamo direttamente l'italiano per evitare crash legati al rilevamento della lingua su Android
    t = TRANSLATIONS["it"]

    page.title = t["title"]
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO  # Scroll nativo della pagina per massima stabilità su mobile
    page.padding = 15

    status_text = ft.Text(t["ready"], size=14, color=ft.colors.WHITE70)
    progress_ring = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)
    
    # Colonna che conterrà i risultati dell'analisi
    results_column = ft.Column(spacing=5)

    def run_analysis(e):
        status_text.value = t["downloading"]
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

            categories = {
                t["cat_valute"]: [
                    "SWISS FRANC", "U.S. DOLLAR INDEX", "MEXICAN PESO", 
                    "NZ DOLLAR", "CANADIAN DOLLAR", "BRAZILIAN REAL", "SOUTH AFRICAN RAND",
                    "BRITISH POUND", "JAPANESE YEN", "EURO FX", "AUSTRALIAN DOLLAR"
                ],
                t["cat_grains"]: [
                    "CORN", "SOYBEANS", "SOYBEAN OIL", "SOYBEAN MEAL", 
                    "WHEAT-SRW", "WHEAT-HRW", "WHEAT-SPRING", "ROUGH RICE", "CANOLA"
                ],
                t["cat_metalli"]: [
                    "GOLD", "SILVER", "COPPER", "PALLADIUM", "PLATINUM", "ALUMINUM"
                ],
                t["cat_softs"]: [
                    "COCOA", "COTTON", "COFFEE", "SUGAR", "ORANGE JUICE", "LUMBER"
                ],
                t["cat_energies"]: [
                    "CRUDE OIL", "GASOLINE", "HEATING OIL", "ULSD", "NATURAL GAS"
                ],
                t["cat_indici"]: [
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
                                open_interest = float(row[7]) if row[7].strip() and float(row[7]) > 0 else 1
                                non_comm_long = float(row[8]) if row[8].strip() else 0
                                non_comm_short = float(row[9]) if row[9].strip() else 0
                                
                                change_long = float(row[11]) if row[11].strip() else 0
                                change_short = float(row[12]) if row[12].strip() else 0
                                
                                pct_long = (non_comm_long / open_interest) * 100
                                pct_short = (non_comm_short / open_interest) * 100
                                
                                line = (
                                    f"{market_name[:25]:<27} | "
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
            signals.append(t["currency_section"])
            if len(sorted_curs) >= 2:
                signals.append(t["top_setup"].format(cur1=sorted_curs[0][0], cur2=sorted_curs[-1][0]))

            for item in all_results:
                results_column.controls.append(ft.Text(item, font_family="monospace", size=11))
            
            results_column.controls.append(ft.Text(f"\n{t['strat_signals']}", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE))
            for sig in signals:
                results_column.controls.append(ft.Text(sig, size=12, color=ft.colors.AMBER_ACCENT))

            status_text.value = t["success"]
        except Exception as ex:
            status_text.value = f"{t['error']}: {ex}"
        
        progress_ring.visible = False
        page.update()

    analyze_btn = ft.ElevatedButton(
        t["btn_text"], 
        on_click=run_analysis, 
        icon=ft.icons.PLAY_ARROW,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE
    )
    
    # Costruiamo la UI principale stabile
    page.add(
        ft.Text(t["title"], size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        status_text,
        ft.Row([analyze_btn, progress_ring], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        results_column
    )

if __name__ == "__main__":
    ft.app(target=main)
