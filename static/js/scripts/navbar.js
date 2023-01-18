

if (location.pathname==="/helpdesk/"){
    console.log(true)
    $("#small-nav").append(`
    <ul class="nav justify-content-center">
      <li class="nav-item ">
        <a class="nav-link  profile-text font-weight-medium d-none d-md-block" href="/">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link profile-text font-weight-medium d-none d-md-block " href="/hr-dashborad">Dashboard</a>
      </li>
      <!-- <li class="nav-item">
        <a class="nav-link text-light" href="#">Link</a>
      </li> -->
      <li class="nav-item">
        <a class="nav-link disabled profile-text font-weight-medium d-none d-md-block active" href="#">Help Desk</a>
      </li>
    </ul>
    `)
  }
 
 $('#False').addClass('pulse').attr('title', 'not conntected to anviz server')
 

const EMPLOYEE = JSON.parse(document.getElementById('employee_user').textContent)
// const IS_APPLICANT = JSON.parse(document.getElementById('is_applicant').textContent)




$('#my_profile').click(function(e){

  e.preventDefault();
 sessionStorage.removeItem('applicant') 
  sessionStorage.setItem('EMP_ID',EMPLOYEE)

  location.href ='/register-staff'
  
 
})

$('#logout').click(function(e){

e.preventDefault();
sessionStorage.removeItem('applicant') 
sessionStorage.removeItem('EMP_ID',EMPLOYEE)
location.href ='/accounts/logout'


})