import requests
import json
import time

# --- CONFIGURAÇÕES ---
TOKEN = "b8ad37b5-67e9-485c-acab-ca7a657090f2"  # Verifique se o token ainda é o mesmo
ARQUIVO_SAIDA = "artigos_movidesk.json"


LISTA_DE_IDS = [
    551342,
    382259,
    123456,
    553732,
552295,
552283,
551342,
549123,
549113,
545088,
545081,
542294,
540901,
540741,
535331,
535031,
534770,
534371,
532878,
532701,
531946,
531905,
527637,
527394,
526187,
526182,
525273,
525124,
524512,
520637,
514332,
514329,
512752,
512743,
512740,
512731,
512727,
511873,
503742,
503735,
502190,
501916,
498480,
498466,
498441,
497559,
495387,
494625,
488361,
481672,
481665,
476297,
474681,
474320,
471623,
471620,
471619,
471614,
471605,
471603,
469958,
466730,
466604,
465801,
464712,
464711,
462438,
462249,
462207,
462200,
462132,
462067,
458694,
458561,
458187,
458163,
458071,
457707,
457602,
457312,
457247,
457245,
457225,
457104,
456627,
456289,
456286,
456284,
456274,
455767,
455750,
455618,
455293,
455283,
453824,
451576,
449478,
449153,
449126,
448564,
448551,
448547,
447773,
447632,
447377,
446595,
445642,
444400,
443874,
443711,
441461,
441453,
441384,
441382,
441336,
441311,
441298,
441293,
440855,
440852,
440629,
439892,
439690,
439689,
438961,
438560,
438145,
435547,
434602,
434571,
432965,
431742,
431741,
431740,
431739,
431737,
431734,
430184,
430182,
430180,
429910,
429908,
429905,
429904,
429869,
429868,
429867,
429866,
429864,
429863,
429860,
426870,
426869,
426868,
426866,
426865,
426862,
426861,
426860,
426859,
426857,
426856,
426855,
426853,
426852,
426849,
426840,
426839,
426838,
426836,
426832,
426830,
426828,
426824,
426823,
426814,
426792,
426711,
426179,
425946,
424766,
422216,
421725,
421613,
421538,
419712,
419249,
419086,
418777,
415379,
414818,
414041,
413990,
412161,
410433,
409123,
409102,
409094,
23068,
23066,
23065,
20223,
19202,
19176,
18641,
18223,
18039,
18035,
17944,
17870,
17771,
17746,
17625,
17606,
17605,
17598,
17582,
17421,
17132,
17113,
17106,
17028,
17013,
16963,
16956,
16945,
16933,
16930,
16920,
16905,
16898,
16796,
16789,
16787,
16752,
7116,
6493
   
]


# --- LÓGICA DO SCRIPT ---
base_url = "https://api.movidesk.com/public/v1/article/"
artigos_encontrados = []
total_ids = len(LISTA_DE_IDS)

print(f"--- INICIANDO BUSCA DE {total_ids} ARTIGOS ESPECÍFICOS ---")

try:
    # Loop 'for' que passa por cada ID da sua lista
    for i, id_atual in enumerate(LISTA_DE_IDS):
        url_completa = f"{base_url}{id_atual}?token={TOKEN}"

        # Imprime o progresso (ex: "Processando 1/150...")
        print(f"Processando {i + 1}/{total_ids} - Tentando ID: {id_atual}...")

        response = requests.get(url_completa)

        if response.status_code == 200:
            artigo_json = response.json()
            info_artigo = {
                "id": artigo_json.get("id"),
                "title": artigo_json.get("title"),
                "categories": [cat.get("name") for cat in artigo_json.get("categories", [])],
                "contentText": artigo_json.get("contentText")
            }
            artigos_encontrados.append(info_artigo)
            print(f"  -> SUCESSO! Artigo '{info_artigo['title']}' encontrado.")

        elif response.status_code == 404:
            print(f"  -> AVISO: O artigo com ID {id_atual} não foi encontrado (404).")
        else:
            print(f"  -> ERRO! Status: {response.status_code}, Resposta: {response.text}")

        # !!! PAUSA OBRIGATÓRIA PARA RESPEITAR O LIMITE DA API !!!
        if i < total_ids - 1: # Não precisa esperar depois do último item
            time.sleep(7)

except KeyboardInterrupt:
    print("\nProcesso interrompido pelo usuário.")

finally:
    if artigos_encontrados:
        print(f"\n--- FIM DA BUSCA ---")
        print(f"Total de {len(artigos_encontrados)} artigos encontrados e salvos.")
        with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
            json.dump(artigos_encontrados, f, ensure_ascii=False, indent=4)
        print(f"✅ Dados salvos com sucesso no arquivo: {ARQUIVO_SAIDA}")
    else:
        print("\nNenhum dos artigos da lista foi encontrado.")