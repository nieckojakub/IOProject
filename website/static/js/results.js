// ##########################################################
// ##################### variables ##########################
// ##########################################################
let searchResult;


// ##########################################################
// ##################### DOM elems ##########################
// ##########################################################
var accordionMain = document.getElementById("accordionMain"); //main accordion
var test;

// run code after loading the page
$(function (){
    let token = window.location.pathname;
    token = token.replace('/results/', '');

    $.ajax({
        url: "/search/" + token,
        type: 'GET',
        success: function(data){
            searchResult = JSON.parse(data);
            generateDOM();
        },
        error: function() {
            // redirect
            window.location.replace(window.location.origin);
        }
    });
});

// ##########################################################
// ##################### functions ##########################
// ##########################################################

//generates DOM elements and fill them with data
//TODO- najniższa cena i najkrótszy czas dostawy
function generateDOM() {
    //TODO- ustaw na 1
    var productsCounter = 3;
    //for now only ceneo is implemented
    var ceneoData = searchResult["ceneo"];
    Object.keys(ceneoData).forEach(userInput => {
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
        accordionButton.setAttribute("id", "productName" + productsCounter);
        if(productsCounter == 1){
            accordionButton.setAttribute("aria-expanded", "true");  
            accordionButton.setAttribute("class", "accordion-button");
        }else{
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
        accordionBodyDiv.setAttribute("id","collapseMain" + productsCounter);
        if(productsCounter == 1){
            accordionBodyDiv.setAttribute("class","accordion-collapse collapse show");
        }else{
            accordionBodyDiv.setAttribute("class","accordion-collapse collapse");
        }
        accordionBodyDiv.setAttribute("aria-labelledby","headingMain" + productsCounter);
        accordionBodyDiv.setAttribute("data-bs-parent","#accordionMain");
        //accordion body
        var accordionBody = document.createElement("div");
        accordionBody.setAttribute("class","accordion-body");
        
        //ambiguous search
        if(Object.keys(ceneoData[userInput]).length == 1){
            var tempData = ceneoData[userInput][0];
            console.log(tempData)

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
                    nameValue.setAttribute("id","productName" + productsCounter );
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
                    ratingValue.setAttribute("id","productRating" + productsCounter );
                    ratingValue.innerHTML = tempData["rating"] + "/5";
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
                    lowPriceValue.setAttribute("id","productLowPrice" + productsCounter );
                    //searching lowest price
                    //TODO- to da sie lepiej zrobić
                    var minTempPrice = 10000000000;
                    tempData["shop_list"].forEach((tempPrice) => {
                        if(tempPrice["price"] <= minTempPrice){
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
                    shorDevTimeValue.setAttribute("id","productLowPrice" + productsCounter );
                    //searching shortest dev time
                    //TODO- to da sie lepiej zrobić
                    var minDevTime = 10000000000;
                    tempData["shop_list"].forEach((tempDevTime) => {
                        if(tempDevTime["delivery_time"] !== null){
                            if(tempDevTime["delivery_time"] <= minDevTime){
                                minDevTime = tempDevTime["delivery_time"];
                            }
                        }
                    })
                    if(minDevTime == 10000000000){
                        shorDevTimeValue.innerHTML = "No data avaible";
                    }else{
                        //TODO- jaka jednostak czasu?
                        shorDevTimeValue.innerHTML = minDevTime + "?TODO";
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
                    DescValue.setAttribute("id","productDesc" + productsCounter );
                    DescValue.innerHTML = tempData["description"].slice(0,1000) + "...";
                    //attaching elements
                    DescRow.appendChild(DescLable);
                    DescRow.appendChild(DescValue);
                //attaching DescRow into detaTableTbody
                detaTableTbody.appendChild(DescRow);



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
        
        
        }else{
        ///////////////unambigious search///////////////////
            
            var tempData = ceneoData[userInput][0];
            console.log(tempData)

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
            ceneoData[userInput].forEach(function(product, ind){
                //radiobutton input
                var inputRadioBtn = document.createElement("input");
                inputRadioBtn.setAttribute("type", "radio");
                inputRadioBtn.setAttribute("class", "btn-check");
                inputRadioBtn.setAttribute("name", "btnradio" + productsCounter);
                inputRadioBtn.setAttribute("id", "btnradio"+(ind+1)+"1Product" + productsCounter);
                inputRadioBtn.setAttribute("autocomplete", "off");
                if(ind == 0){
                    inputRadioBtn.setAttribute("checked", "true");
                }
                //radiobutton label
                var labelRadioBtn = document.createElement("label");
                labelRadioBtn.setAttribute("class", "btn btn-outline-primary");
                labelRadioBtn.setAttribute("for", "btnradio"+(ind+1)+"1Product" + productsCounter);
                labelRadioBtn.innerHTML = (ind + 1) +". "+product["name"].slice(0,8) + "...";

                //attaching input and label to radiButGroupDiv
                radioButGroupDiv.appendChild(inputRadioBtn);
                radioButGroupDiv.appendChild(labelRadioBtn);
            })
            //attaching radiButGroupDiv to accordionBody
            accordionBody.appendChild(radioButGroupDiv);

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
                    nameValue.setAttribute("id","productName" + productsCounter );
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
                    ratingValue.setAttribute("id","productRating" + productsCounter );
                    ratingValue.innerHTML = tempData["rating"] + "/5";
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
                    lowPriceValue.setAttribute("id","productLowPrice" + productsCounter );
                    //searching lowest price
                    //TODO- to da sie lepiej zrobić
                    var minTempPrice = 10000000000;
                    tempData["shop_list"].forEach((tempPrice) => {
                        if(tempPrice["price"] <= minTempPrice){
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
                    shorDevTimeValue.setAttribute("id","productLowPrice" + productsCounter );
                    //searching shortest dev time
                    //TODO- to da sie lepiej zrobić
                    var minDevTime = 10000000000;
                    tempData["shop_list"].forEach((tempDevTime) => {
                        if(tempDevTime["delivery_time"] !== null){
                            if(tempDevTime["delivery_time"] <= minDevTime){
                                minDevTime = tempDevTime["delivery_time"];
                            }
                        }
                    })
                    if(minDevTime == 10000000000){
                        shorDevTimeValue.innerHTML = "No data avaible";
                    }else{
                        //TODO- jaka jednostak czasu?
                        shorDevTimeValue.innerHTML = minDevTime + "?TODO";
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
                    DescValue.setAttribute("id","productDesc" + productsCounter );
                    DescValue.innerHTML = tempData["description"].slice(0,1000) + "...";
                    //attaching elements
                    DescRow.appendChild(DescLable);
                    DescRow.appendChild(DescValue);
                //attaching DescRow into detaTableTbody
                detaTableTbody.appendChild(DescRow);



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
        }



        //accordionBody into accordionBodyDiv
        accordionBodyDiv.appendChild(accordionBody); 
        //accordionBodyDiv into accordionItem
        accordionItem.appendChild(accordionBodyDiv);









        //accordion item into accordion Main
        accordionMain.appendChild(accordionItem)
        productsCounter++;
    });
}