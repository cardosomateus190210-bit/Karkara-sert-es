function entrar(){

  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  if(email === "" || senha === ""){
    alert("Preencha todos os campos!");
    return;
  }

  alert("Login realizado com sucesso!");
}

/* MENU ATIVO */

const items = document.querySelectorAll(".menu-item");

items.forEach(item => {

  item.addEventListener("click", () => {

    items.forEach(i => i.classList.remove("active"));

    item.classList.add("active");

  });

});

/* VOLTAR INÍCIO */

function voltarInicio(){

  window.location.href = "../index.htm";

}

/* cadastro */
function cadastrar(){

  window.location.href = "cadastrar.htm";

}

/* cadastro */
function voltarlogin(){

  window.location.href = "login.htm";

}

function entrar1(){

  window.location.href = "../dashboard.htm";
}

function entrar(){

  window.location.href = "../dashboard.htm";
}