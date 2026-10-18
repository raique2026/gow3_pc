# Troféus locais — fase 1 (experimental)

Esta branch adiciona persistência local ao runtime de troféus do PS4.

## Implementado
- Guarda flags de até 128 IDs em `gow3_trophies.dat` no diretório de trabalho.
- Lê o arquivo na primeira consulta e evita desbloqueios repetidos.
- `sceNpTrophyGetTrophyUnlockState` retorna as flags salvas.

## Limitações e testes obrigatórios
- **Não compilado nem testado em jogo.** Não integrar à branch principal ainda.
- `count=128` é uma capacidade provisória, não a contagem real de troféus. É necessário confirmar a semântica da API e o layout dos bits.
- Ainda não há nomes, ícones, pop-ups, platina automática nem sincronização PSN.
- O arquivo de estado fica no diretório de trabalho, não na pasta configurada de saves.
- O fluxo de substituição do arquivo no Windows precisa de revisão para garantir segurança em falhas.
- Confirmar IDs reais emitidos por `sceNpTrophyUnlockTrophy` com logs e testar persistência após reiniciar.
- Fazer backup dos saves antes de qualquer teste.

Próximos passos: testes do runtime, metadados originais dos troféus, integração com launcher e notificações.
