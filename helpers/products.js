

function has_expire_date_(status) {
    return (status ? 'YES' : 'NO');
}

function has_expired(expired) {
    if (expired === true) {
        return 'YES'
    }
    else if (expired === false) {
        return 'NO'
    }
    else {
        return 'No Expire Date'
    }

}

function convertNullValues(status) {
    return (status ? status : '')
}

// get data into product table after ajax call on add or edit

const displayProductTable = (category_id) => {


    $.ajax({
        
        url: `/store/products-in-category/${category_id}/`,
        type: 'GET',

        success: function (response) {

            populateProductTable(response)
            // console.log(response)

        },
        error: function (jqXHR, textStatus, errorThrown) {
            // alert(textStatus + ' - ' + errorThrown);
            swallAlerts(textStatus + ' - ' + errorThrown, 'error', "bottom-end", 3000, false);

        }
    });

}


// get a product and load it into product fields
function getProduct(product_id) {
    $("#editProductBtn").click();

 
    localStorage.setItem('product_id', product_id);


    const category_name = sessionStorage.getItem('category_name');
    $(".product_title_edit").text(`EDIT ${category_name}`)



    $.ajax({
        type: 'GET',
        url: `/store/product-home/product-list/${product_id}/`,


        success: function (data) {
            // console.log(data.name,data.unit)
            // var unit = $("#inputUnitEdit").prop('selectedIndex', data.unit)
            // console.log("supplier", data.supplier)

            $('#inputnameEdit').val(data.name),
                $('#inputPriceEdit').val(data.price),
                $("#inputDescriptionEdit").val(data.description),
                $('#inputQuantityEdit').val(data.quantity),
                $('#inputUnitEdit').val(data.unit),

                // $('#inputSupplierEdit').val(data.supplier),


                $("#inputSupplierEdit option").prop("selected", function () {
                    return ~$.inArray(this.text, data.supplier);
                });

            $('#inputStockLevelEdit').val(data.stock_level),
                $("#inputShelfNumberEdit").val(data.shelf_number),
                $("#inputMonthsToExpireEdit").val(data.months_to_expire),

                $('#inputHasExpireDateEdit').prop('checked', data.has_expire_date)
            has_expire_date(data.has_expire_date)


            $("#inputExpireDateEdit").val(data.expire_date)


        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown)

        }

    })//end of ajax       

    // })
}






// load unit of measurements to select field

const loadUnit = () => {
    $(".inputUnit").empty()

    
    $(".inputUnit").css('width', '370', 'height', '200').addClass('form-control')
    $.get("/store/unit-home/units/", function (data) {

        for (var index in data.data) {

            $('.inputUnit').append('<option value="' + data.data[index].id + '">' + data.data[index].unit + '</option>');
            // $('#inputUnitEdit').append('<option value="' + data.data[index].id + '">' + data.data[index].unit + '</option>');


            $("#inputUnit").select2({
                placeholder: 'Select Unit',
                dropdownParent: $('#modelProductAdd'),

            });
            // $("#inputUnitEdit").select2({
            //     placeholder: 'Select Unit',
            //     dropdownParent: $('#modelProductEdit')

            // });

        }

    });
}

// load supliers  to select field

const loadSupliers = () => {
    $(".inputSupplier").css('width', '370', 'height', '200').addClass('form-control')
    $(".inputSupplier").empty()
    $.get("/business/all-supliers/", function (data) {


        for (var index in data.data) {
            // console.log(data.data)

            $('.inputSupplier').append('<option value="' + data.data[index].id + '">' + data.data[index].name + '</option>');
            // $('#inputSupplierEdit').append('<option value="' + data.data[index].id + '">' + data.data[index].name + '</option>');


            $("#inputSupplier").select2({
                placeholder: 'Select Suppliers',
                dropdownParent: $('#modelProductAdd'),

            });
            // $("#inputSupplierEdit").select2({
            //     placeholder: 'Select Suppliers',
            //     dropdownParent: $('#modelProductEdit')

            // });

        }
    });

}


// check if product has a expire  date

function has_expire_date(status) {

    if (status) {
        // console.log(status)
        $("#months_to_expireEdit").fadeIn()

        $("#expireDateColEdit").fadeIn()
    }
    else {
        console.log('status', status)
        $("#months_to_expireEdit").fadeOut()
        $("#inputMonthsToExpireEdit").val('')
        $("#expireDateColEdit").fadeOut()
        $("#inputExpireDateEdit").val('')
    }
    $("#has_expire_dateEdit").on("click", function () {
        expire_date = $('#inputHasExpireDateEdit').is(':checked')
        if (expire_date) {
            console.log('if ', expire_date)
            $("#months_to_expireEdit").fadeOut()
            $("#inputMonthsToExpireEdit").val('')
            $("#expireDateColEdit").fadeOut()
            $("#inputExpireDateEdit").val('')
        }
        else {
            console.log('else', expire_date)
            $("#months_to_expireEdit").fadeIn()

            $("#expireDateColEdit").fadeIn()

        }

    })

}


// .select2-container--default .select2-selection--single{
//     /* padding:6px; */
//     height: 45px;
//     width: 300px; 
 
// }


// live search on table
$(document).ready(function () {

    $("#product_search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#products_in_categories  tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});




