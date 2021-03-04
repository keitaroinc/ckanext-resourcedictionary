"use strict";
/*
This JavaScript module handles adding and removing field in the resource dictionary form.
It also renders already existing dictionary fields for the selected resource.
*/
ckan.module('dictionary_form', function ($) {
  return {
    initialize: function () {

      $.proxyAll(this, /_on/);

      $('#add-field-button').on('click', this._onAddField);
      $('.delete-field-button').on('click', this._onDeleteField);
    },
    _onAddField: function(event) {
      // Send an ajax request to CKAN to render the dictionary_field.html
      // snippet with the position for the new field.
      var data = {
          'position': this._calculateFieldsNumber() + 1
      }
      this.sandbox.client.getTemplate('dictionary_field.html', data, this._onReceiveFieldSnippet);
    },
    // Delete event for removing selected field in the form
    _onDeleteField: function(event) {
      event.target.closest("div[class^='dictionary-field-']").remove();
    },
    // Callback function executed when requested snipped is received with success
    _onReceiveFieldSnippet: function(html) {
      // When the snipped is received insert it as a last field in the form
      // and register on delete event for the delete button
      $(html).insertBefore('#dictionary-save-button');
      $('.delete-field-button').on('click', this._onDeleteField);
    },
    // Helper for calculating rendered fields number in the form
    _calculateFieldsNumber: function() {
      return this.el.find("div[class^='dictionary-field-']").length
    },
  };
});