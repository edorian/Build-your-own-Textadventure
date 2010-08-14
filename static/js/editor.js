$(function () {
    var getLocationMarkup = function (location_id) {
        return '[](#' + location_id + ')';
    };
    $('.editor .location').draggable({
        containment: '.editor',
        helper: 'clone'
    });
    $('.editor textarea').droppable({
        drop: function (event, ui) {
            var selection = $(this).getSelection();
            var rel = ui.draggable.attr('rel');
            var markup = getLocationMarkup(rel);
            $(this).replaceSelection(markup, true);

            $(this).setSelection(selection.start + 1);
        }
    });
});
