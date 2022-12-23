




// CHECK IF EMPLOYEE ID EXIST IN SESSION
var DEPENDANTS = []
var EDUCATION = []
var PROFFESIONAL_MEMBERSHIPS = []
var PREVIOUS_EMPLOYMENT = []
const no_beneficiaries = JSON.parse(document.getElementById('no_beneficiaries').textContent)
// GET employee_id from django session and use for employee dependencies eg previosEmployeement etc




$(document).ready(function () {

    load_designation()

    cancel_transfer()

    // employee_date('dob','date_employed','date_completed','dob_dependant')
    employee_date()




    // CHECK IF EMP_ID IS AVAILABLE BEFOR LOADING DATA
    if(sessionStorage.getItem('EMP_ID')!==null){
        const EMP_ID = sessionStorage.getItem('EMP_ID')
        // $('#employee_id').val(employee_id).attr('disabled', 'disabled')
        getdependants(EMP_ID)
        getEducation(EMP_ID)
        getMembership(EMP_ID)
        getEmployment(EMP_ID)
        employee_edit_mode(EMP_ID)
    }
   

})




 if (sessionStorage.getItem('EMP_ID') !== null) {
    $('#add_employee').on('submit', function(event){
        event.preventDefault()
        const EMP_ID = sessionStorage.getItem('EMP_ID')

        $.ajax({
            url: `/employee-api/${EMP_ID}/`,
            type: 'post',
            data: new FormData(this),
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            cache: false,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            success: function(data){
                // console.log(data)
                $('#add_employee_next').click()

            }
        })
    })
 }
 else{
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

                $("#department").empty()
                load_designation()

            }


        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown)
            show_alert(9000, "error", 'ERROR: Unknown error occurred Contact Administrator')
            // console.log(jqXHR.responseText,);
        }

    });
})
  
} //end of if



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
                const count_beneficiary =response.filter(is_beneficiary=>is_beneficiary.is_beneficiary===true)
                no_beneficiaries  <= count_beneficiary.length   ? $('#is_beneficiary').attr('disabled',true) :$('#is_beneficiary').attr('disabled',false);
          
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
    EMP_ID = sessionStorage.getItem('EMP_ID');
    url=`http://${location.host}/employee-data/${EMP_ID}`
    $("#record_link").attr('href', url).text('view your infomation').removeClass('d-none')
    Swal.fire(
        'VIEW RECORD',
        `<a href=${url}>EMPLOYEE RECORD</a>`,
        'info'
     )
        sessionStorage.removeItem('EMP_ID');
        
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



// ENETER EDITING MODE

// $(document).ready(function(){
//     if(sessionStorage.getItem('employee_name')){
//         const employee = sessionStorage.getItem('employee_name')
//         employee_edit_mode(employee)
//     }
// })



// edit employee data
const employee_edit_mode = (employee_id) => {
    // employee = sessionStorage.getItem('employee_name')
    $.ajax({
        url: `/employee-api/${employee_id}/`,
        method: 'GET',
        success: function (response) {
            // console.log(response)

            $(`#title option[value=${response.title}]`).attr("selected", true)
            $('#fname').val(response.first_name)
            $("#country").val(response.country)
            $('#lname').val(response.last_name)
            $("#languages").val(response.languages)
            $('#oname').val(response.other_name)
            $('#email').val(response.email)
            $('#p_phone').val(response.mobile)
            $(`#sex option[value=${response.sex}]`).attr("selected", true)
            $('#nia').val(response.nia)
            $('#emergency_name').val(response.emergency_name)
            $('#emergency_phone').val(response.emergency_phone)
            $('#emergency_address').val(response.emergency_address)
            $('#dob').val(response.dob)
            $('#date_employed').val(response.date_employed)
            $('#res_address').val(response.address)
            $('#place_of_birth').val(response.place_of_birth)
            $(`#is_merried option[value=${response.is_merried}]`).attr("selected", true)
            $(`#department option[value=${response.department}]`).attr("selected", true)

            $("#designation").append(
                `
                 <option value="${response.designation}"> ${response.designation_name} </option> 
                  `
            )
            $(`#hod option[value=${option(response.is_head)}]`).attr("selected", true)

            $('#nationality').val(response.nationality)
            $('#salary').val(response.salary)
            $('#snnit_number').val(response.snnit_number)
            $('#bank_name').val(response.bank_name)
            $('#bank_branch').val(response.bank_branch)
            $('#bank_ac').val(response.bank_ac)
            $('#next_of_kin_name').val(response.next_of_kin_name)
            $('#next_of_kin_phone').val(response.next_of_kin_phone)
            $('#next_of_kin_address').val(response.next_of_kin_address)
            $('#next_of_kin_relationship').val(response.next_of_kin_relationship)
            $('#profile_image').attr('src', response.profile_exists).removeClass('d-none')

            // console.log(response.profile)

            if(response.profile){
                const element = document.getElementById('profile_div');
                return element.remove(); // Removes the div with the 'div-02' id
                
            }
            else{
                const element = document.getElementById('profile_image');
                return element.remove(); // Removes the div with the 'div-02' id
                
                
            }
            
            // $(`#helpdesk_user option:contains('${option(response.employee.helpdesk_user)}')`).prop("selected", true)
                
                
        }
    })

}


function img_increase()
        {
            document.getElementById("profile_image").style.width="300px";
        } 

        function img_decrease()
        {
           document.getElementById("profile_image").style.width="150px";
        }



function option(value) {
    return value === true ? 1 : 0

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





