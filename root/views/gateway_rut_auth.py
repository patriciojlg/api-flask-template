import logging
from flask import request, render_template
import requests
import datetime
from flask.views import View
from root.utils.conexion_mongo import create_user_conexion


db = create_user_conexion()

class UriOauthCentry(View):
    def dispatch_request(self):
        code = request.args.get("code")
        logging.debug("Ingrescon code "+str(code))
        ip = request.remote_addr
        print("IP ="+str(ip))
        # Obtengo credenciales, con el master app
        credenciales = db.cred_centry.find_one(
            {"grant_type": "authorization_code"})

        url = ("https://www.centry.cl/oauth/token?client_id="+credenciales["client_id"] +
            "&client_secret="+credenciales["client_secret"] +
            "&redirect_uri="+credenciales["redirect_uri"] +
            "&grant_type="+credenciales["grant_type"] +
            "&code="+code)
        # genero token
        integrar = requests.post(url=url)
        # Inserto al nuevo usuario
        integrar = integrar.json()
        integrar["code"] = code
        # registro el datetime.now() para gestionar el refresh del token
        integrar["last_refresh"] = datetime.datetime.now()

        print("Datos de integracion: "+str(integrar))

        headers = {
            'Authorization': 'Bearer '+integrar["access_token"],
            'Content-Type': 'application/json'
        }
        # obteniendo el id_company
        url_company = "https://www.centry.cl/conexion/v1/company_info.json"
        company_json = requests.get(url=url_company, headers=headers)
        company_id = company_json.json()["_id"]

        integrar["company_id"] = company_id
        print("estos es company id:" + str(company_id))
        message = {
            "Mensaje": "Integración satisfactoria. Muchas gracias por preferir Contaline."
        }
        # Busco si ya existe la empresa
        existe = db.user_centry.find_one({"company_id": company_id})

        if existe == None:
            datos_de_db = db.user_centry.insert_one(integrar)
        else:
            datos_de_db = db.user_centry.update_one(
                {"company_id": company_id}, {"$set": integrar})
        print(datos_de_db)
        return render_template("index.html", company_id=company_id, code=integrar["code"])
