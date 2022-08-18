

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
            


           const department = `Department:  ${data.department}`
           $("#department").text(department)

           const  designation = `Designation: ${data.designation}`
            $("#designation").text(designation)


            if(data.status==='selected'){

                $("#status").text(data.status).css('color','#6566C3')
                $("#fiarwell").text('CONGRATULATION').css('color','#6566C3')
                $(".succesText").css('display','block')
                $("#link").attr('href',`/offer-letter/${unique_id}`).text('Download Your Acceptance Letter')

            }
            else{
                $("#status").text(data.status).css('color','red')

                $(".succesText").css('display','none')
                // console.log('status', status)
            }
                

            if (data.status =='not selected') {
              $("#comment").text(data.comment)
            }
        //    setTimeout(() => {
            seeker_name = data.full_name.toUpperCase()
            showModal(seeker_name)
        //    }, 3000);

        },

        
        error: function (jqXHR, textStatus, errorThrown) {
            // Swal.fire('ID NOT FOUND TRY AGAIN')
            $('#message').text('ID NOT FOUND TRY AGAIN').css('color', 'red','display, block')
            // alert('ID NOT FOUND TRY AGAIN')
        }

    });
})



const showModal = (title) => {
    $('#model').dialog({
      height: 580,
      width: 400,
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
