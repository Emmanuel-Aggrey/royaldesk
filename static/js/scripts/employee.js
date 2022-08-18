
window.onload = function() {
  employee = sessionStorage.getItem('employee')

    
    $.ajax({  
        url:`/employee/${employee}/`,
        type:'GET',
        success:function(response){
          // console.log(response)
          $("title").text(`${response.employee.employee_id} : DETAILS`)
          $("#employee_id").text(response.employee.employee_id)
          $("#snnit_number").text(response.employee.snnit_number)
          $("#photo").attr("src",response.employee.profile_exists)
          
          $("#full_name").text(`${response.employee.title}. ${response.employee.full_name}`)
          $("#last_name").text(response.employee.last_name)
          $("#other_name").text(`${response.employee.first_name} ${response.employee.other_name}`)
          $("#nia_number").text(response.employee.nia)

          $("#place_of_birth").text(response.employee.place_of_birth)
          $("#date_employed").text(response.employee.date_employed)
          emp_status(response.employee.status)
          $("#sex").text(response.employee.gender)
          $("#dob").text(response.employee.dob)
          $("#is_merried").text(value(response.employee.is_merried))
          $("#nationality").text(response.employee.nationality)
          $("#Country").text(response.employee.country)
          $("#contact_number").text(response.employee.mobile)
          $("#p_email").text(response.employee.email).attr('href',`mailto:${response.employee.email}`)
          $("#residential_address").text(response.employee.address)
          $("#languages").text(response.employee.languages)
          $("#age").text(`${response.employee.age} YEARS`)

          // EMERGENCY INFO
          $("#emergency_name").text(response.employee.emergency_name)
          $("#emergency_address").text(response.employee.emergency_address)
          $("#emergency_phone").text(response.employee.emergency_phone)

          // NEXT OF KIN
          $("#next_of_kin_name").text(response.employee.next_of_kin_name)

          $("#next_of_kin_phone").text(response.employee.next_of_kin_phone)
          $("#next_of_kin_relationship").text(response.employee.next_of_kin_relationship)
          $("#next_of_kin_address").text(response.employee.next_of_kin_address)

          // BANK INFOMATION
          $("#bank_name").text(response.employee.bank_name)
          $("#bank_branch").text(response.employee.bank_branch)
          $("#bank_ac").text(response.employee.bank_ac)
          $("#salary").text(response.employee.salary)

          if (response.employee.applicant_cv_exists) {

            $("#cv").attr("href",response.employee.applicant_cv_exists).text('download cv')
            $('#cv').attr('title',response.employee.applicant_cv_exists.substring(response.employee.applicant_cv_exists.lastIndexOf('/') + 1))

          }
         
          // DEPENDANTS

          response.dependants.forEach(dependent=>{
            full_name = `${dependent.first_name} ${dependent.last_name} ${dependent.other_name}`
            $("#dependencies").append(`
            <tr>
            <th>Name:</th>
            <td>${full_name}</td>
            
            <th>Phone:</th>
            <td>${dependent.mobile}</td>
            </tr>
            <tr>
            <th>Gender:</th>
            <td>${dependent.gender}</td>
            <th>Address:</th>
            <td>${dependent.address}</td>
            <tr> 
            <th>Date of Birth:</th>
            <td>${dependent.dob}</td>
            </tr>
            
            `)  
          })

          response.educations.forEach(education=> {
           $("#education").append(`
           <tr>
           <th>Institution Name:</th>
           <td>${education.school_name}</td>
           
           <th>Course:</th>
           <td>${education.course}</td>
           </tr>
           <tr>
           <th>Certificate:</th>
           <td>${education.certificate}</td>
           <th>Date Completed:</th>
           <td>${education.date_completed}</td>
           </tr>
           `)
          })
          
          response.memberships.forEach(membership => {
            $("#prof_membership").append(`
          
            <td>${membership.name}</td>

            
            `)
          })

          response.employments.forEach(membership => {
            $("#prev_employment").append(`
          
            <tr>
            <th>Company Name:</th>
            <td>${membership.company}</td>
            
            <th>Job Title:</th>
            <td>${membership.job_title}</td>
            <th>Date(resigned):</th>
            <td>${membership.date}</td>
            </tr>
            
            `)
          })


          window.print()

        }
      })

}





$(document).ready(function(){
  // console.log('pageID', $("#pageid").text())
  id = sessionStorage.getItem('employee')
  // console.log('code',page)
  var qrcode = new QRCode(document.getElementById("qrcode"), {
    text: `http://192.168.43.212:8001/employee-info/${id}`,
    width: 90,
    height: 90,
    colorDark : "#000000",
    colorLight : "#ffffff",
    correctLevel : QRCode.CorrectLevel.H,

  });

  current_location = location.href

  employee = current_location.replace('http://192.168.43.212:8001/employee-info/','')


  $.ajax({
      url:`/employee/${employee}`,
      type:'GET',
      success:function(response){
        $("title").text(`${response.employee.employee_id} : DETAILS`)
        $("#employee_id").text(response.employee.employee_id)
        $("#snnit_number").text(response.employee.snnit_number)
        $("#photo").attr("src",response.employee.profile_exists)
        
        $("#full_name").text(`${response.employee.title}. ${response.employee.full_name}`)
        $("#last_name").text(response.employee.last_name)
        $("#nia_number").text(response.employee.nia)

        $("#other_name").text(`${response.employee.first_name} ${response.employee.other_name}`)
        $("#place_of_birth").text(response.employee.place_of_birth)
        $("#date_employed").text(response.employee.date_employed)
        emp_status(response.employee.status)
        $("#sex").text(response.employee.gender)
        $("#dob").text(response.employee.dob)
        $("#is_merried").text(value(response.employee.is_merried))
        $("#nationality").text(response.employee.nationality)
        $("#Country").text(response.employee.country)
        $("#contact_number").text(response.employee.mobile)
        $("#p_email").text(response.employee.email).attr('href',`mailto:${response.employee.email}`)
        $("#residential_address").text(response.employee.address)
        $("#languages").text(response.employee.languages)
        $("#age").text(`${response.employee.age} YEARS`)

        // EMERGENCY INFO
        $("#emergency_name").text(response.employee.emergency_name)
        $("#emergency_address").text(response.employee.emergency_address)
        $("#emergency_phone").text(response.employee.emergency_phone)

        // NEXT OF KIN
        $("#next_of_kin_name").text(response.employee.next_of_kin_name)

        $("#next_of_kin_phone").text(response.employee.next_of_kin_phone)
        $("#next_of_kin_relationship").text(response.employee.next_of_kin_relationship)
        $("#next_of_kin_address").text(response.employee.next_of_kin_address)

        // BANK INFOMATION
        $("#bank_name").text(response.employee.bank_name)
        $("#bank_branch").text(response.employee.bank_branch)
        $("#bank_ac").text(response.employee.bank_ac)
        $("#salary").text(response.employee.salary)


        // DEPENDANTS

        response.dependants.forEach(dependent=>{
          full_name = `${dependent.first_name} ${dependent.last_name} ${dependent.other_name}`
          $("#dependencies").append(`
          <tr>
          <th>Name:</th>
          <td>${full_name}</td>
          
          <th>Phone:</th>
          <td>${dependent.mobile}</td>
          </tr>
          <tr>
          <th>Gender:</th>
          <td>${dependent.gender}</td>
          <th>Address:</th>
          <td>${dependent.address}</td>
          <tr> 
          <th>Date of Birth:</th>
          <td>${dependent.dob}</td>
          </tr>
          
          `)  
        })

        response.educations.forEach(education=> {
         $("#education").append(`
         <tr>
         <th>Institution Name:</th>
         <td>${education.school_name}</td>
         
         <th>Course:</th>
         <td>${education.course}</td>
         </tr>
         <tr>
         <th>Certificate:</th>
         <td>${education.certificate}</td>
         <th>Date Completed:</th>
         <td>${education.date_completed}</td>
         </tr>
         `)
        })
        
        response.memberships.forEach(membership => {
          $("#prof_membership").append(`
        
          <td>${membership.name}</td>

          
          `)
        })

        response.employments.forEach(membership => {
          $("#prev_employment").append(`
        
          <tr>
          <th>Company Name:</th>
          <td>${membership.company}</td>
          
          <th>Job Title:</th>
          <td>${membership.job_title}</td>
          <th>Date(resigned):</th>
          <td>${membership.date}</td>
          </tr>
          
          `)
        })


        window.print()
      }
    })
})




const value =(status)=>{
  return (status ? 'Married' : 'Not Married');
}


const emp_status =(status)=>{
  if (status ==='active'){
    $("#status").text(status).css('color','green','font-size','bold');
  }
  if (status==='resigned'){
    $("#status").text(status).css('color','blue','font-size','bold');

  }
  if (status==='sacked'){
    $("#status").text(status).css('color','red','font-size','bold');

  }
}



// var qrcode = new QRCode("qrcode", { width:100, height:100 });

// $("#text").on("keyup", function () {
// qrcode.makeCode($(this).val());
// }).keyup().focus();