// ##########################################################
// ##################### variables ##########################
// ##########################################################

// list of products {name: '', status: ''} to send to serv
let listToReturn = [];

let productsFromFile = [];
let productsCounter = 0;
let token = Math.floor(Math.random() * (1000000000));
const INITIAL_SEARCH_HELP = "Enter what You are looking for."
const PRODUCTS_NUMBER_EXCEDED = "You have reached maximum 10 products entries limit."

// search done
let searchedProductsCounter = 0;

// progress bar
let max_progres_counter = 0;
let progress_step;
let current_progres = 0;

// statuses
const SearchStatus = {
    NOT_SEARCHED: "X",
    SERVER_ERROR: "ERROR",
    SEARCH_SUCCESS: "OK"
};

// ##########################################################
// ##################### DOM elems ##########################
// ##########################################################

var addButton = document.getElementById("AddButton");
var searchInput = document.getElementById("SearchInput");
var allegroCheckbox = document.getElementById("AllegroCheckbox");
var ceneoCheckbox = document.getElementById("CeneoCheckbox");
var bothCheckbox = document.getElementById("BothCheckbox");

let bar = document.getElementById("progressbar");
let modalSearchOverviewTableBody =
        document.getElementById('modalSearchOverviewTable').
        getElementsByTagName('tbody')[0];
//list
var listOfProducts = document.getElementById("ListOfProducts");

//idk czemu ale jak wstawiam do DOM najpierw z none to nie moge zmienic na inline a jak dam tak i zamienie to od razu to działa
document.getElementById("SubmitBtn").style.display = "none";
document.getElementById("SearchHelp").innerHTML = INITIAL_SEARCH_HELP;

// ##########################################################
// ##################### functions ##########################
// ##########################################################

//adding name of the product to the listToReturn and creating DOM element with the product name in the listOfProducts
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

    //adding product name to the listToReturn
    listToReturn.push({name: searchInput.value, status: SearchStatus.NOT_SEARCHED}); //name

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
    name.style.marginTop= "10px";
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

//adding name of the product to the listToReturn and creating DOM element with the product name in the listOfProducts
function addProductFromFile(fileFromText){

    //showing submit button
    if(productsCounter == 0){
        displaySubmitBtn(1);
    }

    //adding product name to the listToReturn
    listToReturn.push({name: fileFromText, status: SearchStatus.NOT_SEARCHED}); //name

    //creating html elements
    var newProduct = document.createElement("div");
    var nameDiv = document.createElement("div");
    var delateBtnDiv = document.createElement("div");
    var name = document.createElement('h6');
    var delBtn = document.createElement('button');

    //setting attributes
    newProduct.setAttribute("class", "row mb-2 border-bottom border-top border-3");
    newProduct.setAttribute("id",  Math.floor(Math.random() * (1000000000)));
    name.style.float = "left";
    name.style.marginTop= "10px";
    name.innerHTML = fileFromText;
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
    productsCounter++;
    
}

//deleting product from the listToReturn and removing DOM element for listOfProducts
//@param- HTML element containing Delete Button
function deleteProductFromList(element){
    
    //delete element from DOM
    document.getElementById(element.parentNode.parentNode.id).remove();
    //delete from listToReturn
    listToReturn.forEach(function(elementToRemove){
        if(elementToRemove["name"] === element.parentNode.parentNode.children[0].children[0].innerHTML){
            listToReturn = listToReturn.filter(item => item !== elementToRemove)
        }
    })

    //turn on addButton after products counter is no longer equal to limit
    if(productsCounter == 10){
        document.getElementById("AddButton").removeAttribute("disabled");
        document.getElementById("SearchHelp").innerHTML = INITIAL_SEARCH_HELP;
    }

    //hide submit button if there is no product listed
    productsCounter--;
    if(productsCounter == 0){
        displaySubmitBtn(0);
    }

}

//show/hide Submit button 
//@param boolean flag: 1 => show button; 0 => hide button
function displaySubmitBtn(showFlag){
    if(showFlag == 1){//show
        document.getElementById("SubmitBtn").style.display = "inline";
    }else if(showFlag == 0){//hide
        document.getElementById("SubmitBtn").style.display = "none";
    }

}

// refresh modal table
function refreshModalTable(){
    for (let i = 0; i < modalSearchOverviewTableBody.rows.length; i++){
        let row =  modalSearchOverviewTableBody.rows[i];
         row.cells[1].innerHTML= listToReturn[i]['status'];
         if (row.cells[1].innerHTML === SearchStatus.SEARCH_SUCCESS){
             row.cells[1].style.color = "green";
         }else{
             row.cells[1].style.color = "red";
         }
    }
}

// shows modal with product list
function showModal(){
    // validation
    if(!(allegroCheckbox.checked || ceneoCheckbox.checked )){
        alert("Please, chose source of your search first.")
        return 0;
    }

    // clear table with products
    modalSearchOverviewTableBody.innerHTML = "";

    // clear progressbar
    bar.style.width = 0;

     // show search button
    $("#modalSearchBtn").show();
    $("#modalSearchText").hide();
    $("#modalResultsBtn").hide();

    // delete previous searches
    let url = "/search/" + token;
    $.ajax({
        async: false,
        type: 'DELETE',
        url: url
    });

    // reset counter
    searchedProductsCounter = 0;

    // generate overview of products
    listToReturn.forEach((element, ind) => {
        // reset status
        element['status'] = SearchStatus.NOT_SEARCHED;

        // create element
        let row = modalSearchOverviewTableBody.insertRow(ind);
        let name = row.insertCell(0);
        let status = row.insertCell(1);

        // add values
        name.innerHTML = element['name'];
        status.style.color = "red";
        status.innerHTML = element['status'];
    })

    refreshModalTable();

    // show modal
    $('#staticBackdrop').modal('show');
}

//send data to the server
function sendProducts(){
    // hide search button
    $("#modalSearchBtn").hide();
    $("#modalSearchText").show();

    //progressbar var
    if(ceneoCheckbox.checked){
        max_progres_counter = listToReturn.length;
    }

    if(allegroCheckbox.checked){
        max_progres_counter += listToReturn.length;
    }

    //max_progress_counter == 100% progress,
    // progress_step = 1/max_progress_counter*100%
    progress_step = 1/max_progres_counter*100;
    current_progres = 0;

    //if allegro is checked
    if(allegroCheckbox.checked){
       alert("Allegro not supported");
       return 0;
    }

    //if ceneo is checked
    if(ceneoCheckbox.checked){
        listToReturn.forEach((element, ind) => {
            sendOneProduct(element);
        })
    }
}

// extend progress bar after progress is made
function progressbarExtend(){
    if(parseFloat(bar.style.width) < 100 ){
        //TODO 
        var width = 1;
        var id = setInterval(frame, 10);
        function frame() {
            if (width >= current_progres) {
                clearInterval(id);
            } else {
                width++;
                bar.style.width = width + "%";
            }
        }
        current_progres += progress_step;
    }
}

// send one product to search
function sendOneProduct(product){
    // sending data via GET headers to /search/add/<token>
    let url = "/search/add/" + token;
    // send data
    $.ajax({
        async: true,
        type: 'GET',
        url: url,
        data: {target: 'ceneo', product: product['name']},
        success: function (data, status){
            product['status'] = SearchStatus.SEARCH_SUCCESS;
            searchedProductsCounter += 1;
            refreshModalTable();
            progressbarExtend();
            if (searchedProductsCounter === listToReturn.length){
                // show results button
                $("#modalSearchText").hide()
                $("#modalResultsBtn").show();
            }
        },
        error: function (data, status){
            product['status'] = SearchStatus.SERVER_ERROR;
            searchedProductsCounter += 1;
            refreshModalTable();
            progressbarExtend();
            if (searchedProductsCounter === listToReturn.length){
                // show results button
                $("#modalSearchText").hide()
                $("#modalResultsBtn").show();
            }
        }
    });
}

// redirect to results page
function goToResults(){
    // redirect
    url = window.location.origin + "/results/" + token;
    window.location.replace(url);
}


//read .txt file with a list of products and load them to the listOfProducts DOM element
//@input .txt file, each product in new line
function readFromFile(){
    //catch input element
    let fileInput = document.getElementById("addFromFileInput");
    //trigger input and then after the file was chosen catch a file
    fileInput.click();
    fileInput.addEventListener('change', (event) => {
        let reader = new FileReader();
        //translate to String
        reader.readAsText(event.target.files[0]);
        reader.onload = function() {
            productsFromFile = reader.result;
            //split after new line, optionally split after ',' or ' '
            if( productsFromFile.includes("\r\n")){
                productsFromFile = productsFromFile.split("\r\n");
            }else if(productsFromFile.includes(",")){
                productsFromFile = productsFromFile.split(",");
            }else if(productsFromFile.includes(" ")){
                productsFromFile = productsFromFile.split(" ");
            }
            //process data from user
            productsFromFile.forEach(function(toAdd){
                addProductFromFile(toAdd);
            })
          };

        //TODO- alert user about errors & and ensure whether file type is .txt and 10 products limit is not exceeded
        reader.onerror = function() {
            console.log(reader.error);
          };
      });

}