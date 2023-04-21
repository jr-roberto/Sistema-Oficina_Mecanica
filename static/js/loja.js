var atendimento;

const dadosAtendimento = {
    cliente : null,
    servico : [],
}

function statusAtendiemtno(){
    let textArea = document.querySelector('iframe').contentWindow.document.querySelector('textarea');
    console.log(atendimento)

    if (textArea){
        let myJson = textArea.value;

        atendimento = JSON.parse(myJson);

        console.log(atendimento);

        dadosAtendimento.cliente = atendimento;

        return false
    }

    else {

        return setTimeout(statusAtendiemtno,1000);
    }
}

setTimeout(statusAtendiemtno,1000);
