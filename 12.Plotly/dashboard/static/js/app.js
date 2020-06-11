function plots(id) {
    var jfile = "./data/samples.json"
    d3.json(jfile).then((data) => {


        // filter sample values by id 
        var samples = data.samples.filter(s => s.id.toString() === id)[0];

        plotBar(samples);
        plotBubble(samples);

        //var wfreq = data.metadata.map(d => d.wfreq)
        var wfreq = data.metadata.filter(s => s.id.toString() === id)[0];        
        plotGauge(wfreq);

    });
};

function plotBar(data) {

    // Getting the top 10 
    var top10_sample_values = data.sample_values.slice(0, 10).reverse();
    var top10_out_ids = data.otu_ids.slice(0, 10).reverse();
    var top10_otu_labels = data.otu_labels.slice(0, 10).reverse();

    console.log(top10_out_ids);

    // get the otu id's to the desired form for the plot
    var otu_ids = top10_out_ids.map(d => "OTU " + d);
    console.log(otu_ids);


    // Trace1 for the Data
    var trace1 = {
        x: top10_sample_values,
        y: otu_ids,
        text: top10_otu_labels,
        name: "Top 10 OTUs",
        type: "bar",
        orientation: "h"
    };

    // data
    var plot_data = [trace1];

    // Apply the group bar mode to the layout
    var layout = {
        title: "Top 10 OTUs found in that individual",
        margin: {
            l: 100,
            r: 100,
            t: 100,
            b: 30
        }
    };

    // Render the plot to the div tag with id "plot"
    Plotly.newPlot("bar", plot_data, layout);
}

function plotBubble(data) {

    // The bubble chart
    var trace1 = {
        x: data.otu_ids,
        y: data.sample_values,
        mode: "markers",
        marker: {
            size: data.sample_values,
            color: data.otu_ids,
            colorscale: "Earth"
        },
        text: data.otu_labels,

    };

    // set the layout for the bubble plot
    var layout = {
        xaxis: { title: "OTU ID" },
        height: 450
    };

    // creating data variable 
    var plot_data = [trace1];

    // create the bubble plot
    Plotly.newPlot("bubble", plot_data, layout);
}

function plotGauge(data){
   
    console.log(data)
    // The guage chart
    var data_g = [
        {
        domain: { x: [0, 1], y: [0, 1] },
        value: parseFloat(data.wfreq),
        title: { text: "Belly Button Washing Frequency <br> Scrubs per Week", font: { size: 24 }  },
        type: "indicator",
        
        mode: "gauge+number",
        gauge: {axis: { range: [null, 9], tickwidth: 1, tickcolor: "darkblue"  },
                bar: { color: "maroon" },
                bgcolor: "white",
                borderwidth: 1,
                bordercolor: "white",

                steps: [
                  { range: [0, 1], color: "rgba(240, 230,215,.5)"},
                  { range: [1, 2], color: "rgba(232,226,202,.5)"},
                  { range: [2, 3], color: "rgba(210,206,145,.5)" },
                  { range: [3, 4], color: "rgba(202,209,95,.5)" },
                  { range: [4, 5], color: "rgba(170,202,42,.5)" },
                  { range: [5, 6], color: "rgba(110,154,22,.5)" },
                  { range: [6, 7], color: "rgba(14,127,0,.5)" },
                  { range: [7, 8], color: "rgba(10,120,22,.5)" },
                  { range: [8, 9], color: "rgba(0,105,11,.5)" },
                ]}
        }
      ];

      var layout_g = { 
          width: 500, 
          height: 400, 
          margin: { t: 25, r: 25, l: 25, b: 25 },
          paper_bgcolor: "white",
          font: { color: "gray", family: "Arial" }          
        };

      Plotly.newPlot("gauge", data_g, layout_g);

}


function getMetadata(id){


    var jfile = "./data/samples.json"
    // read the data 
    d3.json(jfile).then((data) => {

        var tag_metadata = d3.select("#sample-metadata");
        var mdata = data.metadata.filter(s => s.id.toString() === id)[0];

        // empty info panel each time before getting new id info
        tag_metadata.html("");

        // grab the necessary data for the id and append the info to the panel
        Object.entries(mdata).forEach((key) => {   
            tag_metadata.append("h5").text(key[0].toUpperCase() + ": " + key[1] + "\n");    
        });

    });

}

// create the function for the change event
function optionChanged(id) {
    plots(id);
    getInfo(id);
}

// create the function for the initial data rendering
function init() {
    // select dropdown menu 
    var dropdown = d3.select("#selDataset");
    var jfile = "./data/samples.json"
    // read the data 
    d3.json(jfile).then((data) => {
        console.log(data)

        // get the id data to the dropdwown menu
        data.names.forEach(function (name) {
            dropdown.append("option").text(name).property("value");
        });

        // call the function to plot the data
        plots(data.names[0]);
        // call the function to load the info
        getMetadata(data.names[0]);


    });
}

init();