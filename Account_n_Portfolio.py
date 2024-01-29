import tinkoff.invest
import id.basek
import id.accid

# TOKEN = id.basek.TINKOFF_INVEST_DOG_NEW
# BROKER = id.basek.TINKOFF_INVEST_BROKER
ALL = id.basek.TINKOFF_INVEST_ALL
SDK = tinkoff.invest.Client(ALL)

User_acc_ID = id.accid.ACC_ID

# Для полученния ID
def get_account_info():
    with SDK as client:
        gai = client.users.get_accounts()
    print(gai)

# Для полученния BROKER ID
def get_broker_info():
    with tinkoff.invest.Client(BROKER) as client:
        gai = client.users.get_accounts()
    print(gai)
get_account_info()
# get_broker_info()

# Для получения Портфеля
def show_portfolio():
    with SDK as client:
        portfel = client.operations.get_portfolio(account_id=User_acc_ID)
        print(portfel)

    return

# show_portfolio()

