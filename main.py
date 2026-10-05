from cadastro import (
    criar_catalogo_padrao,
    cadastrar_equipamento,
    criar_imovel,
    adicionar_item_imovel,
    formatar_relatorio,
)











def executar_sistema() -> None:
    catalogo = criar_catalogo_padrao()

    print("--- CADASTRO DO IMÓVEL ---")
    identificador = input("Identificador do imóvel (ex: Apto 101): ").strip()
    responsavel = input("Nome do responsável: ").strip()
    endereco = input("Endereço: ").strip()

    imovel = {
        "identificador": identificador,
        "responsavel": responsavel,
        "endereco": endereco,
        "itens": []
    }

    while True:
        print("\n--- EQUIPAMENTOS DISPONÍVEIS ---")
        for id_eq, eq in catalogo.items():
            print(f"[{id_eq}] {eq['nome']:<25} | Categoria: {eq['categoria']:<15} | {eq['potencia_w']} W")
        print("[0] Finalizar e gerar relatório")
        print("[-1] Cadastrar novo equipamento no catálogo")

        entrada = input("\nSelecione o código desejado: ").strip()
        try:
            opcao = int(entrada)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue

        if opcao == 0:
            break

        if opcao == -1:
            nome = input("Nome do novo equipamento: ").strip()
            categoria = input("Categoria: ").strip()
            try:
                potencia = float(input("Potência nominal (W): "))
                if potencia <= 0:
                    print("A potência deve ser maior que zero.")
                    continue
            except ValueError:
                print("Valor de potência inválido.")
                continue

            novo_id = cadastrar_equipamento(catalogo, nome, categoria, potencia)
            print(f"Equipamento '{nome}' cadastrado com código [{novo_id}].")
            continue

        if opcao not in catalogo:
            print("Código não encontrado no catálogo.")
            continue

        try:
            qtd = int(input(f"Quantidade de '{catalogo[opcao]['nome']}': "))
            horas = float(input("Média diária de uso (horas/dia): "))

            if qtd <= 0:
                print("A quantidade deve ser maior que zero.")
                continue
            if horas < 0 or horas > 24:
                print("O tempo de uso deve estar entre 0 e 24 horas.")
                continue

            imovel["itens"].append({
                "equipamento": catalogo[opcao],
                "quantidade": qtd,
                "horas_dia": horas
            })
            print("Item adicionado ao imóvel.")
        except ValueError:
            print("Entrada numérica inválida.")

    print("\n" + formatar_relatorio(imovel))


if __name__ == "__main__":
    executar_sistema()