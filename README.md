# ROYAL DESK

Built with django, DJango Rest  Framework And Jquary As the Front End

Latest technogies are used to build this project

1. Django And Django RestFramework
2. RabbitMQ As the Message Broker
3. Celery as the channel for communication
4. Celery Beat as the message or task scheduler

The Project consist of Four (4)) Key Models

![1660786181042](https://file+.vscode-resource.vscode-cdn.net/media/aggrey/1EF5-7DBA/HR/image/README/1660786181042.png)

![1660795400296](image/README/1660795400296.png)

1. Human Resource Management System (from interview to hiring as an employee)
2. Leave Management System
3. Help Desk Management System
4. Attendance

# HUMAN RESOURCE MODEL

EMPLOYEES DATA PRESENTED IN CONPREHENSIVE GRAPHS (turn over rates by quarter,number of employees, employees marital status,dependants,countrys of origin etc)

![1660792535911](image/README/1660792535911.png)

![1660792744167](image/README/1660792744167.png)

![1660792755334](image/README/1660792755334.png)

Adding A new Applicant

![1660786706614](image/README/1660786706614.png)

application received by celery to imporve user experience (no delay in sending mail when the use press submit)

![1660786834835](image/README/1660786834835.png)

Celery Have Delivered the mail without any delay from the sender to the reciver

![1660786950980](image/README/1660786950980.png)

Applicant Received the mail and can check the status of the Job Application by using the details provided in the mail ie the Unique ID

![1660787216882](image/README/1660787216882.png)

Applucation Status Under Review By HR Department

![1660787279081](image/README/1660787279081.png)

Application Status Chaged from In Review to **SELECTED**

![1660787608456](image/README/1660787608456.png)

Email Alert have been sent again upon selection by celery

![1660787704797](image/README/1660787704797.png)

Applicant Checking his/her Application Offer again upon receiveing of this email

![1660787823226](image/README/1660787823226.png)

Appicant Can Download Offer Letter Without visiting the Job Location

(can not show the job application offer letter for security reasons *thanks for understanding*)

HR Department Declining a Job Offer

![1660788277526](image/README/1660788277526.png)

HR Department transferring applicant from Job Seeker to Eployee

![1660788374119](image/README/1660788374119.png)

#### PERSONAL INFOMATION

![1660788412082](image/README/1660788412082.png)

DEPENDANTS INFOMATION

![1660788727135](image/README/1660788727135.png)

#### FORMAL EDUCATION INFOMATION

![1660788885181](image/README/1660788885181.png)

### PROFESSIOBAL MEMBERSHIP

![1660789011287](image/README/1660789011287.png)

### PREVIOUS EMPLOYEMENT

![1660789209372](image/README/1660789209372.png)

### FINISED ENROLMENT OF NEW APPLICANT AND EMPLOYEE ID GENERATED

![1660789286956](image/README/1660789286956.png)

EMPLOYEE DETAIL PROFILE FOR THE HR DEPARTMENT

![1660789412620](image/README/1660789412620.png)

# LEAVE MANAGEMENT

#### LEAVE POLICY SETUP

![1660870776558](image/README/1660870776558.png)

Employee Applying for leave

employees can apply for leave(holidays) from the comfort of their homes using their generated ID Number

![1660789585092](image/README/1660789585092.png)

### WELCOMING EMPLOYEE IF EMPLOYEE ID IS VALID

![1660789705306](image/README/1660789705306.png)

#### DISPLAYING ERROR MESSAGE IF ID IS INVALID

![1660789831033](image/README/1660789831033.png)

#### APPLYING FOR LEAVE

![1660789882376](image/README/1660789882376.png)

![1660790134274](image/README/1660790134274.png)

![1660790193462](image/README/1660790193462.png)

### upon succesful of leave application, email alert is sent instanly to the head of department for confirmation

![1660790312290](image/README/1660790312290.png)

ON APPROVAL OF LEAVE BY THE HEAD OF DEPARTMENT, HR WILL ALSO RECIVED A MAIL TO APPROVE THE LEAVE (companies policy)

leave can only be approved by the right authority

![1660790601692](image/README/1660790601692.png)

LEAVE APPROVED BY HR AND HOD

![1660790922435](image/README/1660790922435.png)

LEAVE STATUS CHANGED FROM PENDING TO APPROVE

![1660790954887](image/README/1660790954887.png)

### EMAIL ALERT WILL BE SENT TO THE HR DEPARTMENT AND THE HEAD OF DEPARTMENT ON EMPLOYEES WHO ARE TO REPORT TO WORK THE NEXT DAY WHOM HAVE ONE DAY TO END THEIR LEAVE

![1660791683821](image/README/1660791683821.png)

EMAILS ATTACHEMNT CONTAINS THE LIST OF EMPLOYEES

![1660791740294](image/README/1660791740294.png)

HR DEPARTMENT OR HEAD OF DEPRTMENT ACKNOWLEDGING THAT EMPLOYEE IS BACK FROM LEAVE By ticking the **(From Leave)** Button

![1660791951820](image/README/1660791951820.png)

[Anviz Global | Powering a Smarter World](https://www.anviz.com/)

Anviz time attendance devices data have been integrated with employees data and it detects instantly if an employee  is on leave and have clocked in, the from leave action will be fired authomatically by **django celery beat**

and mark the employee as FROM LEAVE

EMPLOYEES LEAVE HISTORY AVAILABLE FOR HR AND HODS

![1660792406045](image/README/1660792406045.png)

![1660792485511](image/README/1660792485511.png)

##### LEAVE DATA PRSENTED IN GRAPHS

![1660792535911](image/README/1660792535911.png)

HELP DESK

Empoyees can channel means of communication through the helpdesk system to ensure people are accountable when complains are channed to them

![1660792927142](image/README/1660792927142.png)

Emails are sent to the right people when complains are logged in the helpdesk sustem

![1660792992649](image/README/1660792992649.png)

ATTENDACE

[Anviz Global | Powering a Smarter World](https://www.anviz.com/)

anviz time attendace device is used to clockin by Employees but what this system does it that it takes the data from anviz database and presents it in a manner recormmened by the Human Resource Department for easy tracking of employees attandace in the company and authomatically sends monthly and quarterly attendace and reporting to The complanies head quartes view email.

![1660793045938](image/README/1660793045938.png)

# DEPARTMENT AND DESIGNATION SETUP

![1660870653157](image/README/1660870653157.png)


# MONITORING REAL TIME MESSAGES (tasks) with Flower

![1660871709996](image/README/1660871709996.png)![1660871709996](image/README/1660871709996.png)
