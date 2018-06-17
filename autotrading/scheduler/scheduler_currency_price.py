from db.mongodb import mongo_db_handler
from datetime import datetime
from machine.korbit_machine import KorbitMachine

if __name__ == "__main__":
    korbit = KorbitMachine()
    result_etc = korbit.get_filled_orders(currency_type="etc_krw", per="hour")
    result_eth = korbit.get_filled_orders(currency_type="eth_krw", per="hour")
    result_btc = korbit.get_filled_orders(currency_type="btc_krw", per="hour")
    result_xrp = korbit.get_filled_orders(currency_type="xrp_krw", per="hour")
    result_bch = korbit.get_filled_orders(currency_type="bch_krw", per="hour")
    result_btg = korbit.get_filled_orders(currency_type="btg_krw", per="hour")
    mongodb = mongo_db_handler.MongoDBHandler("local", "coiner", "price_info")
    result_list = result_etc + result_eth + result_btc + result_xrp + result_bch + result_btg

    print(result_list)

    if len(result_list) != 0:
        for item in result_list:
            d = datetime.fromtimestamp(item["timestamp"]/1000)
            item["year"] = d.year
            item["month"] = d.month
            item["day"] = d.day
            item["hour"] = d.hour
            item["minute"] = d.minute
            item["second"] = d.second
            item["amount"] = float(item["amount"])
            item["timestamp"] = item["timestamp"] / 1000
            item.pop("tid")
        ids = mongodb.insert_items(result_list)
        print(ids)