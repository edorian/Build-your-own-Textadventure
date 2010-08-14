$(function () {
    var getLocationMarkup = function (location_id, text) {
        text = text || "";
        return '[' + text + '](#' + location_id + ')';
    };
    $('.editor .location').draggable({
        containment: '.editor',
        helper: 'clone'
    });
    $('.editor textarea').droppable({
        drop: function (event, ui) {
            var selection = $(this).getSelection();
            var rel = ui.draggable.attr('rel');
            var markup = getLocationMarkup(rel, selection.text);
            $(this).replaceSelection(markup, true);

            if (selection.length == 0) {
                $(this).setSelection(selection.start + 1);
            } else {
                $(this).setSelection(selection.start + markup.length);
            }
        }
    });
});
