1. Título
Simulação do Jantar dos Filósofos: Uma Abordagem sobre Concorrência e Sincronização em Python

2. Contexto inicial do trabalho (introdução)
O problema do "Jantar dos Filósofos" foi proposto por Edsger Dijkstra em 1965 como um exercício de sincronização de processos. O cenário envolve cinco filósofos sentados à mesa, onde cada um alterna entre pensar e comer. Entre cada filósofo existe um único talher, mas para comer, um filósofo precisa de dois talheres (o da esquerda e o da direita).

Este problema ilustra os desafios fundamentais da computação paralela:

Exclusão Mútua: Dois filósofos vizinhos não podem usar o mesmo talher simultaneamente.

Deadlock (Impasse): Situação onde todos pegam um talher e ninguém consegue o segundo, travando o sistema.

Starvation (Inanição): Quando um filósofo nunca consegue acesso aos recursos para comer.

3. Descrevendo a solução em python para o jantar dos filósofos
Implementando o algoritmo
O algoritmo segue o ciclo de vida clássico de uma thread:

Pensar: O filósofo aguarda um tempo aleatório.

Tentar pegar talheres: Solicita acesso aos recursos compartilhados (Locks).

Comer: Utiliza os recursos por um tempo determinado.

Devolver talheres: Libera os recursos para os vizinhos.

Qual o algoritmo utilizado
Foi utilizado o algoritmo de Ordenação de Recursos (Hierarquia). Em vez de todos os filósofos tentarem pegar primeiro o talher à esquerda (o que causaria Deadlock se todos fizessem ao mesmo tempo), os filósofos são diferenciados por sua posição (ID par ou ímpar).

Implementação do algoritmo em python
A implementação utiliza a biblioteca threading. Cada filósofo é uma instância da classe Filosofo, que herda de threading.Thread. Os talheres são representados por objetos threading.Lock(), garantindo que apenas um filósofo segure um determinado talher por vez.

Python
# Trecho principal da lógica de execução
while self.refeicoes < self.max_refeicoes:
    self.pensar()
    self.pegar_talheres()
    try:
        self.comer()
    finally:
        self.devolver_talheres()
4. Tratando impasse
Qual a estratégia de tratamento de impasses
A estratégia escolhida foi a Quebra da Espera Circular. Em um cenário ingênuo, se todos os 5 filósofos pegarem o talher à esquerda simultaneamente, todos ficarão esperando o talher à direita para sempre.

Para evitar isso, implementamos uma lógica de assimetria:

Filósofos com ID par tentam pegar primeiro o talher da esquerda.

Filósofos com ID ímpar tentam pegar primeiro o talher da direita.

Isso garante que, em qualquer situação de disputa, pelo menos um filósofo conseguirá obter os dois talheres, pois a ordem de aquisição dos recursos não é idêntica para todos.

Implementação do tratamento de impasse em python
No método pegar_talheres, a lógica condicional altera a prioridade do acquire():

Python
if self.philosopher_id % 2 == 0:
    primeiro_talher = self.talher_esquerdo
    segundo_talher = self.talher_direito
else:
    primeiro_talher = self.talher_direito
    segundo_talher = self.talher_esquerdo

primeiro_talher.acquire()
segundo_talher.acquire()
5. Executar o código e descrever comportamento observado
Ao executar o script src/jantar_filosofos.py, observa-se que as threads iniciam de forma assíncrona. O log no console mostra o revezamento: enquanto o Filósofo 0 está comendo, seus vizinhos (1 e 4) permanecem pensando ou aguardando o primeiro talher.

O comportamento é fluido e não ocorre travamento, comprovando a eficácia da quebra de espera circular. O programa encerra com sucesso após todos os filósofos completarem o número máximo de refeições definido.

6. Considerações finais
O projeto demonstrou na prática como gerenciar recursos compartilhados em sistemas multithread. O uso de Locks resolveu a exclusão mútua, enquanto a lógica de alternância entre IDs pares e ímpares foi uma solução elegante e de baixo custo computacional para evitar o Deadlock, sem a necessidade de um coordenador central (árbitro).