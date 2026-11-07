import datetime
import os
import flet as ft

def main(page: ft.Page):
    # --- SISTEMA DI DEMO 60 GIORNI & RACCOLTA LEAD ---
    license_file = "license.key"
    trial_days = 60
    today = datetime.date.today()

    if not os.path.exists(license_file):
        # Prima esecuzione: crea la data di attivazione della demo
        with open(license_file, "w") as f:
            f.write(today.isoformat())
        activation_date = today
    else:
        # Legge la data di attivazione salvata
        with open(license_file, "r") as f:
            saved_date_str = f.read().strip()
        try:
            activation_date = datetime.date.fromisoformat(saved_date_str)
        except ValueError:
            activation_date = today

    # Calcola i giorni trascorsi
    elapsed_days = (today - activation_date).days

    if elapsed_days > trial_days:
        # PERIODO DI PROVA SCADUTO - MOSTRA SCHERMATA PRO / LISTA D'ATTESA + DISCLAIMER
        page.title = "CFTC COT Analyzer - Prova Terminata"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        
        page.add(
            ft.ListView([
                ft.Column([
                    ft.Text("⚠️ IL PERIODO DI PROVA DI 60 GIORNI E' SCADUTO", size=18, weight=ft.FontWeight.BOLD, color="red"),
                    ft.Divider(height=15, color="white24"),
                    ft.Text("Speriamo che l'analisi automatizzata del COT CFTC ti sia stata utile!", size=13, color="white"),
                    ft.Text("La versione PRO commerciale sarà disponibile a brevissimo.", size=13, color="white70"),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("OFFERTA PRE-LANCIO LIFETIME", weight=ft.FontWeight.BOLD, color="yellow", size=12),
                            ft.Text("Prezzo d'acquisto unico (Nessun abbonamento):", size=12, color="white"),
                            ft.Text("SOLO 9,00 €", size=26, weight=ft.FontWeight.BOLD, color="green"),
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        border_radius=10,
                        bgcolor="white10"
                    ),
                    ft.Container(height=15),
                    ft.ElevatedButton(
                        "🌟 Prenota la tua licenza a 9€ (Lista d'Attesa)",
                        bgcolor="purple",
                        color="white",
                        on_click=lambda e: page.launch_url("https://docs.google.com/forms/d/e/1FAIpQLSfWMwAitp2ytV-CXU2YFGEBqLC88QM9rxHijfEelcLh3CgjOQ/viewform?usp=header")
                    ),
                    ft.Container(height=20),
                    ft.Divider(height=10, color="white24"),
                    # --- AVVERTENZA / DISCLAIMER ---
                    ft.Text(
                        "AVVERTENZA!!\n"
                        "Le opzioni e CFD sono strumenti complessi ad alto rischio di perdita di capitale dovuto alla leva. "
                        "Il 74% di conti di investitori al dettaglio perdono denaro a causa delle negoziazioni in CFD. "
                        "Valutate se potete permettervi di correre l’elevato rischio di perdere il vostro denaro. "
                        "La seguente app non fa altro che semplificare la lettura dei dati report cftc visibili sul sito "
                        "https://www.cftc.gov/dea/newcot/deafut.txt e fornire la lettura dei grafici dal sito barchart.com; "
                        "non è in nessun modo un'app da ritenersi come signal bot trading o quant'altro. "
                        "Non siamo in nessun modo responsabili di eventuali perdite di denaro da voi subite.",
                        size=9,
                        color="white54",
                        italic=True,
                        text_align=ft.TextAlign.LEFT
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], expand=True)
        )
        page.update()
        return  # Blocca l'esecuzione dell'app

    # --- CONTINUA CON L'APP NORMALE (VERSIONE DEMO ATTIVA) ---
    page.title = "CFTC COT Analyzer"
    page.theme_mode = ft.ThemeMode.DARK
    
    page.add(
        ft.Text("Benvenuto nella versione Demo del CFTC COT Analyzer!", size=16, color="white")
    )
    page.update()

ft.app(target=main)
import flet as ft
import urllib.request
import csv
import io

# ==========================================
# DIZIONARIO MULTILINGUA COMPLETO
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
        "sec_cross": "--- ANALISI DINAMICA CROSS PRINCIPALI ---",
        "sec_commodities": "--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---",
        "sec_indices": "--- INDICI AZIONARI ---",
        # Segnali dinamici
        "cross_long": "-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f})."
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
        "sec_cross": "--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---",
        "sec_commodities": "--- COMMODITIES & CORRELATION ---",
        "sec_indices": "--- STOCK INDICES ---",
        # Segnali dinamici
        "cross_long": "-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f})."
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
        "sec_cross": "--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---",
        "sec_commodities": "--- MATERIAS PRIMAS ---",
        "sec_indices": "--- ÍNDICES BURSÁTILES ---",
        # Segnali dinamici
        "cross_long": "-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BULLISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f})."
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
        "sec_cross": "--- DYNAMISCHE ANALYSE DER HAUPTKREUZUNGEN ---",
        "sec_commodities": "--- ROHSTOFFE & KORRELATION ---",
        "sec_indices": "--- AKTIENINDIZES ---",
        # Segnali dinamici
        "cross_long": "-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BULLISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f})."
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
        "sec_cross": "--- ANALYSE DYNAMIQUE DES CROISEMENTS MAJEURS ---",
        "sec_commodities": "--- MATIÈRES PREMIÈRES & CORRÉLATION ---",
        "sec_indices": "--- INDICES BOURSIERS ---",
        # Segnali dinamici
        "cross_long": "-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BULLISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f})."
    }
}

BARCHART_LINKS = {
    "SWISS FRANC": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0",
    "USD INDEX": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0",
    "MEXICAN PESO": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0",
    "NZ DOLLAR": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0",
    "CANADIAN DOLLAR": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0",
    "BRAZILIAN REAL": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0",
    "SOUTH AFRICAN RAND": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0",
    "BRITISH POUND": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0",
    "JAPANESE YEN": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0",
    "EURO FX": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0",
    "AUSTRALIAN DOLLAR": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0",
    "CORN": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0",
    "SOYBEANS": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0",
    "SOYBEAN OIL": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0",
    "SOYBEAN MEAL": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0",
    "WHEAT-SRW": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0",
    "WHEAT-HRW": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0",
    "WHEAT-SPRING": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0",
    "ROUGH RICE": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0",
    "CANOLA": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0",
    "GOLD": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0",
    "SILVER": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0",
    "COPPER": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0",
    "PALLADIUM": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0",
    "PLATINUM": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0",
    "ALUMINUM": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0",
    "COCOA": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0",
    "COTTON": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0",
    "COFFEE": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0",
    "SUGAR": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0",
    "ORANGE JUICE": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0",
    "LUMBER": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0",
    "CRUDE OIL": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0",
    "GASOLINE": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0",
    "NY HARBOR ULSD": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0",
    "NATURAL GAS": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0",
    "ETHANOL": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0",
    "S&P 500": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0",
    "NASDAQ-100": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0",
    "DOW JONES": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0",
    "RUSSELL 2000": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0",
    "VIX": "https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0"
}

def main(page: ft.Page):
    try:
        page.data = {"lang": "Italiano"}
        page.title = "CFTC COT Analyzer"
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20

        t = TRANSLATIONS[page.data["lang"]]

        title_text = ft.Text(t["title"], size=22, weight=ft.FontWeight.BOLD, color="white")
        
        def change_language(e):
            page.data["lang"] = lang_dropdown.value
            lang_t = TRANSLATIONS[page.data["lang"]]
            title_text.value = lang_t["title"]
            analyze_btn.text = lang_t["btn_ready"]
            charts_btn.text = lang_t["btn_charts"]
            status_text.value = lang_t["status_ready"]
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
        
        results_column = ft.Column(spacing=2) 
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
            t = TRANSLATIONS[page.data.get("lang", "Italiano")]
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
                        "CRUDE OIL", "GASOLINE", "NY HARBOR ULSD", "NATURAL GAS", "ETHANOL"
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
                                        f"{market_name[:26]:<28} | "
                                        f"Long: {pct_long:5.1f}% ({change_long:+6d}) | "
                                        f"Short: {pct_short:5.1f}% ({change_short:+6d}) | "
                                        f"Slope: {net_slope:+6.1f} [{bias}]"
                                    )
                                    all_results.append((line, "MARKET", kw.upper()))
                                    
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
                
                signals.append((t["sec_cross"], "SUBHEADER"))
                for base, quote in major_pairs:
                    if base in cur_strength and quote in cur_strength:
                        s_base, s_quote = cur_strength[base], cur_strength[quote]
                        diff = s_base - s_quote
                        if diff > 10:
                            signals.append((t["cross_long"].format(base=base, quote=quote, s_base=s_base, s_quote=s_quote), "TEXT"))
                        elif diff < -10:
                            signals.append((t["cross_short"].format(base=base, quote=quote, s_base=s_base, s_quote=s_quote), "TEXT"))

                signals.append((t["sec_commodities"], "SUBHEADER"))
                commodities_to_check = ["GOLD", "SILVER", "CRUDE OIL", "COPPER", "LUMBER", "CORN", "SOYBEANS"]
                usd_slope = cur_strength.get("USD", 0)
                
                for comm in commodities_to_check:
                    comm_data = market_data.get(comm)
                    if comm_data:
                        c_name = comm_data['name'].split('-')[0].strip()
                        slope = comm_data["net_slope"]
                        
                        if comm_data["pct_short"] > 60 and comm_data["chg_short"] < 0:
                            signals.append((t["comm_squeeze"].format(name=c_name, slope=slope), "TEXT"))
                        elif slope > 15 and usd_slope < 0:
                            signals.append((t["comm_bullish"].format(name=c_name, slope=slope), "TEXT"))
                        elif slope < -15 and usd_slope > 0:
                            signals.append((t["comm_bearish"].format(name=c_name, slope=slope), "TEXT"))

                # Inserimento ordinato e uniforme nella UI con intestazioni multilingua
                results_column.controls.append(ft.Text(t["report_header"], weight=ft.FontWeight.BOLD, color="yellow", size=11))
                results_column.controls.append(ft.Text("=" * 70, color="white24", size=10))

                for entry in all_results:
                    if entry[1] == "HEADER":
                        results_column.controls.append(ft.Text(f"\n--- {entry[0]} ---", weight=ft.FontWeight.BOLD, color="cyan", size=12))
                    else:
                        item_text = entry[0]
                        kw_matched = entry[2]
                        
                        url_chart = BARCHART_LINKS.get(kw_matched, "https://www.barchart.com/futures/commitment-of-traders")
                        
                        results_column.controls.append(
                            ft.TextButton(
                                content=ft.Text(
                                    item_text, 
                                    font_family="Consolas", # Oppure "Courier New" / "monospace"
                                    size=11, 
                                    color="white"
                                ),
                                on_click=lambda e, u=url_chart: page.launch_url(u),
                                style=ft.ButtonStyle(padding=0)
                            )
                        )

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
if __name__ == '__main__':
    ft.app(target=main)
