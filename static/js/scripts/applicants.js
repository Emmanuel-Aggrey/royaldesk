


$(document).ready(function () {


  applicants()


  search_applicant_table()

  load_comment_form()
  // fancyTable()

  // showModal1()

})

$('#show_form').click(function () {
  $('#applicant_heading').text('APPLICANT REGISTRATION')
  showModal('model_add', 'APPLICANT REGISTRATION')

  $("#department, #designation").empty()
  designation('department', 'designation')
  $('.date').css('display', 'none')
  getStatus('status')

  

})


const applicants = () => {
  $.ajax({
    url: "/applicants-api/",
    type: "GET",
    success: function (data) {
      // console.log(data)
     let  applicants_data = {}
     
     applicants_data = data.filter(applicant =>{
      return (applicant.status === 'selected')
     })
      
      applicants_data.forEach(element => {
        file = element.cv_exists.substring(element.cv_exists.lastIndexOf('/') + 1)
        applicant_transfer_id = element.employee_uuid ? element.employee_uuid : element.applicant_id
        // console.log(element.employee_uuid )
        $("#applicants_table").append(`
    
        <tr>
        <td scope="row" title="print offer letter" >${element.applicant_id} </td>
        <td scope="row">${element.full_name}</td>
                <td scope="row">${element.phone}</td>
                <td scope="row">${element.email}</td>
                <td scope="row" class="text-capitalize">${element.department_name}</td>
                <td scope="row" class="text-capitalize">${element.designation_name}</td>
                <td scope="row" class="cv_view"><a  target="_blank" rel="noopener noreferrer" title="download ${file}" href="${fileExist(element.cv_exists)}">${fileName(element.cv_exists)}</a></td>

                <td scope="row"> <button type="button" class="btn btn-primary" title='update application' id="${element.applicant_id}" onClick=get_applicant(this)>
                <i class="fa fa-pencil-square" aria-hidden="true"></i> 
                </button>
                ${transfer_applicant_btn(element.status,applicant_transfer_id,element.employee_uuid)} 
                ${offer_letter(element.status,element.applicant_id)}
                </td>
                </tr>
        `)
      });

      $("#filter_applicant").change(function () {
       var value = this.value
       $('#applicants_table').empty();

       if(this.value=='all'){
        
        applicants_data= applicants_data= data.filter((applicant) => {
          return applicant.status != value
  
        })
       }
       else{

       applicants_data= applicants_data= data.filter((applicant) => {
        return applicant.status ==value

      })
    }

      applicants_data.forEach((element) => {
        applicant_transfer_id = element.employee_uuid ? element.employee_uuid : element.applicant_id

        $("#applicants_table").append(`
    
        <tr>
        <td scope="row" title="print offer letter" >${element.applicant_id} </td>
        <td scope="row">${element.full_name}</td>
                <td scope="row">${element.phone}</td>
                <td scope="row">${element.email}</td>
                <td scope="row" class="text-capitalize">${element.department_name}</td>
                <td scope="row" class="text-capitalize">${element.designation_name}</td>
                <td scope="row" class="cv_view"><a  target="_blank" rel="noopener noreferrer" title="download ${file}" href="${fileExist(element.cv_exists)}">${fileName(element.cv_exists)}</a></td>

                <td scope="row"> <button type="button" class="btn btn-primary" title='update application' id="${element.applicant_id}" onClick=get_applicant(this)>
                <i class="fa fa-pencil-square" aria-hidden="true"></i> 
                </button>
                ${transfer_applicant_btn(element.status,applicant_transfer_id,element.employee_uuid)} 
                ${offer_letter(element.status,element.applicant_id)}
                </td>
                </tr>
        `)
        
     
      })

      })
      fancyTable()

    }
  })
}


// NEW APPLICANT
$('#applicant_form').submit(function (event) {
  event.preventDefault();
  
  $.ajax({
    url: '/applicants-api/',
    type: 'POST',
    data: new FormData(this),
    enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

    success: function (data) {

      show_alert(5000, "success", data.full_name + ' Record saved')
      $("#applicant_form")[0].reset()
      $('#applicants_table').empty()
      applicants()

      $(".ui-dialog-titlebar-close").click();

    },
    error: function (jqXHR, textStatus, errorThrown) {
      error = `applicant exist ${textStatus} ${errorThrown}`
      // show_alert(5000, "error", error + '')
      Swal.fire(error);

    }

  })
})

// UPDATE APPLICANT

$('#applicant_form_edit').submit(function (event) {
  event.preventDefault();
  applicant_id = $("#applicant_id").text()
  $.ajax({
    url: `/update_applicant/${applicant_id}/`,
    type: 'POST',
    data: new FormData(this),
    enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    
    success: function (data) {
      // console.log(data);

      show_alert(5000, "success", data.full_name + ' Record Updated')
      // $("#applicant_form_edit")[0].reset()
      $('#applicants_table').empty()
      applicants()

      $(".ui-dialog-titlebar-close").click();

            $('#filter_applicant').prop('selectedIndex',0);


    },
    error: function (jqXHR, textStatus, errorThrown) {
      error = `applicant exist ${textStatus} ${errorThrown}`
      // show_alert(5000, "error", error + '')
      Swal.fire(error);

    }

  })
})


const designation = (department, designation) => {


  $.get("/designation/", function (data) {

    for (var index in data.departments) {
      // console.log(data.departments[index].name);

      $(`#${department}`).append(
        '<option value="' +
        data.departments[index].pk +
        '">' +
        data.departments[index].name +
        "</option>"
      );
    }//END OF DEPARTMENT DROPDOWN
    $(`#${department}`).change(function () {
      $(`#${designation}`).empty()
      let depart = $(`#${department}`).val()
      let desig = data.designations.filter(function (item) {
        return item.department == depart
      })
      for (const key in desig) {
        $(`#${designation}`).append(
          '<option class="option" value="' +
          desig[key].pk +
          '">' +
          desig[key].name +
          "</option>"
        );

      }


    })

  });

};


const get_applicant = (applicant_id) => {
  // console.log(applicant_id)
  // $('#applicant_heading').text('UPDATE  REGISTRATION')

  $("#department_edit, #designation_edit,#offer_letters_docs").empty()
  designation('department_edit', 'designation_edit')
  getStatus('status_edit')

  $("#applicant_id").text(applicant_id.id)
  showModal('model_edit', 'UPDATE  REGISTRATION')
  // console.log('applicant_id',applicant_id.id)
  $.ajax({
    url: `/update_applicant/${applicant_id.id}/`,
    type: 'GET',
    success: function (data) {
      // console.log(data);
      $("#fname_edit").val(data.first_name);
      $("#lname_edit").val(data.last_name);
      $("#oname_edit").val(data.other_name);
      $("#email_edit").val(data.email);
      $("#phone_edit").val(data.phone);
      $("#date_edit").val(data.resuming_date);
      $("#address_edit").val(data.address);
      $("#salary_edit").val(data.applicant_salary);

      status_ = data.status.toUpperCase();

      $("#designation_edit").append(`
      <option value="${data.designation}">${data.designation_name}</option>`)

      $(`#status_edit option:contains('${status_}')`).prop("selected", true)
      $(`#department_edit option:contains('${data.department_name}')`).prop("selected", true)
      $(`#designation_edit option:contains('${data.designation_name}')`).prop("selected", true)
     

      
      $("#cv_url").attr('href', data.cv_exists).text(`${fileName(data.cv_exists)}`).attr('title', data.cv_exists.substring(data.cv_exists.lastIndexOf('/') +1)).css('color','#0078F5')
     
      if(data.applicant_offer_letters.length>0){
        // $(`<p>Offer Letter</p>`).insertAfter( "#cv_url" );
        data.applicant_offer_letters.forEach(function(value){

         const letter_name= value.offer_letter.substring(value.offer_letter.lastIndexOf('/') + 1)
         const letters =  `<a style="color:#0078F5" href=${value.offer_letter} title=${letter_name} target="_blank">${letter_name}</a>`

          $("#offer_letters_docs").append(`<li>${letters}</li>`)
        })
        
      }

      // $("#cv_url").text(data.cv_exists.substring(data.cv_exists.lastIndexOf('/') +1)).css('color','#0078F5')

      // $('#department_edit').prop('checked', data.department)


      $("#file_edit").val('') //empty the file edit input when clicked here

    if ($("#status_edit").val() !='selected') {
      $(".date").css('display','none').attr('required',false);
      
    }else{
      $(".date").css('display', 'block').attr('required',true);
    }

    if(data.cv){
      // document.getElementById('file_edit').remove();
      $("#file_edit").attr('name', 'profile')
    }
    // else{
    //   $("#file_edit").attr('name', 'cv');
    // }
    

    }
  })
}

const file_input_change = ()=>{
   
  if($("#file_edit").val()==''){
    // alert('Please select')
    $("#file_edit").attr('name', 'profile')
  }
  else(
    // alert('Please select ne'),
    $("#file_edit").attr('name', 'cv')
    
  )
}

// SAVE COMMECTS
const load_comment_form =()=>{
  $.ajax({
    url:'/message-to-applicant/',
    type:'GET',
    success: function(response){
      // console.log(response);
      $("#selected").val(response.selected)
      $("#in_review").val(response.in_review)
      $("#not_selected").val(response.not_selected)
    }
  })
}

$("#comment_form").on('submit', function(event){
  event.preventDefault();
  $.ajax({
    url:'/message-to-applicant/',
    type:'POST',
    data: new FormData(this),
    // enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

    success: function(data){
      // console.log(data);
      $("#comment_div" ).dialog( "close" );
      show_alert(6000, "success", 'comment saved')
    },
    error: function(jqXHR, textStatus, errorThrown){
      console.log(jqXHR, textStatus, errorThrown);
      show_alert(6000, "error", 'error saving comment try again')

    }
  })
})

$('#message_btn').click(function () {

  $("#comment_div").removeClass('d-none')
  showModal('comment_div','Message')
})




const showModal = (model, title) => {
  $(`#${model}`).dialog({
    height: 'auto',
    width: 'auto',
    title: title,
    buttons: [
      {
        text: "close",
        click: function () {
          $(this).dialog("close");
        }
      }
    ]
  });
  // $("#comment").height($("#file").height())
  // $("#comment_edit").height($("#file_edit").height())


}




const getStatus = (status) => {
  
$(`#${status}`).change(function () {

  const value = this.value

  if(value =='selected'){
    $(".date").css('display', 'block').attr('required',true)
    // console.log("selected",value)
  }
  else{
    // console.log("status",value)
    $(".date").css('display', 'none').attr('required',false)


  }
})
}


// ADD URL TO APPLICANT PAGE IF SELECTED
function offer_letter(status,applicant) {
  
  if (status !=='selected') {
    
   return `<a href="#"></a>`
  }
  else{
    return `<a class='btn btn-outline-primary bg-info' title="offer letter" href="/offer-letter/${applicant}/" target="_blank" rel="noopener noreferrer">
    <i class="fa fa-file text-light" aria-hidden="true"></i>
    </a>`
    
    
  }

}
// TRANSFER APPLICANT

function transfer_applicant_btn(status,applicant,has_employee_record) {
  
  if (status !=='selected') {
    
   return ''
  }
  if(has_employee_record===null ){
  
    return `<button id="${applicant}" class="btn btn-outline-light text-light bg-danger" title="transer applicant ${applicant}" onclick=transfer_unregistered_applicant(this)>➚</button>`
}
else{

  return     `<button id="${applicant}" class="pulse btn btn-outline-info" title="transer applicant ${applicant}" onclick=transfer_registered_applicant(this)>➚</button>`

}

  
}


// const comment_exist = (comment) =>{
//   if(comment.length >=50){
//      return comment.slice(0, 50) +"..."
//   }
//   else if(comment){
//     return comment.slice(0, 50)
//  }
//   else{
//     return ''
//   }
// }


const transfer_registered_applicant =(applicant)=>{

  // sessionStorage.setItem('EMP_ID',applicant.id)
  //  sessionStorage.setItem('transfer',true)

  // console.log(employee_name)
  sessionStorage.removeItem('applicant')

  window.open(`/update-employee/${applicant.id}/`,'Register Applicant','width=auto,height=auto')

}


const transfer_unregistered_applicant = (applicant)=> {
  // console.log(applicant.id)
  sessionStorage.removeItem('EMP_ID')
  // sessionStorage.setItem('transfer',true)

  $.ajax({
    url: `/update_applicant/${applicant.id}/`,
    type:'GET',
    beforeSend: function(){
            show_alert(5000, "info", 'prepairing the transfer')
    },
    success: function (data) {    
      if(data.id){
        sessionStorage.setItem('applicant', JSON.stringify(data))
    show_alert(5000, "success", 'starting the transfer ...')
    // location.href = '/register-staff/'
    window.open('/register-employee/','Register Applicant','width=auto,height=auto')


      }  
      else{
            show_alert(5000, "error", 'an error occurred try again')

      }

    }
  })

}


function fileExist(file) {
  return (file ? file : '#');
}

function fileName(file) {
  return (file ? 'download cv' : '');
}


// live search on table

const search_applicant_table = () => {
  $("#applicants_table_search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#applicants_table  tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

 
}



