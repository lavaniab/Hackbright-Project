"use strict";

// tippy('#myButton', {
//   content: 'Tooltip'
// });

// tippy(document.querySelectorAll("button"));
// tippy('[data-tippy-content]');

//cut losses with tippy


//should probably have similar for trip and location



$(document).ready(function() {
	const whereTheNotesGo = $('#allTheNotes');

	$('#addNoteForm').submit(function(event) {
		event.preventDefault();
		const formData = $(this).serializeArray()
		const payload = {
			data: { note: formData[0].value },
			method: 'POST',
			url: '/add_note'
		};
		const myRequest = $.ajax(payload);

		myRequest.then(function(response) {
			const htmlToAdd = `<li>${response.note}</li>` //can add href here
			// console.log(htmlToAdd);                      template literal
			whereTheNotesGo.append(htmlToAdd);
		})
		// console.log(formData);
	});
});

// function createEntry(results) {
//     $("#id").html(results);
// }

// function showEntry(evt) {
//     $.get('/add_entry/<int:trip_id>', createEntry);
// }

// $('#id-button').on('click', showEntry);