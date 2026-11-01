import flet as ft
import urllib.request
import csv
import io

# ==========================================
# DIZIONARIO MULTILINGUA
# ==========================================
TRANSLATIONS = {
    "Italiano": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Avvia Analisi",
        "btn_charts": "Apri Barchart COT",
        "status_ready": "Pronto per l'analisi",
        "status_download": "Scaricamento dei dati dal report Legacy CFTC...",
        "status_success": "Analisi completata con successo!",
        "error_prefix": "Errore durante l'esecuzione: ",
        "report_header": "REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE",
        "screening_header": "SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES",
        "cat_valute": "VALUTE",
        "cat_grains": "MATERIE PRIME - GRAINS",
        "cat_metalli": "METALLI",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIES",
        "cat_indici": "INDICI",
        "sig_valute": "--- INCROCI VALUTARI (Forza Relativa Universale) ---",
        "sec_commodities": "--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---",
        "sec_indices": "--- INDICI AZIONARI ---"
    },
    "English": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Start Analysis",
        "btn_charts": "Open Barchart COT",
        "status_ready": "Ready for analysis",
        "status_download": "Downloading data from CFTC Legacy report...",
        "status_success": "Analysis completed successfully!",
        "error_prefix": "Execution error: ",
        "report_header": "COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE",
        "screening_header": "STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES",
        "cat_valute": "CURRENCIES",
        "cat_grains": "COMMODITIES - GRAINS",
        "cat_metalli": "METALS",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIES",
        "cat_indici": "INDICES",
        "sig_valute": "--- CURRENCY CROSSES (Universal Relative Strength) ---",
        "sec_commodities": "--- COMMODITIES & CORRELATION ---",
        "sec_indices": "--- STOCK INDICES ---"
    },
    "Español": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Iniciar Análisis",
        "btn_charts": "Abrir Barchart COT",
        "status_ready": "Listo para el análisis",
        "status_download": "Descargando datos del informe Legacy CFTC...",
        "status_success": "¡Análisis completado con éxito!",
        "error_prefix": "Error durante la ejecución: ",
        "report_header": "INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE",
        "screening_header": "SELECCIÓN ESTRATÉGICA Y CRUCES DE DIVISAS / COMMODITIES",
        "cat_valute": "MONEDAS",
        "cat_grains": "MATERIAS PRIMAS - GRAINS",
        "cat_metalli": "METALES",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGÍAS",
        "cat_indici": "INDICES",
        "sig_valute": "--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---",
        "sec_commodities": "--- MATERIAS PRIMAS ---",
        "sec_indices": "--- ÍNDICES BURSÁTILES ---"
    },
    "Deutsch": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Analyse Starten",
        "btn_charts": "Barchart COT Öffnen",
        "status_ready": "Bereit für die Analyse",
        "status_download": "Daten aus dem CFTC Legacy Report werden heruntergeladen...",
        "status_success": "Analyse erfolgreich abgeschlossen!",
        "error_prefix": "Fehler bei der Ausführung: ",
        "report_header": "COT BERICHT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE",
        "screening_header": "STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN / COMMODITIES",
        "cat_valute": "WÄHRUNGEN",
        "cat_grains": "ROHSTOFFE - GRAINS",
        "cat_metalli": "METALLE",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIE",
        "cat_indici": "INDIZES",
        "sig_valute": "--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---",
        "sec_commodities": "--- ROHSTOFFE & KORRELATION ---",
        "sec_indices": "--- AKTIENINDIZES ---"
    },
    "Français": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Lancer l'analyse",
        "btn_charts": "Ouvrir Barchart COT",
        "status_ready": "Prêt pour l'analyse",
        "status_download": "Téléchargement des données du rapport Legacy CFTC...",
        "status_success": "Analyse terminée avec succès !",
        "error_prefix": "Erreur lors de l'exécution : ",
        "report_header": "RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE",
        "screening_header": "SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES / COMMODITIES",
        "cat_valute": "DEVISES",
        "cat_grains": "MATIÈRES PREMIÈRES - GRAINS",
        "cat_metalli": "MÉTAUX",
        "cat_softs": "SOFTS",
        "cat_energies": "ÉNERGIES",
        "cat_indici": "INDICES",
        "sig_valute": "--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---",
        "sec_commodities": "--- MATIÈRES PREMIÈRES & CORRÉLATION ---",
        "sec_indices": "--- INDICES BOURSIERS ---"
    }
}

# Mappatura link Barchart mirati alle pagine Commitment of Traders (COT)
BARCHART_LINKS = {
    "EURO FX": "https://www.barchart.com/futures/quotes/6E*0/commitment-of-traders",
    "BRITISH POUND": "https://www.barchart.com/futures/quotes/6B*0/commitment-of-traders",
    "JAPANESE YEN": "https://www.barchart.com/futures/quotes/6J*0/commitment-of-traders",
    "AUSTRALIAN DOLLAR": "https://www.barchart.com/futures/quotes/6A*0/commitment-of-traders",
    "NZ DOLLAR": "https://www.barchart.com/futures/quotes/6N*0/commitment-of-traders",
    "CANADIAN DOLLAR": "https://www.barchart.com/futures/quotes/6C*0/commitment-of-traders",
    "SWISS FRANC": "https://www.barchart.com/futures/quotes/6S*0/commitment-of-traders",
    "USD INDEX": "https://www.barchart.com/futures/quotes/DX*0/commitment-of-traders",
    "GOLD": "https://www.barchart.com/futures/quotes/GC*0/commitment-of-traders",
    "SILVER": "https://www.barchart.com/futures/quotes/SI*0/commitment-of-traders",
    "COPPER": "https://www.barchart.com/futures/quotes/HG*0/commitment-of-traders",
    "CRUDE OIL": "https://www.barchart.com/futures/quotes/CL*0/commitment-of-traders",
    "NATURAL GAS": "https://www.barchart.com/futures/quotes/NG*0/commitment-of-traders",
    "CORN": "https://www.barchart.com/futures/quotes/ZC*0/commitment-of-traders",
    "SOYBEANS": "https://www.barchart.com/futures/quotes/ZS*0/commitment-of-traders",
    "S&P 500": "https://www.barchart.com/futures/quotes/ES*0/commitment-of-traders",
    "NASDAQ-100": "https://www.barchart.com/futures/quotes/NQ*0/commitment-of-traders",
    "DOW JONES": "https://www.barchart.com/futures/quotes/YM*0/commitment-of-traders",
    "RUSSELL 2000": "https://www.barchart.com/futures/quotes/RTY*0/commitment-of-traders",
    "VIX": "https://www.barchart.com/futures/quotes/VX*0/commitment-of-traders"
}

def main(page: ft.Page):
    try:
        page.title = "CFTC COT Analyzer"
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20

        current_lang = "Italiano"
        t = TRANSLATIONS[current_lang]

        title_text = ft.Text(t["title"], size=22, weight=ft.FontWeight.BOLD, color="white")
        
        def change_language(e):
            nonlocal current_lang, t
            current_lang = lang_dropdown.value
            t = TRANSLATIONS[current_lang]
            title_text.value = t["title"]
            analyze_btn.text = t["btn_ready"]
            charts_btn.text = t["btn_charts"]
            status_text.value = t["status_ready"]
            page.update()

        lang_dropdown = ft.Dropdown(
            label="Language / Lingua",
            value="Italiano",
            options=[ft.dropdown.Option(lang) for lang in TRANSLATIONS.keys()],
            on_change=change_language,
            width=180,
            text_size=12,
            label_style=ft.TextStyle(size=12)
        )

        status_text = ft.Text(t["status_ready"], size=13, color="green")
        progress_ring = ft.ProgressRing(visible=False, width=20, height=20)
        
        results_column = ft.Column(spacing=2) # Spaziatura ridotta e uniforme per evitare spazi anomali
        results_container = ft.Container(
            content=results_column,
            padding=ft.padding.only(bottom=100)
        )

        horizontal_scroll_view = ft.Row(
            [results_container],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START
        )

        def open_charts(e):
            page.launch_url("https://www.barchart.com/futures/commitment-of-traders")

        def run_analysis(e):
            status_text.value = t["status_download"]
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
                    content = response.read().decode('utf-8', errors='ignore')

                f = io.StringIO(content)
                reader = csv.reader(f)
                rows = list(reader)
                
                categories = {
                    t["cat_valute"]: [
                        "SWISS FRANC", "USD INDEX", "MEXICAN PESO", 
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
                    all_results.append((category_name, "HEADER"))
                    
                    for kw in keywords:
                        for row in rows:
                            if not row or len(row) < 40:
                                continue
                            market_name = str(row[0]).strip()
                            
                            if kw.upper() in market_name.upper():
                                try:
                                    open_interest = float(row[7]) if row[7].strip() and float(row[7]) > 0 else 1
                                    non_comm_long = float(row[8]) if row[8].strip() else 0
                                    non_comm_short = float(row[9]) if row[9].strip() else 0
                                    
                                    change_long = int(float(row[38])) if row[38].strip() else 0
                                    change_short = int(float(row[39])) if row[39].strip() else 0
                                    
                                    pct_long = (non_comm_long / open_interest) * 100
                                    pct_short = (non_comm_short / open_interest) * 100
                                    
                                    prev_long = non_comm_long - change_long
                                    prev_short = non_comm_short - change_short
                                    
                                    pct_growth_long = (change_long / prev_long * 100) if prev_long > 0 else 0
                                    pct_growth_short = (change_short / prev_short * 100) if prev_short > 0 else 0
                                    
                                    score_long = pct_long + (pct_growth_long / 10.0)
                                    score_short = pct_short + (pct_growth_short / 10.0)
                                    net_slope = score_long - score_short
                                    
                                    if net_slope > 15:
                                        bias = "STRONG LONG"
                                    elif net_slope > 5:
                                        bias = "MODERATE LONG"
                                    elif net_slope < -15:
                                        bias = "STRONG SHORT"
                                    elif net_slope < -5:
                                        bias = "MODERATE SHORT"
                                    else:
                                        bias = "NEUTRAL"
                                    
                                    line = (
                                        f"{market_name[:32]:<34} | "
                                        f"Long: {pct_long:5.1f}% ({change_long:+6d} ctr) | "
                                        f"Short: {pct_short:5.1f}% ({change_short:+6d} ctr) | "
                                        f"Net Slope: {net_slope:+6.1f} [{bias}]"
                                    )
                                    all_results.append((line, "MARKET"))
                                    
                                    clean_key = kw.upper()
                                    market_data[clean_key] = {
                                        "name": market_name,
                                        "pct_long": pct_long,
                                        "pct_short": pct_short,
                                        "chg_long": change_long,
                                        "chg_short": change_short,
                                        "net_slope": net_slope
                                    }
                                    break
                                except Exception:
                                    pass

                signals = []
                currencies = {
                    "EURO FX": "EUR", "BRITISH POUND": "GBP", "JAPANESE YEN": "JPY",
                    "AUSTRALIAN DOLLAR": "AUD", "NZ DOLLAR": "NZD", "CANADIAN DOLLAR": "CAD",
                    "SWISS FRANC": "CHF", "USD INDEX": "USD"
                }
                
                cur_strength = {}
                for cur_key, cur_code in currencies.items():
                    if cur_key in market_data:
                        cur_strength[cur_code] = market_data[cur_key]["net_slope"]

                sorted_curs = sorted(cur_strength.items(), key=lambda x: x[1], reverse=True)
                
                signals.append((t["sig_valute"], "SUBHEADER"))
                if len(sorted_curs) >= 2:
                    signals.append((f"-> [TOP SETUP ABS] {sorted_curs[0][0]}/{sorted_curs[-1][0]} | Max div ({sorted_curs[0][0]}: {sorted_curs[0][1]:+.1f} vs {sorted_curs[-1][0]}: {sorted_curs[-1][1]:+.1f})", "TEXT"))

                major_pairs = [
                    ("EUR", "USD"), ("GBP", "USD"), ("AUD", "USD"), ("NZD", "USD"),
                    ("USD", "JPY"), ("USD", "CAD"), ("USD", "CHF"),
                    ("EUR", "GBP"), ("EUR", "JPY"), ("GBP", "JPY"), ("AUD", "JPY")
                ]
                
                signals.append(("--- ANALISI DINAMICA CROSS PRINCIPALI ---", "SUBHEADER"))
                for base, quote in major_pairs:
                    if base in cur_strength and quote in cur_strength:
                        s_base, s_quote = cur_strength[base], cur_strength[quote]
                        diff = s_base - s_quote
                        if diff > 10:
                            signals.append((f"-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})", "TEXT"))
                        elif diff < -10:
                            signals.append((f"-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})", "TEXT"))

                signals.append((t["sec_commodities"], "SUBHEADER"))
                commodities_to_check = ["GOLD", "SILVER", "CRUDE OIL", "COPPER", "LUMBER", "CORN", "SOYBEANS"]
                usd_slope = cur_strength.get("USD", 0)
                
                for comm in commodities_to_check:
                    comm_data = market_data.get(comm)
                    if comm_data:
                        c_name = comm_data['name'].split('-')[0].strip()
                        slope = comm_data["net_slope"]
                        
                        if comm_data["pct_short"] > 60 and comm_data["chg_short"] < 0:
                            signals.append((f"-> [COMMODITY / SQUEEZE] {c_name}: Short in chiusura (Slope: {slope:+.1f}).", "TEXT"))
                        elif slope > 15 and usd_slope < 0:
                            signals.append((f"-> [COMMODITY / BULLISH] {c_name}: Forte long con USD debole (Slope: {slope:+.1f}).", "TEXT"))
                        elif slope < -15 and usd_slope > 0:
                            signals.append((f"-> [COMMODITY / BEARISH] {c_name}: Forte short con USD forte (Slope: {slope:+.1f}).", "TEXT"))

                # Inserimento ordinato nella UI senza salti anomali
                results_column.controls.append(ft.Text(t["report_header"], weight=ft.FontWeight.BOLD, color="yellow", size=11))
                results_column.controls.append(ft.Text("=" * 70, color="white24", size=10))

                for item, itype in all_results:
                    if itype == "HEADER":
                        results_column.controls.append(ft.Text(f"\n--- {item} ---", weight=ft.FontWeight.BOLD, color="cyan", size=12))
                    else:
                        market_key = None
                        for key in BARCHART_LINKS.keys():
                            if key in item.upper():
                                market_key = key
                                break
                        
                        if market_key:
                            url_chart = BARCHART_LINKS[market_key]
                            results_column.controls.append(
                                ft.TextButton(
                                    content=ft.Text(item, font_family="monospace", size=11, color="white"),
                                    on_click=lambda e, u=url_chart: page.launch_url(u),
                                    style=ft.ButtonStyle(padding=0)
                                )
                            )
                        else:
                            results_column.controls.append(ft.Text(item, font_family="monospace", size=11, color="white"))

                results_column.controls.append(ft.Text("\n" + "=" * 70, color="white24", size=10))
                results_column.controls.append(ft.Text(t["screening_header"], weight=ft.FontWeight.BOLD, color="yellow", size=11))
                results_column.controls.append(ft.Text("=" * 70, color="white24", size=10))

                for sig, stype in signals:
                    if stype == "SUBHEADER":
                        results_column.controls.append(ft.Text(f"\n{sig}", weight=ft.FontWeight.BOLD, color="amber", size=12))
                    else:
                        results_column.controls.append(ft.Text(sig, size=11, color="white70"))

                status_text.value = t["status_success"]
            except Exception as ex:
                status_text.value = f"{t['error_prefix']}{ex}"
            
            progress_ring.visible = False
            page.update()

        analyze_btn = ft.ElevatedButton(
            t["btn_ready"], 
            on_click=run_analysis, 
            bgcolor="blue",
            color="white"
        )

        charts_btn = ft.ElevatedButton(
            t["btn_charts"],
            on_click=open_charts,
            bgcolor="green",
            color="white"
        )

        page.add(
            title_text,
            lang_dropdown,
            ft.Divider(height=15, color="white24"),
            status_text,
            ft.Container(height=5),
            ft.Row([analyze_btn, charts_btn, progress_ring], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Divider(height=15, color="white24"),
            horizontal_scroll_view
        )

    except Exception as initialization_error:
        page.clean()
        page.add(
            ft.Text("ERRORE CRITICO DI AVVIO:", size=18, color="red", weight=ft.FontWeight.BOLD),
            ft.Text(str(initialization_error), size=14, color="white")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)

if __name__ == "__main__":
    ft.app(target=main)
