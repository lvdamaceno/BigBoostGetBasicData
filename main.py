import requests
import pandas as pd
import variables as v
import os.path
import time


def get_data(url, q, dataset):
    payload = {
        "Datasets": dataset,
        "q": q
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AccessToken": v.AccessToken,
        "TokenId": v.TokenId
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    return response_json


def get_basic_data(cpf):
    url = "https://plataforma.bigdatacorp.com.br/pessoas"
    q = f"doc{{{cpf}}}"
    dataset = 'registration_data'
    json = get_data(url, q, dataset)
    name = json['Result'][0]['RegistrationData']['BasicData']['Name']
    gender = json['Result'][0]['RegistrationData']['BasicData']['Gender']
    birthdate = json['Result'][0]['RegistrationData']['BasicData']['BirthDate']
    return [name, gender, birthdate]


if __name__ == '__main__':
    # df = pd.read_csv('leads.csv', nrows=1)
    df = pd.read_csv('leads.csv')
    df['CPF'] = df["CPF"].apply(str)
    df['Nome Completo'] = df["Nome Completo"].apply(str)

    names = []
    genders = []
    birthdates = []
    for cpf in df['CPF']:
        print(cpf, get_basic_data(cpf)[0], get_basic_data(cpf)[1], get_basic_data(cpf)[2])
        names.append(get_basic_data(cpf)[0])
        genders.append(get_basic_data(cpf)[1])
        birthdates.append(get_basic_data(cpf)[2])

    edit_birthdates = []
    for date in birthdates:
        ts = time.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
        edit_birthdates.append(time.strftime("%d/%m/%Y", ts))

    df['Nome Completo'] = names
    df['Sexo'] = genders
    df['Data Nascimento'] = edit_birthdates

    path = './leads_data.csv'
    if os.path.exists(path):
        os.remove(path)
    df.to_csv('leads_data.csv')
    print('Arquivo salvo')

