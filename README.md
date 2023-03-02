# Editor

O programa principal é o Editor.pyw, ele possui um interface gráfica de entrada para abrir ou editar uma imagem no mesmo diretório.

Este editor tem o objetivo de fazer artes para jogos 2D, apesar de possuir a opção de criar imagens maiores, é recomendável que o ajuste da tela seja automático, assim ele ajusta a imagem para aproximadamente 500 pixeis na tela, suficiente para que seja visível, mas imagens grandes podem passar o tamanho da tela, oque é indesejável.

As funções mais básicas possuem um botão para serem acessadas graficamente, mas algumas outras possuem uma ativação apenas via teclado:


- Cores selecionáveis -> é possível mudar para a cor que quiser  usando as teclas R(red), G(green) e B(blue), assim pode-se usar = e - para aumentar ou diminuir (respectivamente) a saturação de cada cor, além de A(alpha) para mudar a transparência.\n
- A tecla P(paint) possui a função de ativar a função de pintar, mas esta função ainda não é muito boa, tem grande risco de travar o programa, seja na forma recursiva ou não.\n
- "Andar" pela imagem é possível a partir das setas, existe a mesma função na interface, pela seta é mais rápido, pelo mouse é mais preciso.\n\n

Obs.: O zoom é muito simples, ele carrega a imagem fora de proporção, por isso ele passa a ser muito lento caso o zoom seja alto, além de permitir apenas zooms múltiplos de 2.

O modo paint não é muito bom, ele pinta bem regiões pequenas, mas regiões grandes ou ele trava ou ele demora muito.
