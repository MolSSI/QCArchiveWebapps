
/* Formatting function for row details - modify as you need */
function format_details( data ) {
    // `data` is the original data object for the row

    var details = $('.ds_details_template').clone();
    details.removeClass('ds_details_template');

    details.find('.description').text(data.description);

    citations = '<ul>';
    for (var i in data.citations){
        citations += '<li>' + data.citations[i]._acs_citation + '</li>';
    }
    citations += '</ul>';

    details.find('.citations').append(citations);


    return details;
}

function format_buttons(){

    var buttons = $('.download_template').clone();
    buttons.removeClass('download_template');

    return buttons.html();
}

$(document).ready( function () {
    console.log('Creating datatable');
    var table = $('#ds_table').DataTable({

        dom: 'f l r <t> i p',
        searching: true,
        pageLength: 12,
        ordering:  true,
        paging: true,
        order: [[1, 'asc']], // column #1
        //compact: true,  // styles classes not here

        "ajax": "/ml_datasets_list/",
        "columns": [
            {   // expand button
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
            },
            { title: "Name" , data: "name" },
            { title: "Quality", data: "theory_level" },
            { title: "Data Points", data: "data_points" },
            { title: "Elements", data: "elements" },
            {
                "title": "Download",
                "targets": -1,  // first col from right
                "data": null,
                "orderable": false,
                "defaultContent": format_buttons(),
            }
        ],

        // dom: 'Bfrtip',
        // buttons: [
        //     'copy', 'excel', 'pdf'
        // ]

    });

    function download_dataset(type, data){
        console.log('Downloading..', type);
        console.log('data: ', data);
        alert( data.name +"'s salary is: "+ data.salary);
    }

    $('#ds_table tbody').on( 'click', 'button#hdf5', function () {
        var data = table.row( $(this).parents('tr') ).data();
        download_dataset('hdf5', data);
    } );

    $('#ds_table tbody').on( 'click', 'button#text', function () {
        var data = table.row( $(this).parents('tr') ).data();
        download_dataset('zip', data);
    } );

    // table.buttons().container()
    //     .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );

       // Add event listener for opening and closing details
    $('#ds_table tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            tr.removeClass('light-gray-bg');
        }
        else {
            // Open this row
            row.child( format_details(row.data())  ).show();
            row.child().addClass('light-gray-bg');
            tr.addClass('light-gray-bg');
            tr.addClass('shown');

        }
    } );

} );


