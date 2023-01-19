var last_on_leave_year = ''
var last_on_leave_month = ''

const EMPLOYEE_NAME = window.location.pathname.split("/")[2]


$(document).ready(function () {

  // console.log(EMPLOYEE_NAME)
  // var today = new Date();
  leave_filter()
  // $("#leave_user").val(sessionStorage.getItem('emp_key'))
  $("#leave_user").val(EMPLOYEE_NAME)
  fancyTable()

}); //end ready

const date_setup = (start, end, resuming_date, days) => {
   
  $(`#${start}`).datepicker({
    beforeShowDay: $.datepicker.noWeekends,

    dateFormat: 'yy-mm-dd',
    minDate: new Date(),
    title: 'From',
    
    todayBtn: true,
    // forceParse:true,
    clearBtn: true,

  }).on("change", function () {
    $('#policy').prop('selectedIndex',0)

    // $(`#${policy}`).prop('selectedIndex',0)

    var selected = $(this).val();
    var next_day = new Date(selected)
    next_day.setDate(next_day.getDate() + 1)
    // console.log(new Date(selected))
    start_date = new Date(selected)
    
    // console.log('month ',start_date.getMonth()+1)
    // console.log('year ',start_date.getFullYear())
    // console.log(last_on_leave_year,last_on_leave_month)
    // console.log(toMonthName(last_on_leave_month))
    if (last_on_leave_year==start_date.getFullYear() && last_on_leave_month==start_date.getMonth()+1){
      

      Swal.fire(`Last Date On Leave ${last_on_leave_year} - ${toMonthName(last_on_leave_month)}`)
      $('#start').datepicker().val('');

    }
   
    // console.log('selected',selected,'next_day',next_day)

    $(`#${end}`).datepicker().val('');

    $(`#${end}`).datepicker("destroy");

    $(`#${end}`).datepicker({
      minDate: next_day,//new Date(selected),
      dateFormat: 'yy-mm-dd',
      title: 'To',
      clearBtn: true,
      beforeShowDay: $.datepicker.noWeekends,
      onSelect: function (dateText, inst) {

        $(`#${days}`).text('No. of days applied for: ' + dateDifference(new Date(selected), new Date(dateText)

        )),
        $('#policy').prop('selectedIndex',0)

          resuming = $(this).val();
        var next_day = new Date(resuming)
        next_day.setDate(next_day.getDate() + 1)
        // console.log(next_day)
       
        $(`#${resuming_date}`).datepicker().val('');

        $(`#${resuming_date}`).datepicker("destroy");


        $(`#${resuming_date}`).datepicker({
          beforeShowDay: $.datepicker.noWeekends,
          dateFormat: 'yy-mm-dd',
          minDate: next_day,
          title: 'Resumption Date',
          todayBtn: false,
          // forceParse:true,
          clearBtn: true,

        })
        var todayDate = new Date(next_day).toISOString().slice(0, 10);
        // console.log(todayDate)

        $('#resuming_date').datepicker().val(todayDate);

      }
    }).on("change", function (

      // resuming_date
      // ('#resuming_date').datepicker().val('')
    ) {


      // $($("#days").text('No. of days applied for '+((new Date(dateText) - new Date(selected)) / 1000 / 60 / 60 / 24)))
      // selected1 = $('#end').val()

      // var days = (new Date(selected) - new Date(selected1)) / 1000 / 60 / 60 / 24;


      // var date = $(this).datepicker("getDate");
      // console.log(dateDifference(new Date(selected1),$(this).datepicker("getDate")))
      // console.log('selected')

    });
    
  })
}



// Expects start date to be before end date
// start and end are Date objects
function dateDifference(start, end) {

  // Copy date objects so don't modify originals
  var s = new Date(+start);
  var e = new Date(+end);

  // console.log(s,e)

  // Set time to midday to avoid dalight saving and browser quirks
  s.setHours(12, 0, 0, 0);
  e.setHours(12, 0, 0, 0);

  // Get the difference in whole days
  var totalDays = Math.round((e - s) / 8.64e7);

  // Get the difference in whole weeks
  var wholeWeeks = totalDays / 7 | 0;

  // Estimate business days as number of whole weeks * 5
  var days = wholeWeeks * 5;

  // If not even number of weeks, calc remaining weekend days
  if (totalDays % 7) {
    s.setDate(s.getDate() + wholeWeeks * 7);

    while (s < e) {
      s.setDate(s.getDate() + 1);

      // If day isn't a Sunday or Saturday, add to business days
      if (s.getDay() != 0 && s.getDay() != 6) {
        ++days;
      }
    }
  }
  return days;
}

const toMonthName=(monthNumber)=> {
  const date = new Date();
  //date number to convert to string 1 = Jan
  date.setMonth(monthNumber-1);
  return date.toLocaleString('en-US',{
    month:'short',
  });
}

$(document).ready(function () {

  leave_table()

  // emp_id = sessionStorage.getItem("emp_key");

  url = `/apply-leave-api/${EMPLOYEE_NAME}/`;

  $.get(url, function (data) {
    // console.log(data)
      if(data.last_on_leave){
      //  const  year = data.last_on_leave.start__year
      //  const  month = data.last_on_leave.start__month
        // console.log(year,month)
        last_on_leave_year =  data.last_on_leave.start__year
        last_on_leave_month = data.last_on_leave.start__month
        // last_on_leave(year,month)
      }

    // DISABLE APPLY FOR LEAVE IF ALREADY ON LEAVE
    emp_on_leave(data.on_leave)

    $(".leave").attr('id', data.employee_id)

    user_name = data.user_name.toUpperCase();
    $("#user_name").text(user_name)
    $("#email").val(data.email);
    $("#phone").val(data.phone);


    // LOOP LEAVE POLICY
    data.leave_policies.forEach((element) => {
      //   console.log(element.pk,element.first_name, element.last_name)
      $("#policy")
        .append(
          `<option data-days=${element.days} value="` +
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
  // emp_id = sessionStorage.getItem("emp_key");
  url = `/apply-leave-api/${EMPLOYEE_NAME}/`;
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

      // console.log(data.on_leave);


      Swal.fire("LEAVE APPLIED SUCCESSFULLY");
      $("#table_body").empty();

      $("#leave_form")[0].reset()



      // const emp_key = sessionStorage.getItem('emp_key');
      $("#leave_filter").empty();

      leave_filter()
      $("#leave_filter").prepend(
        `
         <option value="${EMPLOYEE_NAME}">MY DATA</option> 
          `
      )

      leave_table()


      if (data.on_leave === false) {
        $('#my_leave').attr('disabled', true).text('leave status is active').css('color', 'red').addClass('pulse')

      }
      else {
        $('#my_leave').attr('disabled', false).text('New Leave').css('color', 'blue').removeClass('pulse')

      }
      // emp_on_leave(data.on_leave)

      // $('#apply_leave').dialog( "close" );
      $(".ui-dialog-titlebar-close").click();



    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
      Swal.fire("ERROR TRY AGAIN OR CHECK THE APPLICATION DATE");

    },
  });
}); //// APPLY FOR LEAVE END



$("#policy").change(function () {
  // console.log(this.value)
  const policy_days = parseInt($('select[name="policy"]').find(':selected').attr('data-days'))
 const days2 =  $("#days").text()
 const clean_days = parseInt(days2.replace('No. of days applied for:',''))
  //  console.log('policy_days ',policy_days,'clean_days ',clean_days)
  //  console.log(clean_days-policy_days)
  //  console.log(clean_days>policy_days)

 if(clean_days>policy_days){
  $('#start,#end').val('')
 return Swal.fire('more than policy days')
  
 }
//  days1 > clean_days ? Swal.fire('more than policy days'):''
  // console.log(days1,clean_days)
})


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
      // console.log(data.on_leave);
      Swal.fire("LEAVE UPDATED SUCCESSFULLY");

      // $("#leave_form")[0].reset()
      $("#table_body").empty();

      leave_table()
      // emp_on_leave(data.on_leave)

      if (data.on_leave === false) {
        $('#my_leave').attr('disabled', true).text('leave status is active').css('color', 'red').addClass('pulse')

      }
      else {
        $('#my_leave').attr('disabled', false).text('New Leave').css('color', 'blue').removeClass('pulse')

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
  // $("#leave_filter").empty();

  // const emp_key = sessionStorage.getItem('emp_key');
  $("#leave_filter").empty();

  leave_filter()
  $("#leave_filter").prepend(
    `
     <option value="${EMPLOYEE_NAME}">MY DATA</option> 
      `
  )

  // var table = "";

  $(`#leave_filter option:contains('${'MY DATA'}')`).prop("selected", true)

  $.ajax({
    url: `/my-leaves/${EMPLOYEE_NAME}/`,
    type: "GET",
    success: function (response) {

      // console.log(response)


      hod = response.user_type.hod
      hr = response.user_type.hr
      // console.log(hr,hod)
      
// APPROVALS TO LEAVE APPROVALS
      if (hr  & hod) {
        $("#hr__edit").addClass('HR')
        $(".approve_leave_view").css('display', 'block')

      }
       else if (hr ) {
        $("#hr__edit").addClass('HR')
        $(".approve_leave_view").css('display', 'block')
      
      }
      else if (hod) {

        $("#line_manager_edit").addClass("HOD")
        $("#supervisor_edit").addClass("HOD")
        $(".approve_leave_view").css('display', 'block')

      }

      else{
        $( ".on_leave" ).insertBefore( "#from_leave_col" ).addClass('my-4');
        // console.log('#from_leave_col #on_leave')
      }


      // user_type = `${hod} ${hr}`.toUpperCase()


      // console.log('user_type',hod,hr)

      // $("#hr__edit, #line_manager_edit, #on_leave").addClass(user_type)

      // table += "<tr>";
      let desig = {}

      desig = response.data.filter(function (item) {
        return item.employee_id === EMPLOYEE_NAME

      })

      desig.forEach(element => {
        // days = `${(new Date(element.end) - new Date(element.start)) / 1000 / 60 / 60 / 24}`

        // <td>${approve(element.supervisor)}</td>
        // <td>${approve(element.line_manager)}</td>
        // <td>${approve(element.hr_manager)}</td>
        // <td>${emergencyPhone(element.phone)}</td>

        $("#table_body").append(`
        
        <tr> 
        <td>${element.department}</td>
          <td>${element.employee__name}</td>
          <td>${element.policy}</td>
          <td>${element.start}</td>
          <td>${element.end}</td>
          <td>${element.leavedays}</td>
        
          <td class="text-uppercase leave_status ${leave_status(element.status, element.from_leave)}"> ${element.status}</td>
          <td>
          <div class="edit_product btn text-info btn-outline-dark" title="edit items" onclick="getLeave(${element.id})">
          <i class="fa fa-pencil"  style="cursor:pointer;"  aria-hidden="true"></i>
          </div>
          <a href='${element.url}' class="btn text-primary btn-outline-dark">
          <i class="fa fa-eye"  style="cursor:pointer;"  aria-hidden="true"></i>
          </a>
        </td>
        </tr>

        `)

      }); //END OF TABLE

      // FILTER RESPONSE DATA

      $("#leave_filter").change(function () {
        $("#table_body").empty();
        depart = $("#leave_filter").val()
        // console.log(depart)

        if (depart === 'all') {
          // console.log(depart,desig)
          desig = response.data.filter(function (item) {
            return item
          })
        }
        else if (depart === EMPLOYEE_NAME) {
          // console.log(depart,desig)
          // my leaves
          desig = response.data.filter(function (item) {
            return item.employee_id.toString() === depart
          })
        }

        else if (depart === 'on_leave') {

          desig = response.data.filter(function (item) {
            // console.log(depart,item)
            return item.from_leave === false && item.hr_manager === true
          })
          // console.log(desig)
        }
        else if (depart == 'pending') {
          // console.log(depart,desig)
          desig = response.data.filter(function (item) {

            return item.status === 'pending'
          })
        }

        desig.forEach(element => {
          // console.log(element)
          employee_id = element.employee_id
          // days = `${(new Date(element.end) - new Date(element.start)) / 1000 / 60 / 60 / 24}`
          // console.log("days".days)

// <td>${approve(element.supervisor)}</td>
//             <td>${approve(element.line_manager)}</td>
//             <td>${approve(element.hr_manager)}</td>
        // <td>${emergencyPhone(element.phone)}</td>

          $("#table_body").append(`
        
          <tr> 
          <td>${element.department}</td>
            <td>${element.employee__name}</td>
            <td>${element.policy}</td>
            <td>${element.start}</td>
            <td>${element.end}</td>
            <td>${element.leavedays}</td>
            
            <td class="text-uppercase leave_status ${leave_status(element.status, element.from_leave)}"> ${element.status}</td>
            <td>
              <div class="edit_product btn text-info btn-outline-dark" title="edit items" onclick="getLeave(${element.id})">
              <i class="fa fa-eye"  style="cursor:pointer;"  aria-hidden="true"></i>
              </div>

              <a href='${element.url}' class="btn text-primary btn-outline-dark">
              <i class="fa fa-pencil"  style="cursor:pointer;"  aria-hidden="true"></i>
              </a>
            </td>
  
          </tr>
  
          `)

        }); //END OF TABLE

        // document.getElementById("table_body").innerHTML = table;

        // table = document.getElementById("leave_table");


      })//END OF FILTER

      // document.getElementById("table_body").innerHTML = table;

      // table = document.getElementById("leave_table");

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
  return on_leave ? $('#my_leave').attr('disabled', 'disabled').text('leave status is active').css('color', 'red').addClass('pulse') : '';
}





// CHECK IF USER HAVE RIGHT TO GRANT LEAVE
const user_group = (hr_manager_approve) => {
  // console.log(hr_manager_approve,on_leave)


  const hr = document.getElementById("hr__edit").classList.contains("HR")
  const hod = document.getElementById("line_manager_edit").classList.contains("HOD")


  
  // hr && hr_manager_approve  ? $("#submit_btn_edit").addClass('disabled') : $("#submit_btn_edit").removeClass('disabled') 


  hr_manager_approve & !hr ? $("#submit_btn_edit").addClass("disabled"):$("#submit_btn_edit").removeClass("disabled");

  if (hr && hod) {
    // console.log("HR USER")
  }


  if (hr) {
    // console.log("HR USER" ,hr,' hr_manager_approve',hr_manager_approve)

  }
  // else if (hr_manager && !hr) {
  //   hr_manager  ? $(".submit_btn_edit").addClass('disabled') : $(".submit_btn_edit").removeClass('disabled') 

  // }
  else if (hod) {
    // console.log('HOD USER')
    $('#hr__edit').on('change click', function (e) {
      e.preventDefault();
      Swal.fire("INSUFICIENT RIGHT TO PERFORM THIS ACTION");

    })
    $('#supervisor_edit').on('change click', function (e) {
      e.preventDefault();
      const declaration = 'Declaration by Supervisor'

      const statement = 'I am by this endorsement declaring that I will ensure the retuen of ALL Company properties in his/her possession before he/she proceeds on leave'
      // Swal.fire(statement);
      Swal.fire({
        title: declaration,
        text: statement,
        // icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'continue',
      }).then((result) => {
        // console.log(result)
        if (result.isConfirmed) {
         $('#supervisor_edit').prop( "checked" ,true);
         
        }
        else if (result.isDismissed){
          $('#supervisor_edit').prop( "checked",false );

        }
        
      })
    })
  }
  else {
    // console.log('NORAML USER')

    $('#hr__edit, #line_manager_edit, #supervisor_edit').on('change click', function (e) {
      e.preventDefault();
      Swal.fire("INSUFICIENT RIGHT TO PERFORM THIS ACTION");

    })



    // if ( hr_manager_approve & !hr) {

    //   // console.log('on_leave',hr,'hr_manager_approve',hr_manager_approve)
    //   // console.log('on_leave',!hr,'hr_manager_approve',!hr_manager_approve)
    //   return $("#submit_btn_edit").addClass("disabled");
  
    // }
    // else{
    //   return $("#submit_btn_edit").removeClass("disabled");
  
    // }
  
  }





  
//   if(on_leave ){
//     return $("#on_leave").attr('disabled',true);
// }


  

}




function viewLeaveDetail(employee) {
  // data-leave
  const employee_id = $(`#${employee.id}`).attr("data-leave")
  const id = employee.id
  // console.log(employee_id, id)
}


function getLeave(leave_id) {


  date_setup('start_edit', 'end_edit', 'resuming_date_edit', 'days_edit');
  // console.log(leave_id)
  sessionStorage.setItem('leave_id', leave_id)

  $.ajax({
    url: `/getleave/${leave_id}/`,
    type: "GET",
    success: function (response) {

      // console.log(response)

  
      $("#policy_edit").empty();
      policy = response.policy



      // check user group and apply policy
      user_group(response.hr_manager)

      // console.log(response)


      $(".leave").attr('id', response.employee_id)


      leave_days = response.leavedays
      // INITIALISE FIELDS
      $("#start_edit").val(response.start_date)
      $("#end_edit").val(response.end_date)
      $("#phone_edit").val(response.phone)
      $("#days_edit").text('No. of days applied for: ' + response.leave_days)

      $("#resuming_date_edit").val(response.resuming_date)
      $("#status").val(response.status)
      $('#supervisor_edit').prop('checked', response.supervisor)
      $('#line_manager_edit').prop('checked', response.line_manager)
      $('#hr__edit').prop('checked', response.hr_manager)
      $('#on_leave').prop('checked', response.on_leave)
      $("#file_url").attr('href', response.file)
      $('#file_url').text(response.file.substring(response.file.lastIndexOf('/') + 1)).css('color', '#0078F5')


      response.policies.forEach(element => {
        $("#policy_edit").append(
          `
       <option value="${element.pk}">${element.name} (${element.days} days)</option> 
        `
        )

      });
      // $("#policy_edit option[value='2']").attr("selected",true)
      $(`#policy_edit option:contains('${policy}')`).prop("selected", true)

      

      $("#edit_leave").dialog({

        title: "EDIT LEAVE APPLICATION",
        height: 'auto',
        width: 'auto',
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
      
      // response.status =='approved' && response.on_leave ? $("#on_leave, #submit_btn_edit").attr('disabled', true) : $("#on_leave, #submit_btn_edit").attr('disabled', false);
      // response.status =='pending'  ? $("#on_leave").addClass('disabled') : $("#on_leave").removeClass('disabled');

      response.on_leave   ? $("#on_leave,#submit_btn_edit").attr('disabled', true) : $("#on_leave,#submit_btn_edit").attr('disabled', false);

      if(response.status=='pending'){
        return $("#on_leave").attr('disabled',true)
      }
      else{
        return $("#on_leave").attr('readonly',false)

      }

   

      // response.hr_manager  ? $("#on_leave").addClass("pulse"):$("#on_leave").removeClass("pulse");

      // response.on_leave & response.hr_manager  ? $("#on_leave").addClass("pulse"):$("#on_leave").removeClass("pulse");


      // response.on_leave  ? $("#on_leave").addClass("disabled"):$("#on_leave").removeClass("disabled");


    }
  })
}


// FROM LEAVE POST REQUEST
  $("#on_leave" ).change(function() {


    const on_leave = $("#on_leave").prop('checked')
    const leave_id = sessionStorage.getItem("leave_id");

    if (on_leave) {
      Swal.fire({
        title: 'From Leave',
        text: '',
        // icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'NO',
        confirmButtonText: 'YES',
      }).then((result) => {
        // console.log(result)
        if (result.isConfirmed) {
  
        //  ajax request start
  
        $.ajax({
          url: `/emp-on-leave/${leave_id}/`,
          type: "POST",
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    
          success: function (data) {
            // console.log(data.from_leave)
              data.from_leave ? $("#on_leave").prop('checked', true).attr('disabled',true) : $("#on_leave").prop('checked', false)
              data.from_leave  ? $("#submit_btn_edit").addClass('disabled') : $("#submit_btn_edit").removeClass('disabled') 
    
              Swal.fire('saved successfully')
          },
          error: function (jqXHR, textStatus, errorThrown){
            console.log(jqXHR, textStatus, errorThrown)
            Swal.fire('error occurred try again')
          }
        })
        //ajax request end
         
        }
        else if (result.isDismissed){
          $('#on_leave').prop( "checked",false );
  
        }
        
      })
  
      
    }
    else{
      // not on leave
    }

  })



const verify_leave = (employee) => {
  const employee_id = employee.id
  $.ajax({
    url: `/employee-leave/${employee_id}/`,
    type: 'GET',
    success: function (data) {
   
      $("#leave_summary_body").empty()
      // console.log(data.leave_per_year)
      if (data.leave_per_year.length > 0) {
        data.leave_per_year.forEach(element => {

          const out_standing  = element.policy__has_days ? element.out_standing : 'N/A';

          $("#leave_summary_body").append(`
          <tr>
               <td>${element.policy__name}</td>
               <td>${element.start__year}</td>
               <td>${element.policy__days}</td>
               <td>${element.total_spent}</td>
               <td>${out_standing}</td>
               <td>${element.num_application}</td>

             </tr>
         `)
        });


      }
      else {
        Swal.fire("NO Leave History");

      }
      $('#leave_summary_table').dialog({

        title: `${employee_id} LEAVE HISTORY`,
        height: 'auto',
        width: 'auto',
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

  date_setup('start', 'end', 'resuming_date', 'days')

  $("#apply_leave").dialog({

    title: 'APPLY NEW LEAVE',
    height: 'auto',
    width: 'auto',
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



const leave_status = (leave_status, from_leave) => {
  if (leave_status === 'approved' && from_leave === false) {
    return 'text-warning'

  }
  if (leave_status === 'pending') {
    return 'text-info'
  }
  else if (leave_status === 'approved') {
    return 'text-primary'
  }
  else {
    return 'text-danger'
  }
}




const leave_filter = () => {
  $("#leave_filter").append(`
<option value="all">ALL</option>
   <option value="pending">APPROVALS</option> 
        <option value="on_leave">ON LEAVE</option>
`)
}


// function isValidDate(date_value){
//   dateStr = date_value.value
//   date_id = date_value.id
//   const regex = /^\d{4}-\d{2}-\d{2}$/;

//   if (dateStr.match(regex) === null) {
//     return false;
//   }

//   const date = new Date(dateStr);

//   const timestamp = date.getTime();

//   if (typeof timestamp !== 'number' || Number.isNaN(timestamp)) {
//     return false;
//   }

//   return dateIsValid(date.toISOString().startsWith(dateStr),date_id)
// }

// 03-30-2022
// console.log(isValidDate()

// console.log(isValidDate('2022-01-24'));

// const dateIsValid =(valid_date,date_id)=>{
//   valid_date ? $(`#${date_id}`).css('background-color", "blue"') : $(`#${date_id}`).css( "background-color", "yellow" );
// }



// maryamarkaa@gmail.com
// maryamarkaa77@gmail.com

//REDIRECT TO APPLY FOR LEAVE START PAGE IF emp_key is NULL
const employee_is_login = () => {
  if (sessionStorage.getItem('emp_key') === null) {
    location.href = '/apply-leave-start'

  }

}
