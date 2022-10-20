from telegram.ext import * 
from telegram import ParseMode
from uniswap import Uniswap
from decimal import Decimal
from web3 import Web3
from time import sleep
from pycoingecko import CoinGeckoAPI
import datetime

cg = CoinGeckoAPI()
print("Bot started...")

wait_time = datetime.timedelta(seconds = 10)
next_request_time = datetime.datetime.now()

eth = "0x0000000000000000000000000000000000000000"
private_key = None
provider = "https://mainnet.infura.io/v3/a30ae197803a473c8a2560fda0f89889"
uniswap = Uniswap(address = eth, private_key = private_key, version = 2, provider = provider)

xi = '0x295B42684F90c77DA7ea46336001010F2791Ec8c'
kappa = '0x5D2C6545d16e3f927a25b4567E39e2cf5076BeF4'
gamma = '0x1e1eed62f8d82ecfd8230b8d283d5b5c1ba81b55'
beta = '0x35f67c1d929e106fdff8d1a55226afe15c34dbe2'
rho = '0x3f3cd642e81d030d7b514a2ab5e3a5536beb90ec'

def get_price_from_address(token):
    price_in_ETH = uniswap.get_price_input(Web3.toChecksumAddress(token), Web3.toChecksumAddress(eth), 10 ** 18)
    price_in_ETH_adjusted = Web3.fromWei(price_in_ETH, 'ether')
    stats = cg.get_price(ids = 'ethereum', vs_currencies = 'usd', include_24hr_change = 'false', include_market_cap = 'false', include_24hr_vol = 'false')
    ethprice = float(stats['ethereum']['usd'])
    return float(ethprice) * float(price_in_ETH_adjusted)

def start_command(update, context):
    update.message.reply_text("Commands: \n/xi\n/rho\n/beta\n/kappa\n/gamma\n/price")

def xi_command(update, context):
    price = get_price_from_address(xi)
    output = f"Xi is now `${str(round(price,6))}`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)

def gamma_command(update, context):
    price = get_price_from_address(gamma)
    output = f"Gamma is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)

def kappa_command(update, context):
    price = get_price_from_address(kappa)
    output = f"Kappa is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)

def rho_command(update, context):
    price = get_price_from_address(rho)
    output = f"Rho is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)

def beta_command(update, context):
    price = get_price_from_address(beta)
    output = f"Beta is now `${str(round(price,2))}`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)
    
def tip_command(update, context):
    output = f"If you want to tip me for hosting and programming the bot, feel free to send me any shitcoin of your choice here\n`0xf3912BAbBC95b383C1BD13654a4361D252185047`"
    update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)
    
def price_command(update, context):
    global next_request_time
    if (datetime.datetime.now() < next_request_time):
        delta = next_request_time - datetime.datetime.now()
        if(delta.seconds > 60):
            update.message.reply_text(f'Next update possible in {int(delta.seconds/60)} minute(s)!', quote = False)
        else:
            update.message.reply_text(f'Next update possible in {delta.seconds} seconds!', quote = False)
    else:
        try:
            price_beta = get_price_from_address(beta)
            price_gamma = get_price_from_address(gamma)
            price_kappa = get_price_from_address(kappa)
            price_rho = get_price_from_address(rho)
            price_xi = get_price_from_address(xi)
            output = f"Beta: `${str(round(price_beta,2))}`\nRho: `${str(round(price_rho,2))}`\nKappa: `${str(round(price_kappa,2))}`\nGamma: `${str(round(price_gamma,2))}`\nXi: `${str(round(price_xi,6))}`"
            update.message.reply_text(output, parse_mode = ParseMode.MARKDOWN, quote = False)
            next_request_time = datetime.datetime.now() + wait_time
        except:
            update.message.reply_text('Error. Try again later lol', parse_mode = ParseMode.MARKDOWN, quote = False)

def main():
    updater = Updater("1978205069:AAHV1wqGVl7gI3WwfTLFbtwQha4o0oEkcJo", use_context = True)
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
