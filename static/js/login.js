const btnCliente = document.getElementById("cliente");
const btnFuncionario = document.getElementById("funcionario");
const formLogin = document.getElementById("formLogin");
const vUsuario = document.getElementById("usuario");

[btnCliente,btnFuncionario].forEach(i=>{
    i.addEventListener( "click" , botaoEntrar )
});

function botaoEntrar (){
    let idBotao = this.id;

    let inp = document.createElement("input");
    inp.type = "text";
    inp.name = "tipo_usuario";
    inp.hidden = true;

    switch (idBotao) {

        case 'cliente':
            if (vUsuario.value){
                formLogin.appendChild(inp);
                inp.value = "cliente";
                console.log(formLogin);
                formLogin.submit();
            }
            break;
        
        case 'funcionario':
            if (vUsuario.value){
                formLogin.appendChild(inp);
                inp.value = "funcionario";
                console.log(formLogin);
                formLogin.submit();
            }
            break;
    }
}
