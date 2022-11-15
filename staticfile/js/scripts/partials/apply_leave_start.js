      
// APPLY FOR LEAVE

$('#leave_form').on('submit', function (event) {
    // var formData = new FormData(this);
   
    event.preventDefault();
    const apply_leave = $('#apply_leave').val()

    url = `/apply-leave/${apply_leave}/`

    // console.log('url' ,url)
    $.ajax({
        url: url,
        type: "GET",
        
        success: function (data) {
            // TERNARY OPERATOR FOR EMAIL OR USER ID
            var emp_key = data.data.employee_id
            var employee_id  = emp_key ? emp_key : data.data.email

            // console.log('MYDATA ',emp_key);
            sessionStorage.setItem('emp_key',employee_id);

                 Swal.fire('WELCOME REDIRECTING',data.data.user_name.toUpperCase());
                 setInterval(() => {
                  location=`http://${location.host}/apply-leave/`

                 }, 2000);


            $("#leave_form")[0].reset()

            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            Swal.fire('ID NOT FOUND TRY AGAIN')
            // console.log('MYERROR ',jqXHR, textStatus, errorThrown);
        }

    });
})



const swalRedirect =(user)=> {
    let timerInterval
Swal.fire({
  title: `$WELCOME {user} REDIRECTING ...`,
  html: 'will complete  in <b></b> milliseconds.',
  timer: 2000,
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
    location=`http://${location.host}/apply-leave/`

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