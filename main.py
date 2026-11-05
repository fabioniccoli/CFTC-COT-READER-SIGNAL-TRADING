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
        _0x59af68 = ft.Text('CFTC COT Analyzer PRO', size=22, weight=ft.FontWeight.BOLD, color='white')
        _0x83049c = ft.Text("Pronto per l'analisi", size=13, color='green')
        _0x206e6c = ft.ProgressRing(visible=False, width=20, height=20)
        _0xbb4451 = ft.Column(spacing=2)
        _0x5c6a17 = ft.Container(content=_0xbb4451, padding=ft.padding.only(bottom=100))
        _0x34dab4 = ft.Row([_0x5c6a17], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        def change_language(_0x0f4ae6):
            _0xc06cbb = TRANSLATIONS[_0xe4d8ff.value]
            _0x59af68.value = _0xc06cbb['title']
            _0x0d3d48.text = _0xc06cbb['btn_ready']
            _0xe3b5e0.text = _0xc06cbb['btn_charts']
            _0x83049c.value = _0xc06cbb['status_ready']
            page.update()
        _0xe4d8ff = ft.Dropdown(label='Language / Lingua', value='Italiano', options=[ft.dropdown.Option(_0xe887fe) for _0xe887fe in TRANSLATIONS.keys()], on_change=change_language, width=180, text_size=12, label_style=ft.TextStyle(size=12))

        def open_charts(_0x0f4ae6):
            page.launch_url('https://www.barchart.com/futures/commitment-of-traders')

        def run_analysis(_0x0f4ae6):
            _0xc06cbb = TRANSLATIONS[_0xe4d8ff.value]
            _0x83049c.value = _0xc06cbb['status_download']
            _0x206e6c.visible = True
            _0xbb4451.controls.clear()
            page.update()
            try:
                _0x0e9298 = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                _0x5f5183 = urllib.request.Request(_0x0e9298, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(_0x5f5183, timeout=15) as _0x944407:
                    _0x7a2c18 = _0x944407.read().decode('utf-8', errors='ignore')
                _0x093b46 = io.StringIO(_0x7a2c18)
                _0x25a5a5 = csv.reader(_0x093b46)
                _0xa0dd03 = list(_0x25a5a5)
                _0x438210 = {_0xc06cbb['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], _0xc06cbb['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], _0xc06cbb['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], _0xc06cbb['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], _0xc06cbb['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], _0xc06cbb['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']}
                _0xfda54f = []
                _0xc55543 = {}
                for _0x6af8f5, _0xb2b3e4 in _0x438210.items():
                    _0xfda54f.append((_0x6af8f5, 'HEADER'))
                    for _0x35fb55 in _0xb2b3e4:
                        for _0x9c3660 in _0xa0dd03:
                            if not _0x9c3660 or len(_0x9c3660) < 40:
                                continue
                            _0xe2915b = str(_0x9c3660[0]).strip()
                            if _0x35fb55.upper() in _0xe2915b.upper():
                                try:
                                    _0xc62188 = float(_0x9c3660[7]) if _0x9c3660[7].strip() and float(_0x9c3660[7]) > 0 else 1
                                    _0x40a914 = float(_0x9c3660[8]) if _0x9c3660[8].strip() else 0
                                    _0x073cc2 = float(_0x9c3660[9]) if _0x9c3660[9].strip() else 0
                                    _0x71f460 = int(float(_0x9c3660[38])) if _0x9c3660[38].strip() else 0
                                    _0x995d61 = int(float(_0x9c3660[39])) if _0x9c3660[39].strip() else 0
                                    _0xe24012 = _0x40a914 / _0xc62188 * 100
                                    _0x93d901 = _0x073cc2 / _0xc62188 * 100
                                    _0x7c2ec6 = _0x40a914 - _0x71f460
                                    _0x731867 = _0x073cc2 - _0x995d61
                                    _0x7e8fbd = _0x71f460 / _0x7c2ec6 * 100 if _0x7c2ec6 > 0 else 0
                                    _0xde027a = _0x995d61 / _0x731867 * 100 if _0x731867 > 0 else 0
                                    _0x3d0de9 = _0xe24012 + _0x7e8fbd / 10.0
                                    _0xf93c2f = _0x93d901 + _0xde027a / 10.0
                                    _0xb72ff0 = _0x3d0de9 - _0xf93c2f
                                    if _0xb72ff0 > 15:
                                        _0x5b09c3 = 'STRONG LONG'
                                    elif _0xb72ff0 > 5:
                                        _0x5b09c3 = 'MODERATE LONG'
                                    elif _0xb72ff0 < -15:
                                        _0x5b09c3 = 'STRONG SHORT'
                                    elif _0xb72ff0 < -5:
                                        _0x5b09c3 = 'MODERATE SHORT'
                                    else:
                                        _0x5b09c3 = 'NEUTRAL'
                                    _0x8ba4a4 = f'{_0xe2915b[:32]:<34} | Long: {_0xe24012:5.1f}% ({_0x71f460:+6d} ctr) | Short: {_0x93d901:5.1f}% ({_0x995d61:+6d} ctr) | Net Slope: {_0xb72ff0:+6.1f} [{_0x5b09c3}]'
                                    _0xfda54f.append((_0x8ba4a4, 'MARKET', _0x35fb55.upper()))
                                    _0xea38f4 = _0x35fb55.upper()
                                    _0xc55543[_0xea38f4] = {'name': _0xe2915b, 'pct_long': _0xe24012, 'pct_short': _0x93d901, 'chg_long': _0x71f460, 'chg_short': _0x995d61, 'net_slope': _0xb72ff0}
                                    break
                                except Exception:
                                    pass
                _0x40f23c = []
                _0xc21e08 = {'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'}
                _0x355612 = {}
                for _0x63387a, _0xfabf09 in _0xc21e08.items():
                    if _0x63387a in _0xc55543:
                        _0x355612[_0xfabf09] = _0xc55543[_0x63387a]['net_slope']
                _0xa466da = _0xff26ef(_0x355612.items(), key=lambda _0xd7da72: _0xd7da72[1], reverse=True)
                _0x40f23c.append((_0xc06cbb['sig_valute'], 'SUBHEADER'))
                if len(_0xa466da) >= 2:
                    _0x40f23c.append((f'-> [TOP SETUP ABS] {_0xa466da[0][0]}/{_0xa466da[-1][0]} | Max div ({_0xa466da[0][0]}: {_0xa466da[0][1]:+.1f} vs {_0xa466da[-1][0]}: {_0xa466da[-1][1]:+.1f})', 'TEXT'))
                _0xa05a48 = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                _0x40f23c.append((_0xc06cbb['sec_cross'], 'SUBHEADER'))
                for _0x718d34, _0x357cab in _0xa05a48:
                    if _0x718d34 in _0x355612 and _0x357cab in _0x355612:
                        _0x0b28a9, _0x5cd9c7 = (_0x355612[_0x718d34], _0x355612[_0x357cab])
                        _0x559e06 = _0x0b28a9 - _0x5cd9c7
                        if _0x559e06 > 10:
                            _0x40f23c.append((_0xc06cbb['cross_long'].format(base=_0x718d34, quote=_0x357cab, s_base=_0x0b28a9, s_quote=_0x5cd9c7), 'TEXT'))
                        elif _0x559e06 < -10:
                            _0x40f23c.append((_0xc06cbb['cross_short'].format(base=_0x718d34, quote=_0x357cab, s_base=_0x0b28a9, s_quote=_0x5cd9c7), 'TEXT'))
                _0x40f23c.append((_0xc06cbb['sec_commodities'], 'SUBHEADER'))
                _0xe46286 = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                _0xabf819 = _0x355612.get('USD', 0)
                for _0x0346fd in _0xe46286:
                    _0x3017be = _0xc55543.get(_0x0346fd)
                    if _0x3017be:
                        _0x89c0a7 = _0x3017be['name'].split('-')[0].strip()
                        _0xaf6906 = _0x3017be['net_slope']
                        if _0x3017be['pct_short'] > 60 and _0x3017be['chg_short'] < 0:
                            _0x40f23c.append((_0xc06cbb['comm_squeeze'].format(name=_0x89c0a7, slope=_0xaf6906), 'TEXT'))
                        elif _0xaf6906 > 15 and _0xabf819 < 0:
                            _0x40f23c.append((_0xc06cbb['comm_bullish'].format(name=_0x89c0a7, slope=_0xaf6906), 'TEXT'))
                        elif _0xaf6906 < -15 and _0xabf819 > 0:
                            _0x40f23c.append((_0xc06cbb['comm_bearish'].format(name=_0x89c0a7, slope=_0xaf6906), 'TEXT'))
                _0xbb4451.controls.append(ft.Text(_0xc06cbb['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xbb4451.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0xe240a6 in _0xfda54f:
                    if _0xe240a6[1] == 'HEADER':
                        _0xbb4451.controls.append(ft.Text(f'\n--- {_0xe240a6[0]} ---', weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        _0xe20749 = _0xe240a6[0]
                        _0xfef3af = _0xe240a6[2]
                        _0x77ae1e = BARCHART_LINKS.get(_0xfef3af, 'https://www.barchart.com/futures/commitment-of-traders')
                        _0xbb4451.controls.append(ft.TextButton(content=ft.Text(_0xe20749, font_family='monospace', size=11, color='white'), on_click=lambda _0x0f4ae6, _0xeddbdc=_0x77ae1e: page.launch_url(_0xeddbdc), style=ft.ButtonStyle(padding=0)))
                _0xbb4451.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                _0xbb4451.controls.append(ft.Text(_0xc06cbb['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0xbb4451.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0x1500c0, _0xb7ea0c in _0x40f23c:
                    if _0xb7ea0c == 'SUBHEADER':
                        _0xbb4451.controls.append(ft.Text(f'\n{_0x1500c0}', weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        _0xbb4451.controls.append(ft.Text(_0x1500c0, size=11, color='white70'))
                _0x83049c.value = _0xc06cbb['status_success']
            except Exception as ex:
                _0x83049c.value = f"Errore durante l'esecuzione: {_0xc0cb86}"
            _0x206e6c.visible = False
            page.update()
        _0x0f5e3a = TRANSLATIONS['Italiano']
        _0x0d3d48 = ft.ElevatedButton(_0x0f5e3a['btn_ready'], on_click=run_analysis, bgcolor='blue', color='white')
        _0xe3b5e0 = ft.ElevatedButton(_0x0f5e3a['btn_charts'], on_click=open_charts, bgcolor='green', color='white')
        page.add(_0x59af68, _0xe4d8ff, ft.Divider(height=15, color='white24'), _0x83049c, ft.Container(height=5), ft.Row([_0x0d3d48, _0xe3b5e0, _0x206e6c], alignment=ft.MainAxisAlignment.START, spacing=10), ft.Divider(height=15, color='white24'), _0x34dab4)
    except Exception as ex:
                # Usiamo 'ex' che è l'argomento corretto dell'eccezione, non una variabile inventata
                _0x83049c.value = f"Errore: {type(ex).__name__} - {str(ex)}"
                _0x83049c.color = "red"
if __name__ == '__main__':
    ft.app(target=main)
