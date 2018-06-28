var frase = '';
var vetorImagens = {};

function selectImage(id){
	vetorImagens.append(id);
}

function deselectImage(){
	vetorImagens.remove(id);
}

function paginacao(number)
{
     location.href = "/" + number;
}