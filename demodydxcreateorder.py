from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso
import time
import schedule
from dydx3.constants import MARKET_BTC_USD


########################## YOU FILL THIS OUT #################
_private_key = '5d9e195293e8ffddf8160445258f52b79ae27c2a5efbe78767f0dece1246d2e3'
#_private_key is optional and may be set to '' (hardware wallets do not generally provide this information)
#If _private_key is set, you do not need to set _api_key/_api_secret/_api_passphrase/_stark_private_key
_api_key = '51cc76a3-9fdc-d824-fbb4-08e184818dc0'
_api_secret = 'TGvg2kSVEBF75VOWp_HbAGmW1kahMtI27pJTuf6W'
_api_passphrase = 'rbBAJSYuqKIghCyW9HLl'
_stark_private_key = '0x3e1afab8f4fcf5776a25065e83b6dfd00d6d0d0b6fb15b1f1ad534edcb19517'
_eth_address = '0x8b9D414d40E82c6CDCbFf4150754999B21C4daFA'
_network_id = str(constants.NETWORK_ID_GOERLI)
#_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
_api_host = constants.API_HOST_GOERLI
#_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_GOERLI
##############################################################


if _private_key != '':
        client = Client(
                host = _api_host,
                default_ethereum_address = _eth_address,
                eth_private_key = _private_key,
                network_id = _network_id
        )
        derive_stark_key_result = client.onboarding.derive_stark_key()
        stark_private_key = derive_stark_key_result['private_key']
        client.stark_private_key = stark_private_key
else:
        client = Client(
                host = _api_host,
                network_id = _network_id,
                api_key_credentials = {
                        'key': _api_key,
                        'secret': _api_secret,
                        'passphrase': _api_passphrase
                }
        )
        client.stark_private_key = _stark_private_key

get_account_result = client.private.get_account(
        ethereum_address = _eth_address
)

orderbook = client.public.get_orderbook(
  market=MARKET_BTC_USD
)
print(orderbook.data["asks"][1]['price'])

last_ask = orderbook.data["asks"][1]['price']

rebate= 50



def ordenes():
        account = get_account_result.data['account']
        one_minute_from_now_iso = epoch_seconds_to_iso(time.time() + 70)
        create_order_result = client.private.create_order(
                position_id = account['positionId'],
                market = constants.MARKET_BTC_USD,
                side = constants.ORDER_SIDE_BUY,
                order_type = constants.ORDER_TYPE_LIMIT,
                post_only = False,
                size = '1.0',
                price = f'{last_ask - rebate}',
                limit_fee = '0.0005',
                expiration = one_minute_from_now_iso,
        )
        create_order_result = client.private.create_order(
                position_id=account['positionId'],
                market=constants.MARKET_BTC_USD,
                side=constants.ORDER_SIDE_SELL,
                order_type=constants.ORDER_TYPE_LIMIT,
                post_only=False,
                size='1.0',
                price= f'{last_ask - rebate}',
                limit_fee='0.05',
                expiration=one_minute_from_now_iso,
        )
        print(create_order_result.data)
        print(create_order_result.headers)
ordenes()
schedule.every(1).minutes.do(ordenes)

while True:
        schedule.run_pending()
        time.sleep(1)

