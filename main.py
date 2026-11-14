import datetime
import os
import io
import csv
import urllib.request
import urllib.error
import json
import uuid
import flet as ft

FIREBASE_PROJECT_ID = 'cftc-cot-reader-signal-trading'
FIRESTORE_URL = f'https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/licenses'

TRANSLATIONS = {
    'Italiano': {
        'title': 'CFTC COT Analyzer',
        'title1': 'NO Commercial Group',
        'btn_ready': 'Avvia Analisi',
        'btn_charts': 'Apri Barchart COT',
        'status_ready': "Pronto per l'analisi",
        'status_download': 'Scaricamento dei dati dal report Legacy CFTC...',
        'status_success': 'Analisi completata con successo!',
        'error_prefix': "Errore durante l'esecuzione: ",
        'report_header': 'REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE',
        'screening_header': 'SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES',
        'cat_valute': 'VALUTE',
        'cat_grains': 'MATERIE PRIME - GRAINS',
        'cat_metalli': 'METALLI',
        'cat_softs': 'SOFTS',
        'cat_energies': 'ENERGIES',
        'cat_indici': 'INDICI',
        'sig_valute': '--- INCROCI VALUTARI (Forza Relativa Universale) ---',
        'sec_cross': '--- ANALISI DINAMICA CROSS PRINCIPALI ---',
        'sec_commodities': '--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---',
        'sec_indices': '--- INDICI AZIONARI ---',
        'cross_long': '-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'cross_short': '-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).',
        'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).',
        'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).',
        'disclaimer_title': 'AVVERTENZA!!',
        'disclaimer_body': "Le opzioni e CFD sono strumenti complessi ad alto rischio di perdita di capitale dovuto alla leva. Il 74% di conti di investitori al dettaglio perdono denaro a causa delle negoziazioni in CFD. Valutate se potete permettervi di correre l’elevato rischio di perdere il vostro denaro. La seguente app non fa altro che semplificare la lettura dei dati report cftc visibili sul sito https://www.cftc.gov/dea/newcot/deafut.txt e fornire la lettura dei grafici dal sito barchart.com; non è in nessun modo un'app da ritenersi come signal bot trading o quant'altro. Non siamo in nessun modo responsabili di eventuali perdite di denaro da voi subite.",
        'expired_title': '⚠️ PERIODO DI PROVA DI 60 GIORNI SCADUTO',
        'expired_subtitle': "Speriamo che l'analisi automatizzata del COT CFTC ti sia stata utile!\nLa versione PRO commerciale sarà disponibile a brevissimo.",
        'expired_box_title': 'OFFERTA PRE-LANCIO LIFETIME',
        'expired_box_sub': "Prezzo d'acquisto unico (Nessun abbonamento):",
        'expired_price': 'SOLO 9,00 €',
        'expired_btn': "🌟 Prenota la tua licenza a 9€ (Lista d'Attesa)",
        'net_error_title': '⚠️ ERRORE DI CONNESSIONE',
        'net_error_body': "Impossibile connettersi a internet. L'app richiede una connessione attiva per verificare lo stato della licenza demo.",
        'net_error_btn': 'Riprova'
    },
    'English': {
        'title': 'CFTC COT Analyzer',
        'title1': 'NO Commercial Group',
        'btn_ready': 'Start Analysis',
        'btn_charts': 'Open Barchart COT',
        'status_ready': 'Ready for analysis',
        'status_download': 'Downloading data from CFTC Legacy report...',
        'status_success': 'Analysis completed successfully!',
        'error_prefix': 'Execution error: ',
        'report_header': 'COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE',
        'screening_header': 'STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES',
        'cat_valute': 'CURRENCIES',
        'cat_grains': 'COMMODITIES - GRAINS',
        'cat_metalli': 'METALS',
        'cat_softs': 'SOFTS',
        'cat_energies': 'ENERGIES',
        'cat_indici': 'INDICES',
        'sig_valute': '--- CURRENCY CROSSES (Universal Relative Strength) ---',
        'sec_cross': '--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---',
        'sec_commodities': '--- COMMODITIES & CORRELATION ---',
        'sec_indices': '--- STOCK INDICES ---',
        'cross_long': '-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'cross_short': '-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).',
        'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).',
        'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).',
        'disclaimer_title': 'WARNING / RISK DISCLAIMER!!',
        'disclaimer_body': 'CFDs and Options are complex instruments with a high risk of losing money rapidly due to leverage. 74% of retail investor accounts lose money when trading CFDs. You should consider whether you can afford to take the high risk of losing your money. This application simply simplifies the reading of public CFTC report data from https://www.cftc.gov/dea/newcot/deafut.txt and provides chart viewing via barchart.com. It is by no means a trading signal bot or financial advice. We are in no way responsible for any financial losses incurred.',
        'expired_title': '⚠️ 60-DAY TRIAL PERIOD EXPIRED',
        'expired_subtitle': 'We hope the automated CFTC COT analysis was useful to you!\nThe commercial PRO version will be available very soon.',
        'expired_box_title': 'LIFETIME PRE-LAUNCH OFFER',
        'expired_box_sub': 'One-time purchase price (No subscription):',
        'expired_price': 'ONLY €9.00',
        'expired_btn': '🌟 Reserve your €9 license (Waiting List)',
        'net_error_title': '⚠️ CONNECTION ERROR',
        'net_error_body': 'Unable to connect to the internet. An active connection is required to verify the demo license status.',
        'net_error_btn': 'Retry'
    },
    'Español': {
        'title': 'CFTC COT Analyzer',
        'title1': 'NO Commercial Group',
        'btn_ready': 'Iniciar Análisis',
        'btn_charts': 'Abrir Barchart COT',
        'status_ready': 'Listo para el análisis',
        'status_download': 'Descargando datos del informe Legacy CFTC...',
        'status_success': '¡Análisis completado con éxito!',
        'error_prefix': 'Error de ejecución: ',
        'report_header': 'INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE',
        'screening_header': 'SCREENING ESTRATÉGICO & CRUCES MULTIDIVISA / COMMODITIES',
        'cat_valute': 'DIVISAS',
        'cat_grains': 'MATERIAS PRIMAS - GRAINS',
        'cat_metalli': 'METALES',
        'cat_softs': 'SOFTS',
        'cat_energies': 'ENERGÍAS',
        'cat_indici': 'INDICES',
        'sig_valute': '--- CRUCES DE DIVISAS (Fuerza Relativa Universal) ---',
        'sec_cross': '--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---',
        'sec_commodities': '--- MATERIAS PRIMAS & CORRELACIÓN ---',
        'sec_indices': '--- ÍNDICES BURSÁTILES ---',
        'cross_long': '-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'cross_short': '-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).',
        'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Long fuerte con USD débil (Slope: {slope:+.1f}).',
        'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Short fuerte con USD fuerte (Slope: {slope:+.1f}).',
        'disclaimer_title': '¡ADVERTENCIA DE RIESGO!',
        'disclaimer_body': 'Los CFD y las opciones son instrumentos complejos y con alto riesgo de perder dinero rápidamente debido al apalancamiento. El 74% de las cuentas de inversores minoristas pierden dinero al operar con CFD. Debe considerar si comprende cómo funcionan los CFD y si puede permitirse asumir el alto riesgo de perder su dinero. Esta aplicación simplemente simplifica la lectura de datos públicos del informe CFTC visibles en https://www.cftc.gov/dea/newcot/deafut.txt y facilita gráficos a través de barchart.com; no es de ninguna manera una aplicación que deba considerarse un bot de señales de trading ni nada por el estilo. No somos responsables en modo alguno de las pérdidas financieras sufridas.',
        'expired_title': '⚠️ PERIODO DE PRUEBA DE 60 DÍAS CADUCADO',
        'expired_subtitle': '¡Esperamos que el análisis automatizado de COT te haya sido útil!\nLa versión comercial PRO estará disponible muy pronto.',
        'expired_box_title': 'OFERTA LANZAMIENTO LIFETIME',
        'expired_box_sub': 'Pago único (Sin suscripciones):',
        'expired_price': 'SÓLO 9,00 €',
        'expired_btn': '🌟 Reserva tu licencia por 9€ (Lista de Espera)',
        'net_error_title': '⚠️ ERROR DE CONEXIÓN',
        'net_error_body': 'Imposible conectar a internet. Se requiere una conexión activa para verificar el estado de la licencia demo.',
        'net_error_btn': 'Reintentar'
    },
    'Français': {
        'title': 'CFTC COT Analyzer',
        'title1': 'NO Commercial Group',
        'btn_ready': "Lancer l'Analyse",
        'btn_charts': 'Ouvrir Barchart COT',
        'status_ready': "Prêt pour l'analyse",
        'status_download': 'Téléchargement des données du rapport Legacy CFTC...',
        'status_success': 'Analyse terminée avec succès !',
        'error_prefix': "Erreur d'exécution : ",
        'report_header': 'RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE',
        'screening_header': 'SCREENING STRATÉGIQUE & CROISEMENTS DEVISES / MATIÈRES PREMIÈRES',
        'cat_valute': 'DEVISES',
        'cat_grains': 'MATIÈRES PREMIÈRES - GRAINS',
        'cat_metalli': 'MÉTAUX',
        'cat_softs': 'SOFTS',
        'cat_energies': 'ÉNERGIES',
        'cat_indici': 'INDICES',
        'sig_valute': '--- CROISEMENTS DEVISES (Force Relative Universelle) ---',
        'sec_cross': '--- ANALYSE DYNAMIQUE DES PAIRES MAJEURES ---',
        'sec_commodities': '--- MATIÈRES PREMIÈRES & CORRÉLATION ---',
        'sec_indices': '--- INDICES BOURSIERS ---',
        'cross_long': '-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'cross_short': '-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).',
        'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Long fort avec USD faible (Slope: {slope:+.1f}).',
        'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Short fort avec USD fort (Slope: {slope:+.1f}).',
        'disclaimer_title': 'AVERTISSEMENT SUR LES RISQUES !',
        'disclaimer_body': "Les CFD et options sont des instruments complexes présentant un risque élevé de perte rapide en capital due à l'effet de levier. 74% des comptes d'investisseurs particuliers perdent de l'argent lors de la négociation de CFD. Évaluez si vous pouvez vous permettre de courir le risque élevé de perdre votre argent. Cette application simplifie simplement la lecture des données du rapport public CFTC visibles sur https://www.cftc.gov/dea/newcot/deafut.txt et fournit la lecture des graphiques depuis barchart.com ; il ne s'agit en aucun cas d'un bot de signaux de trading ou autre. Nous ne sommes en aucun cas responsables des pertes financières que vous pourriez subir.",
        'expired_title': "⚠️ PÉRIODE D'ESSAI DE 60 JOURS EXPIRÉE",
        'expired_subtitle': "Nous espérons que l'analyse automatisée vous a été utile !\nLa version PRO commerciale sera bientôt disponible.",
        'expired_box_title': 'OFFRE PRÉ-LANCEMENT LIFETIME',
        'expired_box_sub': 'Prix unique (Aucun abonnement) :',
        'expired_price': 'SEULEMENT 9,00 €',
        'expired_btn': "🌟 Réservez votre licence à 9€ (Liste d'Attente)",
        'net_error_title': '⚠️ ERREUR DE CONNEXION',
        'net_error_body': "Impossible de se connecter à internet. Une connexion active est requise pour vérifier la licence.",
        'net_error_btn': 'Réessayer'
    },
    'Deutsch': {
        'title': 'CFTC COT Analyzer',
        'title1': 'NO Commercial Group',
        'btn_ready': 'Analyse Starten',
        'btn_charts': 'Barchart COT Öffnen',
        'status_ready': 'Bereit für die Analyse',
        'status_download': 'Lade Daten vom CFTC Legacy Report herunter...',
        'status_success': 'Analyse erfolgreich abgeschlossen!',
        'error_prefix': 'Ausführungsfehler: ',
        'report_header': 'COT REPORT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE',
        'screening_header': 'STRATEGISCHES SCREENING & WÄHRUNGS- / ROHSTOFF-KREUZUNGEN',
        'cat_valute': 'WÄHRUNGEN',
        'cat_grains': 'ROHSTOFFE - GRAINS',
        'cat_metalli': 'METALLE',
        'cat_softs': 'SOFTS',
        'cat_energies': 'ENERGIEN',
        'cat_indici': 'INDIZES',
        'sig_valute': '--- WÄHRUNGS-KREUZUNGEN (Universelle Relative Stärke) ---',
        'sec_cross': '--- DYNAMISCHE ANALYSE DER HAUPTPAARE ---',
        'sec_commodities': '--- ROHSTOFFE & KORRELATION ---',
        'sec_indices': '--- AKTIENINDIZES ---',
        'cross_long': '-> [LONG {base}/{quote}] Vorteil für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'cross_short': '-> [SHORT {base}/{quote}] Vorteil für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})',
        'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).',
        'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Starker Long bei schwachem USD (Slope: {slope:+.1f}).',
        'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Starker Short bei starkem USD (Slope: {slope:+.1f}).',
        'disclaimer_title': 'RISIKOHINWEIS!',
        'disclaimer_body': 'CFDs und Optionen sind komplexe Instrumente mit einem hohen Risiko von Kapitalverlusten aufgrund von Hebeleffekten. 74% der Kleinanlegerkonten verlieren beim Handel mit CFDs Geld. Überlegen Sie, ob Sie es sich leisten können, das hohe Risiko einzugehen, Ihr Geld zu verlieren. Diese App vereinfacht lediglich das Lesen der öffentlichen CFTC-Berichtsdaten unter https://www.cftc.gov/dea/newcot/deafut.txt und stellt die Diagramme von barchart.com zur Verfügung; sie ist keineswegs als Trading-Signal-Bot oder Ähnliches zu betrachten. Wir haftend in keiner Weise für erlittene finanzielle Verluste.',
        'expired_title': '⚠️ 60-TAGE-TESTZEITRAUM ABGELAUFEN',
        'expired_subtitle': 'Wir hoffen, die automatisierte Analyse war nützlich!\nDie kommerzielle PRO-Version ist in Kürze verfügbar.',
        'expired_box_title': 'LIFETIME VORAB-ANGEBOT',
        'expired_box_sub': 'Einmaliger Kaufpreis (Kein Abonnement):',
        'expired_price': 'NUR 9,00 €',
        'expired_btn': '🌟 Lizenz für 9€ reservieren (Warteliste)',
        'net_error_title': '⚠️ VERBINDUNGSFEHLER',
        'net_error_body': 'Keine Internetverbindung möglich. Eine aktive Verbindung ist erforderlich.',
        'net_error_btn': 'Wiederholen'
    }
}

BARCHART_LINKS = {
    'SWISS FRANC': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0',
    'USD INDEX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0',
    'MEXICAN PESO': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0',
    'NZ DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0',
    'CANADIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0',
    'BRAZILIAN REAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0',
    'SOUTH AFRICAN RAND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0',
    'BRITISH POUND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0',
    'JAPANESE YEN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0',
    'EURO FX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0',
    'AUSTRALIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0',
    'CORN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0',
    'SOYBEANS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0',
    'SOYBEAN OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0',
    'SOYBEAN MEAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0',
    'WHEAT-SRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0',
    'WHEAT-HRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0',
    'WHEAT-SPRING': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0',
    'ROUGH RICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0',
    'CANOLA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0',
    'GOLD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0',
    'SILVER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0',
    'COPPER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0',
    'PALLADIUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0',
    'PLATINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0',
    'ALUMINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0',
    'COCOA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0',
    'COTTON': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0',
    'COFFEE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0',
    'SUGAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0',
    'ORANGE JUICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0',
    'LUMBER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0',
    'CRUDE OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0',
    'GASOLINE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0',
    'NY HARBOR ULSD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0',
    'NATURAL GAS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0',
    'ETHANOL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0',
    'S&P 500': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0',
    'NASDAQ-100': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0',
    'DOW JONES': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0',
    'RUSSELL 2000': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0',
    'VIX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0'
}

def get_or_create_device_id():
    key_file = 'device_id.key'
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return f.read().strip()
    else:
        new_id = str(uuid.uuid4())
        with open(key_file, 'w') as f:
            f.write(new_id)
        return new_id

def check_license_with_firebase(device_id):
    url = f'{FIRESTORE_URL}/{device_id}'
    today_str = datetime.date.today().isoformat()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            fields = data.get('fields', {})
            install_date_str = fields.get('install_date', {}).get('stringValue', today_str)
            install_date = datetime.date.fromisoformat(install_date_str)
            days_passed = (datetime.date.today() - install_date).days
            if days_passed > 60:
                return ('expired', 0)
            return ('active', 60 - days_passed)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            payload = json.dumps({
                'fields': {
                    'install_date': {'stringValue': today_str},
                    'is_pro': {'booleanValue': False}
                }
            }).encode('utf-8')
            try:
                patch_req = urllib.request.Request(
                    url, data=payload, 
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, 
                    method='PATCH'
                )
                with urllib.request.urlopen(patch_req, timeout=10):
                    return ('active', 60)
            except Exception:
                return ('no_net', None)
        else:
            return ('no_net', None)
    except Exception:
        return ('no_net', None)

def main(page: ft.Page):
    try:
        if not page.data:
            page.data = {'lang': 'Italiano'}
        page.title = 'CFTC COT Analyzer'
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20

        device_id = get_or_create_device_id()
        status, days_left = check_license_with_firebase(device_id)

        # Funzione universale per cambiare lingua al volo ovunque ci si trovi
        def change_language_global(e):
            page.data['lang'] = e.control.value
            page.clean()
            main(page)

        if status == 'no_net':
            t = TRANSLATIONS[page.data['lang']]
            err_title = ft.Text(t['net_error_title'], size=16, weight=ft.FontWeight.BOLD, color='red', text_align=ft.TextAlign.CENTER)
            err_body = ft.Text(t['net_error_body'], size=13, color='white54', text_align=ft.TextAlign.CENTER)
            retry_btn = ft.ElevatedButton(
                t['net_error_btn'], 
                bgcolor='blue', 
                color='white', 
                on_click=lambda e: (page.clean(), main(page))
            )
            
            # Selettore lingua anche nella schermata di errore rete
            net_lang_dropdown = ft.Dropdown(
                label='Language / Lingua', value=page.data['lang'], 
                options=[ft.dropdown.Option(lang) for lang in TRANSLATIONS.keys()], 
                on_change=change_language_global, width=180, text_size=12, label_style=ft.TextStyle(size=12)
            )

            page.add(ft.Column([
                net_lang_dropdown,
                ft.Container(height=10),
                err_title, 
                ft.Divider(height=15, color='white24'), 
                err_body, 
                ft.Container(height=20), 
                retry_btn
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
            page.update()
            return

        if status == 'expired':
            t = TRANSLATIONS[page.data['lang']]
            exp_title = ft.Text(t['expired_title'], size=16, weight=ft.FontWeight.BOLD, color='red', text_align=ft.TextAlign.CENTER)
            exp_sub = ft.Text(t['expired_subtitle'], size=13, color='white', text_align=ft.TextAlign.CENTER)
            box_title = ft.Text(t['expired_box_title'], weight=ft.FontWeight.BOLD, color='yellow', size=12)
            box_sub = ft.Text(t['expired_box_sub'], size=12, color='white')
            price = ft.Text(t['expired_price'], size=26, weight=ft.FontWeight.BOLD, color='green')
            buy_btn = ft.ElevatedButton(t['expired_btn'], bgcolor='purple', color='white', on_click=lambda e: page.launch_url('https://forms.gle/h64uQcFrGLGrHa1Y6'))
            disc_title = ft.Text(t['disclaimer_title'], size=14, weight=ft.FontWeight.BOLD, color='red')
            disc_body = ft.Text(t['disclaimer_body'], size=13, color='white54', italic=True)
            
            expired_lang_dropdown = ft.Dropdown(
                label='Language / Lingua', value=page.data['lang'], 
                options=[ft.dropdown.Option(lang) for lang in TRANSLATIONS.keys()], 
                on_change=change_language_global, width=180, text_size=12, label_style=ft.TextStyle(size=12)
            )

            page.add(ft.ListView([
                ft.Column([
                    expired_lang_dropdown,
                    ft.Container(height=10),
                    exp_title, 
                    ft.Divider(height=15, color='white24'), 
                    exp_sub, 
                    ft.Container(height=10), 
                    ft.Container(
                        content=ft.Column([box_title, box_sub, price], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
                        padding=15, border_radius=10, bgcolor='white10'
                    ), 
                    ft.Container(height=15), 
                    buy_btn, 
                    ft.Container(height=20), 
                    ft.Divider(height=10, color='white24'), 
                    disc_title, 
                    disc_body
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], expand=True))
            page.update()
            return

        page.scroll = ft.ScrollMode.AUTO
        t = TRANSLATIONS[page.data['lang']]

        demo_badge = ft.Container(
            content=ft.Text(f'DEMO ({days_left}g)', size=10, weight=ft.FontWeight.BOLD, color='white'), 
            bgcolor='red900', padding=ft.padding.symmetric(horizontal=8, vertical=3), border_radius=5
        )
        
        title_text = ft.Text(t['title'], size=18, weight=ft.FontWeight.BOLD, color='white')
        subtitle_text = ft.Text(t['title1'], size=16, weight=ft.FontWeight.BOLD, color='cyan')
        header_column = ft.Column([title_text, subtitle_text], spacing=0)

        disclaimer_title_text = ft.Text(t['disclaimer_title'], size=14, weight=ft.FontWeight.BOLD, color='red')
        disclaimer_body_text = ft.Text(t['disclaimer_body'], size=13, color='white54', italic=True)
        disclaimer_container = ft.Container(
            content=ft.Column([disclaimer_title_text, disclaimer_body_text], spacing=2), 
            padding=10, border_radius=6, bgcolor='white10', visible=True
        )

        status_text = ft.Text(t['status_ready'], size=13, color='green')
        progress_ring = ft.ProgressRing(visible=False, width=20, height=20)
        results_column = ft.Column(spacing=2)
        results_container = ft.Container(content=results_column, padding=ft.padding.only(bottom=100))
        horizontal_scroll_view = ft.Row([results_container], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        analyze_btn = ft.ElevatedButton(t['btn_ready'], bgcolor='blue', color='white')
        charts_btn = ft.ElevatedButton(t['btn_charts'], on_click=lambda e: page.launch_url('https://www.barchart.com/futures/commitment-of-traders'), bgcolor='green', color='white')

        lang_dropdown = ft.Dropdown(
            label='Language / Lingua', value=page.data['lang'], 
            options=[ft.dropdown.Option(lang) for lang in TRANSLATIONS.keys()], 
            on_change=change_language_global, width=180, text_size=12, label_style=ft.TextStyle(size=12)
        )

        def run_analysis(e):
            active_t = TRANSLATIONS[page.data.get('lang', 'Italiano')]
            disclaimer_container.visible = False
            status_text.value = active_t['status_download']
            progress_ring.visible = True
            results_column.controls.clear()
            page.update()
            try:
                cftc_url = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                req = urllib.request.Request(cftc_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    raw_data = resp.read().decode('utf-8', errors='ignore')
                
                f_obj = io.StringIO(raw_data)
                csv_reader = csv.reader(f_obj)
                rows = list(csv_reader)

                categories = {
                    active_t['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], 
                    active_t['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], 
                    active_t['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], 
                    active_t['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], 
                    active_t['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], 
                    active_t['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']
                }

                market_report_items = []
                market_data = {}

                for cat_name, tickers in categories.items():
                    market_report_items.append((cat_name, 'HEADER'))
                    for ticker_query in tickers:
                        for row in rows:
                            if not row or len(row) < 40:
                                continue
                            market_name = str(row[0]).strip()
                            if ticker_query.upper() in market_name.upper():
                                try:
                                    open_int = float(row[7]) if row[7].strip() and float(row[7]) > 0 else 1
                                    long_spec = float(row[8]) if row[8].strip() else 0
                                    short_spec = float(row[9]) if row[9].strip() else 0
                                    chg_long = int(float(row[38])) if row[38].strip() else 0
                                    chg_short = int(float(row[39])) if row[39].strip() else 0

                                    pct_long = long_spec / open_int * 100
                                    pct_short = short_spec / open_int * 100
                                    net_long_chg = long_spec - chg_long
                                    net_short_chg = short_spec - chg_short
                                    pct_chg_long = chg_long / net_long_chg * 100 if net_long_chg > 0 else 0
                                    pct_chg_short = chg_short / net_short_chg * 100 if net_short_chg > 0 else 0
                                    
                                    score_long = pct_long + pct_chg_long / 10.0
                                    score_short = pct_short + pct_chg_short / 10.0
                                    net_slope = score_long - score_short

                                    if net_slope > 15:
                                        state_str = 'STRONG LONG'
                                    elif net_slope > 5:
                                        state_str = 'MODERATE LONG'
                                    elif net_slope < -15:
                                        state_str = 'STRONG SHORT'
                                    elif net_slope < -5:
                                        state_str = 'MODERATE SHORT'
                                    else:
                                        state_str = 'NEUTRAL'

                                    formatted_line = f"{market_name[:26]:<28} | Long: {pct_long:5.1f}% ({chg_long:+6d}) | Short: {pct_short:5.1f}% ({chg_short:+6d}) | Slope: {net_slope:+6.1f} [{state_str}]"
                                    market_report_items.append((formatted_line, 'MARKET', ticker_query.upper()))
                                    
                                    market_key = ticker_query.upper()
                                    market_data[market_key] = {
                                        'name': market_name, 'pct_long': pct_long, 'pct_short': pct_short, 
                                        'chg_long': chg_long, 'chg_short': chg_short, 'net_slope': net_slope
                                    }
                                    break
                                except Exception:
                                    pass

                signals_list = []
                fx_mapping = {
                    'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 
                    'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 
                    'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'
                }
                cur_strength = {}
                for f_name, f_code in fx_mapping.items():
                    if f_name in market_data:
                        cur_strength[f_code] = market_data[f_name]['net_slope']

                sorted_cur = sorted(cur_strength.items(), key=lambda x: x[1], reverse=True)
                signals_list.append((active_t['sig_valute'], 'SUBHEADER'))
                if len(sorted_cur) >= 2:
                    signals_list.append((f"-> [TOP SETUP ABS] {sorted_cur[0][0]}/{sorted_cur[-1][0]} | Max div ({sorted_cur[0][0]}: {sorted_cur[0][1]:+.1f} vs {sorted_cur[-1][0]}: {sorted_cur[-1][1]:+.1f})", 'TEXT'))

                major_crosses = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                signals_list.append((active_t['sec_cross'], 'SUBHEADER'))
                for base, quote in major_crosses:
                    if base in cur_strength and quote in cur_strength:
                        s_base, s_quote = cur_strength[base], cur_strength[quote]
                        diff = s_base - s_quote
                        if diff > 10:
                            signals_list.append((active_t['cross_long'].format(base=base, quote=quote, s_base=s_base, s_quote=s_quote), 'TEXT'))
                        elif diff < -10:
                            signals_list.append((active_t['cross_short'].format(base=base, quote=quote, s_base=s_base, s_quote=s_quote), 'TEXT'))

                signals_list.append((active_t['sec_commodities'], 'SUBHEADER'))
                target_comms = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                usd_slope = cur_strength.get('USD', 0)
                for comm in target_comms:
                    c_info = market_data.get(comm)
                    if c_info:
                        c_clean_name = c_info['name'].split('-')[0].strip()
                        c_slope = c_info['net_slope']
                        if c_info['pct_short'] > 60 and c_info['chg_short'] < 0:
                            signals_list.append((active_t['comm_squeeze'].format(name=c_clean_name, slope=c_slope), 'TEXT'))
                        elif c_slope > 15 and usd_slope < 0:
                            signals_list.append((active_t['comm_bullish'].format(name=c_clean_name, slope=c_slope), 'TEXT'))
                        elif c_slope < -15 and usd_slope > 0:
                            signals_list.append((active_t['comm_bearish'].format(name=c_clean_name, slope=c_slope), 'TEXT'))

                results_column.controls.append(ft.Text(active_t['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                results_column.controls.append(ft.Text('=' * 70, color='white24', size=10))
                
                for item in market_report_items:
                    if item[1] == 'HEADER':
                        results_column.controls.append(ft.Text(f"\n--- {item[0]} ---", weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        line_text, _, ticker_key = item
                        link_url = BARCHART_LINKS.get(ticker_key, 'https://www.barchart.com/futures/commitment-of-traders')
                        results_column.controls.append(
                            ft.TextButton(
                                content=ft.Text(line_text, font_family='Consolas', size=11, color='white'), 
                                on_click=lambda e, u=link_url: page.launch_url(u), 
                                style=ft.ButtonStyle(padding=0)
                            )
                        )

                results_column.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                results_column.controls.append(ft.Text(active_t['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                results_column.controls.append(ft.Text('=' * 70, color='white24', size=10))

                for text_val, item_type in signals_list:
                    if item_type == 'SUBHEADER':
                        results_column.controls.append(ft.Text(f"\n{text_val}", weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        results_column.controls.append(ft.Text(text_val, size=11, color='white70'))

                status_text.value = active_t['status_success']
            except Exception as ex:
                active_t = TRANSLATIONS[page.data.get('lang', 'Italiano')]
                status_text.value = f"{active_t['error_prefix']}{ex}"
            
            progress_ring.visible = False
            page.update()

        analyze_btn.on_click = run_analysis

        lang_and_badge_row = ft.Row(
            controls=[lang_dropdown, demo_badge], 
            alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
        )

        page.add(
            ft.Container(height=10), 
            header_column, 
            lang_and_badge_row, 
            ft.Divider(height=15, color='white24'), 
            status_text, 
            ft.Container(height=5), 
            ft.Row([analyze_btn, charts_btn, progress_ring], alignment=ft.MainAxisAlignment.START, spacing=10), 
            ft.Container(height=10), 
            disclaimer_container, 
            ft.Divider(height=15, color='white24'), 
            horizontal_scroll_view
        )
        page.update()
        
    except Exception as initialization_error:
        page.clean()
        page.add(
            ft.Text('ERRORE CRITICO DI AVVIO:', size=18, color='red', weight=ft.FontWeight.BOLD), 
            ft.Text(str(initialization_error), size=14, color='white')
        )
        page.update()

if __name__ == '__main__':
    ft.app(target=main)

