'use strict';

$(document).ready(function() {
    $(".task-sender").change(function(ev) {
        var $current = $(this),
            repo = $current.val(),
            task = $current.data("task"),
            sendTo = $current.data("send-to");

        $.ajax({
            type: 'POST',
            url: sendTo,
            data: {
                task: task,
                repo: repo
            }
        })
        .done(function(data) {
            $current.parents("div.collapse").find("span").html("<i class='fi-check'></i>")
        })
        .fail(function() {
            $current.parents("div.collapse").find("span").html("<i class='fi-x'></i>")
        })
    });
});
