


// NUMBER OF EMPLOYMENT PER YEAR 
var employment_rate_year = []
var employee_rate_count = []


// EMPLOYEE TURN OVER RATE

var employement_status_year = []
var employement_status_count = []

// NUMSBER OF LEAVES APPLICATIONS FOR THIS YEAR
var leave_applications_month_this_year = []
var leave_applications_count_this_year = []

// NUMSBER OF LEAVES APPLICATION PER YEAR
var leave_applications_year = []
var leave_applications_count = []
const year_leave = {};

var country_name = []
var country_count = []

var department_name = []
var departmen_count = []


var employee_age_name = []
var employee_age_count = []

var result_department_week_Count_In = []
var result_department_week_name = []
var result_department_week_Count_Out = []


$(document).ready(function () {

 
  $.ajax({
    url: '/hr-reports/',
    type: 'GET',
    success: function (data) {
      // console.log(data['dpeartment_count'])

      // console.log(data.turn_over_rate)
      const turn_over_rate = `Year ${data.turn_over_rate.year}   Rate ${data.turn_over_rate.rate}%`
      $("#turn_over_rate").text(turn_over_rate)
      $("#gender_male").text(`Male: ${data.gender.male}`)
      $("#gender_female").text(`Female: ${data.gender.female}`)

      // console.log(data.is_merried)

      $("#is_merried").text(`Married: ${data.is_merried.married}`)
      $("#is_not_merried").text(`Not Married: ${data.is_merried.not_married}`)


      // EMPLOYEE BENEFICIARY
      const emp_with_beneficiary = data.emp_beneficiary.with_beneficiary
      const emp_without_beneficiary = data.emp_beneficiary.without_beneficiary
      $("#emp_with_beneficiary").text(emp_with_beneficiary)
      $("#emp_with_beneficiary_progressbar").css('width', emp_with_beneficiary, 'aria-valuenow', emp_with_beneficiary, 'aria-valuemin', 0, 'aria-valuemax', emp_with_beneficiary)
      $("#emp_without_beneficiary").text(emp_without_beneficiary)
      $("#emp_without_beneficiary_progressbar").css('width', emp_without_beneficiary, 'aria-valuenow', emp_without_beneficiary, 'aria-valuemin', 0, 'aria-valuemax', emp_without_beneficiary)

      // $('#active_employees_count').text(`${data.active_employees_count}`)


      employee_animate_counter(data.active_employees_count)


      // $('#in_active_employees_count').text(`${data.in_active_employees_count}`)
      

      // $('#active_employees_married').text(`Married ${data.active_employees_merried}`)

      $("#age_above").text(`Above 30: ${data.age.above_30}`)
      $("#age_below").text(`Below 30: ${data.age.below_30}`)

      employee_age_name = ['Above 30', 'Below 30']
      employee_age_count = [data.age.above_30,data.age.below_30]



      // console.log(data.on_leave)

      $("#on_leave").text(`On Leave: ${data.leave.on_leave}`)

      data.leave.applied_leave ? 
                  $("#applied_leave").text(`Applied Leave: ${data.leave.applied_leave}`).addClass('pulse')
                      :
                  $("#applied_leave").text(`Applied Leave: ${data.leave.applied_leave}`)


      data.department_count.forEach(element=>{
      department_name.push(element.department__name)
      departmen_count.push(element.employee_count)
     })

      // console.log(department_name,departmen_count)

      data.country.forEach(element => {


        country_name.push(element.country)
        country_count.push(element.emp_count)


        // working but commented it out
    //     $("#country_name").append(`
    //     <li> 
    //         ${element.country}
    //     </li>
    //     `)
    //     $("#country_number").append(`
    //     <li> 
    //     ${element.emp_count}
    // </li>
    //     `)

        // console.log(element.emp_count)
      });


      // UPCOMING BIRTHDAYS
      data.birthdays.forEach(element => {
        full_name = `${element.first_name} ${element.last_name}`
        // `<div></div>`;
        $('#birthdays').append(`

        <li class="timeline-item">

        <p class="mb-n1 font-weight-semibold text-uppercase">${full_name}</p>
        <small >${element.department__name}</small>
        <br>
        <small class="font-weight-semibold">${element.dob}</small>
        </li>

    

        
        `)

      })




    





      // EMPLOYMENT RATE
      data.employment_rate.forEach(element => {
        employment_rate_year.push(element.date_employed__year)
        employee_rate_count.push(element.employee_count)

      })

      // LEAVE APPLICATIONS APPLIED FOR THIS YEAR


      var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];//replace month numbers with monthNames

      data.leave_this_year.forEach(element => {
        month = element.leave_employees__start__month
        month = monthNames[month - 1]

        leave_applications_month_this_year.push(month)
        leave_applications_count_this_year.push(element.emp_onleave_this_month)

      })

        // LEAVE APPLICATIONS PER YEAR
      data.leave_applications.forEach(element => {
      

        leave_applications_year.push(element.leave_employees__start__year)
        leave_applications_count.push(element.leave_applications)

        // console.log({leave_applications_year})
        // console.log(leave_applications_count)

      })


      // EMPLOYEE TURN OVER RATE
      data.employement_status.forEach(element => {
        var label = `${element.date_employed__year} : ${element.status}`
        employement_status_year.push(label)
        employement_status_count.push(element.employee_count)

        // console.log(employee_turnover_rate_year)
        // console.log(employee_turnover_count)

      })


      //EMPLOYEES EXCCED LEAVE
     
      emp_exceed_leave()


      // // EMPLOYEES ON LEAVE
      emp_on_leave()

      // EMPLOYEES FROM LEAVE RECENT

      emp_from_leave_recent()

      clockins()
      // LOAD CHARTS
   


      employment_rate()

    
    },
    error: function (xhr, textStatus, errorThrown) {

    },
  });

 

})






// EMPLOYEES FROM LEAVE RECENT

const emp_from_leave_recent = () => {

  $.ajax({
    url: '/hr-reports/emp_from_leave_recent/',
    type: 'GET',
    success: function (data) {

      data.forEach(element => {

        $("#emp_from_leave").append(`
        <li class="timeline-item">
        <p class="mb-n1 font-weight-semibold text-uppercase">${element.leave_employees__employee__first_name} ${element.leave_employees__employee__last_name}</p>
  
        <small class="event-time">${element.leave_employees__end}</small>
        </li>
  `)
      });
    }

  })
}

  //EMPLOYEES EXCCED LEAVE

const emp_exceed_leave = () => {
  $.ajax({
    url: '/hr-reports/emp_exceed_leave/',
    type: 'GET',
  success: function (data) {

    data.length >=1 ?
    $("#count_exceed_leave").text(data.length).attr('title','exceeded leave').addClass('pulse')
    :  $("#count_exceed_leave").text(data.length).attr('title','exceeded leave')


    data.forEach(function (element) {
      const full_name = `${element.leave_employees__employee__first_name} ${element.leave_employees__employee__last_name}`
    $('#emp_exceed_leave').append(`
    <li class="timeline-item">
    
    <p class="mb-n1 font-weight-semibold text-uppercase"> ${full_name} </p>
    <smal class="time-event">${element.leave_employees__end}</smal> 
    </li>
    `)
    })
  }
  })
}

// EMPLOYEES ON LEAVE

const emp_on_leave = () => {

  $.ajax({
    url: '/hr-reports/emp_on_leave/',
    type: 'GET',
    success: function (data) {

     const count_on_leave=  data.filter(emp_on_leave=>emp_on_leave.leave_employees__hr_manager===true)

     $("#count_on_leave").text(count_on_leave.length).attr('title','employees on leave')

      let desig = {}

      desig = data.filter(function (item) {
        return item.leave_employees__hr_manager===true ;

      })


      // console.log(data)
      desig.forEach(element => {
        // console.log(element)
        $("#emp_on_leave").append(`
        
        <tr>
                            <td>
                              <p class="mb-1 text-dark font-weight-medium">${element.leave_employees__employee__first_name} ${element.leave_employees__employee__last_name}</p>
                              <p class="mt-3 text-muted">Reporting Date : ${element.leave_employees__resuming_date}</p>
                              </td>
                            <td class="text-primary font-weight-medium">
                              <div onclick="backfromleave(${element.leave_employees__pk})" class="btn btn-primary" title="back from leave"> 
                              <i class="fa fa-pencil" aria-hidden="true"></i>
                              </div>
                              <div id="${element.leave_employees__employee__employee_id}" onclick="get_employee_leave(this)" class="btn btn-info" title="leave history"> 
                              <i class="fa fa-eye" aria-hidden="true"></i>
                              </div>
                            </td>
                          </tr>
        `)
      });


      $("#filter_leave").change(function() {
        $('#emp_on_leave').empty();
        $("#approve_leave").empty()

        leave = $(this).val()
        // $("#emp_on_leave").empty()

        if(leave=='on_leave'){

          // console.log(leave)
          desig = data.filter(function (item) {
              // console.log('on_leave',item)
            return item.leave_employees__hr_manager===true;
          })
        }

        if(leave=='applied_for_leave'){
          // console.log(leave)

          
          desig = data.filter(function (item) {
            // console.log('applied',item)
            return item.leave_employees__hr_manager===false;

          })
        }

        console.log('desig',desig)

        desig.forEach(element => {
        
          // console.log(element)
          // <td class="font-weight-medium">${element.leave_employees__end}</td>
          $("#emp_on_leave").append(`
          
          <tr>
                              <td>
                                <p class="mb-1 text-dark font-weight-medium">${element.leave_employees__employee__first_name} ${element.leave_employees__employee__last_name}</p>
                                <p class="mt-3 text-muted">Reporting Date : ${element.leave_employees__resuming_date}</p>

                              </td>
                            
                              <td class="text-primary font-weight-medium" class="on_leave">
                                <div  onclick="backfromleave(${element.leave_employees__pk})" class="btn btn-primary on_leave" title="back from leave"> 
                                <i class="fa fa-pencil on_leave" aria-hidden="true"></i>
                                </div>
                              </td>
                              <td class="text-primary font-weight-medium" class="approve_leave ">
                              <div  onclick="hr_approve_leave(${element.leave_employees__pk})" class="btn btn-primary approve_leave ${line_manager_approve(element.leave_employees__line_manager)}" title="approve leave"> 
                              <i class="fa fa-pencil approve_leave" aria-hidden="true"></i>
                              </div>
                              <div id="${element.leave_employees__employee__employee_id}" onclick="get_employee_leave(this)" class="btn btn-info" title="leave history"> 
                              <i class="fa fa-eye" aria-hidden="true"></i>
                              </div>
                            </td>

                            </tr>
          `)
          if(leave=='on_leave'){
          $('.approve_leave').css('display', 'none')

          }
          else{
            $('.on_leave').css('display', 'none')

            
          }

        });


         
       })


    }

  })
}

// HR APPROVE LEAVE AND IF NOT LINE MANAGER
const hr_approve_leave =(id)=>{
  // console.log(id)

  $.ajax({
    url: `/hr-approve-leave/${id}/`,
    type: 'POST',
    data: {
      pk: id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },
    success: function (data) {
      $("#emp_on_leave, #emp_from_leave, #emp_exceed_leave").empty();
      // console.log('success', data)
      emp_on_leave()
      emp_from_leave_recent()
      emp_exceed_leave()
      $('#filter_leave').prop('selectedIndex',0);

    },
    error: function (jqXHR, textStatus, errorTh) {
      console.log('error', jqXHR, textStatus, errorTh)
    }
  })
}

// MARK EMPLOYEE AS BACK FROM LEAVE
const backfromleave = (id) => {
  // console.log('back',id)

  $.ajax({
    url: `/emp-on-leave/${id}/`,
    type: 'POST',
    data: {
      pk: id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },
    success: function (data) {
      $("#emp_on_leave, #emp_from_leave, #emp_exceed_leave").empty();
      // console.log('success', data)
      emp_on_leave()
      emp_from_leave_recent()
      emp_exceed_leave()

      

    },
    error: function (jqXHR, textStatus, errorTh) {
      console.log('error', jqXHR, textStatus, errorTh)
    }
  })
}


function line_manager_approve(yes) {
  return (yes ?  '':'bg-danger');
}


 

// GET ATTENDANCE COUNT 
const clockins = () => {
  $.ajax({
    url: '/clockins/',
    type: 'GET',
    success: function (data) {
      // console.log(data.sql_today)
      // if (data.sql_today) {
      //   $("#today_data").text(data.sql_today[0].Count_In)
      // }
      // else{
      //   $("#clockin_text").text('No Data For Today')
      // }
      $("#Yesterday_data").text(data.sql_yesterday[0].Count_In)
      $("#Week_data").text(data.sql_week[0].Count_In)

      data.result_department_yesterday.forEach(element => {
        // console.log(element.Department)
        result_department_week_name.push(element.Department)
        result_department_week_Count_In.push(element.Count_In)
        result_department_week_Count_Out.push(element.Count_Out)
      });
    },

    complete: function () {
      loadChart()
    },
    
    error: function (xhr, textStatus, errorThrown) {
      console.log(xhr, textStatus, errorThrown)
    }

  })
}




// EMPLOYMENT RATE START

const employment_rate = () => {

  if ($("#market-overview-chart").length) {
    
    var MarketingChartCanvas = $("#market-overview-chart").get(0).getContext("2d");
    var Marketing_data_1_1 = employee_rate_count;


    var MarketingChart = new Chart(MarketingChartCanvas, {
     
      // options: {
      //   plugins: {
      //     // Change options for ALL labels of THIS CHART
      //     datalabels: {
      //       color: '#36A2EB'
      //     }
      //   }
      // },
      type: 'bar',  //'bar',
      plugins: [ChartDataLabels],

      data: {
        labels: employment_rate_year,
        datasets: [{

          label: 'Num Of Employees',
          
          data: Marketing_data_1_1,

         
          // backgroundColor: '#826af9',
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],

          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          label: 'Num Of Employees',

          
          hoverOffset: 4,
          // borderColor: '#826af9',
          borderWidth: 1
        },


        ],
       
      },
      
      
      options: {
        
        
        responsive: true,
        maintainAspectRatio: true,
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 20,
            bottom: 0
          },

        },
        scales: {
          yAxes: [{
            ticks: {
              max: 400,
              display: true,
              beginAtZero: true,
              fontColor: "#212529",
              stepSize: 100
            },
            gridLines: {
              display: false,
            }
          }],
          xAxes: [{
            stacked: true,
            ticks: {
              beginAtZero: true,
              fontColor: "#212529"
            },
            gridLines: {
              color: "#e9ebf1",
              display: true
            },
            barPercentage: 0.2
          }]
        },
        legend: {
          display: false
        },
        elements: {
          point: {
            radius: 0
          }
        },
        
        
      }
    });


    // UPDATE EMPLOYMENT NUMBER PER YEAR 
    $("#emp_year").change(function () {

      const quarter = $("#emp_year").val();

      $.ajax({
        url: `/employment-rate/${quarter}/`,
        type: "GET",


        success: function (data) {
          // console.log(data);
          employee_rate_count.length = 0
          employment_rate_year.length = 0

          data.forEach(function (element) {
            employment_rate_year.push(element.date_employed__year)
            employee_rate_count.push(element.employee_count)

    
          })


          var data = MarketingChart.data;
          data.datasets[0].data = Marketing_data_1_1;

          MarketingChart.update();

        }
      })


    })


  }

}



// EMPLOYEE TURN OVER RATE

const loadChart = function () {
  $(function () {
    var lineStatsOptions = {
      scales: {
        yAxes: [{
          display: true
        }],
        xAxes: [{
          display: true
        }]
      },
      legend: {
        display: false
      },
      elements: {
        point: {
          radius: 0
        },
        line: {
          tension: 0
        }
      },
      stepsize: 100

    }

    // EMPLOYEE STATUS START
    if ($('#employement_status').length) {
      var salesChartCanvas = $("#employement_status").get(0).getContext("2d");
      // var gradientStrokeFill_1 = salesChartCanvas.createLinearGradient(0, 100, 200, 0);
      // gradientStrokeFill_1.addColorStop(0, '#fa5539');
      // gradientStrokeFill_1.addColorStop(1, '#fa3252');
      var data_1_1 = employement_status_count;

      var areaData = {
        labels: employement_status_year,

        datasets: [{
          
          label: 'Employement Status',
          data: data_1_1,
          // backgroundColor: gradientStrokeFill_1,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: false,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var salesChart = new Chart(salesChartCanvas, {
        type: 'bar',//'line',
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
      
    }






    

    // EMPLOYEE STATUS START

    // ALL YEAR
    if ($("#leave-application").length) {

      var salesChartCanvas = $("#leave-application").get(0).getContext("2d");
      // var gradientStrokeFill_1 = salesChartCanvas.createLinearGradient(0, 100, 200, 0);
      // gradientStrokeFill_1.addColorStop(0, '#fa5539');
      // gradientStrokeFill_1.addColorStop(1, '#fa3252');
      var data_1_1 = leave_applications_count;

      var areaData = {
        labels: leave_applications_year,

        datasets: [{
          
          label: 'Leave Applications',
          data: data_1_1,
          // backgroundColor: gradientStrokeFill_1,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: true,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var salesChart = new Chart(salesChartCanvas, {
        type: 'doughnut',//'line',pie,
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
    }



    




//LEAVE APPLICATION THIS YEAR START
    if ($('#leave_application_month').length) {
      var currentYear = new Date().getFullYear();
      var salesChartCanvas = $("#leave_application_month").get(0).getContext("2d");
 
      var data_1_1 = leave_applications_count_this_year;

      var areaData = {
        labels: leave_applications_month_this_year,

        datasets: [{
          
          label: `Leave Applications ${currentYear}`, 
          data: data_1_1,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: false,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var salesChart = new Chart(salesChartCanvas, {
        type: 'bar',//'line',
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
    }

    // LEAVE APPLICATION THIS YEAR END




    //EMPLOYEE AGE START
    if ($('#employee_age').length) {
      var departmentChartCanvas = $("#employee_age").get(0).getContext("2d");
 
      var data_1_1 = employee_age_count;

      var areaData = {
        labels: employee_age_name,

        datasets: [{
          
          label: 'EMPLOYEES AGE', 
          data: data_1_1,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: true,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var departmentChart = new Chart(departmentChartCanvas, {
        type: 'bar',//'line',
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
    }

    // EMPLOYEE AGE END



    //EMPLOYEE DEPARTMENT START
    if ($('#department_statistics').length) {
      var departmentChartCanvas = $("#department_statistics").get(0).getContext("2d");
 
      var data_1_1 = departmen_count;

      var areaData = {
        labels: department_name,

        datasets: [{
          
          label: 'EMPLOYEES BY DEPARTMENT', 
          data: data_1_1,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: true,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var departmentChart = new Chart(departmentChartCanvas, {
        type: 'bar',//'line',
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
    }

    // EMPLOYEE DEPARTMENT END

    if ($('#yesterday_attendance').length)  {
      // var currentYear = new Date().getFullYear();
      var salesChartCanvas = $("#yesterday_attendance").get(0).getContext("2d");
      department_name = result_department_week_name.map(string => string.slice(0, 5));

      var data_1_1 = result_department_week_Count_In;


      var areaData = {
        labels: department_name,

        datasets: [{
          
          label: 'Yesterday Attendance', 
          data: data_1_1,
          borderWidth: 0,
          pointRadius: 7,
          pointBorderWidth: 3,
          pointBorderColor: '#fff',
          pointHoverRadius: 7,
          pointHoverBackgroundColor: "#fa394e",
          pointHoverBorderColor: "#fa394e",
          pointHoverBorderWidth: 2,
          pointHitRadius: 7,

         
          borderWidth: 2,
          hoverOffset: 4,

          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 3,

        },

          
        ]
      };
      var areaOptions = {

        responsive: true,
        animation: {
         
          animateScale: true,
          animateRotate: true
        },

       
        elements: {
          point: {
            radius: 3,
            backgroundColor: "#fff"
          },
          
        },
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }

        },


        legend: false,

        scales: {

          xAxes: [{
            display: true,
            ticks: {
              display: true,
              beginAtZero: true,
            },
            gridLines: {
              drawBorder: false
            }
          }],
          yAxes: [{
            ticks: {
              max: 200,
              min: 0,
              stepSize: 50,
              fontColor: "#858585",
              beginAtZero: false
            },
           
          }]
        }
      }
      var salesChart = new Chart(salesChartCanvas, {
        type: 'line',//'line',
        plugins: [ChartDataLabels],

        data: areaData,
        options: areaOptions
      });
    }


    if ($("#realtime-statistics").length) {
      department_name = result_department_week_name.map(string => string.slice(0, 3));

      var realtimeChartCanvas = $("#realtime-statistics").get(0).getContext("2d");
      var realtimeChart = new Chart(realtimeChartCanvas, {

        options: {
          
          plugins: {
            // Change options for ALL labels of THIS CHART
            datalabels: {
              color: '#36A2EB'
            }
          }
        },
        type: 'bar',

        data: {
          labels: department_name,
          
          datasets: [{

            label: 'Clock In',
            data: result_department_week_Count_In,
            backgroundColor: "#0f5bff",
            borderColor: '#0f5bff',
            borderWidth: 0
            
          },
          

          
          {
            label: 'Clock Out',
            data: result_department_week_Count_Out,
            backgroundColor: '#e5e9f2',
            borderColor: '#e5e9f2',
            borderWidth: 1
          }
          ]
        },
        options: {

          responsive: true,
          maintainAspectRatio: true,
          layout: {
            padding: {
              left: 0,
              right: 25,
              top: 0,
              bottom: 0
            }
          },
         
          scales: {
            yAxes: [{
              display: false,
              gridLines: {
                display: false
              }
            }],
            xAxes: [{
              stacked: true,
              ticks: {
                display: false,
                beginAtZero: true,
                fontColor: "#354168"
              },
              gridLines: {
                color: "rgba(0, 0, 0, 0)",
                display: false
              },
              barPercentage: 0.5,
            }]
          },
          legend: {
            display: true
          },
          elements: {
            point: {
              radius: 0
            }
          }
        }
      });
    }

    if ($("#employees_country").length) {
     
      var realtimeChartCanvas = $("#employees_country").get(0).getContext("2d");
      var realtimeChart = new Chart(realtimeChartCanvas, {
        
        type: 'doughnut',
        plugins: [ChartDataLabels],
        // label: 'EMPLOYEES COUNTRY STATISTICS',

        data: {
          labels: country_name,

          datasets: [{
            label: 'EMPLOYEES COUNTRY STATISTICS',

            data: country_count,

            
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 3,
            
  
          }
          ]

        },
       
        
        options: {

          responsive: true,
          maintainAspectRatio: true,
          layout: {
            padding: {
              left: 0,
              right: 25,
              top: 0,
              bottom: 0
            }
          },
          scales: {
            
            
            yAxes: [{
              display: true,
              gridLines: {
                display: false
              }
            }],
            xAxes: [{
              stacked: true,
              
              ticks: {
                display: true,
                beginAtZero: true,
                fontColor: "#354168"
              },
              gridLines: {
                color: "rgba(0, 0, 0, 0)",
                display: false
              },
              barPercentage: 1,
            }]
          },
         legend: {
            display: false,
          },
          elements: {
            point: {
              radius: 0
            }
          },
          

        }
      });
        
    
    }
    
   
  });


  

}



if ($('#dashboard-guage-chart').length) {
 
var gauge = new JustGage({
  id: "dashboard-guage-chart", // the id of the html element
  value: 50,
  min: 0,
  max: 100,
  decimals: 2,
  gaugeWidthScale: 0.6,
  pointer: true,
  gaugeWidthScale: 1,
 
  counter: true
  
  
});

// update the value randomly
setInterval(() => {
gauge.refresh(Math.random() * 100);
}, 5000)

}






const get_employee_leave = (employee) => {
  employee = employee.id
  $.ajax({
    url: `/employee-leave/${employee}/`,
    type: "GET",
    success: function (data) {
      // console.log(data.employees)

      $("#leave_table_body, #leave_summary_body").empty();

      const leave_days = data.out_standing_leaves ? data.out_standing_leaves : 'NA'
      // $(".leave_summary_caption").text('Out Standing Leave Day(s): ' + leave_days).addClass('pulse')

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
              // console.log(element)
              $('#leave_table_body').append(`
              <tr>
                  <td> <a class="text-primary" href=${element.url} target="_blank" rel="noopener noreferrer">${element.policy}</a></td>

                  <td>${element.start}</td>
                  <td>${element.end}</td>
                  <td>${element.leavedays}</td>
      
      
                  <td><a title="download file" href="${fileExist(element.file)}">${file(element.file)}</a></td>
                 
                  <td>${value_(element.supervisor)}</td>
                  <td>${value_(element.line_manager)}</td>
                  <td>${value_(element.hr_manager)}</td>
                  <td class="text-uppercase">${element.status}</td>
                  </tr>
              `)
            });
    
            // model here
            const title = `${employee} | Last Time On Leave : ${data.last_date_on_leave}`

            leave_model('#leave_table',title)

          } else if (result.isDenied) {

            data.leave_per_year.forEach(element => { 
              // console.log(element)
              const out_standing =element.policy__has_days ? element.out_standing :'N/A'
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

            })

            const title = `${employee} | Last Time On Leave : ${data.last_date_on_leave}`

            leave_model('#leave_summary_table',title)

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



const leave_model = (leave_table,employee)=>{
  $(leave_table).dialog({
    
    title: `${employee}`,
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



const value_ = (value) =>{
  return (value ? 'YES' : 'NO');

}

const file = (file) =>{
  return (file ? 'file' : 'NO file');

}

function fileExist(file) {
  return (file ? file : '#');
}



const employee_animate_counter=(total)=>{
  let counts=setInterval(updated);
        let upto=0;
        function updated(){
            var count= document.getElementById("active_employees_count");
            count.innerHTML=++upto;
            if(upto===total)
            {
                clearInterval(counts);
            }
        }
}