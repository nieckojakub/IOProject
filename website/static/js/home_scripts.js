// ##########################################################
// ##################### variables ##########################
// ##########################################################

// list of products to return {name: '', status: '', amount: ''} to send to serv
let listToReturn = [];
let searchStarted = false;

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
function addProduct() {

    //checking if input is nonempty
    if (searchInput.value == "") {
        alert("Please, enter your product first");
        return 0;
    }
    //showing submit button
    if (productsCounter == 0) {
        displaySubmitBtn(1);
    }

    if (isInputDuplicated(searchInput.value)) {
        searchInput.value == ""
        alert("You have already entered that product!");
        return 0;
    }

    //adding product name to the listToReturn
    listToReturn.push({ name: searchInput.value, status: SearchStatus.NOT_SEARCHED, amount: document.getElementById("amountMain").value }); //name

    //creating html elements
    var newProduct = document.createElement("div");
    var nameDiv = document.createElement("div");
    var amountDiv = document.createElement("div");
    var delateBtnDiv = document.createElement("div");
    var name = document.createElement('h6');
    var delBtn = document.createElement('button');
    var inputGroupAmountDiv = document.createElement("div");
    var inputAmount = document.createElement("input");
    var minusButton = document.createElement("button");
    var plusButton = document.createElement("button");


    //setting attributes
    newProduct.setAttribute("class", "row mb-2 border-bottom border-top border-3");
    newProduct.setAttribute("id", Math.floor(Math.random() * (1000000000 - 0) + 0));
    name.style.float = "left";
    name.style.marginTop = "10px";
    name.innerHTML = searchInput.value;
    nameDiv.setAttribute("class", "col");
    amountDiv.setAttribute("class", "col");
    delateBtnDiv.setAttribute("class", "col-auto");
    delBtn.setAttribute("class", "btn btn-danger");
    delBtn.setAttribute("type", "button");
    delBtn.setAttribute("onClick", "deleteProductFromList(this)");
    delBtn.innerHTML = "Delete";
    inputGroupAmountDiv.setAttribute('class', 'input-group');
    inputGroupAmountDiv.style.maxWidth = '140px';
    inputAmount.setAttribute('type', 'text');
    inputAmount.setAttribute('class', 'form-control');
    inputAmount.setAttribute('value', document.getElementById("amountMain").value);
    inputAmount.setAttribute('min', '1');
    inputAmount.setAttribute('max', '10');
    inputAmount.setAttribute('onchange', 'return validateAmount(this);');
    inputAmount.setAttribute('style', 'display:inline; max-width: 60px;');
    minusButton.setAttribute('class', 'btn btn-danger');
    minusButton.setAttribute('type', 'button');
    minusButton.setAttribute('style', 'display:inline; z-index: 0');
    minusButton.setAttribute('onclick', 'return minusBtn(this);');
    minusButton.innerHTML = '-';
    plusButton.setAttribute('class', 'btn btn-success');
    plusButton.setAttribute('type', 'button');
    plusButton.setAttribute('style', 'display:inline; z-index: 0');
    plusButton.setAttribute('onclick', 'return plusBtn(this);');
    plusButton.innerHTML = '+';


    //connecting elements
    nameDiv.appendChild(name);
    delateBtnDiv.appendChild(delBtn);
    inputGroupAmountDiv.appendChild(minusButton);
    inputGroupAmountDiv.appendChild(inputAmount);
    inputGroupAmountDiv.appendChild(plusButton);
    newProduct.appendChild(nameDiv);
    newProduct.appendChild(inputGroupAmountDiv);
    newProduct.appendChild(delateBtnDiv);

    //adding new product to the list
    listOfProducts.appendChild(newProduct);
    searchInput.value = "";
    document.getElementById("amountMain").value = 1;
    productsCounter++;

    //checking if there is max 10 items on the list and disableing addButton
    if (productsCounter >= 10) {
        document.getElementById("AddButton").setAttribute("disabled", "true");
        document.getElementById("SearchHelp").innerHTML = PRODUCTS_NUMBER_EXCEDED;
    }

}

//adding name of the product to the listToReturn and creating DOM element with the product name in the listOfProducts
function addProductFromFile(fileFromText) {

    //showing submit button
    if (productsCounter == 0) {
        displaySubmitBtn(1);
    }

    //adding product name to the listToReturn
    listToReturn.push({ name: fileFromText, status: SearchStatus.NOT_SEARCHED, amount: 1 });

    //creating html elements
    var newProduct = document.createElement("div");
    var nameDiv = document.createElement("div");
    var amountDiv = document.createElement("div");
    var delateBtnDiv = document.createElement("div");
    var name = document.createElement('h6');
    var delBtn = document.createElement('button');
    var inputGroupAmountDiv = document.createElement("div");
    var inputAmount = document.createElement("input");
    var minusButton = document.createElement("button");
    var plusButton = document.createElement("button");

    //setting attributes
    newProduct.setAttribute("class", "row mb-2 border-bottom border-top border-3");
    newProduct.setAttribute("id", Math.floor(Math.random() * (1000000000)));
    name.style.float = "left";
    name.style.marginTop = "10px";
    name.innerHTML = fileFromText;
    amountDiv.setAttribute("class", "col");
    nameDiv.setAttribute("class", "col");
    delateBtnDiv.setAttribute("class", "col-auto");
    delBtn.setAttribute("class", "btn btn-danger");
    delBtn.setAttribute("type", "button");
    delBtn.setAttribute("onClick", "deleteProductFromList(this)");
    delBtn.innerHTML = "Delete";
    inputGroupAmountDiv.setAttribute('class', 'input-group');
    inputGroupAmountDiv.style.maxWidth = '140px';
    inputAmount.setAttribute('type', 'text');
    inputAmount.setAttribute('class', 'form-control');
    inputAmount.setAttribute('value', document.getElementById("amountMain").value);
    inputAmount.setAttribute('min', '1');
    inputAmount.setAttribute('max', '10');
    inputAmount.setAttribute('onchange', 'return validateAmount(this);');
    inputAmount.setAttribute('style', 'display:inline; max-width: 60px;');
    minusButton.setAttribute('class', 'btn btn-danger');
    minusButton.setAttribute('type', 'button');
    minusButton.setAttribute('style', 'display:inline; z-index: 0');
    minusButton.setAttribute('onclick', 'return minusBtn(this);');
    minusButton.innerHTML = '-';
    plusButton.setAttribute('class', 'btn btn-success');
    plusButton.setAttribute('type', 'button');
    plusButton.setAttribute('style', 'display:inline; z-index: 0');
    plusButton.setAttribute('onclick', 'return plusBtn(this);');
    plusButton.innerHTML = '+';

    //connecting elements
    nameDiv.appendChild(name);
    delateBtnDiv.appendChild(delBtn);
    inputGroupAmountDiv.appendChild(minusButton);
    inputGroupAmountDiv.appendChild(inputAmount);
    inputGroupAmountDiv.appendChild(plusButton);
    newProduct.appendChild(nameDiv);
    newProduct.appendChild(inputGroupAmountDiv);
    newProduct.appendChild(delateBtnDiv);

    //adding new product to the list
    listOfProducts.appendChild(newProduct);
    productsCounter++;

}

//deleting product from the listToReturn and removing DOM element for listOfProducts
//@param- HTML element containing Delete Button
function deleteProductFromList(element) {

    //delete element from DOM
    document.getElementById(element.parentNode.parentNode.id).remove();
    //delete from listToReturn
    listToReturn.forEach(function (elementToRemove) {
        if (elementToRemove["name"] === element.parentNode.parentNode.children[0].children[0].innerHTML) {
            listToReturn = listToReturn.filter(item => item !== elementToRemove)
        }
    })

    //turn on addButton after products counter is no longer equal to limit
    if (productsCounter >= 10) {
        document.getElementById("AddButton").removeAttribute("disabled");
        document.getElementById("SearchHelp").innerHTML = INITIAL_SEARCH_HELP;
    }

    //hide submit button if there is no product listed
    productsCounter--;
    if (productsCounter == 0) {
        displaySubmitBtn(0);
    }

}

//show/hide Submit button 
//@param boolean flag: 1 => show button; 0 => hide button
function displaySubmitBtn(showFlag) {
    if (showFlag == 1) {//show
        document.getElementById("SubmitBtn").style.display = "inline";
    } else if (showFlag == 0) {//hide
        document.getElementById("SubmitBtn").style.display = "none";
    }

}

// refresh modal table
function refreshModalTable() {
    for (let i = 0; i < modalSearchOverviewTableBody.rows.length; i++) {
        let row = modalSearchOverviewTableBody.rows[i];
        row.cells[1].innerHTML = listToReturn[i]['status'];
        if (row.cells[1].innerHTML === SearchStatus.SEARCH_SUCCESS) {
            row.cells[1].style.color = "green";
        } else {
            row.cells[1].style.color = "red";
        }
    }
}

// shows modal with product list
function showModal() {
    // validation
    if (!(allegroCheckbox.checked || ceneoCheckbox.checked)) {
        alert("Please, choose source of your search first.")
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

//flag to stop and restart counter
var stopTimer = false;
//count up from 0m 0s
function couuntTime() {
    var countUpDate = new Date();
    //timer
    var x = setInterval(function () {
        var now = new Date();
        var timeDiff = now - countUpDate;

        var minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

        document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s";
        //if flag, stop timer 
        if (stopTimer) {
            clearInterval(x);
            stopTimer = false;
        }
    }, 1000);

}

//restart token after user cancel his searach
function restartToken() {
    if (searchStarted) {
        var isExecuted = confirm("Are you sure? You will lose already found data")
    }
    if (isExecuted) {
        token = Math.floor(Math.random() * (1000000000));
        searchStarted = false;
        stopTimer = true;
        $("#modalPartialResultsBtn").hide();
    }
}

//send data to the server
function sendProducts() {
    searchStarted = true;
    // hide search button
    $("#modalSearchBtn").hide();
    $("#modalSearchText").show();

    couuntTime();

    //progressbar var
    //max_progress_counter == 100% progress,
    max_progres_counter = listToReturn.length;

    progress_step = 1 / max_progres_counter * 100;
    current_progres = 0;

    //send token
    let url = "/search/token/" + token;
    $.ajax({
        async: false,
        type: 'GET',
        url: url,
        data: { length: listToReturn.length },
        success: function (data, status) {
            // send all products to backend
            listToReturn.forEach((element) => {
                sendOneProduct(element);
            })
        },
        error: function (data, status) {

        }
    });

}

// extend progress bar after progress is made
function progressbarExtend(current_wid) {
    if (parseFloat(bar.style.width) < 100) {
        var width = current_wid;
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
function sendOneProduct(product) {
    // sending data via GET headers to /search/add/<token>
    let url = "/search/add/" + token;
    let target;
    if (!allegroCheckbox.checked && ceneoCheckbox.checked) {
        target = 'ceneo';
    } else if (allegroCheckbox.checked && !ceneoCheckbox.checked) {
        target = 'allegro'
    } else {
        target = 'both'
    }

    // send data
    $.ajax({
        async: true,
        type: 'GET',
        url: url,
        data: { target: target, product: product['name'], amount: product["amount"] },
        success: function (data, status) {
            if (token === Number(data)) {
                product['status'] = SearchStatus.SEARCH_SUCCESS;
                searchedProductsCounter += 1;
                refreshModalTable();
                progressbarExtend(parseFloat(bar.style.width));
                if (searchedProductsCounter === listToReturn.length) {
                    // show results button
                    $("#modalSearchText").hide();
                    $("#modalResultsBtn").show();
                    $("#modalPartialResultsBtn").hide();
                    document.getElementById("timeSummar").innerHTML = document.getElementById("timer").innerHTML;
                    document.getElementById("timer").innerHTML = "";
                    negativeEnsure();
                    stopTimer = true;

                } else if (searchedProductsCounter > 0) {
                    $("#modalPartialResultsBtn").show();
                }
            }
        },
        error: function (data, status) {
            if (token === Number(data)) {
                product['status'] = SearchStatus.SERVER_ERROR;
                searchedProductsCounter += 1;
                refreshModalTable();
                progressbarExtend();
                if (searchedProductsCounter === listToReturn.length) {
                    // show results button
                    $("#modalSearchText").hide()
                    $("#modalResultsBtn").show();
                }
            }
        }
    });
}

//confirm user choice 
function ensurePartialResults() {
    $("#ensureDiv").show()

}

//continue searching 
function negativeEnsure() {
    $("#ensureDiv").hide()
}

// redirect to results page
function goToResults() {
    // redirect
    url = window.location.origin + "/results/" + token;
    window.location.replace(url);
}


//read .txt file with a list of products and load them to the listOfProducts DOM element
//@param: event from changing input element, input must be text element, separted by new line, ',' or ' '
function readFromFile(event) {

    let containsDuplicat = false;

    //catch input element
    var fileInput = event.target;
    var productsFromFile = [];
    //trigger input and then after the file was chosen catch a file
    var reader = new FileReader();
    reader.onload = function () {
        productsFromFile = reader.result;
        //split after new line, optionally split after ',' or ' '
        if (productsFromFile.includes("\r\n")) {
            productsFromFile = productsFromFile.split("\r\n");
        } else if (productsFromFile.includes(",")) {
            productsFromFile = productsFromFile.split(",");
        } else if (productsFromFile.includes(" ")) {
            productsFromFile = productsFromFile.split(" ");
        }
        for (toAdd of productsFromFile) {
            if (productsCounter >= 10) {
                alert("You cannot add more than 10 items!");
                break;
            } else {
                if (isInputDuplicated(toAdd)) {
                    containsDuplicat = true;
                } else {
                    addProductFromFile(toAdd);
                }
            }
        }
        if (containsDuplicat) {
            alert("Duplicated items were ommited.");
        }
    };
    reader.readAsText(fileInput.files[0]);

}

//functions that checks if product was already inputed

function isInputDuplicated(product) {

    for (let enteredProduct of listToReturn) {
        if (enteredProduct["name"] === product) {
            return true;
        }
    }
    return false;

}

//functions handling plus/minus products counter
//@param: selected element e.g. minus button, amount input 
//validates product amount in products list element- onchange input
function validateAmount(element) {

    if (!(Number.isInteger(parseInt(element.value)))) {
        alert("You must enter number from 1 to 10!");
        element.value = 1;
        return null;
    } else if (element.value > 10) {
        alert("Maximum amount is 10.");
        element.value = 10;
        return null;
    } else if (element.value < 1) {
        alert("Minimum amount is 1.");
        element.value = 1;
        return null;
    }

    if (element.parentNode.parentNode.parentNode.id === "ListOfProducts") {
        for (let temp of listToReturn) {
            if (temp["name"] === element.parentNode.parentNode.firstChild.firstChild.innerHTML) {
                temp["amount"] = parseInt(element.value);
                break;
            }
        }
    }

}
//validates and decrement product amount in main input element- onclick minus
function minusBtn(element) {

    var counter = element.parentNode.children[1];
    if (counter.value == 1) {
        alert("Minimum amount is 1.");
        return null;
    } else {
        counter.value--;
    }

    //update amount dic
    if (element.parentNode.parentNode.parentNode.id === "ListOfProducts") {
        for (let temp of listToReturn) {
            if (temp["name"] === element.parentNode.parentNode.firstChild.firstChild.innerHTML) {
                temp["amount"] = parseInt(counter.value);
                break;
            }
        }
    }

}

//validates and increment product amount in main input element- onclick plus
function plusBtn(element) {

    var counter = element.parentNode.children[1];
    if (counter.value == 10) {
        alert("Maximum amount is 10.");
        return null;
    } else {
        counter.value++;
    }

    //update amount dic
    if (element.parentNode.parentNode.parentNode.id === "ListOfProducts") {
        for (let temp of listToReturn) {
            if (temp["name"] === element.parentNode.parentNode.firstChild.firstChild.innerHTML) {
                temp["amount"] = parseInt(counter.value);
                break;
            }
        }
    }

}