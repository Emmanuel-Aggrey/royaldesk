      
// APPLY FOR LEAVE

$('#leave_form').on('submit', function (event) {
    // var formData = new FormData(this);
   
    event.preventDefault();
    const apply_leave = $('#apply_leave').val()

    url = `/apply-leave-api/${apply_leave}/`

    // console.log('url' ,url)
    $.ajax({
        url: url,
        type: "GET",
        
        success: function (data) {
            // TERNARY OPERATOR FOR EMAIL OR USER ID
            var emp_key = data.employee_id
            var employee_id  = emp_key ? emp_key : data.email
            username = data.user_name.toUpperCase()

            // console.log('MYDATA ',emp_key);
            // sessionStorage.setItem('emp_key',employee_id);

                 Swal.fire('WELCOME REDIRECTING',data.user_name.toUpperCase());
                 setInterval(() => {
                  location=`http://${location.host}/apply-leave/${employee_id}`

                 }, 2000);
                
                //  swalRedirect(username,employee_id)


            $("#leave_form")[0].reset()

            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            Swal.fire('ID NOT FOUND TRY AGAIN')
            // console.log('MYERROR ',jqXHR, textStatus, errorThrown);
        }

    });
})



const swalRedirect =(user,employee_id)=> {
    let timerInterval
Swal.fire({
  title: `WELCOME ${user} REDIRECTING ...`,
  html: 'will complete  in <b></b> milliseconds.',
  timer: 1000,
  timerProgressBar: true,
  didOpen: () => {
    Swal.showLoading()

    const b = Swal.getHtmlContainer().querySelector('b')
    timerInterval = setInterval(() => {

      b.textContent = Swal.getTimerLeft()

    }, 100)
  },
  willClose: () => {
    clearInterval(timerInterval)
  }
}).then((result) => {
    location=`http://${location.host}/apply-leave/${employee_id}`

  /* Read more about handling dismissals below */
  if (result.dismiss === Swal.DismissReason.timer) {
    console.log('I was closed by the timer')
  }
})
}


const loginUser = ()=> {
  const apply_leave = $("#apply_leave").val()
  apply_leave ? $("#apply_leave_btn").click(): ''
  
}