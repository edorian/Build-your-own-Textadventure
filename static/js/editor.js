$(function () {
    //$('.editor .input').resizable();
    $('.editor .location').draggable({
        containment: '.editor',
        helper: 'clone'
    });
    $('.editor textarea').droppable({
        drop: function (event, ui) {
            var rel = ui.draggable.attr('rel');
            $(this).val(rel);
        }
    });
});
