

$(document).ready(function () {
    search_leave_table()
    attendance()
    time_hour_value()
    filter_between_two_dates()
})

const value = (value) => {
    return (value ? 'YES' : 'NO');

}


const attendance_data = (data) => {

    count_In =[]
    data.forEach(element => { 
       count_In.push(element.Count_In)

       //find the sum of count_In

    })
    sum = count_In.reduce((a, b) => a + b, 0)
        // console.log(sum)
        total = `TOTAL CLOCK IN : ${sum}`
        $('#total_checkin').text(total)

    data.forEach(function (element) {
        $("#attendance_table").append(`
        <tr>
            <td class="font-weight-medium">${element.Department}</td>
            <td class="font-weight-medium">${element.Count_In}</td>
            <td class="font-weight-medium" style="display:none">${element.Count_Out}</td>
   
            `)

    })

}


const attendance = () => {

    $.ajax({
        url: '/time-attendance/',
        type: 'GET',
        success: function (response) {
            attendance_data(response)  
        },
        error: function (error) {
            Swal.fire('ERROR CONNECTING TO CROSSCHEX SERVER')
            
        }
        
    })
}



$("#attendance_form").on("submit", function (event) {
    event.preventDefault();
    const date_from = $("#date_from").val()
    const date_to = $("#date_to").val()

        $.ajax({
            url: '/time-attendance/',
            type : "POST",
            data: {
                date_from:date_from,
                date_to:date_to,
                time_from : $("#time_from").val(),
                time_to :$("#time_to").val(),
                // datetime:$("#datetime").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },

            beforeSend: function () {

                // $('#loadings').css('display', 'block');
                $( "#loadings" ).text( 'Loading data...' ).fadeIn().css('color', 'green');

            },
            success: function (response) {
                $("#attendance_table").empty();

                $("#loadings").fadeOut("slow");

                attendance_data(response)           

                // days difference between date_from and date_to
                const days = Math.ceil((new Date(date_to) - new Date(date_from)) / (1000 * 60 * 60 * 24));
                // console.log(days)
                const num_days = `NUMBER OF DAYS: ${days}`
                $("#days").text(num_days)
            
             }
        })
})


$('#time_from, #time_to').change(function () {
    // console.log(this.value)
    if (this.value ===''){

        return $('#time_to,#time_from').attr('required', false);
    }
    else {
        $('#clear_time').text('clear time').addClass('text-danger');
        return $('#time_to,#time_from').attr('required', true);
    }
})



$("#clear_time").click(function () {
    $('#time_from, #time_to').prop('selectedIndex',0);
    $('#clear_time').text('Time').removeClass('text-danger');
    return $('#time_to,#time_from').attr('required', false);

})


// FILTER BETWEEN TWO DATES

const filter_between_two_dates = () => {

    $("#date_from").change(function () {

        $("#date_to").val("");

    });


    $("#date_to").change(function () {
        startDate = $("#date_from").val()
        endDate = $("#date_to").val()
       

        var start = new Date(startDate);
        var end = new Date(endDate);
        
        if (start <= end) {
                
        }
        else {
            Swal.fire("DATE MUST BE IN THE FUTURE");

            $("#date_to").val("");
        }

    }); //end change function

    $("#time_from").change(function () {

        $("#time_to").val("");

    });

}



const time_hour_value = () => {
    // loop from 0 to 24
    for (let i = 0; i < 24; i++) {
        // add 0 before the hour if it is less than 10
        let hour = (i < 10) ? '0' + i : i;
        // add the option to the select
        $('#time_from').append('<option value="' + hour + '">' + hour + '</option>');
        $('#time_to').append('<option value="' + hour + '">' + hour + '</option>');

    }

}


// live search on table

const search_leave_table = () => {
    $("#attendance_search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#attendance_table  tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

}




