import requests
import click
from pymongo import MongoClient
import datetime
import json
import pprint

db = MongoClient().users


@click.group()
def cli():
    pass


@click.command()
@click.option("--users")
def users(users):
    users = db.user_centry.find()
    for u in users:
        print(u)


@click.command()
def creds():
    creds = db.cred_centry.find()
    for c in creds:
        print(c)


@click.command()
def ws_users():
    ws_users = db.ws_users.find()
    for w in ws_users:
        print(w)


@click.command()
def orders_procesed():
    orders = db.orders.find()
    for o in orders:
        print(o)


@click.command()
def welcome():
    click.echo('Welcome')


@click.command()
def cred_centry_b():
    credb = db.users.cred_centry.find()
    for b in credb:
        print(b)


@click.command()
@click.option("--company_id")
def refresh_token_centry(company_id):
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    if company_id == "" or company_id == None:
        print(
            str({ERROR: "Se debe especificar el company_id para poder refrescar el token"}))
        return False

    credenciales = db.user_centry.find_one({"company_id": company_id})
    try:
        assert len(credenciales) > 0
    except IOError:
        return {ERROR: "No existe usuario con company_id: "+str(company_id)}

    headers = {'Content-Type': 'application/json'}

    url = ("https://www.centry.cl/oauth/token?client_id=d7071e388044a3c612ce7a1a5551c8021996344fff6438ae0540e1f97921f09d" +
           "&client_secret=aa6f9118852ef4da6b69216a4eb77070dee1f5c8ba156528d714c45216fc9e42" +
           "&redirect_uri=http://200.29.191.252:8080/uri-oauth-centry" +
           "&grant_type=refresh_token" +
           "&refresh_token="+credenciales["refresh_token"])

    refreshing_token = requests.post(url=url, headers=headers)

    if refreshing_token.status_code == 200:
        refresh_dict = refreshing_token.json()
        refresh_dict["last_refresh"] = datetime.datetime.now()
        # Update database
        db.user_centry.update_one(
            {"company_id": company_id}, {"$set": refreshing_token.json()})
        out = {SUCCESS: "Token refrescado con éxito"}
        print(out)
    else:
        print("OUCH!")
        out = {ERROR: "Pucha algo pasó y no se pudo refrescar el token error: " +
               str(refreshing_token.status_code)}
        print(out)




@click.command()
@click.option("--company_id")
def showproducts(company_id):
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    if company_id == "" or company_id == None:
        print(
            str({ERROR: "Se debe especificar el company_id para poder refrescar el token"}))
        return False
    get_data_token = db.user_centry.find_one({"company_id": company_id})
    token = get_data_token["access_token"]
    url = "https://www.centry.cl/conexion/v1/products.json"
    headers = {"Authorization": "Bearer "+token}
    product_from_api = requests.get(url=url, headers=headers)
    products = product_from_api.json()
    print(str(products))

@click.command()
@click.option("--company_id")
def webhooks(company_id):
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    if company_id == "" or company_id == None:
        print(
            str({ERROR: "Se debe especificar el company_id para poder refrescar el token"}))
        return False
    get_data_token = db.user_centry.find_one({"company_id": company_id})
    token = get_data_token["access_token"]
    url = "https://www.centry.cl/conexion/v1/webhooks.json" 
    headers = {"Authorization": "Bearer "+token}
    webhook_from_api = requests.get(url=url, headers=headers)
    webhooks = webhook_from_api.json()
    print(str(webhooks))
    
@click.command()
@click.option("--company_id")
def orders(company_id):
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    if company_id == "" or company_id == None:
        print(
            str({ERROR: "Se debe especificar el company_id para poder refrescar el token"}))
        return False
    get_data_token = db.user_centry.find_one({"company_id": company_id})
    token = get_data_token["access_token"]
    url = "https://www.centry.cl/conexion/v1/orders.json" 
    headers = {"Authorization": "Bearer "+token}
    orders_on_api = requests.get(url=url, headers=headers)
    orders = orders_on_api.json()
    order_ids = []
    for i in orders:
        order_ids.append(i["_id"])
    pprint.pprint(order_ids)        

cli.add_command(orders_procesed)
cli.add_command(refresh_token_centry)
cli.add_command(cred_centry_b)
cli.add_command(users)
cli.add_command(orders)
cli.add_command(creds)
cli.add_command(ws_users)
cli.add_command(showproducts)
cli.add_command(webhooks)

if __name__ == '__main__':
    cli()
