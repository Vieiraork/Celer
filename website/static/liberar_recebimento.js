function liberaRecebimento(id){
    let tela = confirm('Deseja realmente liberar o recebimento para o morador?')

    if(tela){
        fetch('/alterar/recebimento_porteiro', {
            method: 'POST',
            body: JSON.stringify({ Id: id})
        }).then(_res => {
            window.location.href = "/listar/encomenda"
        })
    }
}

function recebeEncomenda(id){   
    let recebe = confirm('Deseja marcar como recebida a encomenda?')

    if(recebe){
        fetch('/alterar/recebimento_morador', {
            method: 'POST',
            body: JSON.stringify({ Id: id})
        }).then(_res => {
            window.location.href = "/listar/encomenda_morador"
        })
    }
}