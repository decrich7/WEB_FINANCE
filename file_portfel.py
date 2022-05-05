import csv


def csv_file(name, data, id_stoks):
    sharp_keys = data['stoks']['sharp']['stoks_and_count'].keys()
    volatility_keys = data['stoks']['volatility']['stoks_and_count'].keys()
    path_stoks = f"portfolio_stoks_{name}_{id_stoks}.csv"
    with open(f'static/csv_port/{path_stoks}', 'w') as f:
        spamwriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["sharp_balance", *sharp_keys,
                             "volatility_balance", *volatility_keys])
        spamwriter.writerow([data['stoks']['sharp']["balance"],
                             *data['stoks']['sharp']['stoks_and_count'].values(),
                             data['stoks']['volatility']["balance"],
                             *data['stoks']['volatility']['stoks_and_count'].values()])




