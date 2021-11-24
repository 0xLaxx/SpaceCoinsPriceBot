from telegram.ext import *
from telegram import ParseMode
from uniswap import Uniswap
from decimal import Decimal
from web3 import Web3
from time import sleep
from pycoingecko import CoinGeckoAPI
import requests

cg = CoinGeckoAPI()
print("Bot started...")

eth = "0x0000000000000000000000000000000000000000"
private_key =  None
version = 2
provider = "https://mainnet.infura.io/v3/a30ae197803a473c8a2560fda0f89889"
uniswap = Uniswap(address="0x0000000000000000000000000000000000000000", private_key=private_key, version=version, provider=provider)

xi = '0x295B42684F90c77DA7ea46336001010F2791Ec8c'
kappa = '0x5D2C6545d16e3f927a25b4567E39e2cf5076BeF4'
gamma = '0x1e1eed62f8d82ecfd8230b8d283d5b5c1ba81b55'
beta = '0x35f67c1d929e106fdff8d1a55226afe15c34dbe2'
rho = '0x3f3cd642e81d030d7b514a2ab5e3a5536beb90ec'

def get_price_from_address(token,printsome):
    price_in_ETH = uniswap.get_price_input(Web3.toChecksumAddress(token), Web3.toChecksumAddress(eth), 10**18)
    price_in_ETH_adjusted = Web3.fromWei(price_in_ETH, 'ether')

    #ethprice = requests.get('https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/1/usd/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/?key=ckey_f1ce8b78208646bbacc2800894e')
    #ethprice = ethprice.json()['data'][0]['prices'][0]['price']

    stats = cg.get_price(ids='ethereum', vs_currencies='usd', include_24hr_change='false', include_market_cap='false', include_24hr_vol='false')
    ethprice = float(stats['ethereum']['usd'])

    if(printsome):
        print(ethprice)
        print(price_in_ETH_adjusted)
    
    return float(ethprice) * float(price_in_ETH_adjusted)

def start_command(update, context):
    update.message.reply_text("Commands: \n/xi\n/rho\n/beta\n/kappa\n/gamma\n/price")

def xi_command(update, context):
    price = get_price_from_address(xi,False)
    output = f"Xi is now `${str(round(price,6))}`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)

def gamma_command(update, context):
    price = get_price_from_address(gamma,False)
    output = f"Gamma is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)

def kappa_command(update, context):
    price = get_price_from_address(kappa,False)
    output = f"Kappa is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)

def rho_command(update, context):
    price = get_price_from_address(rho,False)
    output = f"Rho is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)

def beta_command(update, context):
    price = get_price_from_address(beta,False)
    output = f"Beta is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)
    
def tip_command(update, context):
    output = f"If you want to tip me for hosting and programming the bot, feel free to send me any shitcoin of your choice here\n`0xf3912BAbBC95b383C1BD13654a4361D252185047`"
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)
    
def price_command(update, context):

    try:
        price_beta = get_price_from_address(beta,True)
        price_gamma = get_price_from_address(gamma,False)
        price_kappa = get_price_from_address(kappa,False)
        price_rho = get_price_from_address(rho,False)
        price_xi = get_price_from_address(xi,False)
        output = f"Beta: `${str(round(price_beta,2))}`\nRho: `${str(round(price_rho,2))}`\nKappa: `${str(round(price_kappa,2))}`\nGamma: `${str(round(price_gamma,2))}`\nXi: `${str(round(price_xi,6))}`"
        update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN, quote=False)
    except:
        update.message.reply_text('Error. Try again later lol', parse_mode=ParseMode.MARKDOWN, quote=False)

def main():
    updater = Updater("1978205069:AAHV1wqGVl7gI3WwfTLFbtwQha4o0oEkcJo", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("xi", xi_command))
    dp.add_handler(CommandHandler("gamma", gamma_command))
    dp.add_handler(CommandHandler("kappa", kappa_command))
    dp.add_handler(CommandHandler("beta", beta_command))
    dp.add_handler(CommandHandler("rho", rho_command))
    dp.add_handler(CommandHandler("price", price_command))
    dp.add_handler(CommandHandler("tip", tip_command))
    updater.start_polling()
    updater.idle()

main()
