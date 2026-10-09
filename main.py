from banco import Banco
from cliente import Cliente
from contas import Conta, ContaCorrente, ContaInvestimento, ContaPoupanca, formatar_reais


def titulo(texto):
    print(f"\n{'=' * 78}\n{texto}\n{'=' * 78}")


def testar(descricao, acao):
    """Executa uma ação que pode falhar e mostra o resultado com try/except/else."""
    try:
        acao()
    except (ValueError, TypeError) as erro:
        print(f"  [ERRO CAPTURADO] {descricao}\n                   -> {erro}")
    else:
        print(f"  [OK] {descricao}")


def main():
    titulo("1. CRIANDO 5 CLIENTES")
    ana = Cliente("Ana Souza", "ana.souza@email.com", "123.456.789-09")
    bruno = Cliente("Bruno Lima", "bruno.lima@email.com", "111.222.333-44")
    carla = Cliente("Carla Dias", "carla_dias@empresa.com.br", "555.666.777-88")
    diego = Cliente("Diego Alves", "diego.alves@email.com", "987.654.321-00")
    elisa = Cliente("Elisa Rocha", "elisa.rocha@email.com", "321.654.987-91")
    clientes = [ana, bruno, carla, diego, elisa]
    for cliente in clientes:
        print(cliente)

    titulo("2. CRIANDO 8 CONTAS E 1 BANCO (14 objetos no total)")
    banco = Banco("Banco Maranhão")
    contas = [
        ContaCorrente(ana, 2500.00),
        ContaCorrente(bruno, 800.00, tarifa=15.0),
        ContaPoupanca(ana, 10000.00),
        ContaPoupanca(carla, 1500.00, taxa_rendimento=0.006),
        ContaPoupanca(diego, 300.00),
        ContaInvestimento(elisa, 20000.00),
        ContaInvestimento(bruno, 5000.00, taxa_rendimento=0.015),
        ContaCorrente(diego, 50.00),
    ]
    for conta in contas:
        banco.adicionar_conta(conta)
        print(conta)
    print(f"\n{banco}")

    titulo("3. POLIMORFISMO: mesma chamada, respostas diferentes")
    print(f"{'Tipo':<20} {'Rendimento':>14} {'Tarifa':>12}")
    print("-" * 48)
    for conta in banco.contas:
        rendimento = formatar_reais(conta.calcular_rendimento())
        tarifa = formatar_reais(conta.tarifa_mensal())
        print(f"{conta.TIPO:<20} {rendimento:>14} {tarifa:>12}")

    titulo("4. DEPÓSITOS E SAQUES")
    conta_ana = contas[0]
    print(f"Antes : {conta_ana}")
    conta_ana.depositar(500)
    conta_ana.sacar(200)
    print(f"Depois: {conta_ana}")


    titulo("5. FECHAMENTO DO MÊS (polimorfismo em ação)")
    resultados = banco.fechar_mes_todas()
    for conta in banco.contas:
        ganho = resultados[conta.numero]
        print(f"Nº {conta.numero} | {conta.TIPO:<19} | {ganho:+10.2f} | novo saldo: {formatar_reais(conta.saldo)}")
    print(f"\n{banco}")


    titulo("6. MÉTODOS ESPECIAIS: __lt__, __eq__ e __repr__")
    print("Contas ordenadas do maior para o menor saldo (usa __lt__):")
    for conta in sorted(banco.contas, reverse=True):
        print(f"  {conta.numero} - {conta.titular.nome:<12} {formatar_reais(conta.saldo)}")

    outra_ana = Cliente("Ana S.", "ana@outro.com", "12345678909")
    print(f"\nana == outra_ana (mesmo CPF)?  {ana == outra_ana}")
    print(f"ana == bruno?                  {ana == bruno}")
    print(f"contas[0] == contas[0]?        {contas[0] == contas[0]}")
    print(f"contas[0] == contas[1]?        {contas[0] == contas[1]}")
    print(f"\nrepr(contas[0]) = {contas[0]!r}")
    print(f"repr(ana)       = {ana!r}")
    print(f"repr(banco)     = {banco!r}")

    titulo("7. ENTRADAS INVÁLIDAS (try/except)")
    testar("Cliente com e-mail inválido", lambda: Cliente("Fulano", "fulano@", "12345678901"))
    testar("Cliente com nome vazio", lambda: Cliente("", "fulano@email.com", "12345678901"))
    testar("Cliente com CPF de 9 dígitos", lambda: Cliente("Fulano", "fulano@email.com", "123456789"))
    testar("Conta com saldo inicial negativo", lambda: ContaCorrente(ana, -100))
    testar("Conta com saldo inicial em texto", lambda: ContaPoupanca(ana, "mil reais"))
    testar("Saque maior que o saldo", lambda: contas[7].sacar(1000))
    testar("Depósito negativo", lambda: contas[0].depositar(-50))
    testar("Alterar saldo direto para negativo", lambda: setattr(contas[0], "saldo", -1))
    testar("Instanciar a classe abstrata Conta", lambda: Conta(ana))
    testar("Investimento abaixo do depósito mínimo", lambda: ContaInvestimento(ana, 100))
    testar("Adicionar conta repetida no banco", lambda: banco.adicionar_conta(contas[0]))
    testar("Adicionar algo que não é conta", lambda: banco.adicionar_conta("não sou conta"))

    print("\nO objeto continua válido depois do erro?")
    testar("Trocar e-mail da Ana para 'ana@'", lambda: setattr(ana, "email", "ana@"))
    print(f"  E-mail da Ana continua: {ana.email}")


if __name__ == "__main__":
    main()