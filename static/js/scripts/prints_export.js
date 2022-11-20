


 const removeAttr = function(){
    // alert('hi')
    // document.getElementById('i').style.backgroundColor= 'transparent';
    document.body.style.backgroundImage='none';
}
    // PRINT PDF
    function createPDF(heading) {
        // $(".view").text('')
        // $(".view").fadeOut()
        // var sTable = document.getElementById('tab').innerHTML;

        $('#tab').printThis({
            // printContainer: true, 
            beforePrint: removeAttr(),              // function called before iframe is filled
            header:`<h3 style="font: bold 100% sans-serif; letter-spacing: 0.5em;" class="text-center">${heading}</h3>`
        });

       
       
        // var style = "<style>";
        // style = style + "table {width: 100%;font: 17px Calibri;}";
        // style = style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
        // style = style + "padding: 2px 3px;text-align: center;}}";
        // style = style + "td {height: 10%;width: 10% !important;}";
        // style = style + "</style>";
    
        // // CREATE A WINDOW OBJECT.
       
        // var win = window.open('', '', 'height=800,width=900');
    
        // win.document.write('<html><head>');
        // // check the below code its just a pdf title on the pdf (output file)
        // win.document.write(`<title>${heading}</title>`);   // <title> FOR PDF HEADER.
        // win.document.write(style);          // ADD STYLE INSIDE THE HEAD TAG.
        // win.document.write('</head>');
        // win.document.write('<body>');
        // win.document.write(sTable);         // THE TABLE CONTENTS INSIDE THE BODY TAG.
        // win.document.write('</body></html>');
    
        // win.document.close(); 	// CLOSE THE CURRENT WINDOW.
        // // location.reload();
        // // $(".view").fadeIn()
        // // win.focus()
        // win.print();    // PRINT THE CONTENTS.
        // // win.close()
    }
    
    
    
    function createExcel() {
        // $(".view").fadeOut()
        $('.table').tblToExcel({
            beforeSend: function (){
                // $(".view").fadeOut()
            },
            complete: function () {

              // do something
              alert('Completed')
            // $(".view").fadeOut()

            }
          });
    }
    