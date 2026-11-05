import ast
import random
import string
import sys

class PurePythonObfuscator(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.mapping = {}
        # Lista estesa di nomi e chiavi che NON devono essere mai rinominati
        self.reserved = {
            # Librerie e componenti Flet/Python
            'main', 'page', 'ft', 'urllib', 'csv', 'io', 'os', 'datetime', 'hashlib', 'request',
            'TRANSLATIONS', 'BARCHART_LINKS', 'categories', 'market_data', 'cur_strength', 'categories',
            'run_analysis', 'open_charts', 'change_language',
            
            # Categorie e sezioni UI
            'cat_valute', 'cat_grains', 'cat_metalli', 'cat_softs', 'cat_energies', 'cat_indici',
            'sig_valute', 'sec_cross', 'sec_commodities', 'sec_indices', 'report_header', 'screening_header',
            'cross_long', 'cross_short', 'comm_squeeze', 'comm_bullish', 'comm_bearish',
            'title', 'btn_ready', 'btn_charts', 'status_ready', 'status_download', 'status_success', 'error_prefix',

            # Ticker e Mercati CFTC / Barchart
            'SWISS FRANC', 'USD INDEX', 'MEXICAN PESO', 'NZ DOLLAR', 'CANADIAN DOLLAR', 
            'BRAZILIAN REAL', 'SOUTH AFRICAN RAND', 'BRITISH POUND', 'JAPANESE YEN', 
            'EURO FX', 'AUSTRALIAN DOLLAR', 'CORN', 'SOYBEANS', 'SOYBEAN OIL', 
            'SOYBEAN MEAL', 'WHEAT-SRW', 'WHEAT-HRW', 'WHEAT-SPRING', 'ROUGH RICE', 
            'CANOLA', 'GOLD', 'SILVER', 'COPPER', 'PALLADIUM', 'PLATINUM', 'ALUMINUM', 
            'COCOA', 'COTTON', 'COFFEE', 'SUGAR', 'ORANGE JUICE', 'LUMBER', 'CRUDE OIL', 
            'GASOLINE', 'NY HARBOR ULSD', 'NATURAL GAS', 'ETHANOL', 'S&P 500', 
            'NASDAQ-100', 'DOW JONES', 'RUSSELL 2000', 'VIX',
            
            # Simboli Valute
            'EUR', 'GBP', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF', 'USD',

            # Built-in di Python
            'print', 'len', 'range', 'list', 'str', 'int', 'float', 'dict', 'set',
            'tuple', 'open', 'super', 'Exception', 'True', 'False', 'None'
        }

    def _generate_hex_name(self):
        rand_hex = ''.join(random.choices('0123456789abcdef', k=6))
        return f"_0x{rand_hex}"

    def get_new_name(self, original_name):
        if original_name.startswith('__') or original_name in self.reserved:
            return original_name
        if original_name not in self.mapping:
            new_name = self._generate_hex_name()
            while new_name in self.mapping.values():
                new_name = self._generate_hex_name()
            self.mapping[original_name] = new_name
        return self.mapping[original_name]

    def visit_FunctionDef(self, node):
        node.name = self.get_new_name(node.name)
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and 
            isinstance(node.body[0].value.value, str)):
            node.body.pop(0)
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            node.id = self.get_new_name(node.id)
        return node

    def visit_arg(self, node):
        node.arg = self.get_new_name(node.arg)
        return node

def obfuscate_file(input_file="main_pulito.py", output_file="main_protected.py"):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            source = f.read()

        parsed = ast.parse(source)
        obfuscator = PurePythonObfuscator()
        transformed = obfuscator.visit(parsed)
        ast.fix_missing_locations(transformed)

        obfuscated_code = ast.unparse(transformed)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Protected by PurePython Obfuscator\n")
            f.write(obfuscated_code)

        print(f"SUCCESS: File '{input_file}' offuscato con successo in '{output_file}'!")
        print(f"Identificatori ridenominati in hex: {len(obfuscator.mapping)}")

    except Exception as e:
        print(f"ERRORE durante l'offuscamento: {e}")

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "main_pulito.py"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "main_protected.py"
    obfuscate_file(in_file, out_file)
