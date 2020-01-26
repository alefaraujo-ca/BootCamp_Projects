// from data.js
var tableData = data;

// YOUR CODE HERE!

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
    
    var inputElement = d3.select("#datetime");
    var inputValue= inputElement.property("value");

    console.log(inputValue);

    // select the table tbody 
    var table = d3.select("tbody");

    // remove any rows from the table
    table.html("");

    var filteredData = tableData.filter(row => row.datetime === inputValue);

    displayTable(filteredData);

  });