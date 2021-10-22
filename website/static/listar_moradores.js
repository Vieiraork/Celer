function getIdCondominio(){
    let idCondominio = document.getElementById('condominio_id');
    let valor = idCondominio.options[idCondominio.selectedIndex].value;
    const idMorador = document.getElementById('morador_id');
    
    idMorador.innerHTML= '';

    if (valor > 0){
        fetch('/listar/morador_id', {
            method: 'POST',
            body: JSON.stringify({ condId: valor })
        }).then(res => res.json())
        .then( morador => {
            for (const mor of morador) {
                idMorador.innerHTML += `<option value="${mor.id}">${mor.nome} | ${mor.apto}</option>`;
            }
        });
    }
}