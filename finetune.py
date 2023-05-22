import requests
import openai
import argparse
import json

openai.api_key = "gdfgrdvgsdvs api"

def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    print(resp)
    return resp

def file_list():
    resp = openai.File.list()
    print(resp)

def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    print(resp.json())

def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    print(resp.json())

def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)
    print(resp.json())

def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % openai.api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)
    print(resp.json())

def create_jsonl_file(prompts, filename):
    with open(filename, 'w') as outfile:
        for prompt in prompts:
            json.dump(prompt, outfile)
            outfile.write('\n')

def main():
    prompts = [
        {"prompt": "Sobre integração digital - Listagem de usinas> ->", "completion": " <Essa funcionalidade tem como objetivo realizar a ressincronização das integrações do portal terceiro para que elas sejam exibidas no portal da SolarView. Isso reduz o tempo de carregamento da tela de integração para integradores com muitas unidades."},
        {"prompt": "Como realizar uma ressincronização?> ->", "completion": " Você pode realizar a ressincronização das usinas seguindo estes passos: 1) Na tela de integração, acesse o menu de ações de uma integração e selecione a opção 'Usinas'. 2) No modal da integração, escolha a opção 'Ressincronizar as unidades'."},
        {"prompt": "Como confirmar uma ressincronização? ->", "completion": " Quando o botão 'Ressincronizar' for acionado, um modal de confirmação será aberto."},
        {"prompt": "Onde encontrar as unidades após a ressincronização? ->", "completion": " Após confirmar a ressincronização, as unidades que antes não eram listadas serão exibidas na aba 'Unidades novas'. Você poderá selecioná-las para monitoramento ou não."},
        {"prompt": "Quantas ressincronizações posso realizar por dia? ->", "completion": " O limite diário de ressincronizações por credencial é 3. Essas ressincronizações são renovadas no dia seguinte. O modal informará quando a quantidade de ressincronizações para uma determinada credencial estiver esgotada."},
        {"prompt": "Posso realizar mais de uma ressincronização por vez? ->", "completion": " Sim, você pode realizar a ressincronização das unidades de outras credenciais ao mesmo tempo, desde que não exceda o limite diário. Assim, a ressincronização poderá ser realizada."},
        {"prompt": "É necessário realizar esse processo toda vez que quero listar uma nova unidade? ->", "completion": " Não, todos os dias, às 22h, fazemos a coleta geral das unidades no portal terceiro e as armazenamos em nossa base de dados. No entanto, se for necessário listar unidades antes dessa coleta geral, você pode realizá-la a qualquer hora."}
    ]

    create_jsonl_file(prompts, 'prompts.jsonl')

    file_upload('prompts.jsonl')

    if args.list:
        file_list()
        finetune_list()
    
    # Adjust the model here
    file_id = "file-2ycTOdwa2HsmPt9LlL0mZ6UQ"
    suffix = "<my-finetuned-model>"
    finetune_model(file_id, suffix)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare data for fine-tuning GPT-3 model')
    parser.add_argument('--list', action='store_true', help='List fine-tuned models and events')
    args = parser.parse_args()

    main()
