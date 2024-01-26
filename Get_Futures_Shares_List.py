# Получение списка доступных фьючерсов и их запись в файл
import tinkoff.invest
import id.basek
import id.accid
from intro.quotation_dt import quotation_count
# from intro.quotation_dt import moneyvalue_count
from pathlib import Path
import pandas as pd

TOKEN = id.basek.TINKOFF_INVEST_DOG_NEW
SDK_client = tinkoff.invest.Client(TOKEN)
User_acc_ID = id.accid.ACC_ID

class Futures():
    def __init__(self, futures_name=Path('F:/grpc_examples/tinkoff/TI_API_2/csv_files/futures_list.csv'),
                 shares_name= Path('csv_files/shares_list.csv')):
        self.df_futures = pd.read_csv(futures_name)
        self.df_shares = pd.read_csv(shares_name)
        self.future_name = None
        self.future_figi = None
        self.active_row = None

    def set_figi(self, name):
        self.active_row = self.df_futures[self.df_futures['name'] == name]
        self.future_figi = self.active_row['figi'].values[0]
    
    def get_info(self, fields = ['name', 'figi', 'expiration_date', 'currency', 'futures_type']):
        text = ''
        for col in fields:
            text += col + ': ' + str(self.active_row[col].values[0]) + '\n'
        return text
    
def futures_list():
    with SDK_client as client:
        fc = client.instruments.futures(instrument_status=2)
        futur_list = futures_list_structure(fc.instruments)
        return futur_list


def futures_list_structure(instruments: [tinkoff.invest.Future]):
    futures_structure = pd.DataFrame([{
        'name': f.name,
        'futures_type': f.futures_type,
        'figi': f.figi,
        'uid': f.uid,
        'ticker': f.ticker,
        'expiration_date': f.expiration_date,
        'status': f.trading_status,
        'basic_asset_size': quotation_count(f.basic_asset_size),
        'api_trade_available_flag': f.api_trade_available_flag,
        'lot': f.lot,
        'class_code': f.class_code,
        'currency': f.currency,
        'klong': quotation_count(f.klong),
        'kshort': quotation_count(f.kshort),        
        'min_price_increment': quotation_count(f.min_price_increment)
    } for f in instruments])

    return futures_structure


def record_to_csv():
    filepath = Path('csv_files/futures_list.csv')
    df = pd.DataFrame(futures_list())
    df.to_csv(filepath)
    return print('Record complete')


def shares_list():
    with SDK_client as client:
        sc = client.instruments.futures(instrument_status=2)
        shrs_list = shares_list_structure(sc.instruments)
        return shrs_list


def shares_list_structure(instruments: [tinkoff.invest.Share]):
    shares_structure = pd.DataFrame([{
        'name': s.name,
        'figi': s.figi,
        'uid': s.uid,
        'ticker': s.ticker,
        'klong': s.klong,
        'kshort': s.kshort,
        # 'nominal': moneyvalue_count(s.basic_asset_size),
        'api_trade_available_flag': s.api_trade_available_flag,
        'lot': s.lot,
        'class_code': s.class_code,
        'min_price_increment': quotation_count(s.min_price_increment)
    } for s in instruments])

    return shares_structure


def record_shares_to_csv():
    filepath = Path('csv_files/shares_list.csv')
    df = pd.DataFrame(shares_list())
    df.to_csv(filepath)
    return print('Record complete')

def main():
    # print(futures_list())
    # SDK_client = tinkoff.invest.Client(TOKEN)
    # record_to_csv()
    # print(shares_list())
    SDK_client = tinkoff.invest.Client(TOKEN)
    record_shares_to_csv()
    

if __name__ == '__main__':
    main()