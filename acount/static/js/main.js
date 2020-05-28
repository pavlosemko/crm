$('.copy').click(
    function(e) {
       var element= $(this).parent().find('.text')
  var $temp = $("<input>");
       $('.alertMessage').fadeIn();

  $('.alertMessage .text').text('Copied');
  setTimeout(function () {
      $('.alertMessage').fadeOut();
  },2000)
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");

  $temp.remove();
}

)
$('.copy-form').click(
    function(e) {
       var element= $(this).parent().parent().find('.py-2')
  var $temp = $("<input>");
       $('.alertMessage').fadeIn();

  $('.alertMessage .text').text('Copied');
  setTimeout(function () {
      $('.alertMessage').fadeOut();
  },2000)
  $("body").append($temp);
  $temp.val($(element).val()).select();
  document.execCommand("copy");

  $temp.remove();
}

)


