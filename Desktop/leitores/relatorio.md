Problema dos Leitores e Escritores - Estacionamento
1. Introdução
Este projeto apresenta uma solução para o clássico problema de concorrência "Leitores/Escritores", aplicado ao cenário de gerenciamento de vagas de um estacionamento. O sistema utiliza uma arquitetura cliente-servidor para gerenciar 10 vagas sendo disputadas simultaneamente por 50 clientes. O foco principal é garantir que as operações de escrita (ocupar e liberar vaga) sejam feitas com exclusão mútua, evitando condições de disputa.

2. Solução em Python
A implementação foi dividida em dois componentes principais:

Servidor (server.py): Utiliza a biblioteca socket para escutar conexões e threading para tratar cada cliente em uma thread separada. Ele mantém o estado global das vagas e utiliza mecanismos de sincronização.

Cliente (cliente.py): Simula o comportamento de um motorista. O cliente realiza três operações: consulta a disponibilidade, tenta ocupar a vaga e, após um tempo aleatório (simulando o uso da vaga), libera o recurso.

3. Tratamento de Impasse (Deadlock) e Condição de Corrida
Estratégia de Tratamento
A principal estratégia adotada foi a Exclusão Mútua (Mutex). Em sistemas concorrentes, um impasse (deadlock) geralmente ocorre quando há dependência circular de recursos. Como este sistema gerencia apenas um recurso compartilhado (o contador de vagas), o risco mitigado foi a Condição de Corrida (onde dois processos leem o mesmo estado e tentam subtrair a vaga simultaneamente).

Implementação em Python
Para prevenir inconsistências, foi utilizado um objeto threading.Lock() no servidor. Este lock garante que a "Seção Crítica" do código seja atômica.

Python
vagas_lock = threading.Lock()

# Dentro da função de tratamento no servidor:
with vagas_lock:
    if comando == 'pegar_vaga' and vagas_disponiveis > 0:
        vagas_disponiveis -= 1
        resposta = "1"
4. Comportamento Observado
Durante a execução com 50 clientes simultâneos, o padrão observado nos logs validou a eficácia da solução:

Concorrência de Leitura: Múltiplos clientes consultaram o servidor quase no mesmo instante e receberam o valor "10". Isso demonstra que as threads de leitura não bloqueiam o sistema desnecessariamente.

Efeito de Sincronização: Embora muitos tenham lido que havia vaga, apenas os 10 primeiros que tiveram suas requisições de escrita processadas pelo Lock conseguiram a confirmação ("Estacionou com sucesso! ✅").

Tratamento de Lotação: Do 11º cliente em diante, o servidor negou o acesso à vaga consistentemente até que houvesse uma liberação.

Liberação Dinâmica: Após o tempo de permanência aleatório (time.sleep), as threads liberaram as vagas com sucesso, permitindo que o contador voltasse a subir de forma íntegra.

5. Considerações Finais
A atividade demonstrou com sucesso como protocolos de comunicação via Sockets podem ser integrados com mecanismos de sincronização de threads. A implementação garantiu que, mesmo sob alta carga (50 requisições disputando 10 recursos), o estado do estacionamento permaneceu íntegro, provando a robustez do uso de travas remotas em sistemas distribuídos.