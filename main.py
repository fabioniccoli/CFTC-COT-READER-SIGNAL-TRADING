# Protected by PurePython Obfuscator
import flet as ft
import urllib.request
import csv
import io
TRANSLATIONS = {'Italiano': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Avvia Analisi', 'btn_charts': 'Apri Barchart COT', 'status_ready': "Pronto per l'analisi", 'status_download': 'Scaricamento dei dati dal report Legacy CFTC...', 'status_success': 'Analisi completata con successo!', 'error_prefix': "Errore durante l'esecuzione: ", 'report_header': 'REPORT COT (LEGACY) - REPORT ANALITICO CON NET SLOPE', 'screening_header': 'SCREENING STRATEGICO & INCROCI MULTI-VALUTA / COMMODITIES', 'cat_valute': 'VALUTE', 'cat_grains': 'MATERIE PRIME - GRAINS', 'cat_metalli': 'METALLI', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICI', 'sig_valute': '--- INCROCI VALUTARI (Forza Relativa Universale) ---', 'sec_cross': '--- ANALISI DINAMICA CROSS PRINCIPALI ---', 'sec_commodities': '--- MATERIE PRIME & CORRELAZIONE COMMODITIES ---', 'sec_indices': '--- INDICI AZIONARI ---', 'cross_long': '-> [LONG {base}/{quote}] Favorevole a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorevole a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short in chiusura (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Forte long con USD debole (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Forte short con USD forte (Slope: {slope:+.1f}).'}, 'English': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Start Analysis', 'btn_charts': 'Open Barchart COT', 'status_ready': 'Ready for analysis', 'status_download': 'Downloading data from CFTC Legacy report...', 'status_success': 'Analysis completed successfully!', 'error_prefix': 'Execution error: ', 'report_header': 'COT REPORT (LEGACY) - ANALYTICAL REPORT WITH NET SLOPE', 'screening_header': 'STRATEGIC SCREENING & MULTI-CURRENCY / COMMODITIES CROSSES', 'cat_valute': 'CURRENCIES', 'cat_grains': 'COMMODITIES - GRAINS', 'cat_metalli': 'METALS', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CURRENCY CROSSES (Universal Relative Strength) ---', 'sec_cross': '--- DYNAMIC ANALYSIS OF MAJOR CROSSES ---', 'sec_commodities': '--- COMMODITIES & CORRELATION ---', 'sec_indices': '--- STOCK INDICES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable to {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable to {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short covering (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Strong long with weak USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Strong short with strong USD (Slope: {slope:+.1f}).'}, 'Español': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Iniciar Análisis', 'btn_charts': 'Abrir Barchart COT', 'status_ready': 'Listo para el análisis', 'status_download': 'Descargando datos del informe Legacy CFTC...', 'status_success': '¡Análisis completado con éxito!', 'error_prefix': 'Error durante la ejecución: ', 'report_header': 'INFORME COT (LEGACY) - INFORME ANALÍTICO CON NET SLOPE', 'screening_header': 'SELECCIÓN ESTRATÉGICA Y CRUCES DE DIVISAS / COMMODITIES', 'cat_valute': 'MONEDAS', 'cat_grains': 'MATERIAS PRIMAS - GRAINS', 'cat_metalli': 'METALES', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGÍAS', 'cat_indici': 'INDICES', 'sig_valute': '--- CRUCES DE MONEDAS (Fuerza Relativa Universal) ---', 'sec_cross': '--- ANÁLISIS DINÁMICO DE CRUCES PRINCIPALES ---', 'sec_commodities': '--- MATERIAS PRIMAS ---', 'sec_indices': '--- ÍNDICES BURSÁTILES ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable a {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable a {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Cierre de cortos (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Fuerte long con USD débil (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Fuerte short con USD fuerte (Slope: {slope:+.1f}).'}, 'Deutsch': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': 'Analyse Starten', 'btn_charts': 'Barchart COT Öffnen', 'status_ready': 'Bereit für die Analyse', 'status_download': 'Daten aus dem CFTC Legacy Report werden heruntergeladen...', 'status_success': 'Analyse erfolgreich abgeschlossen!', 'error_prefix': 'Fehler bei der Ausführung: ', 'report_header': 'COT BERICHT (LEGACY) - ANALYTISCHER BERICHT MIT NET SLOPE', 'screening_header': 'STRATEGISCHES SCREENING & WÄHRUNGSKREUZUNGEN / COMMODITIES', 'cat_valute': 'WÄHRUNGEN', 'cat_grains': 'ROHSTOFFE - GRAINS', 'cat_metalli': 'METALLE', 'cat_softs': 'SOFTS', 'cat_energies': 'ENERGIE', 'cat_indici': 'INDIZES', 'sig_valute': '--- WÄHRUNGSKREUZUNGEN (Universelle Relative Stärke) ---', 'sec_cross': '--- DYNAMISCHE ANALYSE DER HAUPTKREUZUNGEN ---', 'sec_commodities': '--- ROHSTOFFE & KORRELATION ---', 'sec_indices': '--- AKTIENINDIZES ---', 'cross_long': '-> [LONG {base}/{quote}] Günstig für {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Günstig für {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name}: Short-Eindeckung (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name}: Starkes Long bei schwachem USD (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name}: Starkes Short bei starkem USD (Slope: {slope:+.1f}).'}, 'Français': {'title': 'CFTC COT Analyzer PRO', 'btn_ready': "Lancer l'analyse", 'btn_charts': 'Ouvrir Barchart COT', 'status_ready': "Prêt pour l'analyse", 'status_download': 'Téléchargement des données du rapport Legacy CFTC...', 'status_success': 'Analyse terminée avec succès !', 'error_prefix': "Erreur lors de l'exécution : ", 'report_header': 'RAPPORT COT (LEGACY) - RAPPORT ANALYTIQUE AVEC NET SLOPE', 'screening_header': 'SCREENING STRATÉGIQUE & CROISEMENTS DE DEVISES / COMMODITIES', 'cat_valute': 'DEVISES', 'cat_grains': 'MATIÈRES PREMIÈRES - GRAINS', 'cat_metalli': 'MÉTAUX', 'cat_softs': 'SOFTS', 'cat_energies': 'ÉNERGIES', 'cat_indici': 'INDICES', 'sig_valute': '--- CROISEMENTS DE DEVISES (Force Relative Universelle) ---', 'sec_cross': '--- ANALYSE DYNAMIQUE DES CROISEMENTS MAJEURS ---', 'sec_commodities': '--- MATIÈRES PREMIÈRES & CORRÉLATION ---', 'sec_indices': '--- INDICES BOURSIERS ---', 'cross_long': '-> [LONG {base}/{quote}] Favorable à {base} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'cross_short': '-> [SHORT {base}/{quote}] Favorable à {quote} (Slope: {base} {s_base:+.1f} vs {quote} {s_quote:+.1f})', 'comm_squeeze': '-> [COMMODITY / SQUEEZE] {name} : Couverture de shorts (Slope: {slope:+.1f}).', 'comm_bullish': '-> [COMMODITY / BULLISH] {name} : Long puissant avec USD faible (Slope: {slope:+.1f}).', 'comm_bearish': '-> [COMMODITY / BEARISH] {name} : Short puissant avec USD fort (Slope: {slope:+.1f}).'}}
BARCHART_LINKS = {'SWISS FRANC': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/S6*0', 'USD INDEX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/DX*0', 'MEXICAN PESO': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/M6*0', 'NZ DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/N6*0', 'CANADIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/D6*0', 'BRAZILIAN REAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/L6*0', 'SOUTH AFRICAN RAND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/Z6*0', 'BRITISH POUND': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/B6*0', 'JAPANESE YEN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/J6*0', 'EURO FX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/E6*0', 'AUSTRALIAN DOLLAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/A6*0', 'CORN': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZC*0', 'SOYBEANS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZS*0', 'SOYBEAN OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZL*0', 'SOYBEAN MEAL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZM*0', 'WHEAT-SRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZW*0', 'WHEAT-HRW': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KE*0', 'WHEAT-SPRING': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/MW*0', 'ROUGH RICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ZR*0', 'CANOLA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RS*0', 'GOLD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/GC*0', 'SILVER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SI*0', 'COPPER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HG*0', 'PALLADIUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PA*0', 'PLATINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/PL*0', 'ALUMINUM': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/AL*0', 'COCOA': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CC*0', 'COTTON': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CT*0', 'COFFEE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/KC*0', 'SUGAR': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/SB*0', 'ORANGE JUICE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/OJ*0', 'LUMBER': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/LB*0', 'CRUDE OIL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/CL*0', 'GASOLINE': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/RB*0', 'NY HARBOR ULSD': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/HO*0', 'NATURAL GAS': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NG*0', 'ETHANOL': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/FL*0', 'S&P 500': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/ES*0', 'NASDAQ-100': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/NQ*0', 'DOW JONES': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/YM*0', 'RUSSELL 2000': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/QR*0', 'VIX': 'https://www.barchart.com/futures/commitment-of-traders/interactive-charts/VI*0'}

def main(page: ft.Page):
    try:
        page.title = 'CFTC COT Analyzer PRO'
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20
        _0x02d876 = 'Italiano'
        _0x940aba = TRANSLATIONS[_0x02d876]
        _0x4db0db = ft.Text(_0x940aba['title'], size=22, weight=ft.FontWeight.BOLD, color='white')

        def change_language(_0x43c1a4):
            nonlocal current_lang, t
            _0x02d876 = _0x7bf21a.value
            _0x940aba = TRANSLATIONS[_0x02d876]
            _0x4db0db.value = _0x940aba['title']
            _0x893543.text = _0x940aba['btn_ready']
            _0x5b3e0e.text = _0x940aba['btn_charts']
            _0xa2b9b5.value = _0x940aba['status_ready']
            page.update()
        _0x7bf21a = ft.Dropdown(label='Language / Lingua', value='Italiano', options=[ft.dropdown.Option(_0xedb304) for _0xedb304 in TRANSLATIONS.keys()], on_change=change_language, width=180, text_size=12, label_style=ft.TextStyle(size=12))
        _0xa2b9b5 = ft.Text(_0x940aba['status_ready'], size=13, color='green')
        _0xf65028 = ft.ProgressRing(visible=False, width=20, height=20)
        _0x3eaa02 = ft.Column(spacing=2)
        _0xd6a993 = ft.Container(content=_0x3eaa02, padding=ft.padding.only(bottom=100))
        _0x33fba5 = ft.Row([_0xd6a993], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START)

        def open_charts(_0x43c1a4):
            page.launch_url('https://www.barchart.com/futures/commitment-of-traders')

        def run_analysis(_0x43c1a4):
            _0xa2b9b5.value = _0x940aba['status_download']
            _0xf65028.visible = True
            _0x3eaa02.controls.clear()
            page.update()
            try:
                _0xb6cb30 = 'https://www.cftc.gov/dea/newcot/deafut.txt'
                _0xf7e5e3 = urllib.request.Request(_0xb6cb30, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(_0xf7e5e3, timeout=15) as _0x752ae9:
                    _0x24581e = _0x752ae9.read().decode('utf-8', errors='ignore')
                _0xa2548d = io.StringIO(_0x24581e)
                _0x376eeb = csv.reader(_0xa2548d)
                _0x42ff81 = list(_0x376eeb)
                _0x472a0c = {_0x940aba['cat_valute']: ['SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 'EURO FX', 'AUSTRALIAN DOLLAR'], _0x940aba['cat_grains']: ['CORN', 'SOYBEANS', 'SOYBEAN OIL', 'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 'CANOLA'], _0x940aba['cat_metalli']: ['GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM'], _0x940aba['cat_softs']: ['COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER'], _0x940aba['cat_energies']: ['CRUDE OIL', 'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL'], _0x940aba['cat_indici']: ['S&P 500', 'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX']}
                _0xe2bff9 = []
                _0x0b5346 = {}
                for _0xd1134b, _0x77316b in _0x472a0c.items():
                    _0xe2bff9.append((_0xd1134b, 'HEADER'))
                    for _0xe44af0 in _0x77316b:
                        for _0x12c4ae in _0x42ff81:
                            if not _0x12c4ae or len(_0x12c4ae) < 40:
                                continue
                            _0x576f0d = str(_0x12c4ae[0]).strip()
                            if _0xe44af0.upper() in _0x576f0d.upper():
                                try:
                                    _0x8c89a9 = float(_0x12c4ae[7]) if _0x12c4ae[7].strip() and float(_0x12c4ae[7]) > 0 else 1
                                    _0xc7e652 = float(_0x12c4ae[8]) if _0x12c4ae[8].strip() else 0
                                    _0x53612b = float(_0x12c4ae[9]) if _0x12c4ae[9].strip() else 0
                                    _0x78b241 = int(float(_0x12c4ae[38])) if _0x12c4ae[38].strip() else 0
                                    _0x9bc531 = int(float(_0x12c4ae[39])) if _0x12c4ae[39].strip() else 0
                                    _0x3d67ef = _0xc7e652 / _0x8c89a9 * 100
                                    _0x64ac81 = _0x53612b / _0x8c89a9 * 100
                                    _0xbbd842 = _0xc7e652 - _0x78b241
                                    _0x7f09fd = _0x53612b - _0x9bc531
                                    _0x46011e = _0x78b241 / _0xbbd842 * 100 if _0xbbd842 > 0 else 0
                                    _0x3e510b = _0x9bc531 / _0x7f09fd * 100 if _0x7f09fd > 0 else 0
                                    _0xdc9a0c = _0x3d67ef + _0x46011e / 10.0
                                    _0x752f3f = _0x64ac81 + _0x3e510b / 10.0
                                    _0xdfaddb = _0xdc9a0c - _0x752f3f
                                    if _0xdfaddb > 15:
                                        _0x49e829 = 'STRONG LONG'
                                    elif _0xdfaddb > 5:
                                        _0x49e829 = 'MODERATE LONG'
                                    elif _0xdfaddb < -15:
                                        _0x49e829 = 'STRONG SHORT'
                                    elif _0xdfaddb < -5:
                                        _0x49e829 = 'MODERATE SHORT'
                                    else:
                                        _0x49e829 = 'NEUTRAL'
                                    _0x5b0744 = f'{_0x576f0d[:32]:<34} | Long: {_0x3d67ef:5.1f}% ({_0x78b241:+6d} ctr) | Short: {_0x64ac81:5.1f}% ({_0x9bc531:+6d} ctr) | Net Slope: {_0xdfaddb:+6.1f} [{_0x49e829}]'
                                    _0xe2bff9.append((_0x5b0744, 'MARKET', _0xe44af0.upper()))
                                    _0x4aa4e1 = _0xe44af0.upper()
                                    _0x0b5346[_0x4aa4e1] = {'name': _0x576f0d, 'pct_long': _0x3d67ef, 'pct_short': _0x64ac81, 'chg_long': _0x78b241, 'chg_short': _0x9bc531, 'net_slope': _0xdfaddb}
                                    break
                                except Exception:
                                    pass
                _0x8449af = []
                _0x6a0088 = {'EURO FX': 'EUR', 'BRITISH POUND': 'GBP', 'JAPANESE YEN': 'JPY', 'AUSTRALIAN DOLLAR': 'AUD', 'NZ DOLLAR': 'NZD', 'CANADIAN DOLLAR': 'CAD', 'SWISS FRANC': 'CHF', 'USD INDEX': 'USD'}
                _0x2da5e8 = {}
                for _0x56a7f8, _0x054088 in _0x6a0088.items():
                    if _0x56a7f8 in _0x0b5346:
                        _0x2da5e8[_0x054088] = _0x0b5346[_0x56a7f8]['net_slope']
                _0x55c577 = _0x5a6560(_0x2da5e8.items(), key=lambda _0xfff0df: _0xfff0df[1], reverse=True)
                _0x8449af.append((_0x940aba['sig_valute'], 'SUBHEADER'))
                if len(_0x55c577) >= 2:
                    _0x8449af.append((f'-> [TOP SETUP ABS] {_0x55c577[0][0]}/{_0x55c577[-1][0]} | Max div ({_0x55c577[0][0]}: {_0x55c577[0][1]:+.1f} vs {_0x55c577[-1][0]}: {_0x55c577[-1][1]:+.1f})', 'TEXT'))
                _0x381d01 = [('EUR', 'USD'), ('GBP', 'USD'), ('AUD', 'USD'), ('NZD', 'USD'), ('USD', 'JPY'), ('USD', 'CAD'), ('USD', 'CHF'), ('EUR', 'GBP'), ('EUR', 'JPY'), ('GBP', 'JPY'), ('AUD', 'JPY')]
                _0x8449af.append((_0x940aba['sec_cross'], 'SUBHEADER'))
                for _0x718629, _0x771037 in _0x381d01:
                    if _0x718629 in _0x2da5e8 and _0x771037 in _0x2da5e8:
                        _0x951268, _0xc864f9 = (_0x2da5e8[_0x718629], _0x2da5e8[_0x771037])
                        _0xc5206c = _0x951268 - _0xc864f9
                        if _0xc5206c > 10:
                            _0x8449af.append((_0x940aba['cross_long'].format(base=_0x718629, quote=_0x771037, s_base=_0x951268, s_quote=_0xc864f9), 'TEXT'))
                        elif _0xc5206c < -10:
                            _0x8449af.append((_0x940aba['cross_short'].format(base=_0x718629, quote=_0x771037, s_base=_0x951268, s_quote=_0xc864f9), 'TEXT'))
                _0x8449af.append((_0x940aba['sec_commodities'], 'SUBHEADER'))
                _0xac72dc = ['GOLD', 'SILVER', 'CRUDE OIL', 'COPPER', 'LUMBER', 'CORN', 'SOYBEANS']
                _0x984977 = _0x2da5e8.get('USD', 0)
                for _0xc9784e in _0xac72dc:
                    _0x87e6f5 = _0x0b5346.get(_0xc9784e)
                    if _0x87e6f5:
                        _0x07df7e = _0x87e6f5['name'].split('-')[0].strip()
                        _0x17347c = _0x87e6f5['net_slope']
                        if _0x87e6f5['pct_short'] > 60 and _0x87e6f5['chg_short'] < 0:
                            _0x8449af.append((_0x940aba['comm_squeeze'].format(name=_0x07df7e, slope=_0x17347c), 'TEXT'))
                        elif _0x17347c > 15 and _0x984977 < 0:
                            _0x8449af.append((_0x940aba['comm_bullish'].format(name=_0x07df7e, slope=_0x17347c), 'TEXT'))
                        elif _0x17347c < -15 and _0x984977 > 0:
                            _0x8449af.append((_0x940aba['comm_bearish'].format(name=_0x07df7e, slope=_0x17347c), 'TEXT'))
                _0x3eaa02.controls.append(ft.Text(_0x940aba['report_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0x3eaa02.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0xa8f39e in _0xe2bff9:
                    if _0xa8f39e[1] == 'HEADER':
                        _0x3eaa02.controls.append(ft.Text(f'\n--- {_0xa8f39e[0]} ---', weight=ft.FontWeight.BOLD, color='cyan', size=12))
                    else:
                        _0x012d88 = _0xa8f39e[0]
                        _0xfb7f97 = _0xa8f39e[2]
                        _0xe8b64f = BARCHART_LINKS.get(_0xfb7f97, 'https://www.barchart.com/futures/commitment-of-traders')
                        _0x3eaa02.controls.append(ft.TextButton(content=ft.Text(_0x012d88, font_family='monospace', size=11, color='white'), on_click=lambda _0x43c1a4, _0x63831f=_0xe8b64f: page.launch_url(_0x63831f), style=ft.ButtonStyle(padding=0)))
                _0x3eaa02.controls.append(ft.Text('\n' + '=' * 70, color='white24', size=10))
                _0x3eaa02.controls.append(ft.Text(_0x940aba['screening_header'], weight=ft.FontWeight.BOLD, color='yellow', size=11))
                _0x3eaa02.controls.append(ft.Text('=' * 70, color='white24', size=10))
                for _0xc02784, _0xcd1360 in _0x8449af:
                    if _0xcd1360 == 'SUBHEADER':
                        _0x3eaa02.controls.append(ft.Text(f'\n{_0xc02784}', weight=ft.FontWeight.BOLD, color='amber', size=12))
                    else:
                        _0x3eaa02.controls.append(ft.Text(_0xc02784, size=11, color='white70'))
                _0xa2b9b5.value = _0x940aba['status_success']
            except Exception as ex:
                _0xa2b9b5.value = f"{_0x940aba['error_prefix']}{_0x599483}"
            _0xf65028.visible = False
            page.update()
        _0x893543 = ft.ElevatedButton(_0x940aba['btn_ready'], on_click=run_analysis, bgcolor='blue', color='white')
        _0x5b3e0e = ft.ElevatedButton(_0x940aba['btn_charts'], on_click=open_charts, bgcolor='green', color='white')
        page.add(_0x4db0db, _0x7bf21a, ft.Divider(height=15, color='white24'), _0xa2b9b5, ft.Container(height=5), ft.Row([_0x893543, _0x5b3e0e, _0xf65028], alignment=ft.MainAxisAlignment.START, spacing=10), ft.Divider(height=15, color='white24'), _0x33fba5)
    except Exception as initialization_error:
        page.clean()
        page.add(ft.Text('ERRORE CRITICO DI AVVIO:', size=18, color='red', weight=ft.FontWeight.BOLD), ft.Text(str(_0xc2554d), size=14, color='white'))
        page.update()
if __name__ == '__main__':
    ft.app(target=main)
