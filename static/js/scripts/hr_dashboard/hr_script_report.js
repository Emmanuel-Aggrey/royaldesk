





// TURN OVER RATE START

$("#run_turn_over_rate_action_form").on("submit", function (e) {
  e.preventDefault();

  const date_from = $('#turn_over_rate_date_start').val()
  const date_to = $("#turn_over_rate_date_end").val()

  // console.log(date_from, date_to)

  $.ajax({
    type: 'GET',
    url: '/hr-table/turn-over-rate/',
    data: { 'date_from': date_from, 'date_to': date_to },

    beforeSend: function () {
      $("#caption_turn_over_rate").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {



      data ? $("#caption_turn_over_rate").text('').removeClass('pulse') : ''


      $("#caption_turn_over_rate_body").append(`
      
      <tr class="new_date">

      <td>${data.date_from}</td>
      <td>${data.date_to}</td>
      <td>${data.rate}%</td>
      </tr>
      `)

    }

  })
})


$("#turn_over_rate_btn").on('click', function (e) {


  $("#turn_over_rate_div").removeClass("d-none")

  models('turn_over_rate_div', 'TURN OVER RATE STATISTICS ')
  date_settings()


})


// TURN OVER RATE END





// COUNTRY FILTER START

$("#run_country_stats").on("click", function (e) {
  e.preventDefault();
  $("#country_stats_body").empty();

  const status = $('#country_status').val()
  const country = $("#country_names").val()

  console.log(country, status)

  $.ajax({
    type: 'GET',
    url: '/hr-table/country/',
    data: { 'status': status, 'country': country },

    beforeSend: function () {
      $("#caption_country").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {
      // console.log(data)
      // $("#caption_country").removeClass('pulse')
      data ? $("#caption_country").text(data.length + ' Record(s)').removeClass('pulse') : ''

      var count = 0
      data.forEach(element => {
        count += 1
        const name = `${element.first_name} - ${element.last_name} ${element.other_name}`;

        $("#country_stats_body").append(`
      
        <tr>     <td class="text-capitalize">${count}</td>
                 <td class="text-capitalize">${name}</td>
                  <td class="text-uppercase">${element.status}</td>
        </tr>
        `)
      });
    }

  })
})


$("#country_stats_btn").on('click', function (e) {


  $("#country_stats_div").removeClass("d-none")

  models('country_stats_div', 'COUNTRY STATISTICS ')

})


// COUNTRY FILTER END



// EMPLOYEE STATUS START



$("#employement_status_action_form").on("submit", function (e) {

  e.preventDefault();

  $("#employement_status_stats_body").empty();

  const year = $('#year_field').val()
  // const date_end = $("#employement_status_date_end").val()
  const department = $("#employement_status_department").val()
  const status = $("#employement_status_status").val()


  // console.log({ 'date_start': date_start, 'date_end': date_end,'department': department,'status': status })


  $.ajax({
    type: 'GET',
    url: '/hr-table/employement-status/',
    data: { 'year': year, 'department': department, 'status': status },

    beforeSend: function () {
      $("#employement_status_caption").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {

      // const slider = $("#slider" ).slider( "instance" )
      // console.log(...slider.options.values)

      // console.log(data)
      // $("#caption_country").removeClass('pulse')
      data ? $("#employement_status_caption").text(data.length + ' Record(s)').removeClass('pulse') : ''

      var count = 0
      data.forEach(element => {
        count += 1
        const name = `${element.first_name} - ${element.last_name} ${element.other_name}`;

        const date_employed = element.date_employed ? element.date_employed : 'NA'
        const date_departure = element.date_departure ? element.date_departure : 'NA'

        $("#employement_status_stats_body").append(`
      
        <tr>     <td class="text-capitalize">${count}</td>
                 <td class="text-capitalize">${name}</td>
                 <td class="text-capitalize">${element.department__name}</td>
                 <td class="text-capitalize">${element.status}</td>
                 <td class="text-uppercase">${date_employed}</td>
                  <td class="text-uppercase">${date_departure}</td>
        </tr>
        `)
      });
    }

  })
})

$("#employement_status_btn").on('click', function (e) {


  $("#employement_status_stats_div").removeClass("d-none")



  models('employement_status_stats_div', 'EMPLOYMENT RATE ')
  load_department('employement_status_department')


  year_settings()
  // date_settings()



})


// EMPLOYEE STATUS END





// EMPLOYEMENT RATE FILTER START


$("#employement_qaurter").change(function () {
  // console.log(this.value)

  $('#employement_date_start').val('').attr('required', false)
  $("#employement_date_end").val('').attr('required', false)

})


$("#employement_action_form").on("submit", function (e) {

  e.preventDefault();

  $("#employement_stats_body").empty();

  const date_start = $('#employement_date_start').val()
  const date_end = $("#employement_date_end").val()
  const quarter = $("#employement_qaurter").val()
  const status = $("#employement_status_stats").val()


  console.log({ 'date_start': date_start, 'date_end': date_end,'quarter': quarter,'status': status })


  $.ajax({
    type: 'GET',
    url: '/hr-table/employment-rate/',
    data: { 'date_start': date_start, 'date_end': date_end, 'quarter': quarter, 'status': status },

    beforeSend: function () {
      $("#employement_caption").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {
      console.log(data)
      // $("#caption_country").removeClass('pulse')
      data ? $("#employement_caption").text(data.length + ' Record(s)').removeClass('pulse') : ''

      var count = 0
      data.forEach(element => {
        count += 1
        const name = `${element.first_name} - ${element.last_name} ${element.other_name}`;

        $("#employement_stats_body").append(`
      
        <tr>     <td class="text-capitalize">${count}</td>
                 <td class="text-capitalize">${name}</td>
                 <td class="text-capitalize">${element.department__name}</td>
                  <td class="text-uppercase">${element.status}</td>
        </tr>
        `)
      });
    }

  })
})

$("#employement_stats_btn").on('click', function (e) {


  $("#employement_stats_div").removeClass("d-none")

  models('employement_stats_div', 'EMPLOYMENT RATE ')

  date_settings()

})


// EMPLOYEMENT RATE FILTER END







// LEAVE FILTER START

$('#leave_status').change(function () {
  var value = this.value
  console.log(value)
  if (value == 'approved') {
    $("#hr_manager").attr('checked', true)
    $("#supervisor").attr('checked', true)
    $("#line_manager").attr('checked', true)
  }
  else{
    $("#hr_manager").attr('checked', false)
    $("#supervisor").attr('checked', false)
    $("#line_manager").attr('checked', false)
  }
})

$("#leave_action_form").on("submit", function (e) {
  e.preventDefault();

  $("#leave_stats_body").empty();

  const department = $("#leave_department").val()
  const status = $('#leave_status').val()
  const start_date = $('#leave_date_start').val()
  const end_date = $('#leave_date_end').val()
  const on_leave = $('#is_on_leave').is(':checked')
  const supervisor = $('#supervisor').is(':checked')
  const line_manager = $('#line_manager').is(':checked')
  const hr_manager = $('#hr_manager').is(':checked')


  // console.log({ 'department': department, 'status': status, 'start_date': start_date, 'end_date': end_date, 'on_leave': on_leave, 'supervisor': supervisor, 'line_manager': line_manager, 'hr_manager': hr_manager })




  $.ajax({
    type: 'GET',
    url: '/hr-table/leave/',
    data: { 'department': department, 'status': status, 'start_date': start_date, 'end_date': end_date, 'on_leave': on_leave, 'supervisor': supervisor, 'line_manager': line_manager, 'hr_manager': hr_manager },

    beforeSend: function () {
      $("#leave_caption").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {

      // console.log(data)
      data ? $("#leave_caption").text(data.length + ' Record(s)').removeClass('pulse') : ''



      var count = 0
      const employees = data.map((employee) => {

        const from_leave =employee.from_leave?'YES':'NO'
        const created_at = new Date(employee.created_at).toUTCString();
        const resuming_date = new Date(employee.resuming_date).toDateString()
        return ` <tr>   
        <td>${count += 1}</td>
          <td class="text-capitalize">${employee.employee__name}</td>
          <td class="text-capitalize">${employee.department}</td>
          <td class="text-capitalize">${employee.status}</td>
          <td class="text-capitalize" title='${employee.leavedays} Days '>${employee.policy} (${employee.leavedays} Days)</td>
          <td class="">${from_leave}</td>
          <td class="text-capitalize">${resuming_date}</td>
          <td class="text-capitalize">${created_at}</td>
        </tr>

        `
      })


      $("#leave_stats_body").append(employees)


    }

  })
})


$("#leave_btn").on('click', function (e) {


  $("#leave_stats_div").removeClass("d-none")
  load_department('leave_department')

  models('leave_stats_div', 'EMPLOYEES LEAVE')
  date_settings()

})


// LEAVE FILTER END






// DEPARTMENT FILTER START

$("#run_department_stats").on("click", function (e) {
  e.preventDefault();
  $("#department_stats_body").empty();

  const department = $("#department_name").val()
  const status = $('#department_status').val()


  // console.log(department, status)

  $.ajax({
    type: 'GET',
    url: '/hr-table/department/',
    data: { 'department': department, 'status': status },

    beforeSend: function () {
      $("#department_caption").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {

      data.employees ? $("#department_caption").text(data.employees.length + ' Record(s)').removeClass('pulse') : ''

      // const departments = data.departments.map((department) => {
      //   return ` <tr>   
      //     <td id="${department.department__name}"  class="text-capitalize">${department.department__name} ${department.departmant_count}</td>
      //   </tr>

      //   `
      // })

      var count = 0
      const employees = data.employees.map((employee) => {
        const name = `${employee.first_name} - ${employee.last_name} ${employee.other_name}`;
        return ` <tr>   
        <td>${count += 1}</td>
          <td class="text-capitalize">${name}</td>
          <td class="text-capitalize department__name">${employee.department__name}</td>
          <td class="text-capitalize">${employee.status}</td>

        </tr>

        `
      })

      const result = $("#department_name").val()
      if (result == 'all') {

        $("#department_stats_body").append(`
        ${employees}
        `)
        $(".department__name").fadeIn('fast')
      }
      else {

        $("#department_stats_body").append(`
        ${employees}
        `)
        $(".department__name").fadeOut('fast')
      }

    }

  })
})


$("#department_stats_btn").on('click', function (e) {


  $("#department_stats_div").removeClass("d-none")
  load_department('department_name')

  models('department_stats_div', 'EMPLOYEES BY DEPARTMENT')

})


// DEPARTMENT FILTER END




// EMPLOYEE AGE  FILTER START

$("#employee_age_action_form").on("submit", function (e) {

  e.preventDefault();

  $("#employee_age_body").empty();


  const status = $("#employee_age_status").val()

  const slider = $("#slider").slider("instance")

  age_from = slider.options.values[0]
  age_to = slider.options.values[1]
  // console.log(age_from,age_to,status)



  // console.log({ 'date_start': date_start, 'date_end': date_end,'department': department,'status': status })


  $.ajax({
    type: 'GET',
    url: '/hr-table/employees-age/',
    data: { 'age_from': age_from, 'age_to': age_to, 'status': status },

    beforeSend: function () {
      $("#employee_age_caption").text('sending yout request...').css('color', 'red').addClass('pulse')
    },
    success: function (data) {


      console.log(data)
      // $("#caption_country").removeClass('pulse')
      data ? $("#employee_age_caption").text(data.length + ' Record(s)').removeClass('pulse') : ''

      var count = 0
      data.forEach(element => {
        count += 1
        const name = `${element.first_name} - ${element.last_name} ${element.other_name}`;

        $("#employee_age_body").append(`
      
        <tr>     <td class="text-capitalize">${count}</td>
                 <td class="text-capitalize">${name}</td>
                 <td class="text-capitalize">${element.department__name}</td>
                  <td>${new Date(element.dob).toDateString()}</td>
                  <td>${element.age} Years</td>
        </tr>
        `)
      });
    }

  })
})

$("#employee_age_btn").on('click', function (e) {


  $("#employee_age_stats_div").removeClass("d-none")

 

  models('employee_age_stats_div', 'EMPLOYEES AGE ')
  age_indicator()

})


// EMPLOYEE AGE FILTER END



// load departemnt



const load_department = (department) => {

  $(`#${department}`).empty()
  $.get("/designation/", function (data) {

    // console.log(data)
    for (var index in data.departments) {

      const department_pk = data.departments[index].name.startsWith('Rock') ? `<option selected value=all> ${data.departments[index].name}</option>` : `<option value=${data.departments[index].pk}> ${data.departments[index].name}</option>`
      // console.log(department_pk)


      $(`#${department}`).append(department_pk);


    }//END OF DEPARTMENT DROPDOWN





  })

}

const models = (element, title) => {

  $(`#${element}`).dialog({

    title: title,
    height: 800,
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



const age_indicator = () => {
  age = `From ${20} : To ${70} years`
  $("#age_indicator").text(age)

  $('#slider').slider({
    range: true,
    min: 16,
    max: 70,
    values: [20, 35],

    animate: 'slow',
    slide: function (event, ui) {

      // Allow time for exact positioning

      setTimeout(function () {
        age = `From ${ui.values[0]} : To ${ui.values[1]} years`
        $("#age_indicator").text(age)
        $("#slider").attr('title', ui.values)
      }, 5);
    },

  });
}

const date_settings = () => {
  $('.dob').datepicker({
    dateFormat: 'yy-mm-dd',
    autoclose: true,
    // orientation: "top",
    maxDate: new Date(),
    // yearRange: '1960:',
    // minDate:'-70Y',
    changeMonth: true,
    
    changeYear: true,
    constrainInput: true,
    // showWeek: true,

  }).on("change", function () {
    $('#employement_qaurter').prop('selectedIndex', 0)
    $('#employement_date_start').attr('required', true)
    $("#employement_date_end").attr('required', true)
  })
}



const year_settings = () => {


  let year_satart = 2022;
  let year_end = (new Date).getFullYear(); // current year
  let year_selected = year_end;

  let option = '';
  option = '' // first option

  for (let i = year_satart; i <= year_end; i++) {
    let selected = (i === year_selected ? ' selected' : '');
    option += '<option value="' + i + '"' + selected + '>' + i + '</option>';
  }

  document.getElementById("year_field").innerHTML = option;

}



// PRINT FILTERED RESULT
const printresult = function(table,heading) {
  $(`#${table}`).printThis({
    // printContainer: true, 
    pageTitle: null,
    footer: null,     
    beforePrint: removeAttr(),              // function called before iframe is filled located inside print_export.js file
    header:`<h3 style="font: bold 100% sans-serif; letter-spacing: 0.5em;" class="text-center mt-5 mb-5">${heading}</h3>`
});
};