// from data.js
var tableData = data;

// Create table to show the data
function displayTable(data){
    var tbody = d3.select("tbody");

    data.forEach((ufoData) =>{
        var row = tbody.append("tr");
    
        Object.entries(ufoData).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });  
};

// Display table without filters applied
displayTable(tableData);


var button = d3.select("#filter-btn");

button.on("click", function() {
    
    var inputElementDate = d3.select("#datetime");
    var inputDate = inputElementDate.property("value");

    var inputElementCity = d3.select("#city");
    var inputCity= inputElementCity.property("value");

    var inputElementState = d3.select("#state");
    var inputState= inputElementState.property("value");    

    var inputElementCountry = d3.select("#country");
    var inputCountry= inputElementCountry.property("value");    

    console.log(inputDate);
    console.log(inputCity);
    console.log(inputState);
    console.log(inputCountry);

    // select the table tbody 
    var table = d3.select("tbody");

    // remove any rows from the table
    table.html("");

    var filteredData = tableData.filter(function(row) {
        return  (row.datetime===inputDate || !inputElementDate.property("value") ) && 
                (row.city===inputCity || !inputElementCity.property("value")) &&
                (row.state===inputState || !inputElementState.property("value")) &&
                (row.country===inputCountry || !inputElementCountry.property("value"))

    })
    
//    var filteredData = tableData.filter(row => row.datetime === inputDate
//                                            & row.city === inputCity
//        );

    displayTable(filteredData);

  });


// Load combo with existing cities
var listCity = cities;

function loadCity(city) {

    console.log(city);
    
    d3.select("#city").selectAll("option")
    .data(city)
    .enter() // creates placeholder for new data
    .append("option") // appends an option to placeholder
    .html(function(d) {
      return `<option value="${d}">${d}</option>`;
    }); 

}

loadCity(listCity);

// Load combo with existing states
var listStates = states;

function loadStates(state) {

    console.log(state);
    
    d3.select("#state").selectAll("option")
    .data(state)
    .enter() // creates placeholder for new data
    .append("option") // appends an option to placeholder
    .html(function(d) {
      return `<option value="${d}">${d}</option>`;
    }); 

}

loadStates(listStates);

// Load combo with existing countries
var listCountry = countries;

function loadCountry(country) {

    console.log(country);
    
    d3.select("#country").selectAll("option")
    .data(country)
    .enter() // creates placeholder for new data
    .append("option") // appends an option to placeholder
    .html(function(d) {
      return `<option value="${d}">${d}</option>`;
    }); 

}

loadCountry(listCountry);
