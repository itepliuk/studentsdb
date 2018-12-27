function initJournal() {
    $('.day-box input[type="checkbox"]').click(function(event){
        alert('test click js');
    });
}
$(document).ready(function(){
    initJournal();
});