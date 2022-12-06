// variables
var listToReturn = [];
var productsCounter = 0;
var INITIAL_SEARCH_HELP = "Enter what You are looking for."
var PRODUCTS_NUMBER_EXCEDED = "You have reached maximum 10 products entries limit."
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
document.getElementById("SearchHelp").innerHTML = INITIAL_SEARCH_HELP;

//functions

//adding name of the product to the list
function addProduct(){

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
    name.style.float = "left";
    name.style.marginTop= "2%";
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
    //checking if there is max 10 items on the list and disableing addButton
    if(productsCounter == 10){
        document.getElementById("AddButton").setAttribute("disabled", "true");
        document.getElementById("SearchHelp").innerHTML = PRODUCTS_NUMBER_EXCEDED;
    }
    
}

//deleting product from the list
function deleteProductFromList(element){
    document.getElementById(element.parentNode.parentNode.id).remove();

    //turn on addButton after products counter is no longer equal to limit
    if(productsCounter == 10){
        document.getElementById("AddButton").removeAttribute("disabled");
        document.getElementById("SearchHelp").innerHTML = INITIAL_SEARCH_HELP;
    }

    productsCounter--;
    if(productsCounter == 0){
        displaySubmitBtn(0);
    }

}

//show/hide Submit button --1 => show button; 0 => hide button
function displaySubmitBtn(showFlag){
    if(showFlag == 1){//show
        document.getElementById("SubmitBtn").style.display = "inline";
    }else if(showFlag == 0){//hide
        document.getElementById("SubmitBtn").style.display = "none";
    }

}

//send data to the server
//for example ?list0=name0&list1=name1&list2=name2&allegro=true&ceneo=true -- allegro and ceneo parametras are optionall but at least one of them must be checked"
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
