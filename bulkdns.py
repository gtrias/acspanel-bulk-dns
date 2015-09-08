import requests, json
from flask import Flask, config, render_template, url_for, request

app = Flask(__name__)
app.config.from_object('config')

def get_domains():
    r = requests.get(app.config["DNSDOMAINSURL"], auth = (app.config['USER'], app.config['PASSWORD']))
    dnsdomains = json.loads(r.text)
    return dnsdomains


@app.route("/")
def get_dns_domains():
    dnsdomains = get_domains()

    return render_template('dnsdomains.html',
            dnsdomains = dnsdomains,
            process_link = url_for("create_bulk_dnsrecords")
        )

@app.route("/create-bulk-dnsrecords", methods=['POST'])
def create_bulk_dnsrecords():
    dnsdomains = get_domains()

    print(request.form)

    for dnsdomain in dnsdomains:
        dnsrecord = {"dnsrecordtype": {
            "name": request.form.get('name'),
            "type": request.form.get('type'),
            "content": request.form.get('content'),
            "ttl": request.form.get('ttl'),
            "prio": request.form.get('prio'),
            "dns_domain": dnsdomain["id"]
            }
        }
        print(dnsrecord)
        r = requests.post(app.config['DNSRECORDCREATEURL'], data = json.dumps(dnsrecord),  auth = (app.config['USER'], app.config['PASSWORD']))
        if (r.status_code > 201):
            print(r.text)
            return "Quelcom ha fallat amb la creació dels registres"
        else:
            print(r.text)
        # print(r.url)
    return "Tots els registres creats"

if __name__ == "__main__":
    app.run(debug = True)
