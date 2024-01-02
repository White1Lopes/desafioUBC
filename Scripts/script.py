import pandas as pd
from pysolr import Solr
from datetime import datetime
import time
import logging
import os

def create_dir():
    # Especifique o caminho da pasta que você deseja criar
    urlData = 'SolrData/'
    urlLogs = 'Logs/'

    if not os.path.exists(urlData):
        os.mkdir(urlData)

    if not os.path.exists(urlLogs):
        os.mkdir(urlLogs)

def configure_logging():
  data_e_hora_atual = datetime.now()
  formato_data_hora = '%Y-%m-%d_%H-%M-%S'
  data_e_hora_formatadas = data_e_hora_atual.strftime(formato_data_hora)

  logging.basicConfig(filename= f'Logs/students_log_{data_e_hora_formatadas}.log', level=logging.INFO)

def wait_for_docker():
    docker_running = os.environ.get('docker_running', False)
    if docker_running == "True":
        time.sleep(5)

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def transform_data(dataframe):
    dataframe["Data de Nascimento"] = pd.to_datetime(dataframe["Data de Nascimento"])
    dataframe.drop_duplicates(inplace=True)
    return dataframe

def create_solr_instance(base_url, core_uri):
    url_solr = base_url + core_uri
    return Solr(url_solr, always_commit=True, timeout=10)

def add_documents_to_solr(solr, dataframe):
    documents = []
    for index, row in dataframe.iterrows():
        data_nascimento = row['Data de Nascimento'].strftime('%Y-%m-%dT%H:%M:%SZ')

        documento_solr = {
            'Nome': row['Nome'],
            'Idade': row['Idade'],
            'Serie': row['Série'],
            'Nota_Media': row['Nota Média'],
            'Endereco': row['Endereço'],
            'Nome_do_Pai': row['Nome do Pai'],
            'Nome_da_Mae': row['Nome da Mãe'],
            'Data_de_Nascimento': data_nascimento
        }

        documents.append(documento_solr)

    solr.add(documents)
    solr.commit()

def main():
  try:
    create_dir()
    configure_logging()
    wait_for_docker()

    base_url = os.environ.get('base_url', 'http://localhost:8983')
    core_uri = os.environ.get('core_Uri', '/solr/students')
    file_path = os.environ.get('file_Path', './Dataset/aluno.csv')

    data_csv = read_csv_file(file_path)
    transformed_data = transform_data(data_csv)

    solr_instance = create_solr_instance(base_url, core_uri)
    add_documents_to_solr(solr_instance, transformed_data)

    logging.info("Script executado com sucesso!")

  except Exception as e:
    logging.error(f"Erro: {e}")

if __name__ == "__main__":
    main()

