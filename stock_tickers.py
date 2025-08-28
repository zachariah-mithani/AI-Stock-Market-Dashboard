"""
Stock ticker database with comprehensive list of popular stocks
"""

# Comprehensive stock ticker database
STOCK_TICKERS = {
    # Technology
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc. (Class A)',
    'GOOG': 'Alphabet Inc. (Class C)',
    'AMZN': 'Amazon.com Inc.',
    'META': 'Meta Platforms Inc.',
    'TSLA': 'Tesla Inc.',
    'NVDA': 'NVIDIA Corporation',
    'NFLX': 'Netflix Inc.',
    'ADBE': 'Adobe Inc.',
    'CRM': 'Salesforce Inc.',
    'ORCL': 'Oracle Corporation',
    'INTC': 'Intel Corporation',
    'AMD': 'Advanced Micro Devices Inc.',
    'IBM': 'International Business Machines Corp.',
    'CSCO': 'Cisco Systems Inc.',
    'QCOM': 'Qualcomm Inc.',
    'AVGO': 'Broadcom Inc.',
    'TXN': 'Texas Instruments Inc.',
    'PYPL': 'PayPal Holdings Inc.',
    'UBER': 'Uber Technologies Inc.',
    'LYFT': 'Lyft Inc.',
    'SNAP': 'Snap Inc.',
    'TWTR': 'Twitter Inc.',
    'SPOT': 'Spotify Technology S.A.',
    'ZOOM': 'Zoom Video Communications Inc.',
    'DOCU': 'DocuSign Inc.',
    'SQ': 'Square Inc.',
    'SHOP': 'Shopify Inc.',
    'ROKU': 'Roku Inc.',
    'PLTR': 'Palantir Technologies Inc.',
    'SNOW': 'Snowflake Inc.',
    'DDOG': 'Datadog Inc.',
    'CRWD': 'CrowdStrike Holdings Inc.',
    'ZS': 'Zscaler Inc.',
    'OKTA': 'Okta Inc.',
    'TWLO': 'Twilio Inc.',
    'WORK': 'Slack Technologies Inc.',
    'TEAM': 'Atlassian Corporation',
    'NOW': 'ServiceNow Inc.',
    'WDAY': 'Workday Inc.',
    'SPLK': 'Splunk Inc.',
    'VEEV': 'Veeva Systems Inc.',
    'MELI': 'MercadoLibre Inc.',
    'SE': 'Sea Limited',
    'BABA': 'Alibaba Group Holding Ltd.',
    'JD': 'JD.com Inc.',
    'PDD': 'PDD Holdings Inc.',
    'BIDU': 'Baidu Inc.',
    'NTES': 'NetEase Inc.',
    'TCEHY': 'Tencent Holdings Ltd.',
    'TSM': 'Taiwan Semiconductor Manufacturing Co.',
    'ASML': 'ASML Holding N.V.',
    'SAP': 'SAP SE',
    'SHOP': 'Shopify Inc.',
    
    # Finance
    'JPM': 'JPMorgan Chase & Co.',
    'BAC': 'Bank of America Corp.',
    'WFC': 'Wells Fargo & Co.',
    'C': 'Citigroup Inc.',
    'GS': 'Goldman Sachs Group Inc.',
    'MS': 'Morgan Stanley',
    'BLK': 'BlackRock Inc.',
    'AXP': 'American Express Co.',
    'V': 'Visa Inc.',
    'MA': 'Mastercard Inc.',
    'COF': 'Capital One Financial Corp.',
    'SCHW': 'Charles Schwab Corp.',
    'USB': 'U.S. Bancorp',
    'PNC': 'PNC Financial Services Group Inc.',
    'TFC': 'Truist Financial Corp.',
    'BK': 'Bank of New York Mellon Corp.',
    'STT': 'State Street Corp.',
    'BRK.A': 'Berkshire Hathaway Inc. (Class A)',
    'BRK.B': 'Berkshire Hathaway Inc. (Class B)',
    'SQ': 'Block Inc.',
    'AFRM': 'Affirm Holdings Inc.',
    'SOFI': 'SoFi Technologies Inc.',
    'HOOD': 'Robinhood Markets Inc.',
    'COIN': 'Coinbase Global Inc.',
    'UPST': 'Upstart Holdings Inc.',
    'LC': 'LendingClub Corp.',
    
    # Healthcare & Biotech
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'UNH': 'UnitedHealth Group Inc.',
    'MRNA': 'Moderna Inc.',
    'BNTX': 'BioNTech SE',
    'ABBV': 'AbbVie Inc.',
    'TMO': 'Thermo Fisher Scientific Inc.',
    'DHR': 'Danaher Corp.',
    'BMY': 'Bristol-Myers Squibb Co.',
    'AMGN': 'Amgen Inc.',
    'GILD': 'Gilead Sciences Inc.',
    'REGN': 'Regeneron Pharmaceuticals Inc.',
    'VRTX': 'Vertex Pharmaceuticals Inc.',
    'BIIB': 'Biogen Inc.',
    'ILMN': 'Illumina Inc.',
    'ISRG': 'Intuitive Surgical Inc.',
    'SYK': 'Stryker Corp.',
    'BSX': 'Boston Scientific Corp.',
    'ABT': 'Abbott Laboratories',
    'MDT': 'Medtronic plc',
    'CVS': 'CVS Health Corp.',
    'ANTM': 'Anthem Inc.',
    'CI': 'Cigna Corp.',
    'HUM': 'Humana Inc.',
    'TDOC': 'Teladoc Health Inc.',
    'VEEV': 'Veeva Systems Inc.',
    'DXCM': 'DexCom Inc.',
    'TECH': 'Bio-Techne Corp.',
    'NVTA': 'Invitae Corp.',
    'CRSP': 'CRISPR Therapeutics AG',
    'EDIT': 'Editas Medicine Inc.',
    'BEAM': 'Beam Therapeutics Inc.',
    'ARKG': 'ARK Genomic Revolution ETF',
    
    # Consumer & Retail
    'AMZN': 'Amazon.com Inc.',
    'WMT': 'Walmart Inc.',
    'HD': 'Home Depot Inc.',
    'COST': 'Costco Wholesale Corp.',
    'TGT': 'Target Corp.',
    'LOW': 'Lowe\'s Cos Inc.',
    'SBUX': 'Starbucks Corp.',
    'MCD': 'McDonald\'s Corp.',
    'NKE': 'Nike Inc.',
    'LULU': 'Lululemon Athletica Inc.',
    'ADSK': 'Autodesk Inc.',
    'DIS': 'Walt Disney Co.',
    'NFLX': 'Netflix Inc.',
    'CMCSA': 'Comcast Corp.',
    'T': 'AT&T Inc.',
    'VZ': 'Verizon Communications Inc.',
    'TMUS': 'T-Mobile US Inc.',
    'CHTR': 'Charter Communications Inc.',
    'DISH': 'Dish Network Corp.',
    'SIRI': 'SiriusXM Holdings Inc.',
    'FOXA': 'Fox Corp. (Class A)',
    'FOX': 'Fox Corp. (Class B)',
    'PARA': 'Paramount Global',
    'WBD': 'Warner Bros. Discovery Inc.',
    'ROKU': 'Roku Inc.',
    'FUBO': 'fuboTV Inc.',
    'DKNG': 'DraftKings Inc.',
    'PENN': 'Penn Entertainment Inc.',
    'MGM': 'MGM Resorts International',
    'LVS': 'Las Vegas Sands Corp.',
    'WYNN': 'Wynn Resorts Ltd.',
    'CZR': 'Caesars Entertainment Inc.',
    'ABNB': 'Airbnb Inc.',
    'BKNG': 'Booking Holdings Inc.',
    'EXPE': 'Expedia Group Inc.',
    'TRIP': 'TripAdvisor Inc.',
    'MAR': 'Marriott International Inc.',
    'HLT': 'Hilton Worldwide Holdings Inc.',
    'IHG': 'InterContinental Hotels Group',
    'H': 'Hyatt Hotels Corp.',
    'RCL': 'Royal Caribbean Cruises Ltd.',
    'CCL': 'Carnival Corp.',
    'NCLH': 'Norwegian Cruise Line Holdings Ltd.',
    'AAL': 'American Airlines Group Inc.',
    'DAL': 'Delta Air Lines Inc.',
    'UAL': 'United Airlines Holdings Inc.',
    'LUV': 'Southwest Airlines Co.',
    'JBLU': 'JetBlue Airways Corp.',
    'SAVE': 'Spirit Airlines Inc.',
    'ALK': 'Alaska Air Group Inc.',
    'HA': 'Hawaiian Airlines Inc.',
    
    # Energy
    'XOM': 'Exxon Mobil Corp.',
    'CVX': 'Chevron Corp.',
    'COP': 'ConocoPhillips',
    'EOG': 'EOG Resources Inc.',
    'SLB': 'Schlumberger Ltd.',
    'PSX': 'Phillips 66',
    'VLO': 'Valero Energy Corp.',
    'MPC': 'Marathon Petroleum Corp.',
    'KMI': 'Kinder Morgan Inc.',
    'OKE': 'ONEOK Inc.',
    'WMB': 'Williams Cos Inc.',
    'EPD': 'Enterprise Products Partners L.P.',
    'ET': 'Energy Transfer LP',
    'MMP': 'Magellan Midstream Partners L.P.',
    'MPLX': 'MPLX LP',
    'PAA': 'Plains All American Pipeline L.P.',
    'ENB': 'Enbridge Inc.',
    'TRP': 'TC Energy Corp.',
    'KMI': 'Kinder Morgan Inc.',
    'TRGP': 'Targa Resources Corp.',
    'WES': 'Western Midstream Partners LP',
    'AM': 'Antero Midstream Corp.',
    'PAGP': 'Plains GP Holdings L.P.',
    'USAC': 'USA Compression Partners LP',
    'CEQP': 'Crestwood Equity Partners LP',
    'ENLC': 'EnLink Midstream LLC',
    'NGL': 'NGL Energy Partners LP',
    'SMLP': 'Summit Midstream Partners LP',
    'HESM': 'Hess Midstream LP',
    'DCP': 'DCP Midstream LP',
    'GEL': 'Genesis Energy L.P.',
    'PBFX': 'PBF Logistics LP',
    'CAPL': 'CrossAmerica Partners LP',
    'DMLP': 'Dorchester Minerals L.P.',
    'ENLK': 'EnLink Midstream LLC',
    'EPD': 'Enterprise Products Partners L.P.',
    'ET': 'Energy Transfer LP',
    'KMI': 'Kinder Morgan Inc.',
    'MPLX': 'MPLX LP',
    'OKE': 'ONEOK Inc.',
    'PAA': 'Plains All American Pipeline L.P.',
    'TRGP': 'Targa Resources Corp.',
    'WMB': 'Williams Cos Inc.',
    
    # Special "micro" stocks for the example
    'MICRO': 'Micro Focus International plc',
    'MICR': 'Micron Solutions Inc.',
    'MICT': 'Micronet Enertec Technologies Inc.',
    'MSFT': 'Microsoft Corporation',
    'MU': 'Micron Technology Inc.',
    'MCHP': 'Microchip Technology Inc.',
    'MSTR': 'MicroStrategy Inc.',
    'MGNI': 'Magnite Inc.',
    'MIME': 'Mimecast Ltd.',
    'MTCH': 'Match Group Inc.',
    'MVIS': 'MicroVision Inc.',
    'MVST': 'Microvast Holdings Inc.',
    'MICT': 'Micronet Enertec Technologies Inc.',
    'MBIO': 'Mustang Bio Inc.',
    'MBOT': 'Microbot Medical Inc.',
    'MTEM': 'Molecular Templates Inc.',
    'MCRB': 'Seres Therapeutics Inc.',
    'MCFT': 'MasterCraft Boat Holdings Inc.',
    'MICT': 'Micronet Enertec Technologies Inc.',
    'MICR': 'Micron Solutions Inc.',
    'MCHP': 'Microchip Technology Inc.',
    'MSTR': 'MicroStrategy Inc.',
    'MVIS': 'MicroVision Inc.',
    'MVST': 'Microvast Holdings Inc.',
    'MBOT': 'Microbot Medical Inc.',
    'MTEM': 'Molecular Templates Inc.',
    'MCRB': 'Seres Therapeutics Inc.',
    'MCFT': 'MasterCraft Boat Holdings Inc.',
    
    # Crypto & Fintech
    'COIN': 'Coinbase Global Inc.',
    'MSTR': 'MicroStrategy Inc.',
    'RIOT': 'Riot Blockchain Inc.',
    'MARA': 'Marathon Digital Holdings Inc.',
    'HUT': 'Hut 8 Mining Corp.',
    'BITF': 'Bitfarms Ltd.',
    'CAN': 'Canaan Inc.',
    'EBON': 'Ebang International Holdings Inc.',
    'BTBT': 'Bit Digital Inc.',
    'NBT': 'Nanobiotix S.A.',
    'GBTC': 'Grayscale Bitcoin Trust',
    'ETHE': 'Grayscale Ethereum Trust',
    'BITO': 'ProShares Bitcoin Strategy ETF',
    'ARKK': 'ARK Innovation ETF',
    'ARKG': 'ARK Genomic Revolution ETF',
    'ARKQ': 'ARK Autonomous Technology & Robotics ETF',
    'ARKW': 'ARK Next Generation Internet ETF',
    'ARKF': 'ARK Fintech Innovation ETF',
    'PRNT': 'ARK 3D Printing ETF',
    'IZRL': 'ARK Israel Innovative Technology ETF',
    'CTXR': 'Citius Pharmaceuticals Inc.',
    'ZSAN': 'Zosano Pharma Corp.',
    'VXRT': 'Vaxart Inc.',
    'OCGN': 'Ocugen Inc.',
    'NVAX': 'Novavax Inc.',
    'BVXV': 'BiondVax Pharmaceuticals Ltd.',
    'TPTX': 'Turning Point Therapeutics Inc.',
    'SAVA': 'Cassava Sciences Inc.',
    'AXSM': 'Axsome Therapeutics Inc.',
    'AUPH': 'Aurinia Pharmaceuticals Inc.',
    'BMRN': 'BioMarin Pharmaceutical Inc.',
    'BLUE': 'bluebird bio Inc.',
    'FOLD': 'Amicus Therapeutics Inc.',
    'IONS': 'Ionis Pharmaceuticals Inc.',
    'MYGN': 'Myriad Genetics Inc.',
    'NKTR': 'Nektar Therapeutics',
    'ONCE': 'Oncorus Inc.',
    'PCRX': 'Pacira BioSciences Inc.',
    'PTCT': 'PTC Therapeutics Inc.',
    'RARE': 'Ultragenyx Pharmaceutical Inc.',
    'RGNX': 'Regenxbio Inc.',
    'SGMO': 'Sangamo Therapeutics Inc.',
    'SRPT': 'Sarepta Therapeutics Inc.',
    'TBPH': 'Theravance Biopharma Inc.',
    'TGTX': 'TG Therapeutics Inc.',
    'UTHR': 'United Therapeutics Corp.',
    'XNCR': 'Xencor Inc.',
    'ZLAB': 'Zai Lab Ltd.',
    'ZYNE': 'Zynerba Pharmaceuticals Inc.',
    'ZYXI': 'Zynex Inc.'
}

def search_tickers(query, limit=10):
    """
    Search for stock tickers that match the query
    Returns a list of dictionaries with ticker and company name
    """
    if not query:
        return []
    
    query = query.upper().strip()
    matches = []
    
    # Search in ticker symbols
    for ticker, company in STOCK_TICKERS.items():
        if query in ticker:
            matches.append({
                'ticker': ticker,
                'company': company,
                'match_type': 'ticker'
            })
    
    # Search in company names
    for ticker, company in STOCK_TICKERS.items():
        if query.lower() in company.lower() and ticker not in [m['ticker'] for m in matches]:
            matches.append({
                'ticker': ticker,
                'company': company,
                'match_type': 'company'
            })
    
    # Sort by relevance (exact ticker matches first, then partial matches)
    matches.sort(key=lambda x: (
        x['match_type'] != 'ticker',  # Ticker matches first
        not x['ticker'].startswith(query),  # Starts with query
        len(x['ticker']),  # Shorter tickers first
        x['ticker']  # Alphabetical
    ))
    
    return matches[:limit]

def get_popular_tickers():
    """
    Get a list of popular stock tickers
    """
    popular = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
        'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'DIS', 'PYPL', 'ADBE',
        'CMCSA', 'NFLX', 'XOM', 'VZ', 'KO', 'PFE', 'INTC', 'CSCO',
        'WMT', 'CRM', 'ABT', 'TMO', 'AVGO', 'COST', 'DHR', 'NEE',
        'QCOM', 'TXN', 'HON', 'UPS', 'IBM', 'SBUX', 'LOW', 'ORCL',
        'AMGN', 'CVX', 'MDT', 'GILD', 'AMT', 'SPGI', 'BKNG', 'ISRG'
    ]
    
    return [{'ticker': ticker, 'company': STOCK_TICKERS.get(ticker, '')} for ticker in popular]

def get_micro_stocks():
    """
    Get stocks that contain 'micro' in their ticker or name
    """
    micro_stocks = []
    query = 'micro'
    
    for ticker, company in STOCK_TICKERS.items():
        if query in ticker.lower() or query in company.lower():
            micro_stocks.append({
                'ticker': ticker,
                'company': company
            })
    
    return micro_stocks