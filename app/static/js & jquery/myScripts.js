//this is a personal javascript file that achieves an extra level of responsive view by either hiding some elements depeding on the viewport
//or displaying them accordingly
//below the function are being called when the document is ready
$(document).ready(function () {
   changeElements();
   changeSpans();
   changeNav();
   
    $(window).resize(function() {
        changeElements();
        changeSpans();
        changeNav();
    });
});

//carousel hide for mobilrd
function changeElements(){    
     if ($(window).width() <= 640) {
        $('#myCarousel').hide();
    }else{
        $('#myCarousel').show();
    }
}

//ribbons hide for tablets
function changeSpans(){
     if ($(window).width() >= 641 && $(window).width() <= 1023) {
        $('#boxSpan1').hide();
        $('#boxSpan2').hide();
        $('#boxSpan3').hide();
    }else{
        $('#boxSpan1').show();
        $('#boxSpan2').show();
        $('#boxSpan3').show();
    }
}

//navbar hide for desktops(home option on logo)
function changeNav(){
     if ($(window).width() > 1000) {
        $('#navBar').hide();
    }else{
        $('#navBar').show();

    }
}
