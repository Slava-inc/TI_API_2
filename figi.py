import pandas as pd
import tinkoff.invest
import id
import id.basek
import id.accid

TOKEN = id.basek.TINKOFF_INVEST_DOG_NEW
SDK_client = tinkoff.invest.Client(TOKEN)
User_acc_ID = id.accid.ACC_ID

with SDK_client as client:
    InsrumentsService = client.instruments
    r = pd.DataFrame(InsrumentsService.shares(instrument_status=tinkoff.invest.InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments, columns=['name', 'figi', 'ticker', 'class_code'])
    df = pd.DataFrame(InsrumentsService.bonds(instrument_status=tinkoff.invest.InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments, columns=['name', 'figi', 'ticker', 'class_code'])
    r = pd.concat([r, df])
    req_df = r[r['ticker'].isin(['GAZP', 'LKOH', 'NLMK', 'RUAL', 'RNFT', 'SBER', 'CHMF', 'SGZH', 'YNDX', 'SU26240RMFS0'])]
    print(req_df)    
    req_df.to_csv('./csv_files/figi.csv')