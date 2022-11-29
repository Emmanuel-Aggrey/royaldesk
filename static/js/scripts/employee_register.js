




// CHECK IF EMPLOYEE ID EXIST IN SESSION

$(document).ready(function () {

    load_designation()

    cancel_transfer()

    // employee_date('dob','date_employed','date_completed','dob_dependant')
    employee_date()


    //EMPLOYEE ID ON DESIGNATION TAB
    $('#employee_id').val(sessionStorage.getItem('emp_id')).attr('disabled', 'disabled')

})



// ADD EMPLOYEE
$('#add_employee').on('submit', function (ev) {
    ev.preventDefault();

    $.ajax({
        url: '/allemployees/', 
        type: "POST",
        data: new FormData(this),
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

        success: function (data) {
            // console.log(data)           

            if(data.errors){
                for (let [key,value] of Object.entries(data.errors)) {  
                    // console.log(key,value)
                    errors = `${value}`
                //  Swal.fire('error',errors)

                    show_alert(5000, "error",errors)

                }
            }
           else{
            sessionStorage.setItem('emp_id', data.data)
            $("#employee_id").val(data.data)
            $('#add_employee_next').click()
            // console.log(data)
            show_alert(5000, "success", data.data + ' SAVED')
            sessionStorage.removeItem('applicant')
            $("#cancel_transfer").css('display', 'none')

            // $("#add_employee")[0].reset()

            $("#department").empty()
            load_designation()
           }

            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown)
            show_alert(9000, "error", 'ERROR: THIS USER ALREADY EXIST')
            // console.log(jqXHR.responseText,);
        }

    });
})






// ADD DEPENDANTS

$('#emp_dependant').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    emp_id = sessionStorage.getItem('emp_id');
    url = `/add-dependants/${emp_id}/`
    // console.log(this)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {
            // console.log(data.data);

            if (sessionStorage.getItem('save_another_btn') !== null) {
                $("#dependant_next_btn").click()
                sessionStorage.removeItem('save_another_btn')
            } 
                

          


            if(data.errors){
                for (let [key,value] of Object.entries(data.errors)) {  
                    // console.log(key,value)
                    errors = `${value}`
                //  Swal.fire('error',errors)

                    show_alert(5000, "error",errors)

                }
            }
           else{
            show_alert(5000, "success", data + ' SAVED')
            $("#gender, #first_name, #last_name, #other_name, #mobile, #address, #dob").val('')

            // $("#emp_dependant")[0].reset()


           }



        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown);
            show_alert(6000, "error", 'ERROR: DEPENDANT ALREADY EXIST')

        }

    });
})


function save_continue_btn(clicked) {
    console.log(clicked)
    sessionStorage.setItem('save_another_btn', clicked);
 
} 

// sessionStorage.setItem('save_another_btn', clicked);

// sessionStorage.getItem('save_another_btn')
// if (sessionStorage.getItem('save_another_btn') !== null) {

// } 



// ADD EDUCATION    
$('#emp_education').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    emp_id = sessionStorage.getItem('emp_id');
    url = `/add-education/${emp_id}/`
    console.log(url)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {


            if (sessionStorage.getItem('save_another_btn') !== null) {
                $("#education_next_btn").click()
                sessionStorage.removeItem('save_another_btn')
            } 
                

            if(data.errors){
                for (let [key,value] of Object.entries(data.errors)) {  
                    // console.log(key,value)
                    errors = `${value}`
                //  Swal.fire('error',errors)

                    show_alert(5000, "error",errors)

                }
            }
           else{
            show_alert(5000, "success", data + ' SAVED')
            $("#emp_education")[0].reset()

            // $("#emp_dependant")[0].reset()


           }
            
           
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('error');
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

        }

    });
})




// ADD ProfessionalMembership    
$('#emp_membership').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    emp_id = sessionStorage.getItem('emp_id');
    url = `/add-membership/${emp_id}/`
    console.log(url)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {
            // console.log(data.data);

            if (sessionStorage.getItem('save_another_btn') !== null) {
                $("#membership_next_btn").click()
                sessionStorage.removeItem('save_another_btn')
            } 

            

                if(data.errors){
                    for (let [key,value] of Object.entries(data.errors)) {  
                        // console.log(key,value)
                        errors = `${value}`
                    //  Swal.fire('error',errors)
    
                        show_alert(5000, "error",errors)
    
                    }
                }
               else{
                show_alert(5000, "success", data + ' SAVED')
                $("#emp_membership")[0].reset()
    
                // $("#emp_dependant")[0].reset()
    
    
               }
           
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('error');
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

        }

    });
})


// ADD PreviousEployment    
$('#emp_employment').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    emp_id = sessionStorage.getItem('emp_id');
    url = `/add-emploment/${emp_id}/`
    console.log(url)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {
           

            if(data.errors){
                for (let [key,value] of Object.entries(data.errors)) {  
                    // console.log(key,value)
                    errors = `${value}`
                //  Swal.fire('error',errors)

                    show_alert(5000, "error",errors)

                }
            }
           else{
            show_alert(5000, "success", data + ' SAVED')
            $("#emp_employment")[0].reset()
            sessionStorage.removeItem('emp_id');

            // $("#emp_dependant")[0].reset()


           }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

            console.log('error');
        }

    });
})



// save file

const reg_finished = () => {
    emp_id = sessionStorage.getItem('emp_id');
    Swal.fire(
        'EMPLOYEE  ID',
        `${emp_id}`,
        'info'
    )
   

}




const designation = () => {

    // $(".inputUnit").css('width', '370', 'height', '200').addClass('form-control')
    $.get("/designation/", function (data) {
        // console.log(data.designations);

        // console.log(data.departments);

        for (var index in data.departments) {
            //   console.log(data.departments[index].name);

            $("#department").append(
                '<option value="' +
                data.departments[index].pk +
                '">' +
                data.departments[index].name +
                "</option>"
            );
        }//END OF DEPARTMENT DROPDOWN
        $("#department").change(function () {
            // document.getElementById('designation').innerText =null;
            $("#designation").empty()
            let depart = $("#department").val()
            let desig = data.designations.filter(function (item) {
                return item.department == depart
            })
            for (const key in desig) {
               
                $("#designation").append(
                    '<option class="option" value="' +
                    desig[key].pk +
                    '">' +
                    desig[key].name +
                    "</option>"

                );
                $("#salary").val(Object.entries(desig)[0][1].net_month_salary)


            }

            $("#designation").change(function () {
                // console.log(this.value);
                let depart = $("#designation").val()
                let salary = desig.filter(function (item) {

                    return item.pk == depart
                })
                // net_month_salary

                salary.forEach(function (item) {

                    $("#salary").val(item.net_month_salary)
                })

            })

            // applicant = JSON.parse(sessionStorage.getItem('applicant'))


        })

    });
};




// GET TRANSFERED APPLICANT TO EMPLOYEE FORM

const set_applicant = () => {

    if (sessionStorage.getItem('applicant') !== null) {
        applicant = JSON.parse(sessionStorage.getItem('applicant'))
        // console.log(applicant)
        $('#applicant').val(applicant.id)

        $('#fname').val(applicant.first_name)
        $('#lname').val(applicant.last_name)

        $('#oname').val(applicant.other_name)
        $('#email').val(applicant.email)
        $('#p_phone').val(applicant.phone)
        $('#date_employed').val(applicant.resuming_date)
        $("#res_address").val(applicant.address)
        $("#salary").val(applicant.applicant_salary)

        $("#department").append(
            '<option value="' +
            applicant.department_id +
            '">' +
            applicant.department +
            "</option>"
        );

        $("#designation").append(
            '<option class="option" value="' +
            applicant.designation_id +
            '">' +
            applicant.designation +
            "</option>"
        );


    }
    else {
        // console.log('applicant not available')
    }
}


// LOAD DESIGNATION IF applicant Not AVAILABLE IN SESSION
const load_designation = () => {
    if (sessionStorage.getItem('applicant') !== null) {
        set_applicant()

    }
    else {
        designation()
        $("#applicant").val('')

    }

}

// resturn to applicants page if transfer cancelled
const cancel_transfer = () => {
    if (sessionStorage.getItem('applicant') !== null) {
        $("#cancel_transfer").css('display', 'block')

        $("#cancel_transfer").on("click", () => {
            sessionStorage.removeItem('applicant')
            location.href = '/applicants/'
        })
    }

}


// const employee_date = (dob,date_employed,dob_dependant)=>{
//     $(`#${date_employed},#${dob},#${dob_dependant}`).datepicker({
//         dateFormat: 'yy-mm-dd',
//         autoclose: true,
//         orientation: "top",
//         maxDate: new Date()         
//   });
// }


const employee_date = ()=>{
    $('.dob').datepicker({
        dateFormat: 'yy-mm-dd',
        autoclose: true,
        orientation: "top",
        maxDate: new Date(),
        changeMonth: true,
        changeYear: true,
        showWeek: true,

        // maxDate:'-7y,'
  });
}





