import flet as ft
import pandas as pd
import requests
import io

# ==========================================
# DIZIONARIO MULTILINGUA
# ==========================================
TRANSLATIONS = {
    "Italiano": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Avvia Analisi",
        "status_ready": "Pronto per l'analisi",
        "status_download": "Scaricamento dei dati dal report Legacy CFTC...",
        "status_success": "Analisi completata con successo!",
        "error_prefix": "Errore durante l'esecuzione: ",
        "report_header": "REPORT COT (LEGACY) - MATRICE DI INCROCIO UNIVERSALE",
        "screening_header": "SCREENING STRATEGICO & INCROCI MULTI-VALUTA",
        "cat_valute": "VALUTE",
        "cat_grains": "MATERIE PRIME - GRAINS",
        "cat_metalli": "METALLI",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIES",
        "cat_indici": "INDICI",
        "sig_valute": "--- INCROCI VALUTARI (Forza Relativa Universale) ---",
        "top_setup": "-> [VALUTA TOP SETUP] Valutare LONG su {strong}/{weak}: Massima divergenza di forza istituzionale.",
        "long_aud_usd": "-> [VALUTA CROSS] Setup favorevole per LONG su AUD/USD.",
        "short_aud_usd": "-> [VALUTA CROSS] Setup favorevole per SHORT su AUD/USD.",
        "long_eur_gbp": "-> [VALUTA CROSS] Monitorare LONG su EUR/GBP.",
        "short_eur_gbp": "-> [VALUTA CROSS] Monitorare SHORT su EUR/GBP.",
        "sec_commodities": "\n--- MATERIE PRIME & COMMODITIES ---",
        "squeeze": "-> [MATERIA PRIMA / POSSIBILE SQUEEZE] {name}: Short in chiusura ({val:+d} contratti).",
        "momentum": "-> [MATERIA PRIMA / MOMENTUM RIALZISTA] {name}: Spinta dei fondi ({val:+d} contratti).",
        "sec_indices": "\n--- INDICI AZIONARI ---",
        "ind_continuation": "-> [INDICE / CONTINUAZIONE] {name}: Accumulo rialzista ({val:+d} contratti).",
        "ind_correction": "-> [INDICE / ALLERTA CORREZIONE] {name}: Crescita posizioni ribassiste ({val:+d} contratti)."
    },
    "English": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Start Analysis",
        "status_ready": "Ready for analysis",
        "status_download": "Downloading data from CFTC Legacy report...",
        "status_success": "Analysis completed successfully!",
        "error_prefix": "Execution error: ",
        "report_header": "COT REPORT (LEGACY) - UNIVERSAL CROSS MATRIX",
        "screening_header": "STRATEGIC SCREENING & MULTI-CURRENCY CROSSES",
        "cat_valute": "CURRENCIES",
        "cat_grains": "COMMODITIES - GRAINS",
        "cat_metalli": "METALS",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIES",
        "cat_indici": "INDICES",
        "sig_valute": "--- CURRENCY CROSSES (Universal Relative Strength) ---",
        "top_setup": "-> [CURRENCY TOP SETUP] Consider LONG on {strong}/{weak}: Maximum institutional strength divergence.",
        "long_aud_usd": "-> [CURRENCY CROSS] Favorable setup for LONG on AUD/USD.",
        "short_aud_usd": "-> [CURRENCY CROSS] Favorable setup for SHORT on AUD/USD.",
        "long_eur_gbp": "-> [CURRENCY CROSS] Monitor LONG on EUR/GBP.",
        "short_eur_gbp": "-> [CURRENCY CROSS] Monitor SHORT on EUR/GBP.",
        "sec_commodities": "\n--- COMMODITIES ---",
        "squeeze": "-> [COMMODITY / POTENTIAL SQUEEZE] {name}: Short covering ({val:+d} contracts).",
        "momentum": "-> [COMMODITY / BULLISH MOMENTUM] {name}: Funds buying pressure ({val:+d} contracts).",
        "sec_indices": "\n--- STOCK INDICES ---",
        "ind_continuation": "-> [INDEX / CONTINUATION] {name}: Bullish accumulation ({val:+d} contracts).",
        "ind_correction": "-> [INDEX / CORRECTION ALERT] {name}: Bearish positions growth ({val:+d} contracts)."
    },
    "Español": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Iniciar Análisis",
        "status_ready": "Listo para el análisis",
        "status_download": "Descargando datos del informe Legacy CFTC...",
        "status_success": "¡Análisis completado con éxito!",
        "error_prefix": "Error durante la ejecución: ",
        "report_header": "INFORME COT (LEGACY) - MATRIZ DE CRUCE UNIVERSAL",
        "screening_header": "SELECCIÓN ESTRÁTEGICA Y CRUCES DE DIVISAS",
        "cat_valute": "MONEDAS",
        "cat_grains": "MATERIAS PRIMAS - GRAINS",
        "cat_metalli": "METALES",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGÍAS",
        "cat_indici": "INDICES",
        "sig_valute": "--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---",
        "top_setup": "-> [DIVISA TOP SETUP] Evaluar LONG en {strong}/{weak}: Máxima divergencia de fuerza institucional.",
        "long_aud_usd": "-> [DIVISA CROSS] Configuración favorable para LONG en AUD/USD.",
        "short_aud_usd": "-> [DIVISA CROSS] Configuración favorable para SHORT en AUD/USD.",
        "long_eur_gbp": "-> [DIVISA CROSS] Monitorear LONG en EUR/GBP.",
        "short_eur_gbp": "-> [DIVISA CROSS] Monitorear SHORT en EUR/GBP.",
        "sec_commodities": "\n--- MATERIAS PRIMAS ---",
        "squeeze": "-> [MATERIA PRIMA / POSIBLE SQUEEZE] {name}: Cierre de cortos ({val:+d} contratos).",
        "momentum": "-> [MATERIA PRIMA / MOMENTUM ALCISTA] {name}: Presión compradora de fondos ({val:+d} contratos).",
        "sec_indices": "\n--- ÍNDICES BURSÁTILES ---",
        "ind_continuation": "-> [ÍNDICE / CONTINUACIÓN] {name}: Acumulación alcista ({val:+d} contratos).",
        "ind_correction": "-> [ÍNDICE / ALERTA CORRECCIÓN] {name}: Crecimiento de posiciones bajistas ({val:+d} contratos)."
    },
    "Deutsch": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Analyse Starten",
        "status_ready": "Bereit für die Analyse",
        "status_download": "Daten aus dem CFTC Legacy Report werden heruntergeladen...",
        "status_success": "Analyse erfolgreich abgeschlossen!",
        "error_prefix": "Fehler bei der Ausführung: ",
        "report_header": "COT BERICHT (LEGACY) - UNIVERSELLE KREUZMATRIX",
        "screening_header": "STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN",
        "cat_valute": "WÄHRUNGEN",
        "cat_grains": "ROHSTOFFE - GRAINS",
        "cat_metalli": "METALLE",
        "cat_softs": "SOFTS",
        "cat_energies": "ENERGIE",
        "cat_indici": "INDIZES",
        "sig_valute": "--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---",
        "top_setup": "-> [WÄHRUNG TOP SETUP] LONG bei {strong}/{weak} prüfen: Maximale institutionelle Stärkedivergenz.",
        "long_aud_usd": "-> [WÄHRUNG CROSS] Günstiges Setup für LONG bei AUD/USD.",
        "short_aud_usd": "-> [WÄHRUNG CROSS] Günstiges Setup für SHORT bei AUD/USD.",
        "long_eur_gbp": "-> [WÄHRUNG CROSS] LONG bei EUR/GBP beobachten.",
        "short_eur_gbp": "-> [WÄHRUNG CROSS] SHORT bei EUR/GBP beobachten.",
        "sec_commodities": "\n--- ROHSTOFFE & COMMODITIES ---",
        "squeeze": "-> [ROHSTOFF / MÖGLicher SQUEEZE] {name}: Short-Eindeckung ({val:+d} Kontrakte).",
        "momentum": "-> [ROHSTOFF / BULLISCHES MOMENTUM] {name}: Fonds-Kaufdruck ({val:+d} Kontrakte).",
        "sec_indices": "\n--- AKTIENINDIZES ---",
        "ind_continuation": "-> [INDEX / FORTSETZUNG] {name}: Bullische Akkumulation ({val:+d} Kontrakte).",
        "ind_correction": "-> [INDEX / KORREKTURWARNUNG] {name}: Zunahme bärenstapfiger Positionen ({val:+d} Kontrakte)."
    },
    "Français": {
        "title": "CFTC COT Analyzer",
        "btn_ready": "Lancer l'analyse",
        "status_ready": "Prêt pour l'analyse",
        "status_download": "Téléchargement des données du rapport Legacy CFTC...",
        "status_success": "Analyse terminée avec succès !",
        "error_prefix": "Erreur lors de l'exécution : ",
        "report_header": "RAPPORT COT (LEGACY) - MATRICE DE CROISEMENT UNIVERSEL",
        "screening_header": "SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES",
        "cat_valute": "DEVISES",
        "cat_grains": "MATIÈRES PREMIÈRES - GRAINS",
        "cat_metalli": "MÉTAUX",
        "cat_softs": "SOFTS",
        "cat_energies": "ÉNERGIES",
        "cat_indici": "INDICES",
        "sig_valute": "--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---",
        "top_setup": "-> [DEVISE TOP SETUP] Envisager LONG sur {strong}/{weak} : Divergence maximale de force institutionnelle.",
        "long_aud_usd": "-> [DEVISE CROSS] Configuration favorable pour LONG sur AUD/USD.",
        "short_aud_usd": "-> [DEVISE CROSS] Configuration favorable pour SHORT sur AUD/USD.",
        "long_eur_gbp": "-> [DEVISE CROSS] Surveiller LONG sur EUR/GBP.",
        "short_eur_gbp": "-> [DEVISE CROSS] Surveiller SHORT sur EUR/GBP.",
        "sec_commodities": "\n--- MATIÈRES PREMIÈRES ---",
        "squeeze": "-> [MATIÈRE PREMIÈRE / SQUEEZE POTENTIEL] {name} : Couverture de shorts ({val:+d} contrats).",
        "momentum": "-> [MATIÈRE PREMIÈRE / MOMENTUM HAUSSIER] {name} : Pression acheteuse des fonds ({val:+d} contrats).",
        "sec_indices": "\n--- INDICES BOURSIERS ---",
        "ind_continuation": "-> [INDICE / CONTINUATION] {name} : Accumulation haussière ({val:+d} contrats).",
        "ind_correction": "-> [INDICE / ALERTE CORRECTION] {name} : Croissance des positions baissières ({val:+d} contrats)."
    }
}

def main(page: ft.Page):
    try:
        page.title = "CFTC COT Analyzer"
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20

        # Stato della lingua corrente
        current_lang = "Italiano"
        t = TRANSLATIONS[current_lang]

        # Elementi UI di base
        title_text = ft.Text(t["title"], size=22, weight=ft.FontWeight.BOLD, color="white")
        
        # Selettore Lingua
        def change_language(e):
            nonlocal current_lang, t
            current_lang = lang_dropdown.value
            t = TRANSLATIONS[current_lang]
            title_text.value = t["title"]
            analyze_btn.text = t["btn_ready"]
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
        
        # Contenitore dei risultati con scroll verticale e un ampio padding inferiore (per evitare i tasti di Android)
        results_column = ft.Column(spacing=4)
        results_container = ft.Container(
            content=results_column,
            padding=ft.padding.only(bottom=80) # Spazio extra per i tasti virtuali dello smartphone
        )

        # Contenitore a scorrimento orizzontale per impedire il taglio della formattazione a spaziatura fissa
        horizontal_scroll_view = ft.Row(
            [results_container],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START
        )

        def run_analysis(e):
            status_text.value = t["status_download"]
            progress_ring.visible = True
            results_column.controls.clear()
            page.update()

            try:
                url_current = "https://www.cftc.gov/dea/newcot/deafut.txt"
                headers = {'User-Agent': 'Mozilla/5.0'}
                
                response = requests.get(url_current, headers=headers, timeout=15)
                response.raise_for_status()
                
                df = pd.read_csv(io.StringIO(response.text), header=None, low_memory=False)
                
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
                    all_results.append(f"\n--- {category_name} ---")
                    
                    for kw in keywords:
                        found = False
                        for index, row in df.iterrows():
                            market_name = str(row[0]).strip()
                            
                            if kw.upper() in market_name.upper():
                                try:
                                    open_interest = float(row[7]) if pd.notna(row[7]) and float(row[7]) > 0 else 1
                                    non_comm_long = float(row[8]) if pd.notna(row[8]) else 0
                                    non_comm_short = float(row[9]) if pd.notna(row[9]) else 0
                                    
                                    change_long = int(float(row[38])) if pd.notna(row[38]) else 0
                                    change_short = int(float(row[39])) if pd.notna(row[39]) else 0
                                    
                                    pct_long = (non_comm_long / open_interest) * 100
                                    pct_short = (non_comm_short / open_interest) * 100
                                    
                                    prev_long = non_comm_long - change_long
                                    prev_short = non_comm_short - change_short
                                    
                                    pct_growth_long = (change_long / prev_long * 100) if prev_long > 0 else 0
                                    pct_growth_short = (change_short / prev_short * 100) if prev_short > 0 else 0
                                    
                                    strength_score = (pct_long - pct_short) + (pct_growth_long - pct_growth_short) / 10.0
                                    
                                    line = (
                                        f"{market_name[:32]:<34} | "
                                        f"Long: {pct_long:5.1f}% ({change_long:+d} ctr) | "
                                        f"Short: {pct_short:5.1f}% ({change_short:+d} ctr)"
                                    )
                                    all_results.append(line)
                                    
                                    clean_key = kw.upper()
                                    market_data[clean_key] = {
                                        "name": market_name,
                                        "pct_long": pct_long,
                                        "pct_short": pct_short,
                                        "chg_long": change_long,
                                        "chg_short": change_short,
                                        "strength_score": strength_score
                                    }
                                    
                                    found = True
                                    break
                                except Exception:
                                    pass

                # Motore di incrocio universale
                signals = []
                currencies = {
                    "EURO FX": "EUR", "BRITISH POUND": "GBP", "JAPANESE YEN": "JPY",
                    "AUSTRALIAN DOLLAR": "AUD", "NZ DOLLAR": "NZD", "CANADIAN DOLLAR": "CAD",
                    "SWISS FRANC": "CHF", "U.S. DOLLAR INDEX": "USD"
                }
                
                cur_strength = {}
                for cur_key, cur_code in currencies.items():
                    if cur_key in market_data:
                        data = market_data[cur_key]
                        cur_strength[cur_code] = data["strength_score"]

                sorted_curs = sorted(cur_strength.items(), key=lambda x: x[1], reverse=True)
                
                signals.append(t["sig_valute"])
                if len(sorted_curs) >= 2:
                    strongest_cur = sorted_curs[0]
                    weakest_cur = sorted_curs[-1]
                    signals.append(t["top_setup"].format(strong=strongest_cur[0], weak=weakest_cur[0]))

                if "AUD" in cur_strength and "USD" in cur_strength:
                    if cur_strength["AUD"] > cur_strength["USD"]:
                        signals.append(t["long_aud_usd"])
                    else:
                        signals.append(t["short_aud_usd"])
                        
                if "EUR" in cur_strength and "GBP" in cur_strength:
                    if cur_strength["EUR"] > cur_strength["GBP"]:
                        signals.append(t["long_eur_gbp"])
                    else:
                        signals.append(t["short_eur_gbp"])

                signals.append(t["sec_commodities"])
                commodities_to_check = ["GOLD", "SILVER", "CRUDE OIL", "COPPER", "LUMBER", "CORN", "SOYBEANS"]
                for comm in commodities_to_check:
                    comm_data = market_data.get(comm)
                    if comm_data:
                        c_name = comm_data['name'].split('-')[0].strip()
                        if comm_data["pct_short"] > 60 and comm_data["chg_short"] < 0:
                            signals.append(t["squeeze"].format(name=c_name, val=comm_data['chg_short']))
                        elif comm_data["pct_long"] > 60 and comm_data["chg_long"] > 0:
                            signals.append(t["momentum"].format(name=c_name, val=comm_data['chg_long']))

                signals.append(t["sec_indices"])
                indices_to_check = ["S&P 500", "NASDAQ-100", "DOW JONES", "RUSSELL 2000"]
                for ind in indices_to_check:
                    ind_data = market_data.get(ind)
                    if ind_data:
                        i_name = ind_data['name'].split('-')[0].strip()
                        if ind_data["pct_long"] > 60 and ind_data["chg_long"] > 0:
                            signals.append(t["ind_continuation"].format(name=i_name, val=ind_data['chg_long']))
                        elif ind_data["pct_short"] > 50 and ind_data["chg_short"] > 0:
                            signals.append(t["ind_correction"].format(name=i_name, val=ind_data['chg_short']))

                # Popolamento UI
                results_column.controls.append(ft.Text(t["report_header"], weight=ft.FontWeight.BOLD, color="yellow", size=11))
                results_column.controls.append(ft.Text("=" * 60, color="white24", size=10))

                for item in all_results:
                    if item.startswith("\n---"):
                        results_column.controls.append(ft.Text(item, weight=ft.FontWeight.BOLD, color="cyan", size=12))
                    else:
                        results_column.controls.append(ft.Text(item, font_family="monospace", size=11, color="white"))

                results_column.controls.append(ft.Text("\n" + "=" * 60, color="white24", size=10))
                results_column.controls.append(ft.Text(t["screening_header"], weight=ft.FontWeight.BOLD, color="yellow", size=11))
                results_column.controls.append(ft.Text("=" * 60, color="white24", size=10))

                for sig in signals:
                    if sig.startswith("\n---") or sig.startswith("---"):
                        results_column.controls.append(ft.Text(sig, weight=ft.FontWeight.BOLD, color="amber", size=12))
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

        # Layout Principale
        page.add(
            title_text,
            lang_dropdown,
            ft.Divider(height=15, color="white24"),
            status_text,
            ft.Container(height=5),
            ft.Row([analyze_btn, progress_ring], alignment=ft.MainAxisAlignment.START, spacing=15),
            ft.Divider(height=15, color="white24"),
            horizontal_scroll_view  # Supporta lo scroll orizzontale e verticale integrato
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
