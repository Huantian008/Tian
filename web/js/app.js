console.log("JS已接管页面");
const form =document.querySelector("#todo-form");
const input =document.querySelector("#todo-input");
const list =document.querySelector("#todo-list");

form.addEventListener("submit",function(e){
    e.preventDefault();
    console.log(input.value);
    
    const li =document.createElement("li");
    li.textContent=input.value;
    list.appendChild(li);
});

list.addEventListener("click",function(e){
    e.target.remove();
});

