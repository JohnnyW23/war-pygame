def gerar_evento(exercito, poder_do_round, clima_jogo):
        from modules.objetos.evento import Evento
        from random import choices, choice
        from math import ceil

        ataque = [
            Evento(
                exercito,
                "ataque",
                f"{exercito.nome} lança uma série de misseis contra as tropas de {exercito.inimigo.nome}.",
                "O ataque é bem-sucedido, causando danos significativos.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                f"O ataque falha, seguido de uma forte retaliação de {exercito.inimigo.nome}.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),
            Evento(
                exercito,
                "ataque",
                f"{exercito.nome} tenta uma ofensiva terrestre contra {exercito.inimigo.nome}.",
                "A ofensiva é bem-sucedida, conquistando território inimigo.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                f"A ofensiva é repelida, resultando em baixas para o exército atacante.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),
            Evento(
                exercito,
                "ataque",
                f"{exercito.nome} realiza um ataque aéreo contra {exercito.inimigo.nome}.",
                "O ataque aéreo é bem-sucedido, destruindo alvos estratégicos inimigos.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                f"O ataque aéreo falha, e algumas aeronaves de {exercito.nome} são abatidas.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),
            Evento(
                exercito,
                "ataque",
                f"Embarcações de {exercito.nome} iniciam uma ofensiva contra as frotas de {exercito.inimigo.nome}.",
                "O ataque naval é bem-sucedido, destruindo grande parte dos navios inimigos.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                f"O ataque naval falha, resultando em perdas para o exército atacante.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),
            Evento(
                exercito,
                "ataque",
                f"{exercito.nome} e {exercito.inimigo.nome} iniciam um confronto direto na fronteira.",
                f"O confronto direto é vencido por {exercito.nome}, causando grandes perdas ao inimigo.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                f"O confronto direto é vencido por {exercito.inimigo.nome}, causando grandes perdas ao exército atacante.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            )
        ]

        sorte = [
            Evento(
                exercito,
                "sorte", 
                f"{exercito.nome} encontra um depósito militar abandonado.",
                f"O depósito contém equipamentos valiosos, fortalecendo as tropas de {exercito.nome}.",
                lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                f"O depósito está deteriorado e parte do equipamento explode acidentalmente.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Um informante aparece oferecendo dados sigilosos a {exercito.nome}.",
                f"As informações revelam vulnerabilidades do inimigo, aumentando a vantagem estratégica.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"O informante era falso e espalha desinformação, confundindo {exercito.nome}.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} desenvolve um protótipo de IA integrado a sistemas bélicos.",
                f"O protótipo funciona, elevando o nível tecnológico de {exercito.nome}.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"O protótipo falha e corrompe dados de alguns sistemas.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Forças aliadas auxiliam {exercito.nome} com novos soldados.",
                f"As tropas adicionais elevam a moral e o poder militar de {exercito.nome}.",
                lambda: (setattr(exercito, 'forca', ceil(exercito.forca + poder_do_round / 2)),
                        setattr(exercito, 'moral', ceil(exercito.moral + poder_do_round / 2))),
                f"Os reforços estavam mal treinados e atrapalham a organização de {exercito.nome}.",
                lambda: (setattr(exercito, 'forca', ceil(exercito.forca - poder_do_round / 2)),
                        setattr(exercito, 'moral', ceil(exercito.moral - poder_do_round / 2)))
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} recupera uma caravana de suprimentos extraviada.",
                f"Os suprimentos fortalecem as reservas e apoiam as operações militares.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                f"Parte da caravana estava contaminada e inutilizável.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Um comandante renomado oferece seus serviços a {exercito.nome}.",
                f"A liderança dele melhora a estratégia e a moral das tropas.",
                lambda: (setattr(exercito, 'estrategia', ceil(exercito.estrategia + poder_do_round / 2)),
                        setattr(exercito, 'moral', ceil(exercito.moral + poder_do_round / 2))),
                f"O comandante era incompetente e causa confusão nas fileiras.",
                lambda: (setattr(exercito, 'estrategia', ceil(exercito.estrategia - poder_do_round / 2)),
                        setattr(exercito, 'moral', ceil(exercito.moral - poder_do_round / 2)))
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Uma equipe brilhante de engenheiros desenvolve novos aparatos para {exercito.nome}.",
                f"Os engenheiros criam melhorias rápidas nos equipamentos e sistemas de {exercito.nome}.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"Os engenheiros acabam causando mais problemas do que soluções.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} abre caminho para uma nova rota de suprimentos.",
                f"A rota fornece recursos que fortalecem as operações militares.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                f"A rota estava comprometida e os suprimentos são emboscados.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"O Presidente da nação de {exercito.nome} dirige um grande discurso para suas tropas.",
                f"As palavras fortalecem o espírito das tropas e revitalizam a moral.",
                lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                f"O discurso é mal interpretado e causa confusão entre os soldados.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Uma equipe científica oferece um novo algoritmo tático para {exercito.nome}.",
                f"O algoritmo otimiza estratégias e aumenta o desempenho em combate.",
                lambda: (setattr(exercito, 'forca', exercito.forca + poder_do_round),
                        setattr(exercito, 'estrategia', ceil(exercito.estrategia + poder_do_round / 2))),
                f"O algoritmo contém erros críticos, prejudicando o combate e planejamento.",
                lambda: (setattr(exercito, 'forca', exercito.forca - poder_do_round),
                        setattr(exercito, 'estrategia', ceil(exercito.estrategia - poder_do_round / 2)))
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Guerrilheiros se juntam a {exercito.nome} para combater o inimigo.",
                f"A ajuda dos civis traz suprimentos e aumenta a moral das tropas.",
                lambda: (setattr(exercito, 'suprimentos', ceil(exercito.suprimentos + poder_do_round / 2)),
                        setattr(exercito, 'moral', ceil(exercito.moral + poder_do_round / 2))),
                f"A ajuda dos civis atrapalha e desorganiza a logística das tropas.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} encontra uma arma experimental inimiga em meio ao campo de batalha.",
                f"A arma é muito eficaz e aumenta drasticamente o poder de fogo.",
                lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                f"A arma continha rastreador e escuta, revelando locais e estratégias da tropa.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} encontra um manual de estratégia militar do inimigo.",
                f"As táticas descritas aprimoram o planejamento de batalha.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"O manual contém táticas ultrapassadas que causam desorganização.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} consegue reativar uma fábrica obsoleta de armamentos.",
                f"A produção improvisada reforça o poder militar.",
                lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                f"A fábrica contém falhas estruturais e acaba inutilizável.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"Tropas de {exercito.nome} recebem uma remessa de mantimentos das forças aliadas.",
                f"Os mantimentos melhoram a eficiência das tropas.",
                lambda: (setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round)),
                f"A remessa estava estragada e causa problemas logísticos.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),
            Evento(
                exercito, 
                "sorte", 
                f"{exercito.nome} consegue decodificar arquivos de dados pré-guerra.",
                f"Os arquivos revelam técnicas úteis e melhoram o conhecimento tecnológico.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"Os dados estavam comprometidos e comprometem sistemas internos.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            )
        ]

        melhoria = [
            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} desenvolve um novo programa intensivo de treinamento militar.",
                f"O treinamento aumenta significativamente a força de combate de {exercito.nome}.",
                lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                f"O treinamento é mal executado e causa exaustão nas tropas.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} começa a testar em campo equipamentos modernizados.",
                f"A modernização aumenta o nível tecnológico de {exercito.nome}.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"A modernização apresenta falhas táticas, necessitando de revisão.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} lança uma campanha de motivação entre as tropas.",
                f"A moral das tropas aumenta consideravelmente.",
                lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                f"A campanha não surte efeito e gera desconfiança.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} realiza uma operação de reorganização estratégica.",
                f"A coordenação e estratégia melhoram significativamente.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"A reorganização causa conflitos internos.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} decide otimizar linhas de suprimentos.",
                f"A eficiência logística aumenta e suprimentos são economizados.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                f"A otimização é mal planejada e gera desperdício.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} realiza testes de novas táticas de combate.",
                f"As tropas assimilam as táticas e ganham eficiência.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"As táticas se mostram confusas e ineficazes.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} reorganiza o setor de manutenção de equipamentos.",
                f"A manutenção eficaz aumenta o poder tecnológico das tropas.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"A reorganização atrasa operações críticas.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} realiza exercícios militares em larga escala.",
                f"Os exercícios aumentam a força e a disciplina das tropas.",
                lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                f"Os exercícios resultam em lesões e quedas de desempenho.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} adota novos protocolos de comunicação.",
                f"A organização interna melhora, elevando a estratégia.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"Os protocolos confundem unidades e causam erros.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} decide investir em estoque de munições.",
                f"O abastecimento eficiente melhora os suprimentos disponíveis.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                f"Erros de cálculo dificultam a logística e gera descartes.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} inicia um programa de bem-estar para soldados.",
                f"A moral aumenta e o desempenho das tropas melhora.",
                lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                f"O programa é mal gerido e causa frustração.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} contrata consultores militares especializados.",
                f"As orientações aumentam a precisão estratégica das tropas.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"As consultorias são ineficazes e descoordenam as unidades.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} realiza manutenção geral nas estruturas de apoio.",
                f"As melhorias nas instalações elevam os suprimentos disponíveis.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                f"A manutenção causa interrupções operacionais.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} implanta um novo sistema de identificação de alvos.",
                f"O sistema melhora a eficiência tecnológica em combate.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                f"O sistema apresenta falhas e reduz a confiabilidade.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "melhoria", 
                f"{exercito.nome} investe em treinamento tático avançado.",
                f"O treinamento melhora estratégias e aumenta a precisão operacional.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                f"O treinamento é mal coordenado e causa queda de rendimento.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            )
        ]

        clima = {
            "ensolarado": [
                Evento(
                    exercito, 
                    "clima",
                    f"O clima ensolarado favorece exercícios de campo para {exercito.nome}.",
                    f"Os treinos sob sol melhoram o condicionamento físico das tropas de {exercito.nome}.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O calor intenso atrapalha o rendimento dos soldados de {exercito.nome}.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),

                Evento(
                    exercito,  
                    "clima",
                    f"O clima ensolarado permite que {exercito.nome} opere painéis solares adicionais.",
                    f"A energia extra aumenta a tecnologia operacional de {exercito.nome}.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"Equipamentos superaquecem devido ao sol excessivo.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O sol forte desgasta os suprimentos de {exercito.nome}.",
                    f"As tropas conseguem se adaptar e minimizar as perdas.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),  # leve recuperação
                    f"O calor acelera a deterioração e causa perdas em suprimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),

                Evento(
                    exercito,  
                    "clima",
                    f"O clima ensolarado prolongado afeta o moral de {exercito.nome}.",
                    f"As tropas usam o bom clima para atividades recreativas, recuperando ânimo.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O desgaste pelo calor reduz o moral das tropas.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima ensolarado cria condições ideais para movimentação tática.",
                    f"{exercito.nome} aproveita para consolidar posições e ganhar força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"{exercito.nome} usa o clima para treinos coordenados, aprimorando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O calor intenso do clima ensolarado causa desgaste geral nas tropas.",
                    f"{exercito.nome} tem queda de moral devido à exaustão térmica.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round),
                    f"{exercito.nome} sofre com perda de suprimentos devido ao calor.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                )
            ],
            "nublado": [
                Evento(
                    exercito,  
                    "clima",
                    f"O clima nublado cria condições ideais para movimentações silenciosas.",
                    f"As tropas de {exercito.nome} usam a visibilidade reduzida para melhorar táticas furtivas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"A visibilidade reduzida causa pequenas descoordenações entre as unidades de {exercito.nome}.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima nublado facilita longas marchas para {exercito.nome}.",
                    f"As tropas aproveitam o clima ameno para reforçar sua força física.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O clima cinzento deixa as tropas desmotivadas e lentas.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A falta de luz direta atrapalha sistemas ópticos de {exercito.nome}.",
                    f"As tropas conseguem ajustar os equipamentos e minimizar o impacto.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"Os sensores sofrem interferência e reduzem a eficiência tecnológica.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima nublado afeta a moral das tropas de {exercito.nome}.",
                    f"O comando usa o clima ameno para realizar atividades e elevar o humor.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O ambiente escuro e cinza reduz o ânimo e foco das tropas.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima nublado reduz a visibilidade, abrindo espaço para manobras criativas.",
                    f"{exercito.nome} aproveita para reorganizar discretamente suas posições, aumentando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"{exercito.nome} utiliza a baixa visibilidade para movimentações rápidas, fortalecendo a força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima nublado cria instabilidade no campo de batalha.",
                    f"A baixa luminosidade reduz a precisão e o moral de {exercito.nome}.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round),
                    f"A umidade do clima afeta munições e reduz os suprimentos de {exercito.nome}.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                )
            ],
            "chuva leve": [
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve cria um ambiente ideal para camuflagem natural de {exercito.nome}.",
                    f"As tropas usam o clima para se infiltrar melhor, aumentando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"A chuva atrapalha a movimentação silenciosa e gera falhas táticas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve resfria o terreno, permitindo avanços mais longos para {exercito.nome}.",
                    f"As tropas progridem com menor desgaste, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O terreno úmido causa escorregões e pequenos acidentes nas tropas.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve danifica levemente partes dos equipamentos de {exercito.nome}.",
                    f"As unidades conseguem secar os equipamentos e evitar danos permanentes.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),  # recuperação leve
                    f"A umidade prejudica sensores e sistemas táticos, reduzindo tecnologia.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve deixa o ambiente melancólico para {exercito.nome}.",
                    f"A liderança usa a situação para inspirar as tropas, elevando moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"A chuva constante afeta o ânimo das tropas, reduzindo moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve suaviza ruídos no campo de batalha.",
                    f"{exercito.nome} aproveita para fortalecer suprimentos discretamente.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"{exercito.nome} utiliza a mesma vantagem sonora para treinar movimentos táticos.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva leve torna o solo escorregadio e imprevisível.",
                    f"{exercito.nome} sofre com redução de suprimentos por avarias causadas pela umidade.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round),
                    f"{exercito.nome} perde parte de sua força devido a acidentes menores.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                )
            ],
            "chuva forte": [
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte encobre sons e permite que {exercito.nome} execute manobras furtivas.",
                    f"As tropas usam a cobertura sonora para aprimorar táticas discretas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"A chuva excessiva impede coordenação e atrapalha os movimentos.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte dificulta ataques inimigos à distância contra {exercito.nome}.",
                    f"As tropas aproveitam o clima para avançar de forma mais segura, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O progresso é lento e exaustivo devido ao terreno encharcado.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte afeta sistemas eletrônicos de {exercito.nome}.",
                    f"As equipes técnicas conseguem reparar parte dos danos no local.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),  # leve mitigação
                    f"Os dispositivos falham com frequência devido à umidade intensa.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte deteriora suprimentos essenciais de {exercito.nome}.",
                    f"As tropas improvisam abrigos e salvam parte dos recursos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos +poder_do_round),
                    f"A água invade depósitos e arruina parte dos suprimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte reduz drasticamente a visibilidade no campo.",
                    f"{exercito.nome} usa isso para reforçar posições defensivas, aumentando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"{exercito.nome} realiza movimentações rápidas sem ser detectado, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A chuva forte transforma o terreno em puro lamaçal.",
                    f"{exercito.nome} sofre danos nos equipamentos, reduzindo tecnologia.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round),
                    f"{exercito.nome} perde moral devido ao desgaste físico constante.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                )
            ],
            "tempestade": [
                Evento(
                    exercito,  
                    "clima",
                    f"A tempestade cria um estrondo constante que abafa sons de movimentação.",
                    f"{exercito.nome} usa o barulho para reposicionar tropas sem ser detectado, melhorando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"O barulho excessivo causa falhas de comunicação entre as unidades de {exercito.nome}.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tempestade derruba estruturas leves no campo, dificultando ataques inimigos.",
                    f"{exercito.nome} aproveita o momento para reforçar suas defesas, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"As tropas de {exercito.nome} têm dificuldade para manter posições no vento extremo.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"Os ventos violentos da tempestade afetam severamente dispositivos eletrônicos.",
                    f"As equipes técnicas de {exercito.nome} salvam parte dos sistemas.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"Equipamentos entram em curto devido à tempestade e prejudicam tecnologia de {exercito.nome}.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tempestade encharca profundamente depósitos de suprimentos de {exercito.nome}.",
                    f"A tropa improvisa proteção emergencial e salva parte dos mantimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"A água invade armazéns e arruina suprimentos críticos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tempestade cria caos natural, abrindo oportunidades inesperadas.",
                    f"{exercito.nome} usa o clima para melhorar técnicas de adaptação, elevando moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"{exercito.nome} usa o caos climático para movimentos agressivos, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tempestade causa destruição generalizada em todo o campo de batalha.",
                    f"{exercito.nome} sofre danos em dispositivos sensíveis, perdendo tecnologia.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round),
                    f"{exercito.nome} perde moral devido às condições severas e à exaustão.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                )
            ],
            "tormenta elétrica": [
                Evento(
                    exercito,  
                    "clima",
                    f"A tormenta elétrica causa interferência nas comunicações inimigas.",
                    f"{exercito.nome} aproveita o momento para aprimorar suas táticas sem risco de interceptação.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"A instabilidade elétrica também atinge sistemas de {exercito.nome}, criando confusão.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A forte atividade elétrica energiza equipamentos de captação de energia de {exercito.nome}.",
                    f"A energia acumulada melhora o desempenho tecnológico das unidades.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"A carga elétrica inesperada queima circuitos sensíveis.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"Descargas elétricas atingem áreas próximas às tropas de {exercito.nome}.",
                    f"As tropas conseguem se reposicionar e evitar perigo imediato.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"Relâmpagos danificam equipamentos e ferem soldados, reduzindo força.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                    Evento(
                    exercito,  
                    "clima",
                    f"A tormenta elétrica deixa sensores e radares instáveis para {exercito.nome}.",
                    f"A equipe técnica improvisa ajustes para minimizar danos.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"A interferência elétrica afeta seriamente a capacidade tecnológica.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tormenta elétrica cria janelas de instabilidade nos sistemas do campo todo.",
                    f"{exercito.nome} aproveita para reforçar protocolos de segurança, aumentando tecnologia.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"{exercito.nome} usa a escuridão intermitente para fortalecer estratégias furtivas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A tormenta elétrica causa sobrecarga generalizada no campo.",
                    f"{exercito.nome} sofre queda abrupta de moral devido ao caos dos relâmpagos.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round),
                    f"{exercito.nome} perde suprimentos devido a explosões em depósitos energizados.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                )
            ],
            "ventania": [
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania dispersa poeira e reduz a precisão inimiga contra {exercito.nome}.",
                    f"{exercito.nome} aproveita a cobertura natural para reposicionar tropas, melhorando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"A poeira levantada pela ventania também afeta a coordenação das tropas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania impede ataques aéreos inimigos contra {exercito.nome}.",
                    f"{exercito.nome} aproveita a janela climática para reforçar posições, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"Os ventos dificultam a estabilização das fileiras e reduzem força temporariamente.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania derruba equipamentos frágeis de {exercito.nome}.",
                    f"As tropas conseguem recolher parte dos materiais danificados.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"O vento destrói elementos essenciais do estoque, reduzindo suprimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania dificulta a comunicação entre unidades de {exercito.nome}.",
                    f"As tropas adaptam sinais manuais para minimizar perdas de moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O vento constante cria ruído e confusão, reduzindo moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania muda padrões de movimentação no campo de batalha.",
                    f"{exercito.nome} usa o clima para fortalecer sua estratégia defensiva.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"{exercito.nome} aproveita o vento para executar ataques rápidos e aumentar força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A ventania alcança níveis perigosos, criando caos estrutural.",
                    f"{exercito.nome} sofre quedas de moral, já que o vento dificulta comunicação.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round),
                    f"{exercito.nome} perde tecnologia devido a falhas causadas pelo vento forte.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                )
            ],
            "nevoeiro": [
                Evento(
                    exercito,  
                    "clima",
                    f"O nevoeiro permite que {exercito.nome} avance despercebido pela linha inimiga.",
                    f"As tropas utilizam a baixa visibilidade para melhorar táticas furtivas, aumentando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"As unidades se desorientam no nevoeiro e se perdem, prejudicando a estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O nevoeiro oculta o movimento de tropas de {exercito.nome}.",
                    f"A cobertura permite um avanço seguro que aumenta a moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O clima nebuloso cria apreensão entre soldados, reduzindo moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O nevoeiro denso interfere com equipamentos de navegação de {exercito.nome}.",
                    f"A equipe técnica consegue fazer ajustes rápidos para minimizar danos.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"A falha na navegação compromete sistemas, prejudicando tecnologia.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A umidade extrema do nevoeiro atinge suprimentos de {exercito.nome}.",
                    f"As tropas protegem parte do estoque com lonas improvisadas, reduzindo perdas.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"O nevoeiro encharca caixas de suprimentos e gera perdas significativas.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O nevoeiro reduz a linha de visão para todos.",
                    f"{exercito.nome} aproveita para reforçar posições defensivas, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"{exercito.nome} usa a baixa visibilidade para treinar manobras furtivas, ganhando estratégia.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O nevoeiro cria confusão generalizada no campo de batalha.",
                    f"{exercito.nome} perde moral devido ao nervosismo provocado pelo clima opressivo.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round),
                    f"{exercito.nome} perde força após acidentes causados pela baixa visibilidade.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                )
            ],
            "frio": [
                Evento(
                    exercito,  
                    "clima",
                    f"O clima frio fortalece a resistência física das tropas de {exercito.nome}.",
                    f"As unidades se adaptam ao clima gelado, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O frio intenso causa rigidez muscular nas tropas.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"{exercito.nome} aproveita o frio para testar equipamentos térmicos avançados.",
                    f"Os testes são bem-sucedidos e aumentam a tecnologia de combate.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"As baterias falham no frio e prejudicam sistemas tecnológicos.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O frio extremo afeta seriamente os depósitos de suprimentos de {exercito.nome}.",
                    f"As tropas conseguem proteger parte do estoque.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"Os mantimentos congelam e parte se torna inutilizável.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O moral das tropas de {exercito.nome} é afetado pelo clima congelante.",
                    f"A liderança distribui mantas e bebidas quentes, elevando levemente a moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O frio constante abala o ânimo dos soldados, reduzindo moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"A temperatura congelante cria novas oportunidades estratégicas.",
                    f"{exercito.nome} usa o frio para treinar resistência, aumentando moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"{exercito.nome} adapta suas tropas para sobrevivência em clima gelado, aumentando suprimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O frio intenso causa congelamento de mecanismos e estruturas.",
                    f"{exercito.nome} sofre queda de força pela rigidez muscular do clima.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round),
                    f"{exercito.nome} sofre queda tecnológica devido ao mau funcionamento dos equipamentos.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
                )
            ],
            "calor extremo": [
                Evento(
                    exercito, 
                    "clima", 
                    f"O calor extremo reduz a eficácia dos sensores inimigos, beneficiando {exercito.nome}.",
                    f"{exercito.nome} aproveita a oportunidade para aprimorar estratégias furtivas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia + poder_do_round),
                    f"O calor é intenso demais e prejudica a coordenação tática das tropas.",
                    lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
                ),
                Evento(
                    exercito, 
                    "clima", 
                    f"O calor extremo seca o terreno, facilitando movimentações para {exercito.nome}.",
                    f"As tropas conseguem avançar com velocidade, aumentando força.",
                    lambda: setattr(exercito, 'forca', exercito.forca + poder_do_round),
                    f"O terreno árido causa fadiga excessiva e reduz força.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O calor extremo deteriora suprimentos sensíveis pertencentes a {exercito.nome}.",
                    f"As tropas conseguem salvar parte dos recursos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos + poder_do_round),
                    f"O calor estraga alimentos e munições, reduzindo suprimentos.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
                ),
                Evento(
                    exercito,  
                    "clima",
                    f"O clima insuportável afeta o moral das tropas de {exercito.nome}.",
                    f"A liderança providencia tendas e água adicional, elevando levemente a moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round),
                    f"O calor severo causa desânimo e irritação entre soldados, reduzindo moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
                ),
                Evento(
                    exercito, 
                    "clima",
                    f"O calor extremo força ambos os exércitos a adaptarem suas rotinas.",
                    f"{exercito.nome} melhora métodos de resfriamento e ganha eficiência tecnológica.",
                    lambda: setattr(exercito, 'tecnologia', exercito.tecnologia + poder_do_round),
                    f"{exercito.nome} reorganiza suas fileiras para lidar com o clima, aumentando moral.",
                    lambda: setattr(exercito, 'moral', exercito.moral + poder_do_round)
                ),
                Evento(
                    exercito, 
                    "clima",
                    f"O calor extremo provoca colapso de equipamentos e queda de rendimento.",
                    f"{exercito.nome} perde suprimentos que derretem, queimam ou evaporam.",
                    lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round),
                    f"{exercito.nome} sofre perda de força devido ao desgaste físico.",
                    lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round),
                )
            ]
        }

        tecnologia = [
            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} lança um ataque cibernético contra os sistemas de comando de {exercito.inimigo.nome}.",
                f"O ataque invade redes críticas e desativa sistemas tecnológicos inimigos.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"O ataque é rastreado e {exercito.nome} sofre retaliação digital severa.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} tenta sabotar satélites militares de {exercito.inimigo.nome}.",
                f"A sabotagem é bem-sucedida e compromete comunicações e vigilância inimigas.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A tentativa falha e sistemas orbitais de {exercito.nome} sofrem interferência.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"Unidades de {exercito.nome} realizam guerra eletrônica contra radares de {exercito.inimigo.nome}.",
                f"Os radares inimigos são neutralizados, reduzindo sua capacidade tecnológica.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A interferência é mal calibrada e afeta os próprios sistemas de {exercito.nome}.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} infiltra especialistas para sabotar centros de pesquisa de {exercito.inimigo.nome}.",
                f"A operação destrói protótipos e bancos de dados estratégicos.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A equipe é descoberta e informações sensíveis de {exercito.nome} são comprometidas.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} tenta desativar sistemas automatizados de defesa de {exercito.inimigo.nome}.",
                f"O sistema entra em colapso, reduzindo drasticamente a capacidade tecnológica inimiga.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A tentativa ativa protocolos de segurança que danificam os próprios sistemas.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"Especialistas de {exercito.nome} tentam corromper softwares militares de {exercito.inimigo.nome}.",
                f"O malware se espalha e paralisa sistemas críticos inimigos.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"O código falha e causa instabilidade nos sistemas de {exercito.nome}.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} tenta interceptar e destruir drones avançados de {exercito.inimigo.nome}.",
                f"A interceptação funciona e reduz a superioridade tecnológica do inimigo.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A tentativa falha e {exercito.nome} sofre retaliação.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento(
                exercito, 
                "tecnologia",
                f"{exercito.nome} executa uma operação para inutilizar fábricas tecnológicas de {exercito.inimigo.nome}.",
                f"A produção tecnológica inimiga é severamente afetada.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"A operação é mal planejada e sistemas industriais de {exercito.nome} sofrem danos.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            )
        ]

        suprimentos = [
            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} inicia uma ofensiva sobre um grande hospital de {exercito.inimigo.nome}.",
                "O ataque é bem-sucedido, destruindo todos os suprimentos hospitalares do local.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                f"{exercito.inimigo.nome} já estava preparado, e muitos dos recursos hospitalares foram previamente evacuados.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),
            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} bombardeia depósitos de suprimentos de {exercito.inimigo.nome}.",
                "O ataque é bem-sucedido e destrói grandes estoques de alimentos e munições.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "O ataque falha e a ofensiva consome grande parte dos próprios recursos.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} tenta interromper rotas de abastecimento de {exercito.inimigo.nome}.",
                "As rotas são bloqueadas, causando escassez crítica no exército inimigo.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A operação falha e as tropas gastam recursos sem retorno.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"Forças especiais de {exercito.nome} tentam sabotar armazéns logísticos de {exercito.inimigo.nome}.",
                "A sabotagem é bem-sucedida e compromete o abastecimento inimigo.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A equipe é descoberta e a missão gera perdas logísticas.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} tenta destruir comboios de combustível de {exercito.inimigo.nome}.",
                "Os comboios são destruídos, reduzindo drasticamente a mobilidade inimiga.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "O ataque falha e o esforço logístico se torna um desperdício.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} realiza um ataque aéreo contra centros de distribuição de {exercito.inimigo.nome}.",
                "Os centros são atingidos e o abastecimento inimigo entra em colapso.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A missão falha e consome combustível e munições valiosas.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} tenta envenenar ou inutilizar reservas de suprimentos de {exercito.inimigo.nome}.",
                "As reservas inimigas se tornam inutilizáveis.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A tentativa falha e parte dos próprios suprimentos é perdida.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} tenta capturar depósitos de suprimentos abandonados por {exercito.inimigo.nome}.",
                "Os depósitos são destruídos para evitar reaproveitamento inimigo.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A operação falha e os recursos próprios se esgotam durante a tentativa.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento(
                exercito, 
                "suprimentos",
                f"{exercito.nome} tenta interromper linhas ferroviárias usadas por {exercito.inimigo.nome}.",
                "A interrupção é bem-sucedida e prejudica seriamente a logística inimiga.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A ação falha e exige consumo excessivo de recursos logísticos.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            )
        ]

        moral = [
            Evento(
                exercito, 
                "moral",
                f"{exercito.nome} inicia uma campanha massiva de propaganda contra as tropas de {exercito.inimigo.nome}.",
                "A campanha é eficaz e abala seriamente a confiança das tropas inimigas.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A propaganda é mal recebida e gera descrédito entre as próprias tropas.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} divulga vídeos de vitórias militares para intimidar {exercito.inimigo.nome}.",
                "Os vídeos espalham medo e reduzem o ânimo das tropas inimigas.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "Os vídeos são desmentidos e ridicularizados, afetando a moral interna.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} tenta espalhar rumores de deserção nas fileiras de {exercito.inimigo.nome}.",
                "Os boatos se espalham e causam insegurança entre soldados inimigos.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "Os rumores são descobertos como falsos e desmoralizam quem os espalhou.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} executa operações psicológicas próximas às linhas inimigas.",
                f"A pressão constante desgasta emocionalmente as tropas de {exercito.inimigo.nome}.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A operação falha e expõe vulnerabilidades emocionais das próprias tropas.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} tenta interceptar comunicações para espalhar mensagens desmoralizantes.",
                "As mensagens criam confusão e reduzem o espírito de combate inimigo.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A tentativa falha e mensagens falsas atingem os próprios soldados.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} organiza demonstrações de força próximas a posições de {exercito.inimigo.nome}.",
                "A demonstração intimida e reduz a confiança das tropas inimigas.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A ação é vista como encenação e causa frustração entre as próprias tropas.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} tenta explorar perdas recentes de {exercito.inimigo.nome} para desmoralizar suas tropas.",
                "O impacto psicológico é forte e o ânimo inimigo cai drasticamente.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A tentativa é percebida como oportunista e gera desconforto interno.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento(
                exercito,
                "moral",
                f"{exercito.nome} tenta quebrar a moral inimiga com transmissões contínuas de intimidação.",
                "As transmissões causam estresse e reduzem a resistência psicológica do inimigo.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "A estratégia se volta contra o emissor e cansa as próprias tropas.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            )
        ]

        estrategia = [
            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} executa uma operação de desinformação contra o alto comando de {exercito.inimigo.nome}.",
                "Planos falsos confundem o inimigo e comprometem suas decisões estratégicas.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                "A desinformação é desmascarada e expõe falhas no próprio planejamento.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} tenta atrair {exercito.inimigo.nome} para uma armadilha estratégica.",
                "O inimigo cai no blefe e perde capacidade de coordenação.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                f"A armadilha é prevista e revela fragilidades nos planos de {exercito.nome}.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} tenta interceptar e distorcer ordens estratégicas de {exercito.inimigo.nome}.",
                "Ordens adulteradas causam erros graves no planejamento inimigo.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                f"A tentativa falha e gera confusão interna no comando de {exercito.nome}.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} lança uma série de manobras falsas para confundir {exercito.inimigo.nome}.",
                "O inimigo reage de forma equivocada e perde clareza estratégica.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                "As manobras são mal sincronizadas e prejudicam o próprio planejamento.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} tenta expor divergências internas no comando de {exercito.inimigo.nome}.",
                "Conflitos internos enfraquecem a capacidade de formular planos eficazes.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                f"A tentativa falha e gera desconfiança entre estrategistas de {exercito.nome}.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} realiza uma ofensiva psicológica focada em confundir analistas de {exercito.inimigo.nome}.",
                "Relatórios contraditórios prejudicam a leitura do campo de batalha inimigo.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                "A ofensiva gera excesso de ruído e atrapalha as próprias análises.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} tenta antecipar e neutralizar planos futuros de {exercito.inimigo.nome}.",
                "A antecipação funciona e desmonta estratégias antes de serem executadas.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                f"A previsão é incorreta e leva {exercito.nome} a decisões estratégicas erradas.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento(
                exercito,
                "estrategia",
                f"{exercito.nome} conduz um jogo de blefes para forçar decisões precipitadas do inimigo.",
                "O inimigo age por impulso e compromete sua capacidade estratégica.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                f"O blefe falha e mina a confiança no planejamento de {exercito.nome}.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            )
        ]

        inteligencia = [

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} infiltra agentes nos centros de comando de {exercito.inimigo.nome}.",
                "A operação é um sucesso e os agentes sabotam o planejamento militar inimigo.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                "Os agentes são capturados e expostos a nível internacional.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} tenta roubar códigos de comunicação de {exercito.inimigo.nome}.",
                "As comunicações inimigas foram interceptadas com sucesso, ficando vulneráveis.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                "A tentativa sobrecarrega os sistemas de inteligência.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} executa uma operação urgente de contraespionagem interna.",
                "Os espiões são neutralizados antes de concluírem o plano.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "Os espiões sabotam a cadeia de suprimentos sem serem identificados.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} espalha informações falsas nos canais secretos de {exercito.inimigo.nome}.",
                f"{exercito.inimigo.nome} investe recursos em alvos inexistentes.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "As mentiras perdem o direcionamento e confundem o próprio alto comando.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} envia um espião para interceptar informações confidenciais de {exercito.inimigo.nome}.",
                f"As falhas defensivas de {exercito.inimigo.nome} são expostas.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                "O espião era um agente duplo e expõe ao inimigo planos de longo prazo.",
                lambda: setattr(exercito, 'estrategia', exercito.estrategia - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} inicia um programa secreto de vigilância contra oficiais de {exercito.inimigo.nome}.",
                "O programa é um sucesso e informações seníveis são coletadas de oficiais-chave.",
                lambda: setattr(exercito.inimigo, 'estrategia', exercito.inimigo.estrategia - poder_do_round),
                "A vigilância excessiva compromete aparatos tecnológicos.",
                lambda: setattr(exercito, 'tecnologia', exercito.tecnologia - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} envia espiões de infiltração em bases avançadas de {exercito.inimigo.nome}.",
                "A infiltração resulta em sabotagens pontuais que enfraquecem as forças inimigas.",
                lambda: setattr(exercito.inimigo, 'forca', exercito.inimigo.forca - poder_do_round),
                "A operação exige longas linhas de apoio clandestino, esgotando os estoques internos.",
                lambda: setattr(exercito, 'suprimentos', exercito.suprimentos - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} inicia um programa secreto para sabotar rotas de suprimento de {exercito.inimigo.nome}.",
                "As rotas logísticas inimigas são comprometidas, causando escassez crítica.",
                lambda: setattr(exercito.inimigo, 'suprimentos', exercito.inimigo.suprimentos - poder_do_round),
                "A missão expõe agentes em campo, resultando em perdas militares.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"{exercito.nome} inicia uma campanha com armas psicotrônicas.",
                f"As ondas eletrônicas atingem parte da tropa de {exercito.inimigo.nome}, causando desorientação cognitiva.",
                lambda: setattr(exercito.inimigo, 'moral', exercito.inimigo.moral - poder_do_round),
                "As armas são mal calibradas e geram diversos acidentes autoinfligidos.",
                lambda: setattr(exercito, 'forca', exercito.forca - poder_do_round)
            ),

            Evento( #
                exercito,
                "inteligencia",
                f"Espiões de {exercito.nome} espalham rumores entre as frentes de {exercito.inimigo.nome}.",
                f"{exercito.inimigo.nome} destrói equipamentos próprios supostamente comprometidos.",
                lambda: setattr(exercito.inimigo, 'tecnologia', exercito.inimigo.tecnologia - poder_do_round),
                f"Manobras de contrainteligência fazem {exercito.nome} perder prestígio.",
                lambda: setattr(exercito, 'moral', exercito.moral - poder_do_round)
            )
        ]
        
        eventos = [
            (ataque, 2),
            (sorte, 0.4),
            (melhoria, 0.5),
            (clima, 0.5),
            (tecnologia, 1),
            (suprimentos, 1),
            (moral, 1),
            (estrategia, 1),
            (inteligencia, 0.75),
        ]

        evento = choices(
                [e for e, _ in eventos],
                weights=[p for _, p in eventos],
                k=1
            )[0]


        if isinstance(evento, dict):
            return choice(evento[clima_jogo.lower()])
        
        else:
            return choice(evento)


def poder(exercito):
        from random import choice

        eventos = [
            f"As forças de {exercito.nome} capturaram um importante centro de comando inimigo, elevando seu domínio no conflito.",
            f"{exercito.nome} interceptou e destruiu um contingente crucial de {exercito.inimigo.nome}, alterando o equilíbrio da guerra.",
            f"Uma operação coordenada garantiu a {exercito.nome} o controle total de rotas estratégicas antes dominadas pelo inimigo.",
            f"Após uma ofensiva bem-sucedida, {exercito.nome} desmantelou linhas críticas de defesa de {exercito.inimigo.nome}, consolidando sua superioridade.",
            f"{exercito.nome} obteve uma vitória decisiva em campo aberto, provando sua supremacia militar diante de {exercito.inimigo.nome}.",            
            f"Um avanço estratégico permitiu que {exercito.nome} tomasse controle de posições vitais, enfraquecendo drasticamente o inimigo.",           
            f"As tropas de {exercito.nome} realizaram uma manobra impecável, cercando forças de {exercito.inimigo.nome} e forçando sua retirada.",           
            f"{exercito.nome} interceptou e destruiu um contingente crucial de {exercito.inimigo.nome}, alterando o equilíbrio da guerra.",
            f"Liderança militar de {exercito.nome} executou um plano audacioso que resultou em uma conquista histórica no conflito.",       
            f"{exercito.nome} obteve uma vitória simbólica de grande impacto, fortalecendo sua posição política e militar.",
            f"Ofensiva de {exercito.nome} quebrou a resistência organizada de {exercito.inimigo.nome}, ampliando seu poder no teatro de guerra.",
            f"Operação de forças especiais de {exercito.nome} eliminou o comandante supremo das tropas de {exercito.inimigo.nome}, causando desorganização imediata no front.",
            f"{exercito.nome} executou com sucesso um ataque direcionado que resultou na morte do marechal responsável pela defesa central de {exercito.inimigo.nome}.",
            f"Durante um avanço coordenado, tropas de {exercito.nome} localizaram e neutralizaram o general encarregado da logística de {exercito.inimigo.nome}.",
            f"Bombardeio preciso de {exercito.nome} atingiu o posto de comando móvel de {exercito.inimigo.nome}, matando seu principal estrategista militar.",
            f"Forças de {exercito.nome} interceptaram um comboio de alto escalão e eliminaram o almirante responsável pelas operações navais de {exercito.inimigo.nome}.",
            f"Após semanas de inteligência, {exercito.nome} capturou e executou o oficial responsável pelas contraofensivas de {exercito.inimigo.nome}.",
            f"Incursão atrás das linhas inimigas permitiu que {exercito.nome} eliminasse o comandante das tropas de elite de {exercito.inimigo.nome}.",
            f"Governo de {exercito.nome} firmou um pacto militar emergencial com uma das potências do G7, garantindo apoio estratégico imediato.",
            f"Após atingir as normas, {exercito.nome} assinou um acordo internacional de cooperação militar que liberou acesso a armamentos, instrutores e informações sigilosas.",
            f"Governo de {exercito.nome} conseguiu isolar diplomaticamente {exercito.inimigo.nome}, pressionando outras nações a suspenderem qualquer apoio.",
            f"Uma aliança defensiva foi formalizada por {exercito.nome} com blocos regionais, assegurando reforços militares em caso de escalada do conflito.",
            f"Alto comando político de {exercito.nome} aprovou uma mobilização total da indústria de guerra, ampliando drasticamente sua capacidade militar.",
            f"{exercito.nome} negociou apoio indireto de um bloco regional, garantindo recursos e cobertura política no cenário internacional.",
            f"Governo de {exercito.nome} obteve apoio de facções dissidentes de {exercito.inimigo.nome}. Fontes indicam exploração de divisões internas.",
            f"{exercito.nome} conseguiu aprovação de medidas de guerra que centralizaram o comando militar, acelerando decisões e ofensivas."
        ]

        evento = choice(eventos)
        return evento
