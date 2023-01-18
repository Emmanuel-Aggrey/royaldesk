




// GET NUMBER OF BENEFICIARIES FROM ENVIRONMENT VARIABLES
const no_beneficiaries = JSON.parse(document.getElementById('no_beneficiaries').textContent)
const IS_APPLICANT = JSON.parse(document.getElementById('is_applicant').textContent)
const EMPLOYEE_UUID = JSON.parse(document.getElementById('employee_uuid').textContent)
const CONNECTED_TO_ANVIZ = JSON.parse(document.getElementById('conntected_to_server').textContent)


$(document).ready(function () {


// console.log(IS_APPLICANT,EMPLOYEE_UUID,'CONNECTED_TO_ANVIZ',CONNECTED_TO_ANVIZ)
// REDIRECT TO UPDATE EMPLOYEE IS IS APPLICANT AND HAVE EMPLOYEE RECORDS
IS_APPLICANT && EMPLOYEE_UUID !='' && EMPLOYEE_UUID !='admin' ? location.href =`/update-employee/${EMPLOYEE_UUID}`:''
CONNECTED_TO_ANVIZ ? '':$("#anviz_user").attr('disabled',true)

    load_designation()

    // date from jquary datetime plugin settings
    employee_date()

    // APPLICANT SELF RESIGSTRATION
    if(IS_APPLICANT){
        const APPLICANT_NAME = JSON.parse(document.getElementById('applicant_name').textContent)

        get_applicant(APPLICANT_NAME) 

        // sessionStorage.setItem('EMP_ID',EMPLOYEE_UUID)
    }

    if (sessionStorage.getItem('applicant') !== null) {
        set_applicant()
    }
    
}) //END OF READY


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
                // console.log('applicant_id create ',data.is_applicant)

                data.is_applicant ? $("#verify_btn").removeClass('d-none'):''

                
                if (data.errors) {
                    for (let [key, value] of Object.entries(data.errors)) {
                        // console.log(key,value)
                        errors = `${value}`
                        //  Swal.fire('error',errors)

                        show_alert(5000, "error", errors)

                    }
                }
                if (data.unique_contraints) {
                    show_alert(5000, "error", data.unique_contraints)

                }

                if (data.data) {
                    sessionStorage.setItem('EMP_ID', data.data)
                    $('#add_employee_next').click()
                    // console.log(data)
                    show_alert(5000, "success", 'Record' + ' SAVED')
                    // $("#add_employee").attr('id','update_employee')   

                    sessionStorage.removeItem('applicant')
                    $("#cancel_transfer").css('display', 'none')


                    // $("#add_employee")[0].reset()

                    // $("#department").empty()
                    // load_designation()

                }


            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR, textStatus, errorThrown)
                show_alert(9000, "error", 'ERROR: Unknown error occurred Contact Administrator')
                // console.log(jqXHR.responseText,);
            }

        });
    })






// ADD DEPENDANTS

$('#emp_dependant').on('submit', function (ev) {
    // const EMP_ID = JSON.parse(document.getElementById('EMP_ID').textContent)

    // var formData = new FormData(this);
    ev.preventDefault();

    // EMP_ID = $("#EMP_ID").text()

    EMP_ID = sessionStorage.getItem('EMP_ID');
    // EMP_ID = $("#EMP_ID").text();

    url = `/add-dependants/${EMP_ID}/`
    // console.log(this)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        // enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {
            // console.log(data);
            // dependants(data)
            if (sessionStorage.getItem('save_another_btn') !== null) {
                $("#dependant_next_btn").click()
                sessionStorage.removeItem('save_another_btn')
            }





            if (data.errors) {
                for (let [key, value] of Object.entries(data.errors)) {
                    // console.log(key,value)
                    errors = `${value}`
                    //  Swal.fire('error',errors)

                    show_alert(5000, "error", errors)

                }
            }
            else {
                full_name = `${data.full_name}`.toUpperCase()
                show_alert(5000, "success", full_name + ' SAVED')
                $("#gender, #first_name, #last_name, #other_name, #mobile, #address, #dob_dependant").val('')
                $("#dependant_body").empty()
                // dependants(data)
                getdependants(data.employee_id)

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

const getdependants = (employee_id) => {
    $.ajax({
        url: `/add-dependants/${employee_id}/`,
        method: 'GET',
        success: function (response) {
            // console.log(response);

            // console.log(count_beneficiary.length)

            response.length < 1 ? $("#dependant_body").append(`<div class="text-center">no data</div>`) :
                response.forEach(function (dependant, index) {
                    $('#dependant_body').append(
                        `
                    <tr>
                    <td>${index + 1}</td>
                    <td >${dependant.relation}</td>
                    <td>${dependant.gender}</td>
                    <td class=${is_beneficiary(dependant.is_beneficiary)}>${dependant.full_name}</td>
                    <td>${dependant.mobile}</td>
                    <td>${dependant.address}</td>
                    <td>${dependant.dob}</td>
                    <td><i id=${dependant.id} data-id=${dependant.employee_id} class="fa fa-trash-o text-danger"  onclick=(deleteDependant(this)) style="cursor:pointer" title='delete  ${dependant.full_name}' aria-hidden="true"></i></td>
                    </tr>
                `
                    )

                })
            $("#is_beneficiary").prop('checked', false)
            // check if no_beneficiaries is equal to the number of beneficiaries of the employee and disable  is_beneficiary btn
            const count_beneficiary = response.filter(is_beneficiary => is_beneficiary.is_beneficiary === true)
            no_beneficiaries <= count_beneficiary.length ? $('#is_beneficiary').attr('disabled', true) : $('#is_beneficiary').attr('disabled', false);

        },
        error: function (jqXHR, textStatus) {
            console.log(jqXHR.responseText, textStatus)
            show_alert(7000, "error", ' try again error occurred while processing data')

        }
    })
}


const is_beneficiary = (is_beneficiary) => {
    if (is_beneficiary) {
        return 'text-danger'
    }
    else return ''
}
const deleteDependant = (value) => {

    id = value.id
    var employee_id = document.getElementById(id).getAttribute('data-id')

    url = `/delete-dependent/${employee_id}/${id}/`
    // console.log(id)
    $.ajax({

        url: url,
        type: "DELETE",

        success: function (data) {
            $("#dependant_body").empty()

            getdependants(employee_id)
            show_alert(5000, "success", data.data)

        },
        error: function (message) {
            // console.error(message);
            show_alert(7000, "error", ' try again error occurred')

        }
    });

}


// ask for name of relationship in beneficiary

$("#relation").change(async function () {
    // married = this.value
    // console.log(this.value)
    if (this.value == 'other') {

        const { value: relation } = await Swal.fire({
            // title: 'Input Relationship Type',
            inputPlaceholder: 'Enter Relationship Type',
            input: 'text',
            inputLabel: 'Relationship',

        })

        if (relation) {
            // Swal.fire(`Entered name: ${relation}`)
            $("#relation").append(`
            <option value=${relation}>${relation.toUpperCase()}</option>
            `)
            $(`#relation option[value=${relation}]`).attr("selected", true)

        }
        else {
            $('#relation').prop('selectedIndex', 0)
        }


    }


})




// ADD EDUCATION    
$('#emp_education').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    EMP_ID = sessionStorage.getItem('EMP_ID');
    url = `/add-education/${EMP_ID}/`
    // console.log(url)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {
            // console.log(data)

            if (sessionStorage.getItem('save_another_btn') !== null) {
                $("#education_next_btn").click()
                sessionStorage.removeItem('save_another_btn')
            }


            if (data.errors) {
                for (let [key, value] of Object.entries(data.errors)) {
                    // console.log(key,value)
                    errors = `${value}`
                    //  Swal.fire('error',errors)

                    show_alert(5000, "error", errors)

                }
            }
            else {
                show_alert(5000, "success", data.school_name + ' SAVED')
                $("#emp_education")[0].reset()
                $('#education_body').empty()
                getEducation(data.employee_id)
                // $("#emp_dependant")[0].reset()


            }


        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('error');
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

        }

    });
})



const getEducation = (employee_id) => {
    $.ajax({
        url: `/add-education/${employee_id}/`,
        method: 'GET',
        success: function (response) {
            // console.log(response);
            response.length < 1 ? $("#education_body").append(`<div class="text-center">no data</div>`) :
                response.forEach(function (education, index) {
                    // console.log(education)
                    // $("#education_body").empty();

                    $('#education_body').append(
                        `
                    <tr>
                    <td>${index + 1}</td>
                    <td>${education.school_name}</td>
                    <td>${education.course}</td>
                    <td>${education.certificate}</td>
                    <td>${education.date_completed}</td>
                    <td><i id=${education.id} data-id=${education.employee_id} class="fa fa-trash-o text-danger"  onclick=(deleteEducation(this)) style="cursor:pointer" title='delete  ${education.school_name}' aria-hidden="true"></i></td>
                    </tr>
                `
                    )

                })
        },
        error: function (jqXHR, textStatus) {
            console.log(jqXHR.responseText, textStatus)
            show_alert(7000, "error", ' try again error occurred while processing data')

        }
    })
}

const deleteEducation = (value) => {

    id = value.id
    var employee_id = document.getElementById(id).getAttribute('data-id')
    url = `/delete-education/${employee_id}/${id}/`
    // console.log(id)
    $.ajax({
        url: url,
        type: "DELETE",
        success: function (data) {
            $("#education_body").empty()

            getEducation(employee_id)
            show_alert(5000, "success", data.data)

        },
        error: function (message) {
            // console.error(message);
            show_alert(7000, "error", ' try again error occurred')

        }
    });

}



// ADD ProfessionalMembership    
$('#emp_membership').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    EMP_ID = sessionStorage.getItem('EMP_ID');
    url = `/add-membership/${EMP_ID}/`
    // console.log(url)

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



            if (data.errors) {
                for (let [key, value] of Object.entries(data.errors)) {
                    // console.log(key,value)
                    errors = `${value}`
                    //  Swal.fire('error',errors)

                    show_alert(5000, "error", errors)

                }
            }
            else {
                show_alert(5000, "success", data.name + ' SAVED')
                $("#emp_membership")[0].reset()
                $("#membership_body").empty()
                getMembership(data.employee_id)

                // $("#emp_dependant")[0].reset()


            }

        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('error');
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

        }

    });
})



const getMembership = (employee_id) => {
    $.ajax({
        url: `/add-membership/${employee_id}/`,
        method: 'GET',
        success: function (response) {
            // console.log(response);
            response.length < 1 ? $("#membership_body").append(`<div class="text-center">no data</div>`) :
                response.forEach(function (membership, index) {
                    // console.log(education)
                    // $("#education_body").empty();

                    $('#membership_body').append(
                        `
                    <tr>
                    <td>${index + 1}</td>
                    <td>${membership.name}</td>
                    <td> <a href=${membership.document}>Download</a> </td>
                    
                    <td><i id=${membership.id} data-id=${membership.employee_id} class="fa fa-trash-o text-danger"  onclick=(deleteMembersip(this)) style="cursor:pointer" title='delete  ${membership.name}' aria-hidden="true"></i></td>
                    </tr>
                `
                    )

                })
        },
        error: function (jqXHR, textStatus) {
            console.log(jqXHR.responseText, textStatus)
            show_alert(7000, "error", ' try again error occurred while processing data')

        }
    })
}




const deleteMembersip = (value) => {

    id = value.id
    var employee_id = document.getElementById(id).getAttribute('data-id')
    url = `/delete-membership/${employee_id}/${id}/`
    // console.log(id)
    $.ajax({
        url: url,
        type: "DELETE",
        success: function (data) {
            $("#membership_body").empty()

            getMembership(employee_id)
            show_alert(5000, "success", data.data)

        },
        error: function (message) {
            // console.error(message);
            show_alert(7000, "error", ' try again error occurred')

        }
    });

}



// ADD PreviousEployment    
$('#emp_employment').on('submit', function (ev) {
    // var formData = new FormData(this);
    ev.preventDefault();

    EMP_ID = sessionStorage.getItem('EMP_ID');
    url = `/add-emploment/${EMP_ID}/`
    // console.log(url)

    $.ajax({
        url: url,
        type: "POST",
        data: new FormData(this),
        contentType: false,
        cache: false,
        processData: false,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),


        success: function (data) {


            if (data.errors) {
                for (let [key, value] of Object.entries(data.errors)) {
                    // console.log(key,value)
                    errors = `${value}`
                    //  Swal.fire('error',errors)

                    show_alert(5000, "error", errors)

                }
            }
            else {
                show_alert(5000, "success", data.job_title + ' SAVED')
                $("#emp_employment")[0].reset()
                $("#employment_body").empty()

                getEmployment(data.employee_id)

                // $("#emp_dependant")[0].reset()


            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            show_alert(6000, "error", 'ERROR: ALREADY EXIST')

            console.log('error');
        }

    });
})


const getEmployment = (employee_id) => {
    $.ajax({
        url: `/add-emploment/${employee_id}/`,
        method: 'GET',
        success: function (response) {
            // console.log(response);
            response.length < 1 ? $("#employment_body").append(`<div class="text-center">no data</div>`) :
                response.forEach(function (employment, index) {
                    // console.log(education)
                    // $("#education_body").empty();

                    $('#employment_body').append(
                        `
                    <tr>
                    <td>${index + 1}</td>
                    <td>${employment.job_title}</td>
                    <td> ${employment.company} </td>
                    <td> ${employment.date}</td>
                    <td><i id=${employment.id} data-id=${employment.employee_id} class="fa fa-trash-o text-danger"  onclick=(deleteEmployment(this)) style="cursor:pointer" title='delete  ${employment.job_title}' aria-hidden="true"></i></td>
                    </tr>
                `
                    )

                })
        },
        error: function (jqXHR, textStatus) {
            console.log(jqXHR.responseText, textStatus)
            show_alert(7000, "error", ' try again error occurred while processing data')

        }
    })
}


const deleteEmployment = (value) => {

    id = value.id
    var employee_id = document.getElementById(id).getAttribute('data-id')
    url = `/delete-emploment/${employee_id}/${id}/`
    // console.log(id)
    $.ajax({
        url: url,
        type: "DELETE",
        success: function (data) {
            $("#employment_body").empty()

            getEmployment(employee_id)
            show_alert(5000, "success", data.data)

        },
        error: function (message) {
            // console.error(message);
            show_alert(7000, "error", ' try again error occurred')

        }
    });

}


// save file

const reg_finished = () => {
    // show_alert(3000, "info", 'submiting your request')
  
     
    EMP_ID = sessionStorage.getItem('EMP_ID');
    url = `http://${location.host}/employee-data/${EMP_ID}`
    $("#record_link").attr('href', url).text('view your infomation').removeClass('d-none')
    Swal.fire(
        'VIEW RECORD',
        `<a href=${url}>EMPLOYEE RECORD</a>`,
        'info'
    )
    sessionStorage.removeItem('EMP_ID');

 setInterval(() => {
    window.close();
 }, 2500);

//    setTimeout(() => {
//     location.reload();

// }, 5000);
}


const verify_data =(e)=>{
    EMP_ID = sessionStorage.getItem('EMP_ID');
    url = `http://${location.host}/employee-data/${EMP_ID}`

    $.ajax({
        url: `/verify-data/${EMP_ID}/`,
        type: 'POST',
        beforeSend: function(data) {
            show_alert(3000, "info", 'submiting request')

        },
        success: function(data) {
            sessionStorage.removeItem('EMP_ID');
            Swal.fire(
                'VIEW RECORD',
                `<a href=${url}>EMPLOYEE RECORD</a>`,
                'info'
            )
            
            setInterval(() => {
                window.close();
            }, 5000);
            

        }
     })
}



const load_designation = () => {

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


// $("#anviz_user").change(function(){
//     // console.log(this.value)
//     if(this.value ==1){
//         return $("#anviz_department").attr('required', true)
//     }  
//     else{
//         return $("#anviz_department").attr("required", false); 
//     }
// })

// const load_anviz_department = ()=>{
    
//        $.get("/anviz-department/", function (data) {

//         for (const [key, value] of Object.entries(data)) {
//             // console.log(key);

//             $("#anviz_department").append(
//                 '<option class="option" value="' +
//                 value +
//                 '">' +
//                 key +
//                 "</option>"

//             );
//           }

      
//     });

// }


// GET TRANSFERED APPLICANT TO EMPLOYEE FORM

const set_applicant = () => {



    if (sessionStorage.getItem('applicant') !== null) {
      const  applicant = JSON.parse(sessionStorage.getItem('applicant'))
        // console.log(applicant)
        // helpdesk_div is_applicant
        $("#department").empty()

        applicant.applicant ?  '':  $("#helpdesk_div").remove()
       

        $('#applicant').val(applicant.id)

        $('#fname').val(applicant.first_name)
        $('#lname').val(applicant.last_name)

        $('#oname').val(applicant.other_name)
        $('#email').val(applicant.email)
        $('#p_phone').val(applicant.phone)
        $('#date_employed').val(applicant.resuming_date)
        $("#res_address").val(applicant.address)
        $("#salary").val(applicant.applicant_salary).attr('readonly', true)


        $("#department").append(
            '<option value="' +
            applicant.department +
            '">' +
            applicant.department_name +
            "</option>"
        );

        $("#designation").append(
            '<option class="option" value="' +
            applicant.designation +
            '">' +
            applicant.designation_name +
            "</option>"
        );


    }
    else {
        $("#applicant").val('')
        // console.log('applicant not available')
    }
}







$("#is_merried").change(function(){
    console.log(this.value)
    if(this.value=='married'){
        $("#is_married_selected").removeClass('d-none').fadeIn('slow').effect("slide");
        $("#is_merried_relation,#is_merried_f_name,#is_merried_phone,#is_merried_l_name").attr('required',true)
    }
    else{
        $("#is_married_selected").addClass('d-none').fadeOut('slow')
        $("#is_merried_relation,#is_merried_f_name,#is_merried_phone,#is_merried_l_name").attr('required',false)

    }
})

function img_increase() {
    document.getElementById("profile_image").style.width = "300px";
}

function img_decrease() {
    document.getElementById("profile_image").style.width = "150px";
}



function option(value) {
    return value === true ? 1 : 0

}


// APPLICANT UPDATEING PERSONAL RECORD
const get_applicant = (applicant) => {
    // console.log(applicant)

    $.ajax({
        url: `/update_applicant/${applicant}/`,
        type: 'GET',
        beforeSend: function () {
            show_alert(1000, "info", 'getting applicant data')

        },
        success: function (data) {

            
            $('#applicant').val(data.id)

            $('#fname').val(data.first_name)//.attr('readonly', true)
            $('#lname').val(data.last_name)
            $('#oname').val(data.other_name)
            $('#email').val(data.email)
            $('#p_phone').val(data.phone)
            $('#date_employed').val(data.resuming_date).attr('readonly',true)
            $("#res_address").val(data.address)
            $("#salary").val(data.applicant_salary).attr('readonly',true)

            $("#department,#designation").empty()

            $("#department").empty()
            
            $("#department").append(
                '<option value="' +
                data.department +
                '">' +
                data.department_name +
                "</option>"
            );

            $("#designation").append(
                '<option class="option" value="' +
                data.designation +
                '">' +
                data.designation_name +
                "</option>"
            );

        }
    })

}




// resturn to applicants page if transfer cancelled
const cancel_transfer = () => {
    if (sessionStorage.getItem('transfer') != null) {
        $("#cancel_transfer").css('display', 'block')

        $("#cancel_transfer").on("click", () => {
            sessionStorage.removeItem('applicant')
            window.close()


        })


    }

}









const employee_date = () => {
    $('.dob').datepicker({
        dateFormat: 'yy-mm-dd',
        autoclose: true,
        // orientation: "top",
        maxDate: new Date(),
        yearRange: '1960:',
        // minDate:'-70Y',
        changeMonth: true,
        changeYear: true,
        // showWeek: true,

    });
}






