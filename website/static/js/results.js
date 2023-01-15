// ##########################################################
// ##################### variables ##########################
// ##########################################################
let searchResult;
let selectedProducts = {};

let modalSearchOverviewTableBody =
    document.getElementById('modalSearchOverviewTable').
        getElementsByTagName('tbody')[0];


const InfoStatus = {
    ITEM_ADDED_TO_HISTORY: "Your search was successfully saved.",
    FAIL_TO_SAVE: "Log in first."
}

// ##########################################################
// ##################### DOM elems ##########################
// ##########################################################
var accordionMain = document.getElementById("accordionMain"); //main accordion

// run code after loading the page
$(function () {
    // establish data source (url)
    let pathname = window.location.pathname;
    pathname = pathname.split('/')
    let url = '';
    if (pathname[1] === 'results_db') {
        let history_id = pathname[2];
        url = "/history/" + history_id;
        document.getElementById("saveButton").disabled = true;
    } else if (pathname[1] === 'results') {
        token = pathname[2];
        url = "/search/" + token;
    } else {
        window.location.replace(window.location.origin);
    }

    // request data
    $.ajax({
        url: url,
        type: 'GET',
        success: function (data) {
            searchResult = JSON.parse(data);
            for (let i = 0; i < Object.keys(searchResult["ceneo"]).length; i++) {
                selectedProducts[Object.keys(searchResult["ceneo"])[i]] = 1;
            }
            generateDOM();
        },
        error: function () {
            // redirect
            window.location.replace(window.location.origin);
        }
    });

});

// ##########################################################
// ##################### functions ##########################
// ##########################################################

/*generates DOM elements and fill them with data
id parametrs:

@radiobuttonsgroups -> "specifyProductRadioButtonX";
@radiobutton -> "btnradioYProductX"; 
@image of the product -> "productImgX"; returns <td> element with <img> children inside;
@user input -> "productNameACX";
@table with basic info of product -> "productDetailsX"; returns <td> element with <table> with product details inside;
@basic info of a product:   @products name -> "productNameX"
                            @products raiting -> "productRatingX"
                            @products lowest price -> "productLowPriceX";
                            @products shortest delivery time -> "productShortDevX"
                            @products description -> "productDescX";
                            @products result link -> "productLinkX"
                            @requested amount -> "productAmountX"
                            retuns <td> element with data inside;
@shop list in ul element -> "shopListX"; retuns <ul> element with list of shops avaible for a inside;
@shop name in ul header -> "productXShopZName"; returns <h5> element with shop name inside;
@shop parametrs:    @shop price -> "productXShopZPrice"
                    @shop delivery price -> "productXShopZDevPrice"
                    @shop delivery time -> "productXShopZDevTime"
                    @shop availability -> "productXShopZAva";
                    returns <td> element with data inside;
@buy now button -> "buyButtonProductXShopZ"; returns <a> element with a "href" parametr targeting (_blank) to selected shop url, 
                                             inside the data is shown in a following way: "Buy now for {if not null(delivery_price) + price}"
@save button -> "saveButton"; returns <button> element with a 'onclick' attribute set on 'saveToHistory()' value;
@home button -> "goBackButton"; returns <button> element

where:
*X indicates products (eg. "domek") number, starting from 1 
*Y indicates number of a specific radiobutton in its group, starting from 1
*Z indicates shop number for a specific product, starting from 1

*/

function generateDOM() {
    var productsCounter = 1;
    //for now, only ceneo is implemented
    var ceneoData = searchResult["ceneo"];
    Object.keys(ceneoData).forEach(userInput => {

        // dictionray content, using first element to fullfil data
        var tempData = ceneoData[userInput][0];
        //accordion item
        var accordionItem = document.createElement("div");
        accordionItem.setAttribute("id", "accordionItem" + productsCounter);
        accordionItem.setAttribute("class", "accordion-item");

        //accordion header
        var accordionHeader = document.createElement("h2");
        accordionHeader.setAttribute("id", "headingMain" + productsCounter);
        accordionHeader.setAttribute("class", "accordion-header");
        //accordion button-display
        var accordionButton = document.createElement("button");
        accordionButton.setAttribute("id", "productNameAC" + productsCounter);
        if (productsCounter == 1) {
            accordionButton.setAttribute("aria-expanded", "true");
            accordionButton.setAttribute("class", "accordion-button");
        } else {
            accordionButton.setAttribute("aria-expanded", "false");
            accordionButton.setAttribute("class", "accordion-button collapsed");
        }
        accordionButton.setAttribute("type", "button");
        accordionButton.setAttribute("data-bs-toggle", "collapse");
        accordionButton.setAttribute("data-bs-target", "#collapseMain" + productsCounter);
        accordionButton.setAttribute("aria-controls", "collapseMain" + productsCounter);
        accordionButton.innerHTML = userInput;
        //button into h2
        accordionHeader.appendChild(accordionButton);
        //accordion header into accordion item
        accordionItem.appendChild(accordionHeader);

        //accordion content
        //accordion body div
        var accordionBodyDiv = document.createElement("div");
        accordionBodyDiv.setAttribute("id", "collapseMain" + productsCounter);
        if (productsCounter == 1) {
            accordionBodyDiv.setAttribute("class", "accordion-collapse collapse show");
        } else {
            accordionBodyDiv.setAttribute("class", "accordion-collapse collapse");
        }
        accordionBodyDiv.setAttribute("aria-labelledby", "headingMain" + productsCounter);
        accordionBodyDiv.setAttribute("data-bs-parent", "#accordionMain");
        //accordion body
        var accordionBody = document.createElement("div");
        accordionBody.setAttribute("class", "accordion-body");
        accordionBody.setAttribute("id", "accordionBody" + productsCounter);

        //product not found
        if ((Object.keys(ceneoData[userInput]).length == 0)) {

            var nullInfo = document.createElement("h2");
            nullInfo.innerHTML = "Product not found"
            accordionBody.appendChild(nullInfo);
            //accordionBody into accordionBodyDiv
            accordionBodyDiv.appendChild(accordionBody);
            //accordionBodyDiv into accordionItem
            accordionItem.appendChild(accordionBodyDiv);

            //accordion item into accordion Main
            accordionMain.appendChild(accordionItem)
            productsCounter++;

        } else {
            //unambigious search
            if (!(Object.keys(ceneoData[userInput]).length == 1)) {
                //create info disclamer
                var disclamer = document.createElement("h3");
                disclamer.setAttribute("class", "float-start");
                disclamer.innerHTML = "Did you mean... ";
                //attach disclamer into accordion-body
                accordionBody.appendChild(disclamer);

                //create radiobuttons group
                var radioButGroupDiv = document.createElement("div");
                radioButGroupDiv.setAttribute("id", "specifyProductRadioButton" + productsCounter);
                radioButGroupDiv.setAttribute("class", "btn-group");
                radioButGroupDiv.setAttribute("role", "group" + productsCounter);
                radioButGroupDiv.setAttribute("aria-label", "Basic radio toggle button group");
                //creating radiobuttons
                ceneoData[userInput].forEach(function (product, ind) {
                    //radiobutton input
                    var inputRadioBtn = document.createElement("input");
                    inputRadioBtn.setAttribute("type", "radio");
                    inputRadioBtn.setAttribute("class", "btn-check triggerChangingDataFun");
                    inputRadioBtn.setAttribute("name", "btnradio" + productsCounter);
                    inputRadioBtn.setAttribute("id", "btnradio" + (ind + 1) + "Product" + productsCounter);
                    inputRadioBtn.setAttribute("autocomplete", "off");
                    if (ind == 0) {
                        inputRadioBtn.setAttribute("checked", "true");
                    }
                    //radiobutton label
                    var labelRadioBtn = document.createElement("label");
                    labelRadioBtn.setAttribute("class", "btn btn-outline-primary");
                    labelRadioBtn.setAttribute("for", "btnradio" + (ind + 1) + "Product" + productsCounter);
                    labelRadioBtn.innerHTML = (ind + 1) + ". " + product["name"].slice(0, 8) + "...";

                    //attaching input and label to radiButGroupDiv
                    radioButGroupDiv.appendChild(inputRadioBtn);
                    radioButGroupDiv.appendChild(labelRadioBtn);
                })
                //attaching radiButGroupDiv to accordionBody
                accordionBody.appendChild(radioButGroupDiv);
            }

            //default for both kind of searches
            //table with image and products details
            var tableImgDeta = document.createElement("table");
            tableImgDeta.setAttribute("id", "productTable" + productsCounter);
            tableImgDeta.setAttribute("class", "table table-borderless");

            //tbody
            var tableImgDetaBody = document.createElement("tbody");

            //tr with img and details
            var imageDetaRow = document.createElement("tr");
            //td with img
            var imageCol = document.createElement("td");
            imageCol.setAttribute("id", "productImg" + productsCounter);
            //img
            var productImg = document.createElement("img");
            productImg.setAttribute("src", tempData["img"]);
            productImg.setAttribute("class", "rounded float-start");
            productImg.setAttribute("style", "width: 100px; height: 100px;");
            //attaching elements
            //img into td
            imageCol.appendChild(productImg);
            //td into tr
            imageDetaRow.appendChild(imageCol);

            //td with details
            var detaCol = document.createElement("td");
            detaCol.setAttribute("id", "productDetails" + productsCounter);
            //table with details
            var detaTable = document.createElement("table");
            detaTable.setAttribute("class", "table table-borderless");
            var detaTableTbody = document.createElement("tbody");

            //products name
            var nameRow = document.createElement("tr");
            var nameLable = document.createElement("td");
            nameLable.setAttribute("class", "float-start");
            nameLable.innerHTML = "<b>Name</b>";
            var nameValue = document.createElement("td");
            nameValue.setAttribute("id", "productName" + productsCounter);
            nameValue.innerHTML = tempData["name"];
            //attaching elements
            nameRow.appendChild(nameLable);
            nameRow.appendChild(nameValue);
            //attaching nameRow into detaTableTbody
            detaTableTbody.appendChild(nameRow);

            //products rating
            var ratingRow = document.createElement("tr");
            var ratingLable = document.createElement("td");
            ratingLable.setAttribute("class", "float-start");
            ratingLable.innerHTML = "<b>Rating</b>";
            var ratingValue = document.createElement("td");
            ratingValue.setAttribute("id", "productRating" + productsCounter);
            if (tempData["rating"] === false) {
                ratingValue.innerHTML = "No data avaible";
            } else if (tempData["rating"] !== null) {
                ratingValue.innerHTML = tempData["rating"] + "/5";
            } else {
                ratingValue.innerHTML = "No data avaible";
            }
            //attaching elements
            ratingRow.appendChild(ratingLable);
            ratingRow.appendChild(ratingValue);
            //attaching ratingRow into detaTableTbody
            detaTableTbody.appendChild(ratingRow);

            //products lowest price
            var lowPriceRow = document.createElement("tr");
            var lowPriceLable = document.createElement("td");
            lowPriceLable.setAttribute("class", "float-start");
            lowPriceLable.innerHTML = "<b>Lowest Price</b>";
            var lowPriceValue = document.createElement("td");
            lowPriceValue.setAttribute("id", "productLowPrice" + productsCounter);
            //searching lowest price
            var minTempPrice = 10000000000;
            tempData["shop_list"].forEach((tempPrice) => {
                if (tempPrice["price"] <= minTempPrice) {
                    minTempPrice = tempPrice["price"];
                }
            })
            lowPriceValue.innerHTML = minTempPrice + " zł";
            //attaching elements
            lowPriceRow.appendChild(lowPriceLable);
            lowPriceRow.appendChild(lowPriceValue);
            //attaching lowPriceRow into detaTableTbody
            detaTableTbody.appendChild(lowPriceRow);

            //products shortest delivery time
            var shorDevTimeRow = document.createElement("tr");
            var shorDevTimeLable = document.createElement("td");
            shorDevTimeLable.setAttribute("class", "float-start");
            shorDevTimeLable.innerHTML = "<b>Shortest delivery time</b>";
            var shorDevTimeValue = document.createElement("td");
            shorDevTimeValue.setAttribute("id", "productShortDev" + productsCounter);
            //searching shortest dev time
            var minDevTime = 10000000000;
            tempData["shop_list"].forEach((tempDevTime) => {
                if (tempDevTime["delivery_time"] !== null) {
                    if (tempDevTime["delivery_time"] <= minDevTime) {
                        minDevTime = tempDevTime["delivery_time"];
                    }
                }
            })
            if (minDevTime == 10000000000) {
                shorDevTimeValue.innerHTML = "No data avaible";
            } else {
                shorDevTimeValue.innerHTML = minDevTime + "dni.";
            }
            //attaching elements
            shorDevTimeRow.appendChild(shorDevTimeLable);
            shorDevTimeRow.appendChild(shorDevTimeValue);
            //attaching shorDevTimeRow into detaTableTbody
            detaTableTbody.appendChild(shorDevTimeRow);

            //products Desc
            var DescRow = document.createElement("tr");
            var DescLable = document.createElement("td");
            DescLable.setAttribute("class", "float-start");
            DescLable.innerHTML = "<b>Description</b>";
            var DescValue = document.createElement("td");
            DescValue.setAttribute("id", "productDesc" + productsCounter);
            DescValue.innerHTML = tempData["description"].slice(0, 1000) + "...";
            //attaching elements
            DescRow.appendChild(DescLable);
            DescRow.appendChild(DescValue);
            //attaching DescRow into detaTableTbody
            detaTableTbody.appendChild(DescRow);

            //results link
            var linkRow = document.createElement("tr");
            var linkLable = document.createElement("td");
            linkLable.setAttribute("class", "float-start");
            linkLable.innerHTML = "<b>Results link</b>";
            var linkValue = document.createElement("td");
            linkValue.setAttribute("id", "productLink" + productsCounter);
            var link = document.createElement("a");
            link.innerHTML = "Go to page.";
            link.setAttribute("target", "_blank");
            link.setAttribute("href", tempData["url"]);
            //attaching elements
            linkValue.appendChild(link);
            linkRow.appendChild(linkLable);
            linkRow.appendChild(linkValue);
            //attaching linkRow into detaTableTbody;
            detaTableTbody.appendChild(linkRow);

            // amount
            var amountRow = document.createElement("tr");
            let amountLable = document.createElement("td");
            amountLable.setAttribute("class", "float-start");
            amountLable.innerHTML = "<b>Requested amount</b>";
            let amountValue = document.createElement("td");
            amountValue.setAttribute("id", "productAmount" + productsCounter);
            let amount = document.createElement("span");
            amount.innerHTML = searchResult['amount'][userInput];
            //attaching elements
            amountValue.appendChild(amount);
            amountRow.appendChild(amountLable);
            amountRow.appendChild(amountValue);
            //attaching amountRow into detaTableTbody;
            detaTableTbody.appendChild(amountRow);

            //attaching elements
            //attaching detaTableTbody into dataTable
            detaTable.appendChild(detaTableTbody);
            //attaching details table into details collumn
            detaCol.appendChild(detaTable)
            //attaching detaCol into imageDetaRow
            imageDetaRow.appendChild(detaCol);
            //attaching imageDetaRow into tableImgDetaBody
            tableImgDetaBody.appendChild(imageDetaRow);
            //attach tbody into table
            tableImgDeta.appendChild(tableImgDetaBody);
            //attach table into accordion body
            accordionBody.appendChild(tableImgDeta);

            //creating shops list
            var shopListUl = document.createElement("ul");
            shopListUl.setAttribute("class", "list-group");
            shopListUl.setAttribute("id", "shopList" + productsCounter);
            tempData["shop_list"].forEach((shopDic, ind) => {
                //attaching shopListUl into accordionBody
                accordionBody.appendChild(generateShopListDOM(shopListUl, shopDic, ind, productsCounter));
            })


            //accordionBody into accordionBodyDiv
            accordionBodyDiv.appendChild(accordionBody);
            //accordionBodyDiv into accordionItem
            accordionItem.appendChild(accordionBodyDiv);

            //accordion item into accordion Main
            accordionMain.appendChild(accordionItem)
            productsCounter++;
        }
    });

    //onclick event handler
    //changing presented data after checking another radiobutton
    $(".triggerChangingDataFun").click(function (event) {
        //product number
        var selectedProductNumber = parseInt(event.target.name.split("btnradio")[1]);
        //radiobutton number
        var selectedRadioButtonNumber = parseInt(event.target.id.split("btnradio")[1].split(("Product" + selectedProductNumber)));
        //new data
        refreshNewData(selectedProductNumber, selectedRadioButtonNumber);
        selectedProducts[Object.keys(searchResult["ceneo"])[selectedProductNumber - 1]] = selectedRadioButtonNumber;
    });

    //changing presented data after choseing another accordion
    $(".accordion-button").click(function (event) {
        //product number
        var selectedProductNumber = parseInt(event.target.id.split("productNameAC")[1]);
        if (document.getElementById("accordionBody" + selectedProductNumber).firstChild.innerHTML !== "Product not found") {
            //radiobutton number
            var selectedRadioButtonNumber = 1;
            var productLink_ = document.getElementById("productLink" + selectedProductNumber).firstChild.href;
            var tempCounter = 1;
            for (let cos of searchResult["ceneo"][document.getElementById("productNameAC" + selectedProductNumber).innerHTML]) {
                if (cos["url"] === productLink_) {
                    selectedRadioButtonNumber = tempCounter;
                    break;
                } else {
                    tempCounter++;
                }
            }
            refreshNewData(selectedProductNumber, selectedRadioButtonNumber);
        }
    });
}


// save to history
function saveToHistory() {
    // prepare data to save
    let productsToSaveDict = {};
    Object.keys(searchResult['ceneo']).forEach(function (key, ind) {
        let product_list = searchResult['ceneo'][key];
        let activeProductName = "#productName" + (ind + 1);
        let activeProduct = {};
        if ($(activeProductName).length > 0) {
            activeProductName = $(activeProductName)[0].innerText;
            product_list.forEach(function (product, ind) {
                if (product['name'] === activeProductName) {
                    activeProduct = product;
                }
            });
        } else {
            activeProduct['ceneo'] = [];
        }
        activeProduct['amount'] = searchResult['amount'][key]
        productsToSaveDict[key] = activeProduct;
    });

    $.ajax({
        type: "POST",
        url: "/history",
        async: false,
        data: {
            'products': JSON.stringify(productsToSaveDict)
        },
        success: function () {
            displayInfo("ITEM_ADDED_TO_HISTORY");
            document.getElementById("saveButton").disabled = true;
        },
        error: function () {
            displayInfo("FAIL_TO_SAVE");
        }
    });
}



function showResultsModal(isOptimizedForStorecount) {

    // clear table with products
    modalSearchOverviewTableBody.innerHTML = "";


    // show search button
    $("#modalSaveButton").show();
    $("#modalGoBackButton").show();
    //var selectedProducts = {...selectedProducts};
    //var searchResult  = {...searchResult};
    for(var key in searchResult["ceneo"]){
        if(searchResult["ceneo"][key].length == 0){
            //delete searchResult["ceneo"][key];
            delete selectedProducts[key];
        }
    }

    // optimize results
    if(isOptimizedForStorecount){
        
        
        var selectedProductsStores = {};
        var selectedProductsTemp = {...selectedProducts};

        //count which stores are most common
        while(Object.keys(selectedProductsTemp).length > 0){
            var storeList = {};
            for(var key in selectedProductsTemp){ //iterate over searches
                for(var storeIterated in searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"]){ //iterate over stores for that search
                    if(searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"][storeIterated]["name"] in storeList){
                        storeList[searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"][storeIterated]["name"]]++;
                    } else{
                        storeList[searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"][storeIterated]["name"]] = 1;
                    }
                }
            }
            //choose the most common one
            var max = 0;
            var bestStore;
            for(var key in storeList){
                if (storeList[key] > max){
                    bestStore = key;
                    max = storeList[key];
                }
            }
            //add the most common one to selectedProductsStores and delete the product from searched
            for(var key in selectedProductsTemp){ //iterate over searches
                for(var storeIterated in searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"]){ //iterate over stores for that search
                    if(searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"][storeIterated]["name"] == bestStore){
                        selectedProductsStores[key] = searchResult["ceneo"][key][selectedProductsTemp[key]-1]["shop_list"][storeIterated];
                        delete selectedProductsTemp[key];
                        break;
                    }
                }
            }
        }
        console.log(selectedProductsStores);
        let ind = 0;
        for (var key in selectedProducts) {
            let row = modalSearchOverviewTableBody.insertRow(ind);
            ind = ind + 1;
            let name = row.insertCell(0);
            name.innerHTML = searchResult["ceneo"][key][selectedProducts[key] - 1]["name"];
            let price = row.insertCell(1);
            price.innerHTML = selectedProductsStores[key]['price'];
            let amount = row.insertCell(2);
            amount.innerHTML = searchResult["amount"][key];
            
            let store = row.insertCell(3);
            store.innerHTML = selectedProductsStores[key]['name'];

            let link = row.insertCell(4);
            link.innerHTML = '<a href="' + selectedProductsStores[key]['url'] + '">link</a>';
            //console.log(key, selectedProducts[key]);
        }


    } else {

        let ind = 0;
        for (var key in selectedProducts) {
            let row = modalSearchOverviewTableBody.insertRow(ind);
            ind = ind + 1;
            let nrSklepu = 0;
            let name = row.insertCell(0);
            name.innerHTML = searchResult["ceneo"][key][selectedProducts[key] - 1]["name"];
            let price = row.insertCell(1);
            price.innerHTML = searchResult["ceneo"][key][selectedProducts[key] - 1]["shop_list"][nrSklepu]["price"];
            let amount = row.insertCell(2);
            amount.innerHTML = searchResult["amount"][key];
            let store = row.insertCell(3);
            store.innerHTML = searchResult["ceneo"][key][selectedProducts[key] - 1]["shop_list"][nrSklepu]["name"];
            let link = row.insertCell(4);
            link.innerHTML = '<a href="' + searchResult["ceneo"][key][selectedProducts[key] - 1]
                ["shop_list"][nrSklepu]["url"] + '">link</a>';
            //console.log(key, selectedProducts[key]);
        }
    }
    //refreshModalTable();

    // show modal
    $('#staticBackdrop').modal('show');
}



//refresh currently shown data withe new one, indicated by a radiobutton selected by the user
//@param
//selectedProductNumber- product number e.g. for user input-> ['X','Y','Z'] selectedProductNumber would be 1 for X, 2 for Y and 3 for Z;
//selectedRadioButtonNumber- number of radio button selected by user in a specific radiobutton group- from 1 to 10
function refreshNewData(selectedProductNumber, selectedRadioButtonNumber) {

    //user input
    var userInput = document.getElementById("productNameAC" + selectedProductNumber).innerHTML;
    //selected, new product 
    var newProductData = searchResult["ceneo"][userInput][selectedRadioButtonNumber - 1]; //-1 for table index starts from 0;

    //refreshig basic info data:
    //img
    document.getElementById("productImg" + selectedProductNumber).childNodes[0].src = newProductData["img"];
    //product name
    document.getElementById("productName" + selectedProductNumber).innerHTML = newProductData["name"];
    //product rating
    if (newProductData["rating"] === false) {
        document.getElementById("productRating" + selectedProductNumber).innerHTML = "No data avaible";
    } else if (newProductData["rating"] !== null) {
        document.getElementById("productRating" + selectedProductNumber).innerHTML = newProductData["rating"] + "/5";
    } else {
        document.getElementById("productRating" + selectedProductNumber).innerHTML = "No data avaible";
    }
    //product lowest price
    var minTempPrice = 10000000000;
    newProductData["shop_list"].forEach((tempPrice) => {
        if (tempPrice["price"] <= minTempPrice) {
            minTempPrice = tempPrice["price"];
        }
    })
    document.getElementById("productLowPrice" + selectedProductNumber).innerHTML = minTempPrice + " zł";
    //product shortest delivery time
    var minDevTime = 10000000000;
    newProductData["shop_list"].forEach((tempDevTime) => {
        if (tempDevTime["delivery_time"] !== null) {
            if (tempDevTime["delivery_time"] <= minDevTime) {
                minDevTime = tempDevTime["delivery_time"];
            }
        }
    })
    if (minDevTime == 10000000000) {
        document.getElementById("productShortDev" + selectedProductNumber).innerHTML = "No data avaible";
    } else {
        document.getElementById("productShortDev" + selectedProductNumber).innerHTML = minDevTime + "dni.";
    }
    //product desc
    document.getElementById("productDesc" + selectedProductNumber).innerHTML = newProductData["description"];
    //product link
    document.getElementById("productLink" + selectedProductNumber).firstChild.setAttribute("href", newProductData["url"]);

    //refreshing shop list
    //delete shops
    document.getElementById("shopList" + selectedProductNumber).remove();

    //new shop list
    var newShopList = document.createElement("ul");
    newShopList.setAttribute("class", "list-group");
    newShopList.setAttribute("id", "shopList" + selectedProductNumber);
    newProductData["shop_list"].forEach(function (shopDic, ind) {
        //attaching shopListUl into accordionBody
        document.getElementById("accordionBody" + selectedProductNumber).appendChild(generateShopListDOM(newShopList, shopDic, ind, selectedProductNumber));
    })

}

//generates shop list consisting of HTML <ul> and <li> elements
//@param
//shopListUl- <ul> element into which <li> elements will be inserted
//shopDic- dictionary consisting data about the shop
//ind- index of shopDic in his ancestor
//productsCounter- product number e.g. for user input-> ['X','Y','Z'] productsCounter would be 1 for X, 2 for Y and 3 for Z;
//returns <ul> elements filled with data
function generateShopListDOM(shopListUl, shopDic, ind, productsCounter) {

    //creating li element
    var shopLiElement = document.createElement("li");
    shopLiElement.setAttribute("class", "list-group-item");
    ind = ind + 1;
    //creating shop header with shops name in int
    var shopHeader = document.createElement("h5");
    shopHeader.setAttribute("id", "product" + productsCounter + "Shop" + (ind) + "Name");
    shopHeader.setAttribute("class", "float-start");
    shopHeader.innerHTML = shopDic["name"] + "<br>";
    //creating a table with shop details
    var shopDetTable = document.createElement("table");
    shopDetTable.setAttribute("class", "table table-borderless");
    //attaching header into lielement
    shopLiElement.appendChild(shopHeader);

    //createing tr
    var shopDetTableRow = document.createElement("tr");

    //shop price:
    var shopPriceLabel = document.createElement("td");
    shopPriceLabel.innerHTML = "<b>Price: </b>";
    var shopPriceValue = document.createElement("td");
    shopPriceValue.setAttribute("id", "product" + productsCounter + "Shop" + ind + "Price");
    shopPriceValue.innerHTML = shopDic["price"].toFixed(2) + " zł";
    //attaching elements to tr
    shopDetTableRow.appendChild(shopPriceLabel);
    shopDetTableRow.appendChild(shopPriceValue);

    //shop delivery price:
    var shopDeliveryPriceLabel = document.createElement("td");
    shopDeliveryPriceLabel.innerHTML = "<b>Delivery price: </b>";
    var shopDeliveryPriceValue = document.createElement("td");
    shopDeliveryPriceValue.setAttribute("id", "product" + productsCounter + "Shop" + ind + "DevPrice");
    if (shopDic["delivery_price"] !== null) {
        shopDeliveryPriceValue.innerHTML = shopDic["delivery_price"].toFixed(2) + " zł";
    } else {
        shopDeliveryPriceValue.innerHTML = "Not avaible";
    }
    //attaching elements to tr
    shopDetTableRow.appendChild(shopDeliveryPriceLabel);
    shopDetTableRow.appendChild(shopDeliveryPriceValue);

    //shop delivery time:
    var shopDeliveryTimeLabel = document.createElement("td");
    shopDeliveryTimeLabel.innerHTML = "<b>Delivery time: </b>";
    var shopDeliveryTimeValue = document.createElement("td");
    shopDeliveryTimeValue.setAttribute("id", "product" + productsCounter + "Shop" + ind + "DevTime");
    if (shopDic["delivery_time"] !== null) {
        shopDeliveryTimeValue.innerHTML = shopDic["delivery_time"];
    } else {
        shopDeliveryTimeValue.innerHTML = "Not avaible";
    }
    //attaching elements to tr
    shopDetTableRow.appendChild(shopDeliveryTimeLabel);
    shopDetTableRow.appendChild(shopDeliveryTimeValue);

    //shop availability:
    var shopAvailabilityLabel = document.createElement("td");
    shopAvailabilityLabel.innerHTML = "<b>Availability: </b>";
    var shopAvailabilityValue = document.createElement("td");
    shopAvailabilityValue.setAttribute("id", "product" + productsCounter + "Shop" + ind + "Ava");
    if (shopDic["availability"] !== null) {
        if (shopDic["availability"] == 0) {
            shopAvailabilityValue.innerHTML = "In stock";
        } else {
            shopAvailabilityValue.innerHTML = "Avaible in " + shopDic["availability"] + " days.";
        }
    } else {
        shopAvailabilityValue.innerHTML = "Not avaible";
    }
    //attaching elements to tr
    shopDetTableRow.appendChild(shopAvailabilityLabel);
    shopDetTableRow.appendChild(shopAvailabilityValue);

    //buy now button
    var tdBuyButton = document.createElement("td");
    var buttonDiv = document.createElement("div");
    var buyNowButton = document.createElement("a");
    buyNowButton.setAttribute("role", "button");
    buyNowButton.setAttribute("href", shopDic["url"]);
    buyNowButton.setAttribute("target", "_blank");
    buyNowButton.setAttribute("id", "buyButtonProduct" + productsCounter + "Shop" + ind);
    buyNowButton.setAttribute("class", "btn btn-success me-3");
    if (shopDic["delivery_price"] !== null) {
        buyNowButton.innerHTML = "Buy now for " + (shopDic["delivery_price"] + shopDic["price"]).toFixed(2) + " zł.";
    } else {
        buyNowButton.innerHTML = "Buy now for " + (shopDic["price"]).toFixed(2) + " zł.";
    }
    //attaching button
    buttonDiv.appendChild(buyNowButton)
    tdBuyButton.appendChild(buttonDiv);
    shopDetTableRow.appendChild(tdBuyButton);

    //attaching all elements
    //attaching shopDetTableRow into shopDetTable 
    shopDetTable.appendChild(shopDetTableRow);
    //attaching shopDetTable into shopLiElement
    shopLiElement.appendChild(shopDetTable);
    //attaching shopLiElement into Ul
    shopListUl.appendChild(shopLiElement);

    return shopListUl;
}


//function display info to user
function displayInfo(infoCode){
    document.getElementById("trigerInfoModal").click();
    document.getElementById("infoInModal").innerHTML = InfoStatus[infoCode];
}