$(function () {
    $('[data-toggle="tooltip"]').tooltip();

    // Smooth scrolling for navigation links
    $('a.nav-link').on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Animated modal transitions
    $('.modal').on('show.bs.modal', function (e) {
        $(this).find('.modal-dialog').attr('class', 'modal-dialog animate__animated animate__zoomIn');
    });
    $('.modal').on('hide.bs.modal', function (e) {
        $(this).find('.modal-dialog').attr('class', 'modal-dialog animate__animated animate__zoomOut');
    });
});
