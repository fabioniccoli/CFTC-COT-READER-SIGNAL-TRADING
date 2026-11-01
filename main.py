# Protected by PurePython Obfuscator
import flet as ft
import urllib.request
import csv
import io
TRANSLATIONS = {'Italiano': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Avvia Analisi', 'btn_charts': 'Apri Barchart COT', 'status_ready': "Pronto per l'analisi", 'status_download': 'Scaricamento dei dati dal report Legacy CFTC...', 'status_success': 'Analisi completata con successo!', 'error_prefix': "Errore durante l'esecuzione: ", 'report_header': 'REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE', 'screening_header': 'SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES', 'cat_valute': 'VALUTE', 'cat_grains': 'MATERIE PRIME - GRAINS', 'cat_metalli': 'METALLI', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICI', 'sig_valute': '--- INCROCI VALUTARI (Forza Relativa Universale) ---', 'sec_cross': '--- ANALISI DINAMICA CROSS PRINCIPALI ---', 'sec_commodities': '--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---', 'sec_indices': '--- INDICI AZIONARI ---', 'cross_long': '-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).'}, 'English': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Start Analysis', 'btn_charts': 'Open Barchart COT', 'status_ready': 'Ready for analysis', 'status_download': 'Downloading data from CFTC Legacy report...', 'status_success': 'Analysis completed successfully!', 'error_prefix': 'Execution error: ', 'report_header': 'COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE', 'screening_header': 'STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES', 'cat_valute': 'CURRENCIES', 'cat_grains': 'COMMODITIES - GRAINS', 'cat_metalli': 'METALS', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CURRENCY CROSSES (Universal Relative Strength) ---', 'sec_cross': '--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---', 'sec_commodities': '--- COMMODITIES & CORRELATION ---', 'sec_indices': '--- STOCK INDICES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).'}, 'Español': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Iniciar Análisis', 'btn_charts': 'Abrir Barchart COT', 'status_ready': 'Listo para el análisis', 'status_download': 'Descargando datos del informe Legacy CFTC...', 'status_success': '¡Análisis completado con éxito!', 'error_prefix': 'Error durante la ejecución: ', 'report_header': 'INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE', 'screening_header': 'SELECCIÓN ESTRATÉGICA Y CRUCES DE DIVISAS / COMMODITIES', 'cat_valute': 'MONEDAS', 'cat_grains': 'MATERIAS PRIMAS - GRAINS', 'cat_metalli': 'METALES', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGÍAS', 'cat_indici': 'INDICES', 'sig_valute': '--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---', 'sec_cross': '--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---', 'sec_commodities': '--- MATERIAS PRIMAS ---', 'sec_indices': '--- ÍNDICES BURSÁTILES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f}).'}, 'Deutsch': {'title': 'CFTC COT Analyzer', 'btn_ready': 'Analyse Starten', 'btn_charts': 'Barchart COT Öffnen', 'status_ready': 'Bereit für die Analyse', 'status_download': 'Daten aus dem CFTC Legacy Report werden heruntergeladen...', 'status_success': 'Analyse erfolgreich abgeschlossen!', 'error_prefix': 'Fehler bei der Ausführung: ', 'report_header': 'COT BERICHT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE', 'screening_header': 'STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN / COMMODITIES', 'cat_valute': 'WÄHRUNGEN', 'cat_grains': 'ROHSTOFFE - GRAINS', 'cat_metalli': 'METALLE', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIE', 'cat_indici': 'INDIZES', 'sig_valute': '--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---', 'sec_cross': '--- DYNAMISCHE ANALYSE DER HAUPTKREUZUNGEN ---', 'sec_commodities': '--- ROHSTOFFE & KORRELATION ---', 'sec_indices': '--- AKTIENINDIZES ---', 'cross_long': '-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f}).'}, 'Français': {'title': 'CFTC COT Analyzer', 'btn_ready': "Lancer l'analyse", 'btn_charts': 'Ouvrir Barchart COT', 'status_ready': "Prêt pour l'analyse", 'status_download': 'Téléchargement des données du rapport Legacy CFTC...', 'status_success': 'Analyse terminée avec succès !', 'error_prefix': "Erreur lors de l'exécution : ", 'report_header': 'RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE', 'screening_header': 'SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES / COMMODITIES', 'cat_valute': 'DEVISES', 'cat_grains': 'MATIÈRES PREMIÈRES - GRAINS', 'cat_metalli': 'MÉTAUX', 'cat_softs': 'SOFTS', 'cat_energies': 'ÉNERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---', 'sec_cross': '--- ANALYSE DYNAMIQUE DES CROISEMENTS MAJEURS ---', 'sec_commodities': '--- MATIÈRES PREMIÈRES & CORRÉLATION ---', 'sec_indices': '--- INDICES BOURSIERS ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f}).'}}
BARCHART_LINKS = {'SWISS FRANC': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0', 'USD INDEX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0', 'MEXICAN PESO': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0', 'NZ DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0', 'CANADIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0', 'BRAZILIAN REAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0', 'SOUTH AFRICAN RAND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0', 'BRITISH POUND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0', 'JAPANESE YEN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0', 'EURO FX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0', 'AUSTRALIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0', 'CORN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0', 'SOYBEANS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0', 'SOYBEAN OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0', 'SOYBEAN MEAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0', 'WHEAT-SRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0', 'WHEAT-HRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0', 'WHEAT-SPRING': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0', 'ROUGH RICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0', 'CANOLA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0', 'GOLD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0', 'SILVER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0', 'COPPER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0', 'PALLADIUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0', 'PLATINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0', 'ALUMINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0', 'COCOA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0', 'COTTON': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0', 'COFFEE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0', 'SUGAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0', 'ORANGE JUICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0', 'LUMBER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0', 'CRUDE OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0', 'GASOLINE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0', 'NY HARBOR ULSD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0', 'NATURAL GAS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0', 'ETHANOL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0', 'S&P 500': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0', 'NASDAQ-100': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0', 'DOW JONES': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0', 'RUSSELL 2000': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0', 'VIX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0'}

def main(page: ft.Page):
    try:
        page.title = 'CFTC COT Analyzer'
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20
        _0x6ff4be = 'Italiano'
        _0x5e36fb = TRANSLATIONS[_0x6ff4be]
        _0xfb13f0 = ft.Text(_0x5e36fb['title'], size=22, weight=ft.FontWeight.BOLD, color='white')

        def change_language(_0x6019b8):
            nonlocal current_lang, t
            _0x6ff4be = _0x8a42a2.value
            _0x5e36fb = TRANSLATIONS[_0x6ff4be]
            _0xfb13f0.value = _0x5e36fb['title']
            _0xddef68.text = _0x5e36fb['btn_ready']
            _0x287fb1.text = _0x5e36fb['btn_charts']
            _0xd90943.value = _0x5e36fb['status_ready']
            page.update()
        _0x8a42a2 = ft.Dropdown(label='Language / Lingua', value='Italiano', options=[ft.dropdown.Option(_0x28b497) for _0x28b497 in TRANSLATIONS.keys()], on_change=change_language, width=180, text_size=12, label_style=ft.TextStyle(size=12))
        _0xd90943 = ft.Text(_0x5e36fb['status_ready'], size=13, color='green')
        _0x87c3da = ft.ProgressRing(visible=False, width=20, height=20)
        _0xdec002 = ft.Column(spacing=2)
        _0xaf4b5f = ft.Container(content=_0xdec002, padding=ft.padding.only(bottom=100))
        _0x2499b7 = ft.Row([_0xaf4b5f], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        def open_charts(_0x6019b8):
            page.launch_url('https://www.barchart.com/futures/commitment-of-traders')

        def run_analysis(_0x6019b8):
            _0xd90943.value = _0x5e36fb['status_download']
            _0x87c3da.visible = True
            _0xdec002.controls.clear()
            page.update()
            try:
                _0x5771d1 = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                _0x9d6f96 = urllib.request.Request(_0x5771d1, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(_0x9d6f96, timeout=15) as _0xa9a6ca:
                    _0x893e76 = _0xa9a6ca.read().decode('utf-8', errors='ignore')
                _0x0280ba = io.StringIO(_0x893e76)
                _0xad6668 = csv.reader(_0x0280ba)
                _0xfd2034 = list(_0xad6668)
                _0xc6ae27 = {_0x5e36fb['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], _0x5e36fb['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], _0x5e36fb['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], _0x5e36fb['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], _0x5e36fb['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], _0x5e36fb['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']}
                _0xc0bc55 = []
                _0x364831 = {}
                for _0xf51752, _0xae9f35 in _0xc6ae27.items():
                    _0xc0bc55.append((_0xf51752, 'HEADER'))
                    for _0x6afab2 in _0xae9f35:
                        for _0xdadf75 in _0xfd2034:
                            if not _0xdadf75 or len(_0xdadf75) < 40:
                                continue
                            _0xa5fe0d = str(_0xdadf75[0]).strip()
                            if _0x6afab2.upper() in _0xa5fe0d.upper():
                                try:
                                    _0x70f358 = float(_0xdadf75[7]) if _0xdadf75[7].strip() and float(_0xdadf75[7]) > 0 else 1
                                    _0x0f2565 = float(_0xdadf75[8]) if _0xdadf75[8].strip() else 0
                                    _0xa51005 = float(_0xdadf75[9]) if _0xdadf75[9].strip() else 0
                                    _0xeb932f = int(float(_0xdadf75[38])) if _0xdadf75[38].strip() else 0
                                    _0xc15bc6 = int(float(_0xdadf75[39])) if _0xdadf75[39].strip() else 0
                                    _0x01ff03 = _0x0f2565 / _0x70f358 * 100
                                    _0x14e6ab = _0xa51005 / _0x70f358 * 100
                                    _0x535079 = _0x0f2565 - _0xeb932f
                                    _0xdbb76b = _0xa51005 - _0xc15bc6
                                    _0x959eed = _0xeb932f / _0x535079 * 100 if _0x535079 > 0 else 0
                                    _0xd429bb = _0xc15bc6 / _0xdbb76b * 100 if _0xdbb76b > 0 else 0
                                    _0x026431 = _0x01ff03 + _0x959eed / 10.0
                                    _0x06026f = _0x14e6ab + _0xd429bb / 10.0
                                    _0x5c55b2 = _0x026431 - _0x06026f
                                    if _0x5c55b2 > 15:
                                        _0xc6f13c = 'STRONG LONG'
                                    elif _0x5c55b2 > 5:
                                        _0xc6f13c = 'MODERATE LONG'
                                    elif _0x5c55b2 < -15:
                                        _0xc6f13c = 'STRONG SHORT'
                                    elif _0x5c55b2 < -5:
                                        _0xc6f13c = 'MODERATE SHORT'
                                    else:
                                        _0xc6f13c = 'NEUTRAL'
                                    _0x120d82 = f'{_0xa5fe0d[:32]:<34} | Long: {_0x01ff03:5.1f}% ({_0xeb932f:+6d} ctr) | Short: {_0x14e6ab:5.1f}% ({_0xc15bc6:+6d} ctr) | Net Slope: {_0x5c55b2:+6.1f} [{_0xc6f13c}]'
                                    _0xc0bc55.append((_0x120d82, 'MARKET', _0x6afab2.upper()))
                                    _0xce63fc = _0x6afab2.upper()
                                    _0x364831[_0xce63fc] = {'name': _0xa5fe0d, 'pct_long': _0x01ff03, 'pct_short': _0x14e6ab, 'chg_long': _0xeb932f, 'chg_short': _0xc15bc6, 'net_slope': _0x5c55b2}
                                    break
                                except Exception:
                                    pass
                _0xfb15a7 = []
                _0x49df21 = {'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'}
                _0x6658b8 = {}
                for _0x97cdc3, _0x273e2a in _0x49df21.items():
                    if _0x97cdc3 in _0x364831:
                        _0x6658b8[_0x273e2a] = _0x364831[_0x97cdc3]['net_slope']
                _0x2a8606 = _0x8e72ef(_0x6658b8.items(), key=lambda _0xff071d: _0xff071d[1], reverse=True)
                _0xfb15a7.append((_0x5e36fb['sig_valute'], 'SUBHEADER'))
                if len(_0x2a8606) >= 2:
                    _0xfb15a7.append((f'-> [TOP SETUP ABS] {_0x2a8606[0][0]}/{_0x2a8606[-1][0]} | Max div ({_0x2a8606[0][0]}: {_0x2a8606[0][1]:+.1f} vs {_0x2a8606[-1][0]}: {_0x2a8606[-1][1]:+.1f})', 'TEXT'))
                _0x1ef103 = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                _0xfb15a7.append((_0x5e36fb['sec_cross'], 'SUBHEADER'))
                for _0xfa9c5f, _0x6eafa9 in _0x1ef103:
                    if _0xfa9c5f in _0x6658b8 and _0x6eafa9 in _0x6658b8:
                        _0x2d420e, _0x8e77fc = (_0x6658b8[_0xfa9c5f], _0x6658b8[_0x6eafa9])
                        _0xbafd8a = _0x2d420e - _0x8e77fc
                        if _0xbafd8a > 10:
                            _0xfb15a7.append((_0x5e36fb['cross_long'].format(base=_0xfa9c5f, quote=_0x6eafa9, s_base=_0x2d420e, s_quote=_0x8e77fc), 'TEXT'))
                        elif _0xbafd8a < -10:
                            _0xfb15a7.append((_0x5e36fb['cross_short'].format(base=_0xfa9c5f, quote=_0x6eafa9, s_base=_0x2d420e, s_quote=_0x8e77fc), 'TEXT'))
                _0xfb15a7.append((_0x5e36fb['sec_commodities'], 'SUBHEADER'))
                _0xd0197c = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                _0x382cb6 = _0x6658b8.get('USD', 0)
                for _0xb66626 in _0xd0197c:
                    _0xd8c68b = _0x364831.get(_0xb66626)
                    if _0xd8c68b:
                        _0x1c857d = _0xd8c68b['name'].split('-')[0].strip()
                        _0x86318b = _0xd8c68b['net_slope']
                        if _0xd8c68b['pct_short'] > 60 and _0xd8c68b['chg_short'] < 0:
                            _0xfb15a7.append((_0x5e36fb['comm_squeeze'].format(name=_0x1c857d, slope=_0x86318b), 'TEXT'))
                        elif _0x86318b > 15 and _0x382cb6 < 0:
                            _0xfb15a7.append((_0x5e36fb['comm_bullish'].format(name=_0x1c857d, slope=_0x86318b), 'TEXT'))
                        elif _0x86318b < -15 and _0x382cb6 > 0:
                            _0xfb15a7.append((_0x5e36fb['comm_bearish'].format(name=_0x1c857d, slope=_0x86318b), 'TEXT'))
                _0xdec002.controls.append(ft.Text(_0x5e36fb['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xdec002.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0xb9e4de in _0xc0bc55:
                    if _0xb9e4de[1] == 'HEADER':
                        _0xdec002.controls.append(ft.Text(f'\n--- {_0xb9e4de[0]} ---', weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        _0xdc736e = _0xb9e4de[0]
                        _0xe75b11 = _0xb9e4de[2]
                        _0xa95ab6 = BARCHART_LINKS.get(_0xe75b11, 'https://www.barchart.com/futures/commitment-of-traders')
                        _0xdec002.controls.append(ft.TextButton(content=ft.Text(_0xdc736e, font_family='monospace', size=11, color='white'), on_click=lambda _0x6019b8, _0xb0b089=_0xa95ab6: page.launch_url(_0xb0b089), style=ft.ButtonStyle(padding=0)))
                _0xdec002.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                _0xdec002.controls.append(ft.Text(_0x5e36fb['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xdec002.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0x72fe6f, _0x2e4cb6 in _0xfb15a7:
                    if _0x2e4cb6 == 'SUBHEADER':
                        _0xdec002.controls.append(ft.Text(f'\n{_0x72fe6f}', weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        _0xdec002.controls.append(ft.Text(_0x72fe6f, size=11, color='white70'))
                _0xd90943.value = _0x5e36fb['status_success']
            except Exception as ex:
                _0xd90943.value = f"{_0x5e36fb['error_prefix']}{_0x042cad}"
            _0x87c3da.visible = False
            page.update()
        _0xddef68 = ft.ElevatedButton(_0x5e36fb['btn_ready'], on_click=run_analysis, bgcolor='blue', color='white')
        _0x287fb1 = ft.ElevatedButton(_0x5e36fb['btn_charts'], on_click=open_charts, bgcolor='green', color='white')
        page.add(_0xfb13f0, _0x8a42a2, ft.Divider(height=15, color='white24'), _0xd90943, ft.Container(height=5), ft.Row([_0xddef68, _0x287fb1, _0x87c3da], alignment=ft.MainAxisAlignment.START, spacing=10), ft.Divider(height=15, color='white24'), _0x2499b7)
    except Exception as initialization_error:
        page.clean()
        page.add(ft.Text('ERRORE CRITICO DI AVVIO:', size=18, color='red', weight=ft.FontWeight.BOLD), ft.Text(str(_0x995247), size=14, color='white'))
        page.update()
if __name__ == '__main__':
    ft.app(target=main)
