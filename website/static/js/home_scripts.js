// variables
var listToReturn = [];
var productsCounter = 0;
let token = Math.floor(Math.random() * (1000000000));
const INITIAL_SEARCH_HELP = "Enter what You are looking for."
const PRODUCTS_NUMBER_EXCEDED = "You have reached maximum 10 products entries limit."

// DOM elements
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

//deleting product from the list
function deleteProductFromList(element){
    document.getElementById(element.parentNode.parentNode.id).remove();
    listToReturn = listToReturn.filter(item => item !== element.parentNode.parentNode.children[0].children[0].innerHTML)

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

// shows modal with product list
function showModal(){
    // clear table with products
    modalSearchOverviewTableBody.innerHTML = "";

    // clear progressbar
    bar.style.width = 0;

    // validation
    if(!(allegroCheckbox.checked || ceneoCheckbox.checked )){
        alert("Please, chose source of your search first.")
        return 0;
    }

    // generate overview of products
    listToReturn.forEach((element, ind) => {
        // create element
        let row = modalSearchOverviewTableBody.insertRow(ind);
        let name = row.insertCell(0);
        let status = row.insertCell(1);

        // add values
        name.innerHTML = element;
        status.style.color = "red";
        status.innerHTML = "X";
    })

    // show modal
    $('#staticBackdrop').modal('show');
}

//send data to the server
function sendProducts(){
    // search DOM elements
    let modalSearchBtn = $("#modalSearchBtn");
    let modalResultsBtn = $("#modalResultsBtn");
    let modalSearchText = $("#modalSearchText");

    // hide search button
    modalSearchBtn.hide();
    modalSearchText.show();

    //progressbar var
    let max_progres_counter = 0;
    if(ceneoCheckbox.checked){
        max_progres_counter = listToReturn.length;
    }

    if(allegroCheckbox.checked){
        max_progres_counter += listToReturn.length;
    }

    //max_progress_counter == 100% progress,
    // progress_step = 1/max_progress_counter*100%
    let progress_step = 1/max_progres_counter*100;
    let current_progres = 0;

    //if allegro is checked
    if(allegroCheckbox.checked){
       alert("Allegro not supported");
       return 0;
    }

    // sending data via GET headers to /search/add/<token>
    let url = "/search/add/" + token;

    //if ceneo is checked
    if(ceneoCheckbox.checked){
        listToReturn.forEach((element, ind) => {
            $.ajax({
                async: true,
                type: 'GET',
                url: url,
                data: {target: 'ceneo', product: element},
                success: function (data, status){
                    if(parseFloat(bar.style.width) < 100 ){
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
                        // product status
                        modalSearchOverviewTableBody.rows[ind].cells[1].innerHTML = "OK";
                        modalSearchOverviewTableBody.rows[ind].cells[1].style.color = "green";
                    }
                }
            });
        })
    }
    // show results button
    modalSearchText.hide()
    modalResultsBtn.show();
}

// redirect to results page
function goToResults(){
    // redirect
    url = window.location.origin + "/results/" + token;
    window.location.replace(url);
}
