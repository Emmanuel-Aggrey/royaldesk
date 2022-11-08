

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
            data.departments[index].name+
            "</option>"
        );
      }//END OF DEPARTMENT DROPDOWN
      $("#department").change(function () {
        // document.getElementById('designation').innerText =null;
        $("#issue").empty()
          let depart = $("#department").val()
          // console.log(depart)
          let desig = data.issues.filter(function (item){
               return item.department ==depart
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

      $(`#ticket_filter option:contains('PENDING')`).prop("selected",true)

      desig = response.data.filter(function (item) {
        return item.status =='pending'

      })

      desig.forEach(element => {
        // console.log(new Date(element.created_at))
        var today = new Date(element.created_at);
        var year = today.getFullYear();
        var mes = today.getMonth()+1;
        var dia = today.getDate();
        var data =dia+"-"+mes+"-"+year;

        var hr = today.getHours();
        var min = today.getMinutes()+1;
        var sec = today.getSeconds();
        var time =hr+"-"+min+"-"+sec;

        table += ``
          + `<td >` + element.department + `</td>`
          + `<td >` + `${data} : ${time}`+ `</td>`
          + `<td >` + element.subject + `</td>`
          // + `<td style="width:10%;">` + element.description + `</td>`
          + `<td >` + element.issue + `</td>`
          + `<td >` + `<a target="_blank" rel="noopener noreferrer" title="download file" href="${fileExist(element.image)}">${fileName(element.image)}</a>` + `</td>`
          + `<td >` + element.priority + `</td>`
          + `<td class="text-uppercase">` + element.status + `</td>`
          // + `<td >` + ` ${approve(element.hr_manager)}` + `</td>`
          // + `<td >` + element.status + `</td>`

          + `<td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="getData(${element.id})" >` + `<i class="fa fa-edit  mx-4"  style="cursor:pointer;"  aria-hidden="true"></i>` + `</td>`



        table += "</tr>";

      }); //END OF TABLE

      // FILTER RESPONSE DATA

      $("#ticket_filter").change(function () {
        depart = $("#ticket_filter").val()
        // console.log(depart)

        if (depart === 'all') {
          // console.log(depart,desig)
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

            var today = new Date(element.created_at);
        var year = today.getFullYear();
        var mes = today.getMonth()+1;
        var dia = today.getDate();
        var data =dia+"-"+mes+"-"+year;

        var hr = today.getHours();
        var min = today.getMinutes()+1;
        var sec = today.getSeconds();
        var time =hr+"-"+min+"-"+sec;
          table += ``
          + `<td >` + element.department + `</td>`
          + `<td >` + `${data} : ${time}`+ `</td>`
          + `<td >` + element.subject + `</td>`
          // + `<td >` + element.description + `</td>`
          + `<td >` + element.issue + `</td>`
          + `<td >` + `<a  target="_blank" rel="noopener noreferrer" title="download file" href="${fileExist(element.image)}">${fileName(element.image)}</a>` + `</td>`
          + `<td >` + element.priority + `</td>`
          + `<td class="text-uppercase">` + element.status + `</td>`
          // + `<td >` + ` ${approve(element.hr_manager)}` + `</td>`
          // + `<td >` + element.status + `</td>`

          + `<td class="edit_product  btn btn-light btn-outline-info"  title="edit items" onclick="getData(${element.id})" >` + `<i class="fa fa-edit  mx-4"  style="cursor:pointer;"  aria-hidden="true"></i>` + `</td>`



          table += "</tr>";






        }); //END OF TABLE

        document.getElementById("table_body").innerHTML = table;

        table = document.getElementById("leave_table");


      })//END OF FILTER

      document.getElementById("table_body").innerHTML = table;

      table = document.getElementById("leave_table");

    }
    

  });
  
  search_desk_table()

}//LEAVE TABLE AND



const getData=(id)=>{
  // console.log(id)
  // JUST USING ticket_id TO STORE THIS ID FOR EDITING
  ticket_id=  document.getElementById('ticket_id').innerHTML=id

  $.ajax({
    url: `/get_issue_data/${id}/`,
    type: "GET",
    success: function (response) {
      // console.log('response',response)
      const issue =  response.issue
      const department= response.department
      var priority= response.priority.toUpperCase()
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
      $('#file_url').text(response.image.substring(response.image.lastIndexOf('/') +1)).css('color','#0078F5')
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
      // $('#hr__edit').prop('checked', response.hr_manager)
      // $("#file_url").attr('href', response.file)
      // $('#file_url').text(response.file.substring(response.file.lastIndexOf('/') +1)).css('color','#0078F5')
      // // document.getElementById("file_url").textContent = response.file
     
      // // $("#policy_edit option[value='2']").attr("selected",true)
        // $(`#department_edit option:contains('${department}')`).prop("selected",true)
        // $(`#status_id option:contains('${status}')`).prop("selected",true)



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
          $(`#assiend_to option[value='${handle_over_to}']`).attr("selected",true)



    }
  })
 
} 


const edit_helpdesk_table=(ticket_number)=>{
  // console.log(status)
  $("#edit_help_desk").dialog({

    title: `REVIEW TICKET ${ticket_number}`,
    height: 580,
    width: 1100,
    // hide: { effect: "explode", duration: 1000 }
  })
  // $("#commentss").dialog({
  //   title: 'Commnets'
  // })

  // check if checkbox is ticked
  is_resolved()
}

  $("#btn_comment").click(function() {
    $("#commentss").dialog({
      width: 800,
      height: 500,
      title: 'Commnets',
    
    buttons: [
      {
        text: "close",
        click: function() {
          $( this ).dialog( "close" );
        }
      }
    ]
    
  })
  // get comments from db
  get_comments()

  })


  function is_resolved() {
    if (document.getElementById('status_id').checked) {

     $('#ticket_status').text('TICKET RESOLVED').css( "color", "red" ).addClass('pulse');
     $("#submit_ticket_edit").attr('disabled', 'disabled')
     show_alert(6000,"success",'Ticket Closed')

    

    } 
}


function fileExist(file) {
  return (file ? file : '#');
}


function resolved(value) {
  return (value=='resolved' ? true : false);
}

function fileName(file) {
  return (file ? 'file' : 'no file');
}


$("#assiend_to").change(function () {
  assiend_to = $("#assiend_to").val()
  if (!assiend_to){
    console.log('no',assiend_to)
    $(".submit-btn-edit").css('display', 'none')

  }
  else{
    console.log('yes',assiend_to)
    $(".submit-btn-edit").css('display', 'block')

  }
  

})

$("#new_report").click(function (e) {

  // table = $("#leave_table").find('tr').length - 2
  // var table = document.getElementById("leave_table").rows.length-2;
  // console.log(table);
  $("#new_report_table").dialog({

    title: 'ISSUE NEW REPORT',
    height: 500,
    width: 1000,
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

$(document).ready(function () {
 
    $("#ticket_filter").change(function () {
      var value = $(this).val().toLowerCase();
      console.log(value);
      // $("#table_body  tr").filter(function () {
      //   $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      // });
    });
  
  
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
      console.log(data);
      Swal.fire("TICKET SENT SUCCESSFULLY");

      // $("#leave_form")[0].reset()
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
      // console.log(data);
      Swal.fire("TICKET UPDATED SUCCESSFULLY");

      // $("#leave_form")[0].reset()
      helpdesk_table()
      // $('#apply_leave').dialog( "close" );
      // $(".ui-dialog-titlebar-close").click();
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
  const url =`/comment/${ticket_id}/`

  $.ajax({
    url: url,
    type: "POST",
    
    data: {
      comment:$('#comment_text').val(),
      ticket_id:ticket_id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },

    success: function (data) {
      // console.log(data)
      $("#comment_text").val('')
      show_alert(6000,"success",'comment saved')
      get_comments()

    },
    error: function (jqXHR, textStatus, errorThrown) {
      // console.log(jqXHR, textStatus, errorThrown);
      show_alert(6000,"error",`${textStatus} ${errorThrown}`)

    },
  });

})


const get_comments = () => {
  const ticket_id = $("#ticket_id").text()
  const url =`/comment/${ticket_id}/`

  $.ajax({
    url: url,
    type: "GET",
    
    data: {
      comment:$('#comment_text').val(),
      ticket_id:ticket_id,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),

    },

    success: function (data) {
      $("#comments").empty();
      val=  $("#user_id").text()

      data.forEach(element => {

        const obj = {val: val,user: element.user};



         function fil(){
          // console.log('user ',user,'val ',val)
          if (obj.val==obj.user){
            return 'sent'
          }
          else{
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
    
      $("#submit_comment").attr("disabled", true).attr('title','enter text to send');
  }
else{
  $("#submit_comment").attr("disabled", false).attr('title','send text');;

}

}


