

  const applicant_name = JSON.parse(document.getElementById('applicant_name').textContent)

$(document).ready(function() {

  $("#check_status_next,#offer_letter_next_btn").fadeOut();
})


document.getElementById('unique_id').focus();

$("#applicant_form").submit( (e)=> {
    e.preventDefault();
    const unique_id = $("#unique_id").val()
    sessionStorage.setItem('unique_id',unique_id)
    $.ajax({
        url: `/update_applicant/${unique_id}/`,
        type: "GET",
        beforeSend: function(){
          
            $('#message').text('checking application Status').css('color', 'red').addClass('pulse')

        },
        success: function (data) {
            
          // console.log(data)
            data.status =='selected' ?  $("#check_status_next").fadeIn(): $("#check_status_next").fadeOut();
            data.applicant_offer_letters.length >0 ?  $("#offer_letter_next_btn").fadeIn(): $("#offer_letter_next_btn").fadeOut();

            if(data.applicant_offer_letters.length>0){
              
              data.applicant_offer_letters.forEach(function(value){

               const letter_name= value.offer_letter.substring(value.offer_letter.lastIndexOf('/') + 1)
               const letters =  `<a  href=${value.offer_letter} target="_blank">${letter_name}</a>`

                $("#offer_letters_docs").append(`<li>${letters}</li>`)
              })
              
            }



           const department = `${data.department_name} ${data.designation_name}`
           $("#department").text(department)

          //  const  designation = `Designation: ${data.designation}`
            $("#status").text(data.status).css('display','block').css('color','#6566C3')
            $("#text_message").text(data.message)


            if(data.status=='selected'){
                
                $("#link").attr('href',`/offer-letter/${unique_id}`).text('Download Your Offer Letter').removeClass('d-none')
                // $("#rch_message").text('We at {{company_name}} Wish You Best Of Luck and meet you soon.')

            }
            else{
              $("#link").addClass('d-none')

            }
           
                

           
            // setTimeout(() => {
            seeker_name = data.full_name.toUpperCase()
            showModal('model',seeker_name)
            // }, 3000);

        },

        
        error: function (jqXHR, textStatus, errorThrown) {
            Swal.fire('ID NOT FOUND TRY AGAIN')
            // $('#message').text('ID NOT FOUND TRY AGAIN').css('color', 'red','display, block')
            // alert('ID NOT FOUND TRY AGAIN')
        }

    });
})


$("#btn_letter").click(function(e) {
  $("#offter_div").removeClass('d-none')
  showModal('offter_div','UPLOAD OFFER LETTER')
})




// NEW APPLICANT
$('#offter_letter_form').submit(function (event) {
  event.preventDefault();
  unique_id = sessionStorage.getItem('unique_id');
  $.ajax({
    url: `/upload-offer-letter/${unique_id}/`,
    type: 'POST',
    data: new FormData(this),
    enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

    success: function (data) {
      // console.log(data);
        
      // data.applicant_offer_letters.length >0 ?  $("#check_status_next").fadeIn(): $("#check_status_next").fadeOut();

     
      show_alert(5000, "success", 'Record' + ' SAVED')
      $('#offer_letter_next_btn').click()

      // $(".ui-dialog-titlebar-close").click();

    },
    error: function (jqXHR, textStatus, errorThrown) {

      error = `applicant exist ${textStatus} ${errorThrown}`
      show_alert(5000, "success", error)
      console.log(error)
      // show_alert(5000, "error", error + '')
      // Swal.fire(error);

    }

  })
})



const showModal = (model_id,title) => {
    $(`#${model_id}`).dialog({
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
    $('#message').css('display', 'none');

  }
  


//   $("#link").attr('href','http://10.42.0.1:8001/media/media/cv/2022-07-26/dirsync__PyPI_VFLWqHL.pdf').text('Download Your Acceptance Letter').addClass('btn-outline-primary')
