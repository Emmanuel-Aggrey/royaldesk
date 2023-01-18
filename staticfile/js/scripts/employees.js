
// object to get employee deocuments
var documents_objects={}

var employee_objects={}

$(document).ready(function () {

  search_employees_table()
  $.ajax({
    url: '/employees/',
    type: 'GET',
    success: function (response) {
      // console.log(response)
  

      employee_objects = Object.assign(response.employees);
      $("#count_on_leave").text(response.employees_on_leave).attr('title', 'employees on leave')

      response.employees_exceed_leave  ?
      $("#count_exceed_leave").text(response.employees_exceed_leave).attr('title','exceeded leave').addClass('pulse ')
      : 
      $("#count_exceed_leave").text(response.employees_exceed_leave).attr('title','exceeded leave')


      // console.log(employee_objects);

      let employees = {}
      employees = employee_objects.filter(function (item) {
        return item.status == 'active'
      })

      employees.forEach(function (element) {
        // console.log(element)

        $("#employees_table").append(`
                
            <tr>
                                
                                <td  class="font-weight-medium employees_image" title="view leave history"> <img  class='img' src="${element.profile_exists}" alt="employee prifile image"></td>
                                <td class="font-weight-medium">${element.employee_id}</td>

                                <td class="font-weight-medium">${element.full_name}</td>
                                <td class="font-weight-medium">${element.department}</td>
                                <td class="font-weight-medium">${element.mobile}</td>
                                <td class="font-weight-medium">${element.email}</td>
                                <td class="font-weight-medium">${element.address}</td>
                                <td class="font-weight-medium">${element.date_employed}</td>

                                <td class="text-primary font-weight-medium" class="">
                               
                                  <div  id="${element.employee_id}" onclick="get_employee(this)" data-emp_uiid=${element.emp_uiid} class="btn btn-info btn-outline-primary text-light" title="view employee  details"> 
                                  <i class="fa fa-eye-slash" aria-hidden="true"></i>
                                  </div>

                                  
                                </td>
                               
  
                              </tr>
            `)
      })

      //  fancyTable()
      // employees = {}
      $("#filter_emp").change(function () {
        val = $(this).val()
        $('#employees_table').empty();
        // alert(val)
        // console.log(val)
        employees = employee_objects.filter(function (item) {
          return item.status === val || item.with_beneficiary == val || item.is_merried === val;
        })

        // console.log(employees)
        employees.forEach(element => {
          $("#employees_table").append(`
                
                <tr>
                                    
                <td class="font-weight-medium employees_image" title="view leave history"> <img class='img' src="${element.profile_exists}" alt="employee prifile image"></td>
                            
                                    <td class="font-weight-medium">${element.employee_id}</td>
                                    <td class="font-weight-medium">${element.full_name}</td>
                                    <td class="font-weight-medium">${element.department}</td>

                                    <td class="font-weight-medium">${element.mobile}</td>
                                    <td class="font-weight-medium">${element.email}</td>
                                    <td class="font-weight-medium">${element.address}</td>
                                    <td class="font-weight-medium">${element.date_employed}</td>
    
                                    <td class="text-primary font-weight-medium" class="">
                                  

                                      <div  id="${element.employee_id}" onclick="get_employee(this)" data-emp_uiid=${element.emp_uiid} class="btn btn-info btn-outline-primary text-light" title="view employee details"> 
                                      <i class="fa fa-eye " aria-hidden="true"></i>
                                      </div>
                                     
                                      
                                    </td>
                                   
      
                                  </tr>
                `)

        });

      })
      fancyTable()

    }

  })

});



$(document).ready(function () {
$("#edit_employee").on('click', function () {

  employee_name = sessionStorage.getItem('EMP_ID')
  console.log(employee_name)
  window.open('/register-staff/','Edit Staff','width=auto,height=auto')

})
})








const get_employee = (employee) => {
  emp_uiid = $(employee).attr('data-emp_uiid');
  employee = employee.id

  console.log(employee,emp_uiid)
  

  model_dialog('d_model', employee)
    sessionStorage.setItem('employee_name',employee)

    sessionStorage.setItem('EMP_ID',emp_uiid)
    
 

  $.ajax({
    url: `/employee-leave/${employee}/`,
    type: "GET",
    success: function (data) {


      $("#leave_detail_badge").text(data.employees.length)
      $("#leave_summary_badge").text(data.leave_per_year.length)
      $("#emp_document_badge").text(data.document_count)
      // console.log(data.out_standing_leaves)
      const leave_days = data.out_standing_leaves ? data.out_standing_leaves : 'N/A'
      // $(".leave_summary_caption").text('Out Standing Leave Day(s): ' + leave_days).addClass('pulse')

      // console.log('doc ',data.document_count)


      $("#leave_detail").on('click', function () {
        $("#leave_table_body, #leave_summary_body").empty();



        if (data.employees.length > 0) {

          const title = `${employee} | Last Time On Leave : ${data.last_date_on_leave}`
          model_dialog('leave_table', title)
          // $(".leave_summary_caption").text('Out Standing Leave: ' + data.out_standing_leaves)


          data.employees.forEach(element => {
            // console.log(element)
            $('#leave_table_body').append(`
            <tr>
                <td> <a class="text-primary" href=${element.url} target="_blank" rel="noopener noreferrer">${element.policy}</a></td>
                <td>${element.start}</td>
                <td>${element.end}</td>
                <td>${element.resuming_date}</td>
                <td>${element.leavedays}</td>
    
    
                <td><a title="download file" href="${fileExist(element.file)}">${file(element.file)}</a></td>
               
                <td>${value(element.supervisor)}</td>
                <td>${value(element.line_manager)}</td>
                <td>${value(element.hr_manager)}</td>
                <td class="text-uppercase">${element.status}</td>
                </tr>
            `)

          });

        }

        // else{
        //   Swal.fire(`NO  DATA AVAILABLE FOR ${employee}`);

        // }

      })


      $("#employee_status").on("click", function () {
        model_dialog('employee_status_view', employee)
                // employee_exit_model()

      
      })

      $("#leave_summary").on('click', function () {

        $("#leave_table_body, #leave_summary_body").empty();

        // console.log(data.employees.length)

        // console.log(data.leave_per_year)
        // const out_standing_leave = data.leave_per_year.filter((element)=>element.policy__has_days===true)

        // const out_standing_leave_days = out_standing_leave.map((element)=> `${element.policy__name} ${element.out_standing}`)

        // console.log(out_standing_leave_days)


        if (data.employees.length > 0) {
          const title = `${employee} | Last Time On leave : ${data.last_date_on_leave}`

          model_dialog('leave_summary_table', title)


          data.leave_per_year.forEach(element => {
            console.log(element)
            const out_standing =  element.policy__has_days ? element.out_standing : 'N/A'

            $("#leave_summary_body").append(`
            <tr>
            <td>${element.policy__name}</td>
            <td>${element.start__year}</td>
            <td>${element.policy__days}</td>
            <td>${element.total_spent}</td>
            <td>  ${out_standing}</td>
            <td>${element.num_application}</td>
          </tr>
            `)

          })

        }
        // else{
        //   Swal.fire(`NO  DATA AVAILABLE FOR ${employee}`);

        // }

      })


      $("#emp_reocord").on('click', function () {

        // alert('emp_reocord'+ employee)
        url = `/employee-data/${emp_uiid}/`
        window.open(url, '_blank')

      })


      $("#emp_document").on('click', function () {


            filename('filenames') //populate the filenames


            // display document data
            documents_data(employee)



          
            model_dialog('doc_container', employee)

      

      })


      // Swal.fire('Changes are not saved', '', 'info')

    }

  })

}


// upload documents data to dom
const documents_data = (employee) => {

  $.ajax({
    url: `/add-document/${employee}/`,
    type: "GET",
    success: function (response) {
      // console.log(response.document)

      documents_objects = Object.assign(response.document);

      // documents_objects.push(response.document)

      // console.log(documents_objects)


      $("#document_table_body").empty();
      $("#create_document").fadeOut('fast')

        
      $("#filenames, li").click(function (e) {
        var doc_id = e.target.id
        // $("#document_id").val(doc_id)
        document.getElementById('document_id').value = doc_id
        console.log(doc_id)
        sessionStorage.setItem('document_name',e.target.innerHTML)
        // sessionStorage.setItem('employee_name',employee)
        $("#document_table_body").empty();

        $("#create_document").fadeIn('fast')


        const documents =documents_objects.filter((value)=>{
          return value.category_id == doc_id
        })

        documents.forEach(function (element) {
          $("#document_table_body").append(`
          <tr>
          <td style="display: none">${element.category}</td>
  
            <td> <a title="download file" class="text-primary text-capitalize" href="${element.file}"> ${element.description}</a> </td>
            <td scope="row">${element.date}</td>
  
            <td>
            <div  id="${element.pk}" data-employee=${employee} onclick="delete_document_data(this)"  class="btn btn-danger btn-outline-primary" title="delete"> 
            <i class="fa fa-trash-o" aria-hidden="true"></i>
            </div>
            </td>
            
          </tr>
          `)
        });
        
      });
      

     

     
    }

  })
  

}


const delete_document_data = (element, employee) => {
  employee = $(element).attr('data-employee');

  // console.log(element.id,employee)
  url = `/delate-document/${employee}/${element.id}/`

  // console.log(url)

  $.ajax({
    url: url,
    type: "POST",
    data: {
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

    },
    success: function () {
   
      $("#emp_document_badge").text(documents_objects.length)

   
      documents_data(employee)
      

      
      show_alert(6000, "success", 'delated successfully')

    },
    error: function (jqXHR, textStatus, errorThrown){
      alert(errorThrown)
    }
  })

}

const filename = (filename) => {

  $.ajax({
    url: '/filename/',
    type: "GET",
    success: function (response) {
      $("#filenames").empty();

      // console.log(response.data);
      response.data.forEach(function (element) {

        // console.log(element)
        $(`#${filename}`).append(`<li  class="font-weight-bold  text-capitalize" style="cursor:pointer" id=${element.pk}> ${element.name}</li>`)
      });
    }

  })

}


const employee_exit_model =()=>{
  employee = sessionStorage.getItem('employee_name')

  $.ajax({
    url: `/exit_employee/${employee}/`,
    type: "GET",
    success: function (data) {
      $("#employee_exit_status_form")[0].reset()

      if(data.date_exited != null){
        // console.log(data)
        $("#employee_status_exit").val(data.employee_status)
        $("#date_exited").val(data.date_exited)
        $("#exit_check").attr('checked', data.exit_check)
        $("#reason_exiting").val(data.reason_exiting)
      }
      
      //here
    }
  })
}



$(document).ready(function () {

  $("#employee_exit_status_form").on("submit", function (event) {
    var employee = sessionStorage.getItem('employee_name')
    event.preventDefault();

    $.ajax({
      url: `/exit_employee/${employee}/`,
      type: "POST",
      data: new FormData(this),
      processData: false,
      contentType: false,
      cache: false,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      success: function (response) {
        // console.log(response.employee_id);


        employee_objects.map((employee) =>{
          if (employee.employee_id == response.employee_id) {
            // console.log(employee)

           return employee.status = response.status
          }
          else return employee
        })
    
        // console.log(employee_objects);

        $("#employee_exit_status_form")[0].reset()
        $('#employee_status_view').dialog("close");
        

        show_alert(6000, "success", 'saved successfully')

      },
      error: function (jqXHR, textStatus, errorThrown) {
        // console.log(jqXHR, textStatus, errorThrown);
        Swal.fire('error occurred try again', '', 'info')

      }

    });
  })

})


$(document).ready(function () {

  $("#file_form").on("submit", function (event) {

    event.preventDefault();

    $.ajax({
      url: "/filename/",
      type: "POST",
      data: new FormData(this),
      processData: false,
      contentType: false,
      cache: false,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      success: function (data) {
        // console.log(data)
        $("#filenames").prepend(data).slideUp(300).fadeIn(400);
        $("#filename").val('')

      },
      error: function (jqXHR, textStatus, errorThrown) {
        // console.log(jqXHR, textStatus, errorThrown);
        Swal.fire('error occurred try again', '', 'info')

      }

    });
  })

})




$(document).ready(function () {

  $("#create_document").on("click", function () {

    var document = sessionStorage.getItem('document_name')
    var employee = sessionStorage.getItem('employee_name')

    var head_title = `NEW ${document} - ${employee}`.toUpperCase()
    model_dialog('file_container', head_title)

  })

  // save employee document

  $("#new_file_form").on("submit", function (event) {
    event.preventDefault()
    // var filename = sessionStorage.getItem('file_name')
    var employee = sessionStorage.getItem('employee_name')
    // alert('New file')
    // url = `/add-document/${employee.id}/${employee.name}/`
    $.ajax({
      url: `/add-document/${employee}/`,
      type: "POST",

      data: new FormData(this),
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      cache: false,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      success: function (response) {
        // console.log(response)
        documents_objects = [...documents_objects,response]

        $("#emp_document_badge").text(documents_objects.length)

        
        // console.log(documents_objects.length)
        
        $("#document_table_body").prepend(`
        <tr>
          
          <td> <a title="download file" class="text-primary" href="${response.file}"> ${response.description}</a> </td>
          <td scope="row">${response.date}</td>
          <td>
          <div  id="${response.pk}" data-employee=${employee} onclick="delete_document_data(this)"  class="btn btn-danger btn-outline-primary" title="delete"> 
          <i class="fa fa-trash-o" aria-hidden="true"></i>
          </div>
          </td>
       
        </tr>
        `)

        show_alert(6000, "success", 'saved successfully')
        $("#new_file_form")[0].reset()
        $('#file_container').dialog("close");

      },
      error: function (jqXHR, textStatus, errorThrown) {
        // console.log(jqXHR, textStatus, errorThrown);
        Swal.fire('error occurred try again', '', 'info')

      }

    });

  })



});




const model_dialog = (element, title) => {
  $(`#${element}`).dialog({
    title: title,
    height: 'auto',
    width: 'auto',
    resizable: false,
    buttons: [
      {
        text: "Close",
        click: function () {
          $(this).dialog("close");
        }

      }
    ]
  });
}





const value = (value) => {
  return (value ? 'YES' : 'NO');

}

const file = (file) => {
  return (file ? 'file' : 'NO file');

}

function fileExist(file) {
  return (file ? file : '#');
}


// live search on table

const search_employees_table = () => {
  $("#emp_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#employees_table  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
}


const search_employee_table = (value) => {
    var value = value.toLowerCase();
    $("#document_table_body  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
  
  });
}



const employee_name_available = () => {
  if (sessionStorage.getItem('employee_name') === null) {
    location.href = '/accounts/logout'

  }

}
