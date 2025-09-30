var dataIndexURL = "https://raw.githubusercontent.com/argosopentech/argos-train/refs/heads/master/data-index.json";

$(document).ready(function(){
    var baseDiv = $("#data-index-table");
    var table = $("<table/>");
    baseDiv.append(table);

    // table heading
    var heading = $("<tr/>");
    heading.append("<th>Name</th>");
    heading.append("<th>From</th>");
    heading.append("<th>To</th>");
    heading.append("<th>Size</th>");
    heading.append("<th>Reference</th>");
    heading.append("<th>Download</th>");
    table.append(heading);

    // store data globally for filtering
    var fullData = [];

    $.ajax({
        url: dataIndexURL,
        success: function(response) {
            fullData = $.parseJSON(response);

            // populate filters
            var fromCodes = [...new Set(fullData.map(d => d.from_code))].sort();
            var toCodes   = [...new Set(fullData.map(d => d.to_code))].sort();
            fromCodes.forEach(c => $("#from-filter").append(`<option value="${c}">${c}</option>`));
            toCodes.forEach(c => $("#to-filter").append(`<option value="${c}">${c}</option>`));

            renderTable(fullData);
        }
    });

    function renderTable(data) {
        table.find("tr:gt(0)").remove(); // clear rows except header

        $.each(data, function(i, d) {
            var tr = $("<tr>");

            tr.append($("<td/>").text(d.name));
            tr.append($("<td/>").text(d.from_code));
            tr.append($("<td/>").text(d.to_code));
            tr.append($("<td/>").text(formatSize(d.size)));
            tr.append($("<td/>").text(d.reference));

            var linkTd = $("<td/>");
            if (d.links && d.links.length > 0) {
                var link = $("<a/>").attr("href", d.links[0]).text("get");
                linkTd.append(link);
            }
            tr.append(linkTd);

            table.append(tr);
        });
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        let i = Math.floor(Math.log(bytes) / Math.log(1024));
        let sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        return (bytes / Math.pow(1024, i)).toFixed(1) + " " + sizes[i];
    }

    // filtering
    function applyFilters() {
        var search = $("#search-box").val().toLowerCase();
        var from = $("#from-filter").val();
        var to = $("#to-filter").val();

        var filtered = fullData.filter(d => {
            var matchesSearch = d.name.toLowerCase().includes(search) ||
                                d.reference.toLowerCase().includes(search);
            var matchesFrom = !from || d.from_code === from;
            var matchesTo   = !to   || d.to_code === to;
            return matchesSearch && matchesFrom && matchesTo;
        });

        renderTable(filtered);
    }

    $("#search-box").on("input", applyFilters);
    $("#from-filter").on("change", applyFilters);
    $("#to-filter").on("change", applyFilters);
});

