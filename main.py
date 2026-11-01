# Protected by PurePython Obfuscator
import flet as ft
import urllib.request
import csv
import io
TRANSLATIONS = {'Italiano': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Avvia Analisi', 'btn_charts': 'Apri Barchart COT', 'status_ready': "Pronto per l'analisi", 'status_download': 'Scaricamento dei dati dal report Legacy CFTC...', 'status_success': 'Analisi completata con successo!', 'error_prefix': "Errore durante l'esecuzione: ", 'report_header': 'REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE', 'screening_header': 'SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES', 'cat_valute': 'VALUTE', 'cat_grains': 'MATERIE PRIME - GRAINS', 'cat_metalli': 'METALLI', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICI', 'sig_valute': '--- INCROCI VALUTARI (Forza Relativa Universale) ---', 'sec_cross': '--- ANALISI DINAMICA CROSS PRINCIPALI ---', 'sec_commodities': '--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---', 'sec_indices': '--- INDICI AZIONARI ---', 'cross_long': '-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).'}, 'English': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Start Analysis', 'btn_charts': 'Open Barchart COT', 'status_ready': 'Ready for analysis', 'status_download': 'Downloading data from CFTC Legacy report...', 'status_success': 'Analysis completed successfully!', 'error_prefix': 'Execution error: ', 'report_header': 'COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE', 'screening_header': 'STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES', 'cat_valute': 'CURRENCIES', 'cat_grains': 'COMMODITIES - GRAINS', 'cat_metalli': 'METALS', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CURRENCY CROSSES (Universal Relative Strength) ---', 'sec_cross': '--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---', 'sec_commodities': '--- COMMODITIES & CORRELATION ---', 'sec_indices': '--- STOCK INDICES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).'}, 'Español': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Iniciar Análisis', 'btn_charts': 'Abrir Barchart COT', 'status_ready': 'Listo para el análisis', 'status_download': 'Descargando datos del informe Legacy CFTC...', 'status_success': '¡Análisis completado con éxito!', 'error_prefix': 'Error durante la ejecución: ', 'report_header': 'INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE', 'screening_header': 'SELECCIÓN ESTRATÉGICA Y CRUCES DE DIVISAS / COMMODITIES', 'cat_valute': 'MONEDAS', 'cat_grains': 'MATERIAS PRIMAS - GRAINS', 'cat_metalli': 'METALES', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGÍAS', 'cat_indici': 'INDICES', 'sig_valute': '--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---', 'sec_cross': '--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---', 'sec_commodities': '--- MATERIAS PRIMAS ---', 'sec_indices': '--- ÍNDICES BURSÁTILES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f}).'}, 'Deutsch': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Analyse Starten', 'btn_charts': 'Barchart COT Öffnen', 'status_ready': 'Bereit für die Analyse', 'status_download': 'Daten aus dem CFTC Legacy Report werden heruntergeladen...', 'status_success': 'Analyse erfolgreich abgeschlossen!', 'error_prefix': 'Fehler bei der Ausführung: ', 'report_header': 'COT BERICHT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE', 'screening_header': 'STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN / COMMODITIES', 'cat_valute': 'WÄHRUNGEN', 'cat_grains': 'ROHSTOFFE - GRAINS', 'cat_metalli': 'METALLE', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIE', 'cat_indici': 'INDIZES', 'sig_valute': '--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---', 'sec_cross': '--- DYNAMISCHE ANALYSE DER HAUPTKREUZUNGEN ---', 'sec_commodities': '--- ROHSTOFFE & KORRELATION ---', 'sec_indices': '--- AKTIENINDIZES ---', 'cross_long': '-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f}).'}, 'Français': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': "Lancer l'analyse", 'btn_charts': 'Ouvrir Barchart COT', 'status_ready': "Prêt pour l'analyse", 'status_download': 'Téléchargement des données du rapport Legacy CFTC...', 'status_success': 'Analyse terminée avec succès !', 'error_prefix': "Erreur lors de l'exécution : ", 'report_header': 'RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE', 'screening_header': 'SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES / COMMODITIES', 'cat_valute': 'DEVISES', 'cat_grains': 'MATIÈRES PREMIÈRES - GRAINS', 'cat_metalli': 'MÉTAUX', 'cat_softs': 'SOFTS', 'cat_energies': 'ÉNERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---', 'sec_cross': '--- ANALYSE DYNAMIQUE DES CROISEMENTS MAJEURS ---', 'sec_commodities': '--- MATIÈRES PREMIÈRES & CORRÉLATION ---', 'sec_indices': '--- INDICES BOURSIERS ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f}).'}}
BARCHART_LINKS = {'SWISS FRANC': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0', 'USD INDEX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0', 'MEXICAN PESO': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0', 'NZ DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0', 'CANADIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0', 'BRAZILIAN REAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0', 'SOUTH AFRICAN RAND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0', 'BRITISH POUND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0', 'JAPANESE YEN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0', 'EURO FX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0', 'AUSTRALIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0', 'CORN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0', 'SOYBEANS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0', 'SOYBEAN OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0', 'SOYBEAN MEAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0', 'WHEAT-SRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0', 'WHEAT-HRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0', 'WHEAT-SPRING': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0', 'ROUGH RICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0', 'CANOLA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0', 'GOLD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0', 'SILVER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0', 'COPPER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0', 'PALLADIUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0', 'PLATINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0', 'ALUMINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0', 'COCOA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0', 'COTTON': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0', 'COFFEE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0', 'SUGAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0', 'ORANGE JUICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0', 'LUMBER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0', 'CRUDE OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0', 'GASOLINE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0', 'NY HARBOR ULSD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0', 'NATURAL GAS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0', 'ETHANOL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0', 'S&P 500': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0', 'NASDAQ-100': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0', 'DOW JONES': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0', 'RUSSELL 2000': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0', 'VIX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0'}

def main(page: ft.Page):
    try:
        page.title = 'CFTC COT Analyzer PRO'
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20
        _0x0ca767 = ft.Text('CFTC COT Analyzer PRO', size=22, weight=ft.FontWeight.BOLD, color='white')
        _0xb41d80 = ft.Text("Pronto per l'analisi", size=13, color='green')
        _0x0be357 = ft.ProgressRing(visible=False, width=20, height=20)
        _0x230e53 = ft.Column(spacing=2)
        _0xc3b61c = ft.Container(content=_0x230e53, padding=ft.padding.only(bottom=100))
        _0xe522f1 = ft.Row([_0xc3b61c], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        def change_language(_0x7729d0):
            _0xe16536 = TRANSLATIONS[_0xc4e660.value]
            _0x0ca767.value = _0xe16536['title']
            _0xc5c92b.text = _0xe16536['btn_ready']
            _0xf701a0.text = _0xe16536['btn_charts']
            _0xb41d80.value = _0xe16536['status_ready']
            page.update()
        _0xc4e660 = ft.Dropdown(label='Language / Lingua', value='Italiano', options=[ft.dropdown.Option(_0xfdd79c) for _0xfdd79c in TRANSLATIONS.keys()], on_change=change_language, width=180, text_size=12, label_style=ft.TextStyle(size=12))

        def open_charts(_0x7729d0):
            page.launch_url('https://www.barchart.com/futures/commitment-of-traders')

        def run_analysis(_0x7729d0):
            _0xe16536 = TRANSLATIONS[_0xc4e660.value]
            _0xb41d80.value = _0xe16536['status_download']
            _0x0be357.visible = True
            _0x230e53.controls.clear()
            page.update()
            try:
                _0x91ad40 = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                _0xe6bfae = urllib.request.Request(_0x91ad40, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(_0xe6bfae, timeout=15) as _0xa4e769:
                    _0x7e1341 = _0xa4e769.read().decode('utf-8', errors='ignore')
                _0x8b61c8 = io.StringIO(_0x7e1341)
                _0x4a3df3 = csv.reader(_0x8b61c8)
                _0xe16799 = list(_0x4a3df3)
                _0xf9d623 = {_0xe16536['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], _0xe16536['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], _0xe16536['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], _0xe16536['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], _0xe16536['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], _0xe16536['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']}
                _0xb24178 = []
                _0xe8ba90 = {}
                for _0x783c8b, _0x2b1378 in _0xf9d623.items():
                    _0xb24178.append((_0x783c8b, 'HEADER'))
                    for _0x7cb940 in _0x2b1378:
                        for _0x4fa265 in _0xe16799:
                            if not _0x4fa265 or len(_0x4fa265) < 40:
                                continue
                            _0xdc9f20 = str(_0x4fa265[0]).strip()
                            if _0x7cb940.upper() in _0xdc9f20.upper():
                                try:
                                    _0x0ad1e2 = float(_0x4fa265[7]) if _0x4fa265[7].strip() and float(_0x4fa265[7]) > 0 else 1
                                    _0x8d5182 = float(_0x4fa265[8]) if _0x4fa265[8].strip() else 0
                                    _0xdd3436 = float(_0x4fa265[9]) if _0x4fa265[9].strip() else 0
                                    _0x796aa0 = int(float(_0x4fa265[38])) if _0x4fa265[38].strip() else 0
                                    _0x1bf8f6 = int(float(_0x4fa265[39])) if _0x4fa265[39].strip() else 0
                                    _0x91b743 = _0x8d5182 / _0x0ad1e2 * 100
                                    _0x17e8a7 = _0xdd3436 / _0x0ad1e2 * 100
                                    _0xdab56d = _0x8d5182 - _0x796aa0
                                    _0xb0a516 = _0xdd3436 - _0x1bf8f6
                                    _0x776fbd = _0x796aa0 / _0xdab56d * 100 if _0xdab56d > 0 else 0
                                    _0xe21bf0 = _0x1bf8f6 / _0xb0a516 * 100 if _0xb0a516 > 0 else 0
                                    _0x5a5a7d = _0x91b743 + _0x776fbd / 10.0
                                    _0xef4e26 = _0x17e8a7 + _0xe21bf0 / 10.0
                                    _0xa11381 = _0x5a5a7d - _0xef4e26
                                    if _0xa11381 > 15:
                                        _0x551d85 = 'STRONG LONG'
                                    elif _0xa11381 > 5:
                                        _0x551d85 = 'MODERATE LONG'
                                    elif _0xa11381 < -15:
                                        _0x551d85 = 'STRONG SHORT'
                                    elif _0xa11381 < -5:
                                        _0x551d85 = 'MODERATE SHORT'
                                    else:
                                        _0x551d85 = 'NEUTRAL'
                                    _0x931a72 = f'{_0xdc9f20[:32]:<34} | Long: {_0x91b743:5.1f}% ({_0x796aa0:+6d} ctr) | Short: {_0x17e8a7:5.1f}% ({_0x1bf8f6:+6d} ctr) | Net Slope: {_0xa11381:+6.1f} [{_0x551d85}]'
                                    _0xb24178.append((_0x931a72, 'MARKET', _0x7cb940.upper()))
                                    _0xf8cd0d = _0x7cb940.upper()
                                    _0xe8ba90[_0xf8cd0d] = {'name': _0xdc9f20, 'pct_long': _0x91b743, 'pct_short': _0x17e8a7, 'chg_long': _0x796aa0, 'chg_short': _0x1bf8f6, 'net_slope': _0xa11381}
                                    break
                                except Exception:
                                    pass
                _0x5d0f86 = []
                _0x280461 = {'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'}
                _0xcc27ca = {}
                for _0x60364b, _0x5718f9 in _0x280461.items():
                    if _0x60364b in _0xe8ba90:
                        _0xcc27ca[_0x5718f9] = _0xe8ba90[_0x60364b]['net_slope']
                _0x6b9f88 = _0xc2b7e9(_0xcc27ca.items(), key=lambda _0x7c9711: _0x7c9711[1], reverse=True)
                _0x5d0f86.append((_0xe16536['sig_valute'], 'SUBHEADER'))
                if len(_0x6b9f88) >= 2:
                    _0x5d0f86.append((f'-> [TOP SETUP ABS] {_0x6b9f88[0][0]}/{_0x6b9f88[-1][0]} | Max div ({_0x6b9f88[0][0]}: {_0x6b9f88[0][1]:+.1f} vs {_0x6b9f88[-1][0]}: {_0x6b9f88[-1][1]:+.1f})', 'TEXT'))
                _0x22636c = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                _0x5d0f86.append((_0xe16536['sec_cross'], 'SUBHEADER'))
                for _0xc36c42, _0xf689de in _0x22636c:
                    if _0xc36c42 in _0xcc27ca and _0xf689de in _0xcc27ca:
                        _0x414aeb, _0xc363d1 = (_0xcc27ca[_0xc36c42], _0xcc27ca[_0xf689de])
                        _0xe9f860 = _0x414aeb - _0xc363d1
                        if _0xe9f860 > 10:
                            _0x5d0f86.append((_0xe16536['cross_long'].format(base=_0xc36c42, quote=_0xf689de, s_base=_0x414aeb, s_quote=_0xc363d1), 'TEXT'))
                        elif _0xe9f860 < -10:
                            _0x5d0f86.append((_0xe16536['cross_short'].format(base=_0xc36c42, quote=_0xf689de, s_base=_0x414aeb, s_quote=_0xc363d1), 'TEXT'))
                _0x5d0f86.append((_0xe16536['sec_commodities'], 'SUBHEADER'))
                _0xbd5880 = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                _0x4be466 = _0xcc27ca.get('USD', 0)
                for _0xf6ee4d in _0xbd5880:
                    _0x56f3bb = _0xe8ba90.get(_0xf6ee4d)
                    if _0x56f3bb:
                        _0x75b073 = _0x56f3bb['name'].split('-')[0].strip()
                        _0xed1733 = _0x56f3bb['net_slope']
                        if _0x56f3bb['pct_short'] > 60 and _0x56f3bb['chg_short'] < 0:
                            _0x5d0f86.append((_0xe16536['comm_squeeze'].format(name=_0x75b073, slope=_0xed1733), 'TEXT'))
                        elif _0xed1733 > 15 and _0x4be466 < 0:
                            _0x5d0f86.append((_0xe16536['comm_bullish'].format(name=_0x75b073, slope=_0xed1733), 'TEXT'))
                        elif _0xed1733 < -15 and _0x4be466 > 0:
                            _0x5d0f86.append((_0xe16536['comm_bearish'].format(name=_0x75b073, slope=_0xed1733), 'TEXT'))
                _0x230e53.controls.append(ft.Text(_0xe16536['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0x230e53.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0x7f9c97 in _0xb24178:
                    if _0x7f9c97[1] == 'HEADER':
                        _0x230e53.controls.append(ft.Text(f'\n--- {_0x7f9c97[0]} ---', weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        _0xf4dff7 = _0x7f9c97[0]
                        _0xaf4ee8 = _0x7f9c97[2]
                        _0x0e33b2 = BARCHART_LINKS.get(_0xaf4ee8, 'https://www.barchart.com/futures/commitment-of-traders')
                        _0x230e53.controls.append(ft.TextButton(content=ft.Text(_0xf4dff7, font_family='monospace', size=11, color='white'), on_click=lambda _0x7729d0, _0x299ab4=_0x0e33b2: page.launch_url(_0x299ab4), style=ft.ButtonStyle(padding=0)))
                _0x230e53.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                _0x230e53.controls.append(ft.Text(_0xe16536['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0x230e53.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0x97b4ca, _0xc428bf in _0x5d0f86:
                    if _0xc428bf == 'SUBHEADER':
                        _0x230e53.controls.append(ft.Text(f'\n{_0x97b4ca}', weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        _0x230e53.controls.append(ft.Text(_0x97b4ca, size=11, color='white70'))
                _0xb41d80.value = _0xe16536['status_success']
            except Exception as ex:
                _0xb41d80.value = f"Errore durante l'esecuzione: {_0xedcdfa}"
            _0x0be357.visible = False
            page.update()
        _0xba87df = TRANSLATIONS['Italiano']
        _0xc5c92b = ft.ElevatedButton(_0xba87df['btn_ready'], on_click=run_analysis, bgcolor='blue', color='white')
        _0xf701a0 = ft.ElevatedButton(_0xba87df['btn_charts'], on_click=open_charts, bgcolor='green', color='white')
        page.add(_0x0ca767, _0xc4e660, ft.Divider(height=15, color='white24'), _0xb41d80, ft.Container(height=5), ft.Row([_0xc5c92b, _0xf701a0, _0x0be357], alignment=ft.MainAxisAlignment.START, spacing=10), ft.Divider(height=15, color='white24'), _0xe522f1)
    except Exception as initialization_error:
        page.clean()
        page.add(ft.Text('ERRORE CRITICO DI AVVIO:', size=18, color='red', weight=ft.FontWeight.BOLD), ft.Text(str(_0x5beef6), size=14, color='white'))
        page.update()
if __name__ == '__main__':
    ft.app(target=main)
if __name__ == '__main__':
    ft.app(target=main)
