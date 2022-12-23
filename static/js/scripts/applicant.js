

document.getElementById('unique_id').focus();

$("#appicant_form").submit( (e)=> {
    e.preventDefault();
    const unique_id = $("#unique_id").val()

    $.ajax({
        url: `/update_applicant/${unique_id}/`,
        type: "GET",
        beforeSend: function(){
          
            $('#message').text('checking application Status').css('color', 'red').addClass('pulse')

        },
        success: function (data) {
            
          // console.log(data.status,data.message)
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
  
  $.ajax({
    url: '/FileUploadView/ENARTEYT-2022/',
    type: 'POST',
    data: new FormData(this),
    enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

    success: function (data) {
      console.log(data);
      // show_alert(5000, "success", 'Record' + '  saved')
 

      // $(".ui-dialog-titlebar-close").click();

    },
    error: function (jqXHR, textStatus, errorThrown) {

      error = `applicant exist ${textStatus} ${errorThrown}`

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
