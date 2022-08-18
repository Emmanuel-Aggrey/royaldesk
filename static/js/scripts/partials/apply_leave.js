$(document).ready(function () {
  // var today = new Date();

  let today = new Date().toISOString().slice(0, 10);

  $("#start").change(function () {
    var start = new Date($("#start").val());
    toda = new Date(today);

    if (start < toda) {
      Swal.fire("PAST DATE NOT ALLOWED",);
      $("#start").val("");

    }
  });

  $("#end").change(function () {
    var start = new Date($("#start").val());
    var end = new Date($("#end").val());

    if (start < end) {
      var days = (end - start) / 1000 / 60 / 60 / 24;
      $("#days").text('NO OF DAYS APPLIED FOR ' + days);
    } else {
      Swal.fire("END DATE MUST BE IN THE FUTURE");

      //   $("#start").val("");
      $("#end").val("");
      $("#days").text("");
    }
  }); //end change function
}); //end ready



$(document).ready(function () {

  leave_table()

  
  emp_id = sessionStorage.getItem("emp_key");

  url = `/apply-leave/${emp_id}/`;

  $.get(url, function (data) {
      // console.log(data)


    
    // DISABLE APPLY FOR LEAVE IF ALREADY ON LEAVE
    emp_on_leave(data.data.on_leave)

    $(".leave").attr('id',data.data.employee_id)

    user_name =data.data.user_name.toUpperCase();
    $("#user_name").text(user_name)
    $("#email").val(data.data.email);
    $("#phone").val(data.data.phone);
    // LOOP EMPLOYEES
    data.data.handle_over_to.forEach((element) => {
      //   console.log(element.pk,element.first_name, element.last_name)
      $("#handle_over_to")
        .append(
          '<option value="' +
          element.pk +
          '">' +
          `${element.first_name} ${element.last_name}` +
          "</option>"
        )
        .css("height", "50");
    });

    // LOOP LEAVE POLICY
    data.data.leave_policies.forEach((element) => {
      //   console.log(element.pk,element.first_name, element.last_name)
      $("#policy")
        .append(
          '<option value="' +
          element.pk +
          '">' +
          `${element.name} (${element.days} days)` +
          "</option>"
        )
        .css("height", "50");
    });

    // console.log(data.data.leave_policies)
  });
});

// APPLY FOR LEAVE START

$("#leave_form").on("submit", function (event) {
  // var formData = new FormData(this);

  event.preventDefault();
  // alert('Please enter')
  emp_id = sessionStorage.getItem("emp_key");
  url = `/apply-leave/${emp_id}/`;
  $.ajax({
    url: url,
    type: "POST",
    data: new FormData(this),
    enctype: "multipart/form-data",
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    success: function (data) {

      console.log(data.on_leave);


      Swal.fire("LEAVE APPLIED SUCCESSFULLY");

      $("#leave_form")[0].reset()


      leave_table()

      if(data.on_leave === false){
        $('#my_leave').attr('disabled',true).text('leave status is active').css('color','red').addClass('pulse')

      }
      else{
        $('#my_leave').attr('disabled',false).text('New Leave').css('color','blue').removeClass('pulse')

      }
      // emp_on_leave(data.on_leave)

      // $('#apply_leave').dialog( "close" );
      $(".ui-dialog-titlebar-close").click();



    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
    },
  });
}); //// APPLY FOR LEAVE END






// UPADTE LEAVE START

$("#edit_leave_form").on("submit", function (event) {
  // var formData = new FormData(this);

  event.preventDefault();
  // alert('Please enter')
  leave_id = sessionStorage.getItem("leave_id");
  url = `/update-leave/${leave_id}/`;
  $.ajax({
    url: url,
    type: "POST",
    data: new FormData(this),
    enctype: "multipart/form-data",
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    success: function (data) {
      console.log(data.on_leave);
      Swal.fire("LEAVE APPLIED SUCCESSFULLY");

      // $("#leave_form")[0].reset()
      leave_table()
      // emp_on_leave(data.on_leave)

      if(data.on_leave === false){
        $('#my_leave').attr('disabled',true).text('leave status is active').css('color','red').addClass('pulse')

      }
      else{
        $('#my_leave').attr('disabled',false).text('New Leave').css('color','blue').removeClass('pulse')

      }


      $(".ui-dialog-titlebar-close").click();



    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
    },
  });
}); //// UPDATE LEAVE END


// LEAVE TABLE START


const leave_table = () => {
  // $("#emp_filter").empty();

  const emp_key = sessionStorage.getItem('emp_key');
  // $("#emp_filter").empty();

  $("#emp_filter").prepend(
      `
     <option value="${emp_key}">MY DATA</option> 
      `
    )
    

  var table = "";

  $(`#emp_filter option:contains('${'MY DATA'}')`).prop("selected",true)

  $.ajax({
    url: `/my-leaves/${emp_key}/`,
    type: "GET",
    success: function (response) {

      // console.log(response)

     
      hod = response.user_type.hod
      hr = response.user_type.hr

      if (hod ===true){
        $("#line_manager_edit").addClass("HOD")
      }
     if (hr===true) {
      $("#hr__edit").addClass('HR')
     }
    

      // user_type = `${hod} ${hr}`.toUpperCase()


      // console.log('user_type',hod,hr)

      // $("#hr__edit, #line_manager_edit, #on_leave").addClass(user_type)
      
      table += "<tr>";
      let desig = {}

      desig = response.data.filter(function (item) {
        return item.employee_id === emp_key

      })

      desig.forEach(element => {
        days = `${(new Date(element.end) - new Date(element.start)) / 1000 / 60 / 60 / 24}`
        table += ``
        + `<td >` + element.department + `</td>`

        + `<td class="" >` + element.employee__name + `</td>`

          + `<td >` + element.policy + `</td>`
          + `<td >` + `${emergencyPhone(element.phone)}` + `</td>`
          + `<td >` + element.start + `</td>`
          + `<td >` + element.end + `</td>`
          + `<td >` + days + `</td>`
          // + `<td >` + element.reason + `</td>`
          + `<td >` + `${element.handle_over_to} ` + `</td>`
          + `<td >` + `<a title="download file" href="${fileExist(element.file)}">${fileName(element.file)}</a>` + `</td>`
          + `<td >` + `${approve(element.collegue_approve)}` + `</td>`
          + `<td >` + ` ${approve(element.line_manager)}` + `</td>`
          + `<td >` + ` ${approve(element.hr_manager)}` + `</td>`
          + `<td class="text-uppercase ${leave_status(element.status,element.from_leave)}">` + element.status + `</td>`

          + `<td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="get_employee(${element.id})" >` + `<i class="fa fa-pencil  mx-4"  style="cursor:pointer;"  aria-hidden="true">edit</i>` + `</td>`



        table += "</tr>";

      }); //END OF TABLE

      // FILTER RESPONSE DATA

      $("#emp_filter").change(function () {
        
        depart = $("#emp_filter").val()
        // console.log(depart)

        if (depart === 'all') {
          // console.log(depart,desig)
          desig = response.data.filter(function (item) {
            return item
          })
        }
        else if (depart ===emp_key) {
          // console.log(depart,desig)
          // my leaves
          desig = response.data.filter(function (item) {
            return item.employee_id.toString() === depart
          })
        }

         else if (depart ==='on_leave') {
         
          desig = response.data.filter(function (item) {
            // console.log(depart,item)
            return item.from_leave ===false && item.hr_manager ===true 
          })
          console.log(desig)
        }
        else if (depart == 'approvals') {
          // console.log(depart,desig)
          desig = response.data.filter(function (item) {
          
            return item.employee_id !=emp_key
          })
        }

        desig.forEach(element => {
          days = `${(new Date(element.end) - new Date(element.start)) / 1000 / 60 / 60 / 24}`
          // console.log("days".days)
          table += ``
          + `<td >` + element.department + `</td>`
          + `<td  class="" >` + element.employee__name + `</td>`
            + `<td >` + element.policy + `</td>`
            + `<td >` + `${emergencyPhone(element.phone)}` + `</td>`
            + `<td >` + element.start + `</td>`
            + `<td >` + element.end + `</td>`
            + `<td >` + days + `</td>`
            // + `<td >` + element.reason + `</td>`
            + `<td >` + `${element.handle_over_to} ` + `</td>`
            + `<td >` + `<a title="download file" href="${fileExist(element.file)}">${fileName(element.file)}</a>` + `</td>`
            + `<td >` + `${approve(element.collegue_approve)}` + `</td>`
            + `<td >` + ` ${approve(element.line_manager)}` + `</td>`
            + `<td >` + ` ${approve(element.hr_manager)}` + `</td>`
            + `<td  class="text-uppercase leave_status ${leave_status(element.status,element.from_leave)}">` + element.status + `</td>`

            + `<td class="edit_leave  btn btn-light btn-outline-info"  title="edit items" onclick="get_employee(${element.id})" >` + `<i class="fa fa-pencil mx-4"  style="cursor:pointer;"  aria-hidden="true">edit</i>` + `</td>`



          table += "</tr>";






        }); //END OF TABLE

        document.getElementById("table_body").innerHTML = table;

        table = document.getElementById("leave_table");


      })//END OF FILTER

      document.getElementById("table_body").innerHTML = table;

      table = document.getElementById("leave_table");

    }
    

  });
  
  search_leave_table()

}//LEAVE TABLE AND


// CONDITIONS ON TABLE

function approve(status) {
  // emp_key = sessionStorage.getItem('emp_key')
  
  return (status ? 'YES' : 'NO');
}

function fileExist(file) {
  return (file ? file : '#');
}

function emergencyPhone(phone) {
  return (phone ? phone : 'None');
}

function fileName(file) {
  return (file ? 'file' : 'no file');
}

    // DISABLE APPLY FOR LEAVE IF ALREADY ON LEAVE

function emp_on_leave(on_leave) {
  return on_leave ? $('#my_leave').attr('disabled','disabled').text('leave status is active').css('color','red').addClass('pulse') : '';
}





// CHECK IF USER HAVE RIGHT TO GRANT LEAVE
const user_group = (username,on_leave) => {
  user_name = $('#user_name').text()

  const hr =document.getElementById("hr__edit").classList.contains("HR")
  const hod =document.getElementById("line_manager_edit").classList.contains("HOD")

  user_name = user_name.toLowerCase() 
  if(user_name === username){
    // console.log(user_name===username)
    $(".collegue_approve_edit").fadeIn()
    }
    else{
      $(".collegue_approve_edit").fadeOut()


    }

  if(hr && hod ){
    // console.log("HR USER")
    }
    
    else if (hr){
      $('#line_manager_edit').on('change click',function (e){
        e.preventDefault();
        Swal.fire("INSUFICIENT RIGHT TO PERFORM THIS ACTION");

     })
    }
    else if(hod){
        // console.log('HOD USER')
        $('#hr__edit').on('change click',function (e){
          e.preventDefault();
          Swal.fire("INSUFICIENT RIGHT TO PERFORM THIS ACTION");
  
       })
    }
    else{
      // console.log('NORAML USER')

      $('#hr__edit, #line_manager_edit').on('change click',function (e){
        e.preventDefault();
        Swal.fire("INSUFICIENT RIGHT TO PERFORM THIS ACTION");

     })

    
    }

    if (on_leave) {
      
      // console.log('on_leave',on_leave)
      return $("#submit_btn_edit").attr("disabled",true);
}
else{
  return $("#submit_btn_edit").attr("disabled",false);
}

}

function get_employee(leave_id) {

  // console.log(leave_id)
  sessionStorage.setItem('leave_id', leave_id)

  $.ajax({
    url: `/getleave/${leave_id}/`,
    type: "GET",
    success: function (response) {

      // console.log(response)


      $("#policy_edit, #handle_over_to_edit").empty();
      policy = response.policy
      handle_over_to = response.handle_over_to

  

      user_group(handle_over_to.toLowerCase(),response.on_leave)


      $(".leave").attr('id',response.employee_id)

      
      leave_days = response.leave_days
      // INITIALISE FIELDS
      $("#start_edit").val(response.start_date)
      $("#end_edit").val(response.end_date)
      $("#phone_edit").val(response.phone)

      // $("#handle_over_to_edit").removeAttr("class")
      
      // $("#handle_over_to_edit").addClass(handle_over)

      $("#handle_over_to_edit").val(handle_over_to)
      $("#reason_edit").val(response.reason)
      $("#status").val(response.status)
      $('#collegue_approve_edit').prop('checked', response.collegue_approve)
      $('#line_manager_edit').prop('checked', response.line_manager)
      $('#hr__edit').prop('checked', response.hr_manager)
      $('#on_leave').prop('checked', response.on_leave)
      $("#file_url").attr('href', response.file)
      $('#file_url').text(response.file.substring(response.file.lastIndexOf('/') +1)).css('color','#0078F5')
      // document.getElementById("file_url").textContent = response.file


      response.policies.forEach(element => {
        $("#policy_edit").append(
        `
       <option value="${element.pk}">${element.name} (${element.days} days)</option> 
        `
      )

      });
      // $("#policy_edit option[value='2']").attr("selected",true)
        $(`#policy_edit option:contains('${policy}')`).prop("selected",true)

        response.collegues.forEach(element => {
          $("#handle_over_to_edit").append(
          `
         <option value="${element.pk}">${element.first_name} ${element.last_name} </option> 
          `
        )
  
        });

        $(`#handle_over_to_edit option:contains('${handle_over_to}')`).prop("selected",true)
        // console.log(handle_over_to)



      $("#edit_leave").dialog({

        title: `NO OF DAYS APPLIED FOR ${leave_days}`,
        height: 580,
        width: 900,
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

      // console.log('response',response.status)
      if (response.status ==='pending'){
        return $("#on_leave").attr('disabled', true);
      }
      else{
        return $("#on_leave").attr('disabled', false);

      }
      // is_collegue(handle_over_to.toLowerCase())

    }
  })
}


const verify_leave =(employee) => {
  const  employee_id= employee.id
  $.ajax({
    url: `/employee-leave/${employee_id}/`,
    type: 'GET',
    success: function(data) {
      // console.log(data.leave_per_year)
      if(data.leave_per_year.length > 0){
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
        });
       

      }
      else{
        Swal.fire("NO Leave History");

      }
      $('#leave_summary_table').dialog({
    
        title: `${employee_id} LEAVE HISTORY`,
        height: 600,
        width: 700,
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
  })

}

$("#my_leave").click(function (e) {

  table = $("#leave_table").find('tr').length - 2
  // var table = document.getElementById("leave_table").rows.length-2;
  // console.log(table);
  $("#apply_leave").dialog({

    title: 'APPLY NEW LEAVE',
    height: 550,
    width: 900,
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

})


const update_leave_table = () => {

}

// live search on table

const search_leave_table = () => {
  $("#leave_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#table_body  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
}



const leave_status =  (leave_status,from_leave) => {
  if (leave_status ==='approved' && from_leave ===false){
    return 'text-warning'

  }
  if (leave_status ==='pending'){
  return 'text-info'
}
else if (leave_status ==='approved'){
   return 'text-primary'
}
else{
  return 'text-danger'
}
}