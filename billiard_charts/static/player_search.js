$(document).ready(function() {
    var selectedItems = {
        players: [],
        organizers: []
    };

    function setupAutocomplete(selector, type, displaySelector) {
        $(selector).autocomplete({
            source: playerSearchUrl,
            minLength: 3,
            select: function(event, ui) {
                var selectedItem = {
                    label: ui.item.label,
                    pk: ui.item.pk
                };
                selectedItems[type].push(selectedItem);

                // Zobrazení vybraných položek
                $(displaySelector).empty();
                selectedItems[type].forEach(function(item) {
                    $(displaySelector).append('<div>' + item.label + '</div>');
                });

                return false;
            }
        });
    }

    setupAutocomplete("#players-search", "players", "#selected_players_display");
    setupAutocomplete("#organizers-search", "organizers", "#selected_organizers_display");

    // Přidání vybraných hráčů a organizátorů do skrytého pole při odeslání formuláře
    $("form").submit(function() {
        $("#selected_players_input").val(JSON.stringify(selectedItems.players.map(item => item.pk)));
        $("#selected_organizers_input").val(JSON.stringify(selectedItems.organizers.map(item => item.pk)));
    });
});
