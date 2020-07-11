(function() {
    google.charts.load("current", {
        packages: ["timeline"]
    });
    google.charts.setOnLoadCallback(drawChart);
})()

function drawChart() {
    var container = document.getElementById('timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({
        type: 'string',
        id: 'Description'
    });
    dataTable.addColumn({
        type: 'string',
        id: 'Name'
    });
    dataTable.addColumn({
        type: 'date',
        id: 'Start'
    });
    dataTable.addColumn({
        type: 'date',
        id: 'End'
    });

    var rowComponents = [
        new DrtMonitorComponent(drt_monitor_data),
        new CameraDetectionComponent(cam_detection_data),
        new PlayerActionComponent(player_actions_data)
    ];

    var rows = rowComponents.flatMap((component) => component.rows().flat());
    console.log(rows);

    dataTable.addRows(rows);

    var options = {
        vAxis: {
            title: 'DRT Stadistics'
        },
        timeline: {
            showBarLabels: false,
            colorByRowLabel: true,
        },
        hAxis: {
            format: 'HH:mm:ss'
        },
        avoidOverlappingGridLines: false,
    };

    chart.draw(dataTable, options);
}