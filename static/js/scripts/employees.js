$(document).ready(function () {
  $.ajax({
    url: '/employees/',
    type: 'GET',
    success: function (response) {
      // console.log(response)


      let employees = {}
      employees = response.data.filter(function (item) {
        return item.status == 'active'
      })

      employees.forEach(function (element) {
        // console.log(element)

        $("#employees_table").append(`
                
            <tr>
                                
                                <td class="font-weight-medium" title="view leave history"> <img class='img' src="${element.profile_exists}" alt="employee prifile image"></td>
                                <td class="font-weight-medium">${element.employee_id}</td>

                                <td class="font-weight-medium">${element.full_name}</td>
                                <td class="font-weight-medium">${element.department}</td>
                                <td class="font-weight-medium">${element.mobile}</td>
                                <td class="font-weight-medium">${element.email}</td>
                                <td class="font-weight-medium">${element.address}</td>
                                <td class="font-weight-medium">${element.date_employed}</td>

                                <td class="text-primary font-weight-medium" class="">
                                  <div id="${element.emp_uiid}" onclick="get_employee(this)" class="btn btn-primary btn-outline-info text-light" title="view employee info"> 
                                  <i class="fa fa-eye " aria-hidden="true"></i>
                                  </div>
                                  <div  id="${element.employee_id}" onclick="get_employee_leave(this)" class="btn btn-info btn-outline-primary text-light" title="view leave history"> 
                                  <i class="fa fa-eye-slash" aria-hidden="true"></i>
                                  </div>
                                </td>
                               
  
                              </tr>
            `)
      })

      search_leave_table()
      //  fancyTable()

      $("#filter_emp").change(function () {
        val = $(this).val()
        $('#employees_table').empty();

        if (val == 1) {
          // alert("active")
          employees = response.data.filter(function (item) {
            return item.status === 'active';
          })

        }
        if (val == 2) {
          employees = response.data.filter(function (item) {
            return item.status === 'resigned';
          })
          // alert("resigned")
        }
        if (val == 3) {
          employees = response.data.filter(function (item) {
            return item.status === 'sacked';
          })
        }
        if (val == 4) {
          employees = response.data.filter(function (item) {
            return item.with_beneficiary === true;
          })
        }
        if (val == 5) {
          employees = response.data.filter(function (item) {
            return item.with_beneficiary === false;
          })
        }

        employees.forEach(element => {
          $("#employees_table").append(`
                
                <tr>
                                    
                <td class="font-weight-medium" title="view leave history"> <img class='img' src="${element.profile_exists}" alt="employee prifile image"></td>
                            
                                    <td class="font-weight-medium">${element.employee_id}</td>
                                    <td class="font-weight-medium">${element.full_name}</td>
                                    <td class="font-weight-medium">${element.department}</td>

                                    <td class="font-weight-medium">${element.mobile}</td>
                                    <td class="font-weight-medium">${element.email}</td>
                                    <td class="font-weight-medium">${element.address}</td>
                                    <td class="font-weight-medium">${element.date_employed}</td>
    
                                    <td class="text-primary font-weight-medium" class="">
                                      <div  id="${element.emp_uiid}" onclick="get_employee(this)" class="btn btn-primary btn-outline-info text-light" title="view employee info"> 
                                      <i class="fa fa-eye " aria-hidden="true"></i>
                                      </div>

                                      <div  id="${element.employee_id}" onclick="get_employee_leave(this)" class="btn btn-info btn-outline-primary text-light" title="view leave history"> 
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



// RESIRECT TO EMPLOYEE DETAIL PAGE
const get_employee = (employee) => {
  emp_id = employee.id
  // console.log('emp_id',emp_id)
  url = `/employee-info/${emp_id}/`;
  // console.log(url,id);

  sessionStorage.setItem("employee", emp_id)
  // location.href =url
  window.open(url, "_blank");

}

const get_employee_leave = (employee) => {
  employee = employee.id
  $.ajax({
    url: `/employee-leave/${employee}/`,
    type: "GET",
    success: function (data) {
      // console.log(data.employees)

      $("#leave_table_body, #leave_summary_body").empty();

      // console.log(data.length);
      if (data.employees.length > 0) {

        Swal.fire({
          title: 'SELECT THE LEAVE OPTIONS',
          showDenyButton: true,
          showCancelButton: true,
          confirmButtonText: 'Detailed View',
          denyButtonText: `Summary View`,
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            // Swal.fire('Saved!', '', 'success')
            data.employees.forEach(element => {
              $('#leave_table_body').append(`
              <tr>
                  <td>${element.policy}</td>
                  <td>${element.start}</td>
                  <td>${element.end}</td>
                  <td>${element.leave_days}</td>
                  <td>${element.reason}</td>
      
                  <td>${element.handle_over_to}</td>
      
                  <td><a title="download file" href="${fileExist(element.file)}">${file(element.file)}</a></td>
                 
                  <td>${value(element.collegue_approve)}</td>
                  <td>${value(element.line_manager)}</td>
                  <td>${value(element.hr_manager)}</td>
                  <td class="text-uppercase">${element.status}</td>
                  </tr>
              `)
            });
    
            // model here
            leave_model('#leave_table',employee,1100,700)

          } else if (result.isDenied) {
            console.log(data.leave_per_year)

            data.leave_per_year.forEach(element => { 
              $("#leave_summary_body").append(`
              <tr>
              <td>${element.policy__name}</td>
              <td>${element.start__year}</td>
              <td>${element.policy__days}</td>
              <td>${element.total_spent}</td>
              <td>${element.out_standing}</td>
              <td>${element.num_application}</td>
            </tr>
              `)

            })

            leave_model('#leave_summary_table',employee,750,500)

            // Swal.fire('Changes are not saved', '', 'info')
          }
        })

      }

      else {
        Swal.fire(`NO  DATA AVAILABLE FOR ${employee}`);

      }




    }

  })

}



const leave_model = (leave_table,employee,width,height)=>{
  $(leave_table).dialog({
    
    title: `${employee} LEAVE HISTORY`,
    height: height,
    width: width,
    draggable: true,
    buttons: [
      {
        text: "close",
        click: function () {
          $(this).dialog("close");
        }
      }
    ]
  })
  
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

const search_leave_table = () => {
  $("#emp_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#employees_table  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

}


