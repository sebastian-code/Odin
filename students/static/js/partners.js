'use strict';

$(function() {
    var $partnerNameContainer = $('#partner-name-input-container'),
        $partnerSelectionContainer = $('#partner-selection-container'),
        $cantFindPartnerButton = $('#cant-find-partner'),
        $backButton = $('#back-to-partners-list');

    function hideAll(elements) {
        elements.forEach(function($el) {
            $el.hide();
        });
    }

    function showAll(elements) {
        elements.forEach(function($el) {
            $el.show();
        });
    }

    function defaultState() {
        var toShow = [],
            toHide = [$partnerNameContainer, $backButton];

        showAll(toShow);
        hideAll(toHide);
    }

    function pickPartnerFromListState() {
        var toShow = [$cantFindPartnerButton, $partnerSelectionContainer],
            toHide = [$backButton, $partnerNameContainer];

        showAll(toShow);
        hideAll(toHide);
    }

    function cantFindPartnerState() {
        var toShow = [$backButton, $partnerNameContainer],
            toHide = [$cantFindPartnerButton, $partnerSelectionContainer];

        showAll(toShow);
        hideAll(toHide);
    }


    $cantFindPartnerButton.on('click', function(event) {
        event.preventDefault();
        cantFindPartnerState();
    });

    $backButton.on('click', function(event) {
        event.preventDefault();
        pickPartnerFromListState();
    });

    defaultState();
});
