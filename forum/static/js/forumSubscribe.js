$('#unsubscribe').on("click", function() {
    $.get("{% url 'forum:unsubscribe' topic.id %}", function(data) {
        }).done(function() {
            $("#unsubscribe-text").hide("slow");
    });
});

$('#subscribe').on("click", function() {
    $.get("{% url 'forum:subscribe' topic.id %}", function(data) {
        }).done(function() {
            $("#subscribe-text").hide("slow");
    });
});
