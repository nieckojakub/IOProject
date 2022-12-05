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



//functions

//adding name of the product to the list
function addProduct(){

    if(productsCounter > 10){
        alert("You can only add 10 items!")
    }
    //checking if input is nonempty
    if(searchInput.value == ""){
        alert("Please, enter your product first");
        return 0;
    }

    listToReturn.push([searchInput.value]); //name
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

//deleting product from the list- TODO
function deleteProductFromList(element){
    document.getElementById(element.parentNode.parentNode.id).remove();
    productsCounter--;
}

