import datetime
import os
import io
import csv
import urllib.request
import flet as ft

# ==========================================
# DIZIONARIO MULTILINGUA COMPLETO
# ==========================================
TRANSLATIONS = {
    "Italiano": {
        "title": "CFTC COT Analyzer",
        "title1": "NO Commercial Group",
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
        "cross_long": "-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).",
        "disclaimer_title": "AVVERTENZA!!",
        "disclaimer_body": (
            "Le opzioni e CFD sono strumenti complessi ad alto rischio di perdita di capitale dovuto alla leva. "
            "Il 74% di conti di investitori al dettaglio perdono denaro a causa delle negoziazioni in CFD. "
            "Valutate se potete permettervi di correre l’elevato rischio di perdere il vostro denaro. "
            "La seguente app non fa altro che semplificare la lettura dei dati report cftc visibili sul sito "
            "https://www.cftc.gov/dea/newcot/deafut.txt e fornire la lettura dei grafici dal sito barchart.com; "
            "non è in nessun modo un'app da ritenersi come signal bot trading o quant'altro. "
            "Non siamo in nessun modo responsabili di eventuali perdite di denaro da voi subite."
        ),
        # Testi specifici schermata scadenza demo
        "expired_title": "⚠️ PERIODO DI PROVA DI 60 GIORNI SCADUTO",
        "expired_subtitle": "Speriamo che l'analisi automatizzata del COT CFTC ti sia stata utile!\nLa versione PRO commerciale sarà disponibile a brevissimo.",
        "expired_box_title": "OFFERTA PRE-LANCIO LIFETIME",
        "expired_box_sub": "Prezzo d'acquisto unico (Nessun abbonamento):",
        "expired_price": "SOLO 9,00 €",
        "expired_btn": "🌟 Prenota la tua licenza a 9€ (Lista d'Attesa)"
    },
    "English": {
        "title": "CFTC COT Analyzer",
        "title1": "NO Commercial Group",
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
        "cross_long": "-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).",
        "disclaimer_title": "WARNING / RISK DISCLAIMER!!",
        "disclaimer_body": (
            "CFDs and Options are complex instruments with a high risk of losing money rapidly due to leverage. "
            "74% of retail investor accounts lose money when trading CFDs. "
            "You should consider whether you can afford to take the high risk of losing your money. "
            "This application simply simplifies the reading of public CFTC report data from "
            "https://www.cftc.gov/dea/newcot/deafut.txt and provides chart viewing via barchart.com. "
            "It is by no means a trading signal bot or financial advice. "
            "We are in no way responsible for any financial losses incurred."
        ),
        "expired_title": "⚠️ 60-DAY TRIAL PERIOD EXPIRED",
        "expired_subtitle": "We hope the automated CFTC COT analysis was useful to you!\nThe commercial PRO version will be available very soon.",
        "expired_box_title": "LIFETIME PRE-LAUNCH OFFER",
        "expired_box_sub": "One-time purchase price (No subscription):",
        "expired_price": "ONLY €9.00",
        "expired_btn": "🌟 Reserve your €9 license (Waiting List)"
    },
    "Español": {
        "title": "CFTC COT Analyzer",
        "title1": "NO Commercial Group",
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
        "cross_long": "-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f}).",
        "disclaimer_title": "ADVERTENCIA DE RIESGO!!",
        "disclaimer_body": (
            "Los CFD y las opciones son instrumentos complejos y conllevan un alto riesgo de perder dinero rápidamente debido al apalancamiento. "
            "El 74% de las cuentas de inversores minoristas pierden dinero al negociar CFD. "
            "Debe considerar si comprende cómo funcionan los CFD y si puede permitirse asumir el alto riesgo de perder su dinero. "
            "Esta aplicación solo simplifica la lectura de los datos oficiales de los informes CFTC y redirige a los gráficos de barchart.com; "
            "no debe considerarse en ningún caso un bot de señales de trading. No nos hacemos responsables de las pérdidas económicas sufridas."
        ),
        "expired_title": "⚠️ PERIODO DE PRUEBA DE 60 DÍAS CADUCADO",
        "expired_subtitle": "¡Esperamos que el análisis automatizado del COT CFTC te haya sido útil!\nLa versión PRO comercial estará disponible muy pronto.",
        "expired_box_title": "OFERTA PRE-LANZAMIENTO LIFETIME",
        "expired_box_sub": "Precio de compra único (Sin suscripción):",
        "expired_price": "SOLO 9,00 €",
        "expired_btn": "🌟 Reserva tu licencia por 9€ (Lista de espera)"
    },
    "Deutsch": {
        "title": "CFTC COT Analyzer",
        "title1": "NO Commercial Group",
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
        "cross_long": "-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f}).",
        "disclaimer_title": "WARNHINWEIS!!",
        "disclaimer_body": (
            "CFDs und Optionen sind komplexe Instrumente und gehen wegen der Hebelwirkung mit einem hohen Risiko einher, schnell Geld zu verlieren. "
            "74% der Konten von Kleinanlegern verlieren beim CFD-Handel Geld. "
            "Sie sollten überlegen, ob Sie es sich leisten können, das hohe Risiko einzugehen, Ihr Geld zu verlieren. "
            "Diese App vereinfacht lediglich das Lesen öffentlich zugänglicher CFTC-Berichtsdaten und bietet Verlinkungen zu barchart.com; "
            "sie ist in keiner Weise als Trading-Signal-Bot oder Finanzberatung zu verstehen."
        ),
        "expired_title": "⚠️ 60-TAGE-TESTPHASE ABGELAUFEN",
        "expired_subtitle": "Wir hoffen, die automatisierte CFTC COT-Analyse war nützlich für Sie!\nDie kommerzielle PRO-Version wird in Kürze verfügbar sein.",
        "expired_box_title": "LIFETIME VORSTART-ANGEBOT",
        "expired_box_sub": "Einmaliger Kaufpreis (Kein Abonnement):",
        "expired_price": "NUR 9,00 €",
        "expired_btn": "🌟 Reservieren Sie Ihre 9€-Lizenz (Warteliste)"
    },
    "Français": {
        "title": "CFTC COT Analyzer",
        "title1": "NO Commercial Group",
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
        "cross_long": "-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "cross_short": "-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})",
        "comm_squeeze": "-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).",
        "comm_bullish": "-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).",
        "comm_bearish": "-> [COMMODITY / BEARISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f}).",
        "disclaimer_title": "AVERTISSEMENT DE RISQUE!!",
        "disclaimer_body": (
            "Les CFD et les options sont des instruments complexes et présentent un risque élevé de perte rapide en capital en raison de l'effet de levier. "
            "74% des comptes d'investisseurs de détail perdent de l'argent lors de la négociation de CFD. "
            "Vous devez vous demander si vous pouvez vous permettre de prendre le risque élevé de perdre votre argent. "
            "Cette application simplifie uniquement la lecture des données publiques des rapports CFTC et renvoie vers barchart.com ; "
            "elle ne doit en aucun cas être considérée comme un bot de signaux de trading."
        ),
        "expired_title": "⚠️ PÉRIODE D'ESSAI DE 60 JOURS EXPIRÉE",
        "expired_subtitle": "Nous espérons que l'analyse automatisée du COT CFTC vous a été utile !\nLa version PRO commerciale sera disponible très prochainement.",
        "expired_box_title": "OFFRE DE PRÉ-LANCEMENT LIFETIME",
        "expired_box_sub": "Prix d'achat unique (Aucun abonnement) :",
        "expired_price": "SEULEMENT 9,00 €",
        "expired_btn": "🌟 Réservez votre licence à 9€ (Liste d'attente)"
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
        
        # ==========================================
        # 1. CONTROLLO DEMO 60 GIORNI
        # ==========================================
        license_file = "license.key"
        trial_days = 60
        today = datetime.date.today()

        if not os.path.exists(license_file):
            with open(license_file, "w") as f:
                f.write(today.isoformat())
            activation_date = today
        else:
            with open(license_file, "r") as f:
                saved_date_str = f.read().strip()
            try:
                activation_date = datetime.date.fromisoformat(saved_date_str)
            except ValueError:
                activation_date = today

        elapsed_days = (today - activation_date).days

        if elapsed_days > trial_days:
            # --- SCHERMATA DI SCADENZA PROVA (CON SUPPORTO LINGUA) ---
            page.title = "CFTC COT Analyzer - Prova Terminata"
            page.theme_mode = ft.ThemeMode.DARK
            page.padding = 20
            
            t_exp = TRANSLATIONS[page.data["lang"]]

            # Elementi dinamici della schermata di scadenza
            exp_title = ft.Text(t_exp["expired_title"], size=16, weight=ft.FontWeight.BOLD, color="red", text_align=ft.TextAlign.CENTER)
            exp_sub1 = ft.Text(t_exp["expired_subtitle"], size=13, color="white", text_align=ft.TextAlign.CENTER)
            
            box_title = ft.Text(t_exp["expired_box_title"], weight=ft.FontWeight.BOLD, color="yellow", size=12)
            box_sub = ft.Text(t_exp["expired_box_sub"], size=12, color="white")
            price_text = ft.Text(t_exp["expired_price"], size=26, weight=ft.FontWeight.BOLD, color="green")
            
            waitlist_btn = ft.ElevatedButton(
                t_exp["expired_btn"],
                bgcolor="purple",
                color="white",
                on_click=lambda e: page.launch_url("https://forms.gle/h64uQcFrGLGrHa1Y6")
            )
            
            disc_title = ft.Text(t_exp["disclaimer_title"], size=14, weight=ft.FontWeight.BOLD, color="red")
            disc_body = ft.Text(t_exp["disclaimer_body"], size=13, color="white54", italic=True)

            def change_expired_language(e):
                page.data["lang"] = expired_lang_dropdown.value
                lt = TRANSLATIONS[page.data["lang"]]
                
                exp_title.value = lt["expired_title"]
                exp_sub1.value = lt["expired_subtitle"]
                box_title.value = lt["expired_box_title"]
                box_sub.value = lt["expired_box_sub"]
                price_text.value = lt["expired_price"]
                waitlist_btn.text = lt["expired_btn"]
                disc_title.value = lt["disclaimer_title"]
                disc_body.value = lt["disclaimer_body"]
                page.update()

            expired_lang_dropdown = ft.Dropdown(
                label="Language / Lingua",
                value="Italiano",
                options=[ft.dropdown.Option(lang) for lang in TRANSLATIONS.keys()],
                on_change=change_expired_language,
                width=160,
                text_size=12,
                label_style=ft.TextStyle(size=12)
            )

            # Barra in alto con menu lingua nella schermata di scadenza
            expired_top_row = ft.Row(
                controls=[ft.Container(), expired_lang_dropdown],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

            page.add(
                ft.ListView([
                    ft.Column([
                        expired_top_row,
                        ft.Container(height=5),
                        exp_title,
                        ft.Divider(height=15, color="white24"),
                        exp_sub1,
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column([
                                box_title,
                                box_sub,
                                price_text,
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=15,
                            border_radius=10,
                            bgcolor="white10"
                        ),
                        ft.Container(height=15),
                        waitlist_btn,
                        ft.Container(height=20),
                        ft.Divider(height=10, color="white24"),
                        disc_title,
                        disc_body
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], expand=True)
            )
            page.update()
            return  # Interrompe l'esecuzione se la demo è scaduta

        # ==========================================
        # 2. SCHERMATA DEMO ATTIVA (APP NORMALE)
        # ==========================================
        page.title = "CFTC COT Analyzer-NO Commercial Group"
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20

        t = TRANSLATIONS[page.data["lang"]]

        # --- BADGE "DEMO" PERMANENTE IN ALTO A DESTRA ---
        demo_badge = ft.Container(
            content=ft.Text("DEMO", size=10, weight=ft.FontWeight.BOLD, color="white"),
            bgcolor="red900",
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            border_radius=5
        )

        title_text = ft.Text(t["title"], size=18, weight=ft.FontWeight.BOLD, color="white")
        title1_text = ft.Text(t["title1"], size=16, weight=ft.FontWeight.BOLD, color="cyan")
        title_column = ft.Column([title_text, title1_text], spacing=0)

        # --- BLOCCO DISCLAIMER DINAMICO (SCOMPARE AD AVVIO ANALISI) ---
        disclaimer_title_text = ft.Text(t["disclaimer_title"], size=14, weight=ft.FontWeight.BOLD, color="red")
        disclaimer_body_text = ft.Text(t["disclaimer_body"], size=13, color="white54", italic=True)

        disclaimer_container = ft.Container(
            content=ft.Column([
                disclaimer_title_text,
                disclaimer_body_text
            ], spacing=2),
            padding=10,
            border_radius=6,
            bgcolor="white10",
            visible=True
        )

        def change_language(e):
            page.data["lang"] = lang_dropdown.value
            lang_t = TRANSLATIONS[page.data["lang"]]
            title_text.value = lang_t["title"]
            analyze_btn.text = lang_t["btn_ready"]
            charts_btn.text = lang_t["btn_charts"]
            status_text.value = lang_t["status_ready"]
            disclaimer_title_text.value = lang_t["disclaimer_title"]
            disclaimer_body_text.value = lang_t["disclaimer_body"]
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
            
            disclaimer_container.visible = False
            
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
                                    font_family="Consolas",
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

        lang_and_badge_row = ft.Row(
            controls=[lang_dropdown, demo_badge],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15  # Distanza tra il menu della lingua e il badge DEMO
        )

        page.add(
            ft.Container(height=10),
            title_column,
            lang_and_badge_row,
            ft.Divider(height=15, color="white24"),
            status_text,
            ft.Container(height=5),
            ft.Row([analyze_btn, charts_btn, progress_ring], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Container(height=10),
            disclaimer_container,
            ft.Divider(height=15, color="white24"),
            horizontal_scroll_view
        )
        page.update()

    except Exception as initialization_error:
        page.clean()
        page.add(
            ft.Text("ERRORE CRITICO DI AVVIO:", size=18, color="red", weight=ft.FontWeight.BOLD),
            ft.Text(str(initialization_error), size=14, color="white")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
