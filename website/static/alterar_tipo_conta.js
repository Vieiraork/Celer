function alteraCampos(){
    let select = document.getElementById('tipo_conta');
    let valor = select.options[select.selectedIndex].value;
    const div = document.getElementById('campos_alterados');
    
    if(valor === "Morador"){
        div.innerHTML = `<div class="form-group row">
        <label for="apartamento" class="col-sm-1 col-form-label">Apartamento</label>
        <div class="col-sm-10">
            <input type="text" name="apartamento" class="form-control" id="apartamento" placeholder="Apto 105">
        </div>
    </div>
    <div class="form-group row">
        <label for="usuario_condominio" class="col-sm-1 col-form-label">Condomínio</label>
        <div class="col-sm-10">
            <select class="form-control" name="usuario_condominio" id="usuario_condominio">
                <option>Selecione</option>
                {% for cond in condominio %}
                    <option value="{{ cond.id }}">'{{ cond.nome }}'</option>
                {% endfor %}
            </select>
        </div>
    </div>`;
    } else if(valor === "Porteiro"){
        div.innerHTML = `<div class="form-group row">
            <label for="usuario_condominio" class="col-sm-1 col-form-label">Condomínio</label>
            <div class="col-sm-10">
                <select class="form-control" name="usuario_condominio" id="usuario_condominio">
                    <option>Selecione</option>
                    {% for cond in condominio %}
                        <option value="{{ cond.id }}">'{{ cond.nome }}'</option>
                    {% endfor %}
                </select>
            </div>
        </div>`;
    } else{
        div.innerHTML = "";
    }
}