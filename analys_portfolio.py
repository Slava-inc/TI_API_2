import tinkoff.invest
import id.basek
import id.accid
import pandas as pd

# TOKEN = id.basek.TINKOFF_INVEST_DOG_NEW
TOKEN = id.basek.TINKOFF_INVEST_ALL
SDK = tinkoff.invest.Client(TOKEN)
User_acc_ID = id.accid.ACC_ID

# Для получения Портфеля
def get_portfolio():
    with SDK as client:
        return client.operations.get_portfolio(account_id=User_acc_ID)

portf = get_portfolio()

# portf_df = pd.DataFrame(portf)
etf = []
currency = []
instrs = []
share = []
SDK = tinkoff.invest.Client(TOKEN)
with SDK as client:
    etfs = client.instruments.etfs(instrument_status=2).instruments
    curs = client.instruments.currencies(instrument_status=2).instruments
    shares = client.instruments.shares(instrument_status=2).instruments
for position in portf.positions:
    # if position.blocked:
    #    continue
    inst_type = position.instrument_type
    if inst_type == 'etf':
        etf.append(position.figi)
    elif inst_type == 'currency':
        currency.append(position.figi) 
    elif inst_type == 'share':
        share.append(position.figi)   
    # print('figi {}, instrument_type {}, current_price {}'.format(position.figi,
                                                                # position.instrument_type,
                                                                # position.current_price))
etf_df = pd.DataFrame({'etf': etf, 'ticker': '', 'name': ''})
cur_df = pd.DataFrame({'figi': currency, 'ticker': '', 'name': ''})
share_df = pd.DataFrame({'figi': share, 'ticker': '', 'name': ''})

for instr in etfs:
    if instr.figi in(etf):
        etf_df['ticker'] = etf_df.apply(lambda row: instr.ticker if row.etf == instr.figi else row.ticker, axis = 1)
        etf_df['name'] = etf_df.apply(lambda row: instr.name if row['etf'] == instr.figi else row['name'], axis = 1) 
    
print(etf_df)  

for instr in curs:
    if instr.figi in(currency):
        cur_df['ticker'] = cur_df.apply(lambda row: instr.ticker if row.figi == instr.figi else row.ticker, axis = 1)
        cur_df['name'] = cur_df.apply(lambda row: instr.name if row['figi'] == instr.figi else row['name'], axis = 1) 
    
print(cur_df)   

for instr in shares:
    if instr.figi in(share):
        share_df['ticker'] = share_df.apply(lambda row: instr.ticker if row.figi == instr.figi else row.ticker, axis = 1)
        share_df['name'] = share_df.apply(lambda row: instr.name if row['figi'] == instr.figi else row['name'], axis = 1) 
    
print(share_df) 