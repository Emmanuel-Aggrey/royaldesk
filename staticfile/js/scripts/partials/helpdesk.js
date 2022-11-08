

$(document).ready(function () {

  // $(".inputUnit").css('width', '370', 'height', '200').addClass('form-control')
  $.get("/departments-issue/", function (data) {
    // console.log(data);

    // console.log(data.departments);
    // $("#department").empty()
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
      $("#issue").empty()
      let depart = $("#department").val()
      // console.log(depart)
      let desig = data.issues.filter(function (item) {
        return item.department == depart
      })
      for (const key in desig) {
        $("#issue").append(
          '<option class="option" value="' +
          desig[key].pk +
          '">' +
          desig[key].issue_name +
          "</option>"
        );
        //   $("#designation").toggle("slow" );

        // console.log(desig[key].name)
      }
      //   console.log(desig)


    })

  });
  helpdesk_table()

})




// LEAVE TABLE START


const helpdesk_table = () => {
  const user_id = $("#user_id").text()


  var table = "";

  // $(`#ticket_filter option:contains('${'MY DATA'}')`).prop("selected",true)

  $.ajax({
    url: `/helpdesk-cases/${user_id}/`, ///helpdesk-cases/2/
    type: "GET",
    success: function (response) {
      // console.log('ticket_filter',response)
      //  $("#ticket_filter").empty();
      // console.log(response)

      table += "<tr>";
      let desig = {}

      $(`#ticket_filter option:contains('PENDING')`).prop("selected", true)

      desig = response.data.filter(function (item) {
        return item.status == 'pending'

      })

      desig.forEach(element => {
        // console.log(new Date(element.created_at))
        var today = new Date(element.date);
        var year = today.getFullYear();
        var mes = today.getMonth() + 1;
        var dia = today.getDate();
        var data = dia + "-" + mes + "-" + year;

        var hr = today.getHours();
        var min = today.getMinutes() + 1;
        var sec = today.getSeconds();
        var time = hr + "-" + min + "-" + sec;

        $("#table_body").append(`
        <tr>
        <td>${element.department}</td>
        <td>${data} : ${time}</td>
        <td>${element.subject}</td>
        <td>${element.issue}</td>
        <td>${element.status}</td>
        <td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="getData(${element.id})" ><i class="fa fa-edit  mx-4"  style="cursor:pointer;"  aria-hidden="true"></i></td>

        
        </tr>
        `)



      }); //END OF TABLE

      // FILTER RESPONSE DATA

      $("#ticket_filter").change(function () {
        $("#table_body").empty();
        depart = $("#ticket_filter").val()
        // console.log(depart)

        if (depart === 'all') {
          console.log(depart)
          desig = response.data.filter(function (item) {
            return item
          })
        }
        else if (depart != 'all') {
          // console.log(depart,desig)
          desig = response.data.filter(function (item) {
            return item.status === depart
          })
        }


        desig.forEach(element => {
          // console.log(element)

          var today = new Date(element.date);
          var year = today.getFullYear();
          var mes = today.getMonth() + 1;
          var dia = today.getDate();
          var data = dia + "-" + mes + "-" + year;

          var hr = today.getHours();
          var min = today.getMinutes() + 1;
          var sec = today.getSeconds();
          var time = hr + "-" + min + "-" + sec;

          $("#table_body").append(`
          <tr>
          <td>${element.department}</td>
          <td>${data} ${time}</td>
          <td>${element.subject}</td>
          <td>${element.issue}</td>
          <td>${element.status}</td>
          <td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="getData(${element.id})" ><i class="fa fa-edit  mx-4"  style="cursor:pointer;"  aria-hidden="true"></i></td>
  
          
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

  search_desk_table()

}//LEAVE TABLE AND




// FILTER BETWEEN TWO DATES

$("#date_to").change(function () {
  var table = "";

  var start = new Date($("#date_from").val());
  var end = new Date($("#date_to").val());

  if (start > end) {
    Swal.fire("END DATE MUST BE IN THE FUTURE");
    $("#date_to").val("");

  } else if ($.trim($("#date_from").val()) === "") {
    Swal.fire("SELECT START DATE");
    $("#date_to").val("");

  }

  else {

    const user_id = $("#user_id").text()
    const url = `/filter-helpdesk/${user_id}/`;

    $.ajax({
      url: url,
      type: "GET",
      data: {
        date_from: $("#date_from").val(),
        date_to: $("#date_to").val(),
      },
      beforeSend: function () {
        $('#loading').css('display', 'block');
        setTimeout(hideLoader, 20 * 1000);
      },
      success: function (response) {
        $('#loading').hide();
        // console.log(response)

        response.data.forEach(element => {

          var today = new Date(element.created_at);
          var year = today.getFullYear();
          var mes = today.getMonth() + 1;
          var dia = today.getDate();
          var data = dia + "-" + mes + "-" + year;

          var hr = today.getHours();
          var min = today.getMinutes() + 1;
          var sec = today.getSeconds();
          var time = hr + "-" + min + "-" + sec;
          table += ``
            + `<td >` + element.department + `</td>`
            + `<td >` + `${data} : ${time}` + `</td>`
            + `<td>` + `<div class="a">${element.subject}</div>` + `</td>`
            // + `<td >` + element.description + `</td>`
            + `<td >` + element.issue + `</td>`
            + `<td >` + `<a  target="_blank" rel="noopener noreferrer" title="download file" href="${fileExist(element.image)}">${fileName(element.image)}</a>` + `</td>`

            + `<td class="text-uppercase">` + element.status + `</td>`
            // + `<td >` + ` ${approve(element.hr_manager)}` + `</td>`
            // + `<td >` + element.status + `</td>`

            + `<td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="getData(${element.id})" >` + `<i class="fa fa-edit  mx-4"  style="cursor:pointer;"  aria-hidden="true"></i>` + `</td>`



          table += "</tr>";
        }) //END OF FOREACH

        document.getElementById("table_body").innerHTML = table;

        table = document.getElementById("leave_table");

      }
    })
  }
}); //end change function




// Strongly recommended: Hide loader after 20 seconds, even if the page hasn't finished loading

function hideLoader() {
  $('#loading').hide();
}


// GET SINGLE DATA
const getData = (id) => {
  // console.log(id)
  // JUST USING ticket_id TO STORE THIS ID FOR EDITING
  ticket_id = document.getElementById('ticket_id').innerHTML = id

  $.ajax({
    url: `/get_issue_data/${id}/`,
    type: "GET",
    success: function (response) {
      // console.log('response',response)
      const issue = response.issue
      const department = response.department
      var priority = response.priority.toUpperCase()
      var status = response.status.toUpperCase()
      const handle_over_to = response.handle_over_to_pk
      // console.log('handle_over_to ',handle_over_to)

      ticket_number = response.ticket_number

      // console.log(handle_over_to)
      $("#assiend_to").empty()

      $("#comments_count").text(response.comments)
      $("#subject_edit").val(response.subject)
      // $("#description_edit").val(response.description)
      $("#file_url").attr('href', response.image)
      $('#file_url').text(response.image.substring(response.image.lastIndexOf('/') + 1)).css('color', '#0078F5')
      $("#priority_edit").append(
        `
        <option value="${response.priority}"> ${priority} </option> 
         `
      )
      $("#department_edit").append(
        `
        <option value="${response.department_pk}"> ${department} </option> 
         `
      )
      // $("#status").val(status)
      $('#status_id').prop('checked', resolved(response.status))



      // $('#issue_edit').val(issue)
      $("#issue_edit").append(
        `
        <option value="${response.issue_pk}"> ${issue} </option> 
         `
      )
      // $('#department_edit').val(department)

      edit_helpdesk_table(ticket_number)




      $("#assiend_to").append(
        `
          <option value="4">Help Desk</option>

          `
      )
      response.employees.forEach(element => {
        $("#assiend_to").append(
          `

         <option value="${element.pk}">${element.first_name} ${element.last_name} </option> 
          `
        )

      });

      // $(`#assiend_to option:contains('${handle_over_to}')`).prop("selected",true)
      $(`#assiend_to option[value='${handle_over_to}']`).attr("selected", true)



    }
  })

}


const edit_helpdesk_table = (ticket_number) => {
  // console.log(status)
  $("#edit_help_desk").dialog({

    title: `REVIEW TICKET ${ticket_number}`,
    height: 'auto',
    width: 'auto',
    buttons: [
      {
        text: "close",
        click: function () {
          $(this).dialog("close");
        }
      }
    ]
  })


  // check if checkbox is ticked
  is_resolved()
}

$("#btn_comment").click(function () {
  $("#commentss").dialog({
    width: 'auto',
    height: 'auto',
    title: 'Commnets',

    buttons: [
      {
        text: "close",
        click: function () {
          $(this).dialog("close");
        }
      }
    ]

  })
  // get comments from db
  get_comments()

})


function is_resolved() {
  status_id = document.getElementById('status_id').checked
  // console.log(status_id)
  if (status_id) {

    return $("#submit_ticket_edit").attr('disabled', 'disabled').text('TICKET RESOLVED').addClass('pulse');

    //  $('#ticket_status').text('TICKET RESOLVED').css( "color", "red" ).addClass('pulse');
    //  show_alert(6000,"success",'Ticket Closed')
  }
  else {

    return $("#submit_ticket_edit").removeAttr('disabled')

  }
}


function fileExist(file) {
  return (file ? file : '#');
}


function resolved(value) {
  return (value == 'resolved' ? true : false);
}

function fileName(file) {
  return (file ? 'file' : 'no file');
}


$("#assiend_to").change(function () {
  assiend_to = $("#assiend_to").val()
  if (!assiend_to) {
    // console.log('no', assiend_to)
    $(".submit-btn-edit").css('display', 'none')

  }
  else {
    console.log('yes', assiend_to)
    $(".submit-btn-edit").css('display', 'block')

  }


})

$("#new_report").click(function (e) {

  // table = $("#leave_table").find('tr').length - 2
  // var table = document.getElementById("leave_table").rows.length-2;
  // console.log(table);
  $("#new_report_table").dialog({

    title: 'ISSUE NEW REPORT',
    height: 'auto',
    width: 'auto',
    buttons: [
      {
        text: "close",
        click: function () {
          $(this).dialog("close");
        }
      }
    ]

    // hide: { effect: "explode", duration: 1000 },
  })

})



// live search on table

const search_desk_table = () => {
  $("#leave_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#table_body  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });


}


// FILTER TABLE
$("#ticket_filster").change(function () {
  if (depart != 'all') {

    // var value = $(this).val().toLowerCase();
    $("#table_body  tr").filter(function () {
      $(this).toggle($(this).text().indexOf(depart) > -1)
    });

  }

})

// APPLY NEW ISSUE START

$("#issue_form").on("submit", function (event) {
  // var formData = new FormData(this);

  event.preventDefault();
  // alert('Please enter')
  const user_id = $("#user_id").text()

  url = '/send-report/'
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
      // console.log(data);
      Swal.fire("TICKET SENT SUCCESSFULLY");

      $("#issue_form")[0].reset()
      $("#table_body").empty();

      helpdesk_table()
      // $('#apply_leave').dialog( "close" );
      $(".ui-dialog-titlebar-close").click();



    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
    },
  });
}); // APPLY NEW ISSUE END





// EDIT NEW ISSUE START

$("#issue_form_edit").on("submit", function (event) {
  // var formData = new FormData(this);
  const ticket_id = $("#ticket_id").text()
  event.preventDefault();

  user_id
  url = `/get_issue_data/${ticket_id}/`
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
      $("#table_body").empty();
      // console.log(data);
      Swal.fire("TICKET UPDATED SUCCESSFULLY");

      // $("#leave_form")[0].reset()
      helpdesk_table()
      // $('#apply_leave').dialog( "close" );
      $(".ui-dialog-titlebar-close").click();
      is_resolved()



    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
    },
  });
}); // EDIT NEW ISSUE END




// send comment
$("#submit_comment").on("click", function (event) {
  event.preventDefault();
  const ticket_id = $("#ticket_id").text()



  // console.log($('#comment_text').val(),ticket_id)
  const url = `/comment/${ticket_id}/`

  $.ajax({
    url: url,
    type: "POST",

    data: {
      comment: $('#comment_text').val(),
      ticket_id: ticket_id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },

    success: function (data) {
      // console.log(data)
      $("#comment_text").val('')
      show_alert(6000, "success", 'comment saved')
      get_comments()

    },
    error: function (jqXHR, textStatus, errorThrown) {
      // console.log(jqXHR, textStatus, errorThrown);
      show_alert(6000, "error", `${textStatus} ${errorThrown}`)

    },
  });

})


const get_comments = () => {
  const ticket_id = $("#ticket_id").text()
  const url = `/comment/${ticket_id}/`

  $.ajax({
    url: url,
    type: "GET",

    data: {
      comment: $('#comment_text').val(),
      ticket_id: ticket_id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },

    success: function (data) {
      $("#comments").empty();
      val = $("#user_id").text()


      $("#comments_count").text(data.length)

      data.forEach(element => {

        const obj = { val: val, user: element.user };

        function fil() {
          // console.log('user ',user,'val ',val)
          if (obj.val == obj.user) {
            return 'sent'
          }
          else {
            return 'received'

          }
        }

        $("#comments").append(`
        <div class=${fil()} list-unstyled>${element.comment} </div>
        `)
      })

    },
    error: function (jqXHR, textStatus, errorThrown) {

    },
  });
}



function ticket_input_valid() {

  if ($.trim($("#comment_text").val()) === "") {

    $("#submit_comment").attr("disabled", true).attr('title', 'enter text to send');
  }
  else {
    $("#submit_comment").attr("disabled", false).attr('title', 'send text');;

  }

}


