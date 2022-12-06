// variables
var listToReturn = [];
var productsCounter = 0;
//input formu
var addButton = document.getElementById("AddButton");
var searchInput = document.getElementById("SearchInput");
var allegroCheckbox = document.getElementById("AllegroCheckbox");
var ceneoCheckbox = document.getElementById("CeneoCheckbox");
var bothCheckbox = document.getElementById("BothCheckbox");
//list
var listOfProducts = document.getElementById("ListOfProducts");

//idk czemu ale jak wstawiam do DOM najpierw z none to nie moge zmienic na inline a jak dam tak i zamienie to od razu to działa
document.getElementById("SubmitBtn").style.display = "none";

//functions

//adding name of the product to the list
function addProduct(){

    //checking if there is max 10 items on the list
    if(productsCounter > 10){
        alert("You can only add 10 items!")
        return 0;
    }
    //checking if input is nonempty
    if(searchInput.value == ""){
        alert("Please, enter your product first");
        return 0;
    }
    //showing submit button
    if(productsCounter == 0){
        displaySubmitBtn(1);
    }

    listToReturn.push(searchInput.value); //name
    //creating html elements
    var newProduct = document.createElement("div");
    var nameDiv = document.createElement("div");
    var delateBtnDiv = document.createElement("div");
    var name = document.createElement('h6');
    var delBtn = document.createElement('button');
    //setting attributes
    newProduct.setAttribute("class", "row mb-2 border-bottom border-top border-3");
    newProduct.setAttribute("id",  Math.floor(Math.random() * (1000000000 - 0) + 0));
    name.innerHTML = searchInput.value;
    nameDiv.setAttribute("class", "col");
    delateBtnDiv.setAttribute("class", "col-auto");
    delBtn.setAttribute("class", "btn btn-danger");
    delBtn.setAttribute("type", "button");
    delBtn.setAttribute("onClick", "deleteProductFromList(this)");
    delBtn.innerHTML = "Delete";
    //connecting elements
    nameDiv.appendChild(name);
    delateBtnDiv.appendChild(delBtn);
    newProduct.appendChild(nameDiv);
    newProduct.appendChild(delateBtnDiv);
    //adding new product to the list
    listOfProducts.appendChild(newProduct);
    searchInput.value = "";
    productsCounter++;
    
}

//deleting product from the list
function deleteProductFromList(element){
    document.getElementById(element.parentNode.parentNode.id).remove();
    productsCounter--;
    if(productsCounter == 0){
        displaySubmitBtn(0);
    }

}

//show/hide Submit button --1 => show button; 0=> hide button
function displaySubmitBtn(showFlag){
    if(showFlag == 1){//show
        document.getElementById("SubmitBtn").style.display = "inline";
    }else if(showFlag == 0){//hide
        document.getElementById("SubmitBtn").style.display = "none";
    }

}

//send data to the server
function sendProducts(){
    if(!(allegroCheckbox.checked || ceneoCheckbox.checked )){
        alert("Please, chose source of your search first.")
        return 0;
    }
    
    var dataToReturn = {};
    //preparing data
    listToReturn.forEach((productName,ind) => {
        dataToReturn["list" + ind] = productName;
    })

    //sources
    if(allegroCheckbox.checked){
        dataToReturn["allegro"] = true;
    }
    //sources
    if(ceneoCheckbox.checked){
        dataToReturn["ceneo"] = true;
    }

    //sending data via GET headers to /search
    $.ajax({
        method: "GET",
        url: "/search",
        data: dataToReturn
      })
}
