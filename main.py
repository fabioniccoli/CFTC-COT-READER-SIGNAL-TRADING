# Protected by PurePython Obfuscator
import flet as ft
import urllib.request
import csv
import io
import os
import datetime
import hashlib
TRANSLATIONS = {'Italiano': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Avvia Analisi', 'btn_charts': 'Apri Barchart COT', 'btn_activate': 'Attiva Versione Pro', 'status_ready': "Pronto per l'analisi", 'status_download': 'Scaricamento dei dati dal report Legacy CFTC...', 'status_success': 'Analisi completata con successo!', 'error_prefix': "Errore durante l'esecuzione: ", 'report_header': 'REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE', 'screening_header': 'SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES', 'cat_valute': 'VALUTE', 'cat_grains': 'MATERIE PRIME - GRAINS', 'cat_metalli': 'METALLI', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICI', 'sig_valute': '--- INCROCI VALUTARI (Forza Relativa Universale) ---', 'sec_cross': '--- ANALISI DINAMICA CROSS PRINCIPALI ---', 'sec_commodities': '--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---', 'sec_indices': '--- INDICI AZIONARI ---', 'cross_long': '-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).', 'demo_active': 'Versione DEMO ({days} giorni rimanenti)', 'pro_active': 'Versione PRO ATTIVA (A vita)', 'expired_title': 'PERIODO DI PROVA SCADUTO', 'expired_msg': "Il periodo di prova di 60 giorni è scaduto. Inserisci una chiave Pro valida per sbloccare l'app.", 'dlg_title': 'Attivazione Licenza Pro', 'dlg_hint': 'Inserisci il tuo codice seriale', 'dlg_btn': 'Verifica e Attiva', 'dlg_success': "Attivazione riuscita! Riavvia l'app.", 'dlg_error': 'Codice non valido.'}, 'English': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Start Analysis', 'btn_charts': 'Open Barchart COT', 'btn_activate': 'Activate Pro Version', 'status_ready': 'Ready for analysis', 'status_download': 'Downloading data from CFTC Legacy report...', 'status_success': 'Analysis completed successfully!', 'error_prefix': 'Execution error: ', 'report_header': 'COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE', 'screening_header': 'STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES', 'cat_valute': 'CURRENCIES', 'cat_grains': 'COMMODITIES - GRAINS', 'cat_metalli': 'METALS', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CURRENCY CROSSES (Universal Relative Strength) ---', 'sec_cross': '--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---', 'sec_commodities': '--- COMMODITIES & CORRELATION ---', 'sec_indices': '--- STOCK INDICES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).', 'demo_active': 'DEMO Version ({days} days remaining)', 'pro_active': 'PRO Version ACTIVE (Lifetime)', 'expired_title': 'TRIAL PERIOD EXPIRED', 'expired_msg': 'Your 60-day trial period has expired. Please enter a valid Pro key to unlock the app.', 'dlg_title': 'Activate Pro License', 'dlg_hint': 'Enter your serial key', 'dlg_btn': 'Verify & Activate', 'dlg_success': 'Activation successful! Please restart the app.', 'dlg_error': 'Invalid code.'}, 'Español': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Iniciar Análisis', 'btn_charts': 'Abrir Barchart COT', 'btn_activate': 'Activar Versión Pro', 'status_ready': 'Listo para el análisis', 'status_download': 'Descargando datos del informe Legacy CFTC...', 'status_success': '¡Análisis completado con éxito!', 'error_prefix': 'Error durante la ejecución: ', 'report_header': 'INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE', 'screening_header': 'SELECCIÓN ESTRATÉGICA Y CRUCES DE DIVISAS / COMMODITIES', 'cat_valute': 'MONEDAS', 'cat_grains': 'MATERIAS PRIMAS - GRAINS', 'cat_metalli': 'METALES', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGÍAS', 'cat_indici': 'INDICES', 'sig_valute': '--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---', 'sec_cross': '--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---', 'sec_commodities': '--- MATERIAS PRIMAS ---', 'sec_indices': '--- ÍNDICES BURSÁTILES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f}).', 'demo_active': 'Versión DEMO ({days} días restantes)', 'pro_active': 'Versión PRO ACTIVA (De por vida)', 'expired_title': 'PERIODO DE PRUEBA CADUCADO', 'expired_msg': 'El periodo de prueba de 60 días ha caducado. Introduce una clave Pro válida.', 'dlg_title': 'Activar Licencia Pro', 'dlg_hint': 'Introduce tu clave de serie', 'dlg_btn': 'Verificar y Activar', 'dlg_success': '¡Activación exitosa! Reinicia la aplicación.', 'dlg_error': 'Código no válido.'}, 'Deutsch': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Analyse Starten', 'btn_charts': 'Barchart COT Öffnen', 'btn_activate': 'Pro-Version Aktivieren', 'status_ready': 'Bereit für die Analyse', 'status_download': 'Daten aus dem CFTC Legacy Report werden heruntergeladen...', 'status_success': 'Analyse erfolgreich abgeschlossen!', 'error_prefix': 'Fehler bei der Ausführung: ', 'report_header': 'COT BERICHT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE', 'screening_header': 'STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN / COMMODITIES', 'cat_valute': 'WÄHRUNGEN', 'cat_grains': 'ROHSTOFFE - GRAINS', 'cat_metalli': 'METALLE', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIE', 'cat_indici': 'INDIZES', 'sig_valute': '--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---', 'sec_cross': '--- DYNAMISCHE ANALYSE DER HAUPTKREUZUNGEN ---', 'sec_commodities': '--- ROHSTOFFE & KORRELATION ---', 'sec_indices': '--- AKTIENINDIZES ---', 'cross_long': '-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f}).', 'demo_active': 'DEMO-Version ({days} Tage verbleibend)', 'pro_active': 'PRO-Version AKTIV (Lebenslang)', 'expired_title': 'TESTZEITRAUM ABGELAUFEN', 'expired_msg': 'Der 60-tägige Testzeitraum ist abgelaufen. Bitte geben Sie einen Pro-Key ein.', 'dlg_title': 'Pro-Lizenz Aktivieren', 'dlg_hint': 'Geben Sie Ihren Lizenzschlüssel ein', 'dlg_btn': 'Prüfen & Aktivieren', 'dlg_success': 'Aktivierung erfolgreich! Bitte App neu starten.', 'dlg_error': 'Ungültiger Code.'}, 'Français': {'title': 'CFTC COT Analyzer', 'btn_ready': "Lancer l'analyse", 'btn_charts': 'Ouvrir Barchart COT', 'btn_activate': 'Activer la Version Pro', 'status_ready': "Prêt pour l'analyse", 'status_download': 'Téléchargement des données du rapport Legacy CFTC...', 'status_success': 'Analyse terminée avec succès !', 'error_prefix': "Erreur lors de l'exécution : ", 'report_header': 'RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE', 'screening_header': 'SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES / COMMODITIES', 'cat_valute': 'DEVISES', 'cat_grains': 'MATIÈRES PREMIÈRES - GRAINS', 'cat_metalli': 'MÉTAUX', 'cat_softs': 'SOFTS', 'cat_energies': 'ÉNERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---', 'sec_cross': '--- ANALYSE DYNAMIQUE DES CROISEMENTS MAJEURS ---', 'sec_commodities': '--- MATIÈRES PREMIÈRES & CORRÉLATION ---', 'sec_indices': '--- INDICES BOURSIERS ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f}).', 'demo_active': 'Version DEMO ({days} jours restants)', 'pro_active': 'Version PRO ACTIVE (À vie)', 'expired_title': "PÉRIODE D'ESSAI EXPIRÉE", 'expired_msg': "La période d'essai de 60 jours a expiré. Veuillez entrer une clé Pro valide.", 'dlg_title': 'Activer la Licence Pro', 'dlg_hint': 'Entrez votre clé de série', 'dlg_btn': 'Vérifier & Activer', 'dlg_success': "Activation réussie ! Veuillez redémarrer l'application.", 'dlg_error': 'Code invalide.'}}
BARCHART_LINKS = {'SWISS FRANC': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0', 'USD INDEX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0', 'MEXICAN PESO': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0', 'NZ DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0', 'CANADIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0', 'BRAZILIAN REAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0', 'SOUTH AFRICAN RAND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0', 'BRITISH POUND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0', 'JAPANESE YEN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0', 'EURO FX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0', 'AUSTRALIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0', 'CORN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0', 'SOYBEANS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0', 'SOYBEAN OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0', 'SOYBEAN MEAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0', 'WHEAT-SRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0', 'WHEAT-HRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0', 'WHEAT-SPRING': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0', 'ROUGH RICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0', 'CANOLA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0', 'GOLD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0', 'SILVER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0', 'COPPER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0', 'PALLADIUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0', 'PLATINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0', 'ALUMINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0', 'COCOA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0', 'COTTON': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0', 'COFFEE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0', 'SUGAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0', 'ORANGE JUICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0', 'LUMBER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0', 'CRUDE OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0', 'GASOLINE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0', 'NY HARBOR ULSD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0', 'NATURAL GAS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0', 'ETHANOL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0', 'S&P 500': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0', 'NASDAQ-100': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0', 'DOW JONES': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0', 'RUSSELL 2000': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0', 'VIX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0'}
LICENSE_FILE = 'license.key'
INSTALL_FILE = 'install.dat'
MASTER_SECRET = '(P4nebianco_Cristina_1952)'

def check_license_status():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r') as _0xf36789:
                _0xbf00fb = _0xf36789.read().strip()
                _0xc5b3f2 = hashlib.sha256(MASTER_SECRET.encode()).hexdigest()[:16].upper()
                if _0xbf00fb == _0xc5b3f2:
                    return ('PRO', 0)
        except Exception:
            pass
    _0xbb1e92 = datetime.datetime.now()
    if not os.path.exists(INSTALL_FILE):
        try:
            with open(INSTALL_FILE, 'w') as _0xf36789:
                _0xf36789.write(_0xbb1e92.strftime('%Y-%m-%d'))
            _0x744b1b = _0xbb1e92
        except Exception:
            _0x744b1b = _0xbb1e92
    else:
        try:
            with open(INSTALL_FILE, 'r') as _0xf36789:
                _0xeaa9e7 = _0xf36789.read().strip()
                _0x744b1b = datetime.datetime.strptime(_0xeaa9e7, '%Y-%m-%d')
        except Exception:
            _0x744b1b = _0xbb1e92
    _0x419425 = (_0xbb1e92 - _0x744b1b).days
    _0x8b2fd3 = 60 - _0x419425
    if _0x8b2fd3 <= 0:
        return ('EXPIRED', 0)
    return ('DEMO', _0x8b2fd3)

def save_pro_key(_0x336e72):
    _0xc5b3f2 = hashlib.sha256(MASTER_SECRET.encode()).hexdigest()[:16].upper()
    if _0x336e72.strip().upper() == _0xc5b3f2:
        try:
            with open(LICENSE_FILE, 'w') as _0xf36789:
                _0xf36789.write(_0xc5b3f2)
            return True
        except Exception:
            return False
    return False

def main(page: ft.Page):
    try:
        page.title = 'CFTC COT Analyzer'
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20
        _0x481c0f = 'Italiano'
        _0x161921 = TRANSLATIONS[_0x481c0f]
        _0x0a0752, _0x840028 = check_license_status()
        _0xd0fc2f = ft.Text(_0x161921['title'], size=22, weight=ft.FontWeight.BOLD, color='white')
        if _0x0a0752 == 'PRO':
            _0x121e6e = ft.Text(_0x161921['pro_active'], size=12, color='cyan', weight=ft.FontWeight.BOLD)
        elif _0x0a0752 == 'DEMO':
            _0x121e6e = ft.Text(_0x161921['demo_active'].format(days=_0x840028), size=12, color='orange', weight=ft.FontWeight.BOLD)
        else:
            _0x121e6e = ft.Text(_0x161921['expired_title'], size=12, color='red', weight=ft.FontWeight.BOLD)

        def change_language(_0xd43708):
            nonlocal current_lang, t
            _0x481c0f = _0x83c358.value
            _0x161921 = TRANSLATIONS[_0x481c0f]
            _0xd0fc2f.value = _0x161921['title']
            _0x6a0416.text = _0x161921['btn_ready']
            _0x62d98c.text = _0x161921['btn_charts']
            _0x1b5c19.text = _0x161921['btn_activate']
            _0x763480.value = _0x161921['status_ready']
            if _0x0a0752 == 'PRO':
                _0x121e6e.value = _0x161921['pro_active']
            elif _0x0a0752 == 'DEMO':
                _0x121e6e.value = _0x161921['demo_active'].format(days=_0x840028)
            else:
                _0x121e6e.value = _0x161921['expired_title']
            page.update()
        _0x83c358 = ft.Dropdown(label='Language / Lingua', value='Italiano', options=[ft.dropdown.Option(_0xfba2fc) for _0xfba2fc in TRANSLATIONS.keys()], on_change=change_language, width=180, text_size=12, label_style=ft.TextStyle(size=12))
        _0x763480 = ft.Text(_0x161921['status_ready'], size=13, color='green')
        _0x808a4b = ft.ProgressRing(visible=False, width=20, height=20)
        _0xe65c00 = ft.Column(spacing=2)
        _0x962b6f = ft.Container(content=_0xe65c00, padding=ft.padding.only(bottom=100))
        _0xd040dd = ft.Row([_0x962b6f], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        def open_charts(_0xd43708):
            page.launch_url('https://www.barchart.com/futures/commitment-of-traders')
        _0xa2ab8c = ft.TextField(label=_0x161921['dlg_hint'], password=True, can_reveal_password=True)
        _0x54c426 = ft.Text('', size=12)

        def verify_and_activate(_0xd43708):
            if save_pro_key(_0xa2ab8c.value):
                _0x54c426.value = _0x161921['dlg_success']
                _0x54c426.color = 'green'
                page.update()
            else:
                _0x54c426.value = _0x161921['dlg_error']
                _0x54c426.color = 'red'
                page.update()
        _0x273355 = ft.AlertDialog(title=ft.Text(_0x161921['dlg_title']), content=ft.Column([_0xa2ab8c, _0x54c426], tight=True), actions=[ft.ElevatedButton(_0x161921['dlg_btn'], on_click=verify_and_activate, bgcolor='green', color='white')])

        def open_activation_dialog(_0xd43708):
            page.dialog = _0x273355
            _0x273355.open = True
            page.update()

        def run_analysis(_0xd43708):
            if _0x0a0752 == 'EXPIRED':
                page.dialog = ft.AlertDialog(title=ft.Text(_0x161921['expired_title']), content=ft.Text(_0x161921['expired_msg']), actions=[ft.ElevatedButton('OK', on_click=lambda _0x3630ba: page.window_close())])
                page.dialog.open = True
                page.update()
                return
            _0x763480.value = _0x161921['status_download']
            _0x808a4b.visible = True
            _0xe65c00.controls.clear()
            page.update()
            try:
                _0x88271d = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                _0x557764 = urllib.request.Request(_0x88271d, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(_0x557764, timeout=15) as _0xbb7de5:
                    _0xf033ae = _0xbb7de5.read().decode('utf-8', errors='ignore')
                _0xf36789 = io.StringIO(_0xf033ae)
                _0x79c5a8 = csv.reader(_0xf36789)
                _0xa55b81 = list(_0x79c5a8)
                _0x262dfc = {_0x161921['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], _0x161921['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], _0x161921['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], _0x161921['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], _0x161921['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], _0x161921['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']}
                _0x943feb = []
                _0x1ab98c = {}
                for _0x1198b1, _0xaf92f5 in _0x262dfc.items():
                    _0x943feb.append((_0x1198b1, 'HEADER'))
                    for _0x6a7a94 in _0xaf92f5:
                        for _0x1b50c4 in _0xa55b81:
                            if not _0x1b50c4 or len(_0x1b50c4) < 40:
                                continue
                            _0xaca086 = str(_0x1b50c4[0]).strip()
                            if _0x6a7a94.upper() in _0xaca086.upper():
                                try:
                                    _0xf03f8c = float(_0x1b50c4[7]) if _0x1b50c4[7].strip() and float(_0x1b50c4[7]) > 0 else 1
                                    _0xe59f1a = float(_0x1b50c4[8]) if _0x1b50c4[8].strip() else 0
                                    _0x7cf029 = float(_0x1b50c4[9]) if _0x1b50c4[9].strip() else 0
                                    _0x4d05ff = int(float(_0x1b50c4[38])) if _0x1b50c4[38].strip() else 0
                                    _0x3f5fdc = int(float(_0x1b50c4[39])) if _0x1b50c4[39].strip() else 0
                                    _0x140faf = _0xe59f1a / _0xf03f8c * 100
                                    _0x6af288 = _0x7cf029 / _0xf03f8c * 100
                                    _0x90523e = _0xe59f1a - _0x4d05ff
                                    _0xd5cfd8 = _0x7cf029 - _0x3f5fdc
                                    _0x1b7b18 = _0x4d05ff / _0x90523e * 100 if _0x90523e > 0 else 0
                                    _0x133ddd = _0x3f5fdc / _0xd5cfd8 * 100 if _0xd5cfd8 > 0 else 0
                                    _0x6d1b24 = _0x140faf + _0x1b7b18 / 10.0
                                    _0xa6398b = _0x6af288 + _0x133ddd / 10.0
                                    _0xbb301f = _0x6d1b24 - _0xa6398b
                                    if _0xbb301f > 15:
                                        _0xff0cb8 = 'STRONG LONG'
                                    elif _0xbb301f > 5:
                                        _0xff0cb8 = 'MODERATE LONG'
                                    elif _0xbb301f < -15:
                                        _0xff0cb8 = 'STRONG SHORT'
                                    elif _0xbb301f < -5:
                                        _0xff0cb8 = 'MODERATE SHORT'
                                    else:
                                        _0xff0cb8 = 'NEUTRAL'
                                    _0x46ec27 = f'{_0xaca086[:32]:<34} | Long: {_0x140faf:5.1f}% ({_0x4d05ff:+6d} ctr) | Short: {_0x6af288:5.1f}% ({_0x3f5fdc:+6d} ctr) | Net Slope: {_0xbb301f:+6.1f} [{_0xff0cb8}]'
                                    _0x943feb.append((_0x46ec27, 'MARKET', _0x6a7a94.upper()))
                                    _0x2b41b6 = _0x6a7a94.upper()
                                    _0x1ab98c[_0x2b41b6] = {'name': _0xaca086, 'pct_long': _0x140faf, 'pct_short': _0x6af288, 'chg_long': _0x4d05ff, 'chg_short': _0x3f5fdc, 'net_slope': _0xbb301f}
                                    break
                                except Exception:
                                    pass
                _0xda4d12 = []
                _0x9180b4 = {'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'}
                _0x25b13f = {}
                for _0x4a7fb3, _0xa8ea4f in _0x9180b4.items():
                    if _0x4a7fb3 in _0x1ab98c:
                        _0x25b13f[_0xa8ea4f] = _0x1ab98c[_0x4a7fb3]['net_slope']
                _0x8a0da9 = _0xba6115(_0x25b13f.items(), key=lambda _0x6ca31a: _0x6ca31a[1], reverse=True)
                _0xda4d12.append((_0x161921['sig_valute'], 'SUBHEADER'))
                if len(_0x8a0da9) >= 2:
                    _0xda4d12.append((f'-> [TOP SETUP ABS] {_0x8a0da9[0][0]}/{_0x8a0da9[-1][0]} | Max div ({_0x8a0da9[0][0]}: {_0x8a0da9[0][1]:+.1f} vs {_0x8a0da9[-1][0]}: {_0x8a0da9[-1][1]:+.1f})', 'TEXT'))
                _0x0b8598 = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                _0xda4d12.append((_0x161921['sec_cross'], 'SUBHEADER'))
                for _0x22c70b, _0xa6dde4 in _0x0b8598:
                    if _0x22c70b in _0x25b13f and _0xa6dde4 in _0x25b13f:
                        _0x02d010, _0x93fb52 = (_0x25b13f[_0x22c70b], _0x25b13f[_0xa6dde4])
                        _0x0b0abc = _0x02d010 - _0x93fb52
                        if _0x0b0abc > 10:
                            _0xda4d12.append((_0x161921['cross_long'].format(base=_0x22c70b, quote=_0xa6dde4, s_base=_0x02d010, s_quote=_0x93fb52), 'TEXT'))
                        elif _0x0b0abc < -10:
                            _0xda4d12.append((_0x161921['cross_short'].format(base=_0x22c70b, quote=_0xa6dde4, s_base=_0x02d010, s_quote=_0x93fb52), 'TEXT'))
                _0xda4d12.append((_0x161921['sec_commodities'], 'SUBHEADER'))
                _0x470e43 = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                _0x464fc7 = _0x25b13f.get('USD', 0)
                for _0xe38d42 in _0x470e43:
                    _0x48bea7 = _0x1ab98c.get(_0xe38d42)
                    if _0x48bea7:
                        _0x4db4b5 = _0x48bea7['name'].split('-')[0].strip()
                        _0xf30077 = _0x48bea7['net_slope']
                        if _0x48bea7['pct_short'] > 60 and _0x48bea7['chg_short'] < 0:
                            _0xda4d12.append((_0x161921['comm_squeeze'].format(name=_0x4db4b5, slope=_0xf30077), 'TEXT'))
                        elif _0xf30077 > 15 and _0x464fc7 < 0:
                            _0xda4d12.append((_0x161921['comm_bullish'].format(name=_0x4db4b5, slope=_0xf30077), 'TEXT'))
                        elif _0xf30077 < -15 and _0x464fc7 > 0:
                            _0xda4d12.append((_0x161921['comm_bearish'].format(name=_0x4db4b5, slope=_0xf30077), 'TEXT'))
                _0xe65c00.controls.append(ft.Text(_0x161921['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xe65c00.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0xbff575 in _0x943feb:
                    if _0xbff575[1] == 'HEADER':
                        _0xe65c00.controls.append(ft.Text(f'\n--- {_0xbff575[0]} ---', weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        _0x88e4fe = _0xbff575[0]
                        _0xd885b6 = _0xbff575[2]
                        _0x596802 = BARCHART_LINKS.get(_0xd885b6, 'https://www.barchart.com/futures/commitment-of-traders')
                        _0xe65c00.controls.append(ft.TextButton(content=ft.Text(_0x88e4fe, font_family='monospace', size=11, color='white'), on_click=lambda _0xd43708, _0xb37022=_0x596802: page.launch_url(_0xb37022), style=ft.ButtonStyle(padding=0)))
                _0xe65c00.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                _0xe65c00.controls.append(ft.Text(_0x161921['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xe65c00.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0x33b4e7, _0xebca5f in _0xda4d12:
                    if _0xebca5f == 'SUBHEADER':
                        _0xe65c00.controls.append(ft.Text(f'\n{_0x33b4e7}', weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        _0xe65c00.controls.append(ft.Text(_0x33b4e7, size=11, color='white70'))
                _0x763480.value = _0x161921['status_success']
            except Exception as ex:
                _0x763480.value = f"{_0x161921['error_prefix']}{_0x08ff45}"
            _0x808a4b.visible = False
            page.update()
        _0x6a0416 = ft.ElevatedButton(_0x161921['btn_ready'], on_click=run_analysis, bgcolor='blue', color='white')
        _0x62d98c = ft.ElevatedButton(_0x161921['btn_charts'], on_click=open_charts, bgcolor='green', color='white')
        _0x1b5c19 = ft.ElevatedButton(_0x161921['btn_activate'], on_click=open_activation_dialog, bgcolor='purple', color='white')
        page.add(_0xd0fc2f, _0x121e6e, _0x83c358, ft.Divider(height=15, color='white24'), _0x763480, ft.Container(height=5), ft.Row([_0x6a0416, _0x62d98c, _0x1b5c19, _0x808a4b], alignment=ft.MainAxisAlignment.START, spacing=10), ft.Divider(height=15, color='white24'), _0xd040dd)
        if _0x0a0752 == 'EXPIRED':
            page.dialog = ft.AlertDialog(title=ft.Text(_0x161921['expired_title']), content=ft.Text(_0x161921['expired_msg']), actions=[ft.ElevatedButton(_0x161921['btn_activate'], on_click=open_activation_dialog)])
            page.dialog.open = True
            page.update()
    except Exception as initialization_error:
        page.clean()
        page.add(ft.Text('ERRORE CRITICO DI AVVIO:', size=18, color='red', weight=ft.FontWeight.BOLD), ft.Text(str(_0x45e036), size=14, color='white'))
        page.update()
if __name__ == '__main__':
    ft.app(target=main)
