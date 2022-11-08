$(document).ready(function () {
    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    var current = 1;
    var steps = $("form").length;

    setProgressBar(current);

    $("#current").text(`step ${current} of 5`)

    $(".next").click(function () {
      current_fs = $(this).parent();
      next_fs = $(this).parent().next();

      $("#current").text(`step ${current+1} of 5`)

      //Add Class Active
      $("#progressbar li").eq($("form").index(next_fs)).addClass("active");

      //show the next form
      next_fs.show();
      //hide the current form with style
      current_fs.animate(
        { opacity: 0 },
        {
          step: function (now) {
            // for making fielset appear animation
            opacity = 1 - now;

            current_fs.css({
              display: "none",
              position: "relative",
            });
            next_fs.css({ opacity: opacity });
          },
          duration: 500,
        }
      );
      setProgressBar(++current);
    });

    $(".previous").click(function () {
      current_fs = $(this).parent();
      previous_fs = $(this).parent().prev();

      $("#current").text(`step ${current-1} of 5`)


      //Remove class active
      $("#progressbar li")
        .eq($("form").index(current_fs))
        .removeClass("active");

      //show the previous form
      previous_fs.show();

      //hide the current form with style
      current_fs.animate(
        { opacity: 0 },
        {
          step: function (now) {
            // for making fielset appear animation
            opacity = 1 - now;

            current_fs.css({
              display: "none",
              position: "relative",
            });
            previous_fs.css({ opacity: opacity });
          },
          duration: 500,
        }
      );
      setProgressBar(--current);
    });

    function setProgressBar(curStep) {
      var percent = parseFloat(100 / steps) * curStep;
      percent = percent.toFixed();
      $(".progress-bar").css("width", percent + "%");
    }

    $(".submit").click(function () {
      return false;
    });
  });

  // sweetalerts
  const show_alert =(duration,type,message)=> {
    const Toast = Swal.mixin({
      toast: true,
      position: 'bottom-end',
      showConfirmButton: false,
      timer: duration,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    })
    
    Toast.fire({
      icon: `${type}`,
      title: `${message}`
    })
  }